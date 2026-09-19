"""Import a bounded, pinned P4 release. Never read private paths into public output."""
import argparse,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P4_SHA='bb0daf523980482bc681e7c5fc98d3cc160f4a6abab67283ae3d5aa4e35fe87a'
UNIT_KEYS=('raider','war_ram','skullthrower')
BUILDING_KEYS=('workshop','academy','main','barracks','rally_point')
def canonical(obj):return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n'
def project(payload):
 if payload['format']!='tw-public-reference-v3':raise ValueError('Unsupported public input')
 facts=payload['facts'];ref=payload['reference'];catalogue=payload['catalogue']
 pagefacts={p['id']:p['fact_ids'] for p in payload['pages']}
 entities={}
 names={r['id']:r['name'] for r in catalogue['buildings']}
 names.update({r['entity_id']:r['name'] for r in ref['factions']})
 names.update({'unit.'+r['entity_id']:r['value'] for r in facts if r['predicate']=='name'})
 def rules(page):return [r for r in ref['rules'] if r['id'] in pagefacts[page]]
 for key in UNIT_KEYS:
  rows=[r for r in facts if r['entity_id']==key];by={r['predicate']:r for r in rows};eid='unit.'+key
  entities[eid]={'id':eid,'key':key,'kind':'unit','name':by['name']['value'],'path':'reference/units/'+key.replace('_','-')+'/',
   'facts':rows,'detail':next(r for r in ref['units'] if r['entity_id']==eid),
   'upgrades':[r for r in ref['unit_upgrades'] if r['entity_id']==eid],'rules':rules('wiki.unit.'+key)}
 for key in BUILDING_KEYS:
  eid='building.'+key;cat=next(r for r in catalogue['buildings'] if r['id']==eid)
  entities[eid]={'id':eid,'key':key,'kind':'building','name':cat['name'],'path':'reference/buildings/'+('town-hall' if key=='main' else key.replace('_','-'))+'/',
   'catalogue':cat,'detail':next(r for r in ref['buildings'] if r['entity_id']==eid),
   'effects':[r for r in ref['building_effects'] if r['entity_id']==eid],'rules':rules('wiki.building.'+key)}
 faction=next(r for r in ref['factions'] if r['entity_id']=='faction.stormfang_clans')
 entities[faction['entity_id']]={'id':faction['entity_id'],'key':'stormfang_clans','kind':'faction','name':faction['name'],'path':'reference/factions/stormfang-clans/','detail':faction,'rules':rules('wiki.faction.stormfang_clans')}
 return {'format':'tw-wiki-slice-v1','upstream_sha256':P4_SHA,'snapshot_date':'2026-09-14','resources':catalogue['resources'],'entities':entities,
  'names':{k:v for k,v in names.items() if k in entities or k in faction['unit_ids']},
  'scope':'Three Stormfang units, their faction and five prerequisite buildings. Not the complete wiki.'}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('--tw',type=Path);a=ap.parse_args()
 raw=a.source.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=P4_SHA:raise ValueError('New public release requires explicit review and pin update')
 payload=json.loads(raw)
 if a.tw:
  sys.path.insert(0,str(a.tw/'00_PILOTAGE/OUTILS/CSV/implementation'));import export_public;export_public.verify_sources(a.tw,payload)
 out=canonical(project(payload)).encode();dest=ROOT/'knowledge';dest.mkdir(exist_ok=True)
 (dest/'bundle.json').write_bytes(out)
 (dest/'manifest.json').write_text(json.dumps({'format':'tw-wiki-slice-v1','upstream_sha256':P4_SHA,'bundle_sha256':hashlib.sha256(out).hexdigest(),'entities':9},indent=2)+'\n')
 print('Imported 9 source-linked entities')

"""Import a bounded, pinned P4 release. Never read private paths into public output."""
import argparse,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P4_SHA='bb0daf523980482bc681e7c5fc98d3cc160f4a6abab67283ae3d5aa4e35fe87a'
EXPECTED_COUNTS={'unit':40,'building':39,'faction':4,'field':4,'research':63,'rules':11}
SECTIONS={'unit':'units','building':'buildings','faction':'factions','field':'fields','research':'research','rules':'mechanics'}
TOPICS={'settlements':'Settlements & capitals','research':'Research & progression','siege':'Siege','combat':'Combat','community-confirmations':'Community confirmations','september-update':'September 2026 update','alliance':'Alliance','culture':'Culture & celebrations','trade':'Trade & transport','buildings':'Building rules','interface':'Interface changes'}
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
 for record in ref['units']:
  key=record['entity_id'].removeprefix('unit.')
  rows=[r for r in facts if r['entity_id']==key];by={r['predicate']:r for r in rows};eid='unit.'+key
  entities[eid]={'id':eid,'key':key,'kind':'unit','name':by['name']['value'],'path':'reference/units/'+key.replace('_','-')+'/',
   'facts':rows,'detail':next(r for r in ref['units'] if r['entity_id']==eid),
   'upgrades':[r for r in ref['unit_upgrades'] if r['entity_id']==eid],'rules':rules('wiki.unit.'+key)}
 for record in catalogue['buildings']:
  key=record['key']
  eid='building.'+key;cat=next(r for r in catalogue['buildings'] if r['id']==eid)
  entities[eid]={'id':eid,'key':key,'kind':'building','name':cat['name'],'path':'reference/buildings/'+('town-hall' if key=='main' else key.replace('_','-'))+'/',
   'catalogue':cat,'detail':next(r for r in ref['buildings'] if r['entity_id']==eid),
   'effects':[r for r in ref['building_effects'] if r['entity_id']==eid],'rules':rules('wiki.building.'+key)}
 for faction in ref['factions']:
  key=faction['entity_id'].removeprefix('faction.')
  entities[faction['entity_id']]={'id':faction['entity_id'],'key':key,'kind':'faction','name':faction['name'],'path':'reference/factions/'+key.replace('_','-')+'/','detail':faction,'rules':rules('wiki.faction.'+key)}
 for field in catalogue['fields']:
  eid=field['id'];names[eid]=field['name']
  entities[eid]={'id':eid,'key':field['key'],'kind':'field','name':field['name'],'path':'reference/fields/'+field['key']+'/','catalogue':field,
   'detail':{'description':None,'evidence':field['evidence'],'scope':field['limits']},'rules':rules('wiki.'+eid)}
 for research in catalogue['research']:
  eid=research['id'];names[eid]=research['name'];key=research['key']
  entities[eid]={'id':eid,'key':key,'kind':'research','name':research['name'],'path':'reference/research/'+key.replace('.','/').replace('_','-')+'/',
   'catalogue':research,'detail':{'description':None,'evidence':research['evidence'],'scope':'Official English research name. Rank effects are reviewed translations of the certified client descriptions; not new purchase tests. Later qualifications and unresolved scope remain explicit.'},
   'effects':[r for r in ref['research_effects'] if r['entity_id']==eid],'rules':rules('wiki.'+eid)}
 for topic,title in TOPICS.items():
  eid='rules.'+topic;rows=rules('wiki.'+eid);names[eid]=title
  entities[eid]={'id':eid,'key':topic,'kind':'rules','name':title,'path':'reference/mechanics/'+topic+'/',
   'detail':{'description':None,'evidence':[e for r in rows for e in r['evidence']],'scope':'Selected reviewed rules, with their original authority, conditions and limits. This is not an exhaustive mechanics guide.'},'rules':rows}
 return {'format':'tw-wiki-reference-v1','upstream_sha256':P4_SHA,'snapshot_date':'2026-09-14','resources':catalogue['resources'],'entities':entities,
  'names':names,'counts':EXPECTED_COUNTS,'sections':SECTIONS,'excluded_blocks':ref['exclusions'],
  'scope':'All 150 catalogue entities and 11 selected mechanics pages from the reviewed P4 public export. Excluded findings and unwritten guides are not promoted to approved facts.'}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('--tw',type=Path);a=ap.parse_args()
 raw=a.source.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=P4_SHA:raise ValueError('New public release requires explicit review and pin update')
 payload=json.loads(raw)
 if a.tw:
  sys.path.insert(0,str(a.tw/'00_PILOTAGE/OUTILS/CSV/implementation'));import export_public;export_public.verify_sources(a.tw,payload)
 out=canonical(project(payload)).encode();dest=ROOT/'knowledge';dest.mkdir(exist_ok=True)
 (dest/'bundle.json').write_bytes(out)
 (dest/'manifest.json').write_text(json.dumps({'format':'tw-wiki-reference-v1','upstream_sha256':P4_SHA,'bundle_sha256':hashlib.sha256(out).hexdigest(),'entities':sum(EXPECTED_COUNTS.values()),'counts':EXPECTED_COUNTS},indent=2)+'\n',encoding='utf-8',newline='\n')
 print('Imported all 161 source-linked reference pages')

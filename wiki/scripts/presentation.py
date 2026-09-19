"""Explicit presentation labels and joins. Raw facts/evidence are retained."""
from collections import defaultdict

EFFECTS={
 'allianceMemberCapacity':('Alliance member capacity','count'),
 'armyUnitUpgradeSpeed':('Unit upgrade duration factor','factor'),
 'buildingSpeed':('Construction duration factor','factor'),
 'cavalryTrainingSpeed':('Cavalry training duration factor','factor'),
 'cavalryUpkeepReduction':('Cavalry upkeep reduction series','value'),
 'celebrationDuration':('Celebration duration factor','factor'),
 'concurrentAttacks':('Concurrent attacks','count'),
 'defenceFlat':('Flat defence','value'),
 'healingSpeed':('Healing speed parameter','value'),
 'merchantCarryCapacityBonus':('Merchant carrying capacity factor','factor'),
 'merchantsAvailable':('Merchants available','count'),
 'offenseBonus':('Offence factor','factor'),
 'storageLimit.granary':('Food storage capacity','resources'),
 'storageLimit.warehouse':('Warehouse capacity','resources'),
 'trainingSpeed':('Training duration factor','factor'),
 'trapCapacity':('Trap capacity','count'),
 'troopSpeedBeyond20':('Troop speed factor beyond 20 tiles','factor'),
 'upgradeQueueSize':('Upgrade queue size','count'),
 'villageDurability':('Village durability factor','factor'),
 'woundedCapacity':('Wounded troop capacity','count'),
}
RESOURCE_NAMES={'wood':'Lumber','clay':'Stone','iron':'Metal','crop':'Food'}
for key,name in RESOURCE_NAMES.items():
 EFFECTS['productionMultiplier.'+key]=(name+' production factor','factor')
 EFFECTS['hiddenResources.'+key]=('Hidden '+name.lower(),'resources')
AUTHORITY={'developer_statement':'Developer statement','source_document_or_ui':'Documented source / interface','player_testimony':'Player testimony'}

def decorate(m,b):
 m['sort_key']=m['name'].casefold()+'|'+m['id']
 m['section']=b['sections'][m['kind']]
 m['kind_label']={'unit':'Unit','building':'Building','faction':'Faction','field':'Resource field','research':'Research','rules':'Mechanics'}[m['kind']]
 m['description']=m['description'] or {'field':'Base production, upgrade costs and settlement access.','research':'Rank effects, source context and documented prerequisites.','rules':'Reviewed rules with their conditions, provenance and remaining limits.'}.get(m['kind'],'Catalogue values and requirements; no source description is supplied.')
 summaries={}
 for e in m['evidence']:
  key=(e['source_id'],e['sha256']);summaries.setdefault(key,set()).add(e['entity_key'])
 m['proof_summary']=[{'source_id':k[0],'sha256':k[1],'records':len(v)} for k,v in sorted(summaries.items())]
 if m['kind']=='unit':
  factions=[f for f in b['entities'].values() if f['kind']=='faction' and m['id'] in f['detail']['unit_ids']]
  if len(factions)!=1:raise ValueError('Unit faction is not unique')
  m['faction_id']=factions[0]['id'];m['faction_path']=factions[0]['path']
 if m['kind']=='building':
  groups=defaultdict(list)
  for row in m['effects']:
   if row['effect_id'] not in EFFECTS:raise ValueError('Unreviewed effect display label '+row['effect_id'])
   groups[(row['effect_id'],row['faction_id'] or '')].append(row)
  m['effect_groups']=[{'label':EFFECTS[key[0]][0],'unit':EFFECTS[key[0]][1],'technical_id':key[0],'faction':b['names'].get(key[1],''),'rows':sorted(rows,key=lambda r:r['level'])} for key,rows in sorted(groups.items())]
  m['hosted_fields']=[e['id'] for e in b['entities'].values() if e['kind']=='field' and e['catalogue']['host_building_id']==m['id']]
  m['research_unlocks']=[{'id':e['id'],'name':e['name'],'path':e['path'],'level':r['level']} for e in b['entities'].values() if e['kind']=='unit' for r in e['detail']['unlock_requirements'] if r['entity_id']==m['id']]
  m['static_groups']=[]
  static_labels={'merchantCarryCapacity':'Base merchant carrying capacity','merchantSpeed':'Base merchant speed','defenceBonus':'Catalogue defence factor','durability':'Catalogue durability parameter'}
  for key,values in m['detail']['static_effects'].items():
   if key not in static_labels:raise ValueError('Unreviewed static effect '+key)
   m['static_groups'].append({'label':static_labels[key],'rows':[{'faction':b['names']['faction.'+f],'value':v} for f,v in values.items()]})
 if m['kind']=='research':
  m['rank_rows']=[]
  for rank in range(1,m['catalogue']['ranks']+1):
   row=next((x for x in m['effects'] if x['rank']==rank),None)
   if row is None:raise ValueError('Missing reviewed rank description')
   text=row['description'].removeprefix('Total effect at this rank, not the sum of ranks. ').removesuffix(' Editorial translation of the certified French text, not an independent English UI observation.')
   m['rank_rows'].append(dict(row,readable_description=text))
 m['rule_views']=[dict(r,authority_label=AUTHORITY.get(r['authority'],r['authority'].replace('_',' '))) for r in m['rules']]
 return m

"""Fail-closed build: pinned public knowledge -> Hugo -> Pagefind -> checks."""
import argparse,hashlib,json,os,re,shutil,subprocess,sys,tempfile
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from import_tw import canonical,EXPECTED_COUNTS,SECTIONS
from presentation import decorate
def sha(raw):return hashlib.sha256(raw).hexdigest()
def checked_bundle():
 raw=(ROOT/'knowledge/bundle.json').read_bytes();manifest=json.loads((ROOT/'knowledge/manifest.json').read_bytes())
 if sha(raw)!=manifest['bundle_sha256']:raise ValueError('Knowledge changed without reviewed import/manifest')
 b=json.loads(raw)
 if b['format']!='tw-wiki-reference-v1' or b['upstream_sha256']!=manifest['upstream_sha256']:raise ValueError('Knowledge contract changed')
 if Counter(e['kind'] for e in b['entities'].values())!=EXPECTED_COUNTS or len({e['path'] for e in b['entities'].values()})!=sum(EXPECTED_COUNTS.values()):raise ValueError('Reference scope/path collision')
 if [r['name'] for r in b['resources']]!=['Lumber','Stone','Metal','Food']:raise ValueError('Official resource labels changed')
 for eid,m in b['entities'].items():
  if m['id']!=eid or not m['name'] or not re.fullmatch(r'reference/'+SECTIONS[m['kind']]+r'/(?:[a-z0-9-]+/)+',m['path']):raise ValueError('Invalid entity identity or path')
  if b['names'][eid]!=m['name']:raise ValueError('Conflicting display name')
  if not m['detail']['evidence']:raise ValueError('Missing source')
  for r in m['detail'].get('requirements',m['detail'].get('unlock_requirements',[])):
   if r['entity_id'] not in b['entities']:raise ValueError('Prerequisite page missing')
 return b,manifest
def gather_proofs(obj):
 found=[]
 def visit(v):
  if isinstance(v,dict):
   for e in v.get('evidence',[]):
    if not re.fullmatch('[0-9a-f]{64}',e['sha256']) or not e['fields']:raise ValueError('Invalid provenance')
    if e not in found:found.append(e)
   for k,x in v.items():
    if k!='evidence':visit(x)
  elif isinstance(v,list):
   for x in v:visit(x)
 visit(obj);return found
def prepare():
 b,manifest=checked_bundle();g=ROOT/'generated';g.mkdir(exist_ok=True)
 # Refuse stale content; only this explicitly owned generated subtree is cleaned.
 content=(g/'content').resolve()
 if not content.is_relative_to(ROOT.resolve()) or content.name!='content':raise ValueError('Unsafe generated target')
 if content.exists():shutil.rmtree(content)
 content.mkdir();(g/'data').mkdir(exist_ok=True)
 rendered={}
 for eid,original in b['entities'].items():
  m=dict(original);m['description']=m['detail']['description'];m['evidence']=gather_proofs(original)
  m['source_revision']=manifest['bundle_sha256'];m['snapshot_date']=b['snapshot_date']
  if m['kind']=='unit':
   facts={r['predicate']:r['value'] for r in m['facts']};m.update(faction=facts['faction']['name'],role=facts['role'].capitalize(),cost=facts['training_cost'],research_cost=facts['research_cost'])
   s=m['detail']['stats'];m['summary']=[{'label':'Attack','value':s['attack']},{'label':'Base speed','value':s['speed']},{'label':'Carrying capacity','value':s['carry_capacity']}]
  elif m['kind']=='building':
   lvl=next(r for r in m['catalogue']['levels'] if r['level']==1);m['cost']=lvl['cost'];m['level_one']=lvl
   caps=m['detail']['level_caps'];m['summary']=[{'label':'Village level cap','value':caps.get('nonCityVillage',caps.get('all','Not specified'))},{'label':'City level cap','value':caps.get('city',caps.get('all','Not specified'))},{'label':'Catalogue levels','value':m['catalogue']['catalogue_max_level']}]
  elif m['kind']=='faction':m['summary']=[{'label':'Catalogue roster','value':len(m['detail']['unit_ids'])},{'label':'Playable faction','value':'Yes' if m['detail']['playable'] else 'No'}]
  elif m['kind']=='field':
   lvl=next(r for r in m['catalogue']['levels'] if r['level']==1);m['cost']=lvl['cost'];m['level_one']=lvl
   m['summary']=[{'label':'Level 1 base production / hour','value':lvl['production_per_hour']},{'label':'Catalogue maximum level','value':m['catalogue']['catalogue_max_level']},{'label':'Level rows','value':len(m['catalogue']['levels'])}]
  elif m['kind']=='research':m['summary']=[{'label':'Research tier','value':{'minor':'Minor','major':'Major','keystone':'Keystone'}[m['catalogue']['tier_id']]},{'label':'Catalogue ranks','value':m['catalogue']['ranks']},{'label':'Rank descriptions','value':len(m['effects'])}]
  else:m['summary']=[{'label':'Selected rules','value':len(m['rules'])},{'label':'Evidence classes','value':len({r['authority'] for r in m['rules']})}]
  m=decorate(m,b)
  rendered[eid]=m
  target=content/m['path'].rstrip('/');target.parent.mkdir(parents=True,exist_ok=True)
  target.with_suffix('.md').write_text(json.dumps({'title':m['name'],'entity':eid,'layout':'single','kind_label':m['kind_label'],'description':m['description']})+'\n',encoding='utf-8',newline='\n')
 for path in (ROOT/'content').rglob('*.md'):
  target=content/path.relative_to(ROOT/'content');target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
 for rel,title,kind in [('reference','Reference',''),('reference/units','Units','unit'),('reference/buildings','Buildings','building'),('reference/factions','Factions','faction'),('reference/fields','Resource fields','field'),('reference/research','Research','research'),('reference/mechanics','Mechanics','rules')]:
  target=content/rel/'_index.md';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps({'title':title,'collection':kind})+'\n',encoding='utf-8',newline='\n')
 (g/'data/bundle.json').write_text(canonical(b),encoding='utf-8',newline='\n');(g/'data/entities.json').write_text(canonical(rendered),encoding='utf-8',newline='\n')
 return b,manifest,rendered
def build(base_url,destination):
 if not base_url.startswith(('https://','http://127.0.0.1:','http://localhost:')) or not base_url.endswith('/'):raise ValueError('Explicit trailing-slash base URL required')
 b,manifest,models=prepare();lock=json.loads((ROOT/'toolchain.json').read_text())
 binaries={name:ROOT/'.tools'/(name+('.exe' if os.name=='nt' else '')) for name in ('hugo','pagefind')}
 for name,bin in binaries.items():
  if not bin.exists():raise ValueError('Run scripts/bootstrap.py first')
  actual=subprocess.check_output([str(bin),'version' if name=='hugo' else '--version'],text=True,encoding='utf-8')
  if lock[name]['version'] not in actual:raise ValueError('Unpinned '+name)
 destination=destination.resolve()
 if not destination.is_relative_to(ROOT.resolve()) or destination==ROOT.resolve():raise ValueError('Destination must be a child of the site source')
 if destination.exists():raise ValueError('Use a new destination; do not overwrite a last-known-good build')
 subprocess.run([str(binaries['hugo']),'--source',str(ROOT),'--destination',str(destination),'--baseURL',base_url,'--noBuildLock','--panicOnWarning'],check=True)
 for eid,m in models.items():
  target=destination/'data'/(eid+'.json');target.parent.mkdir(exist_ok=True);target.write_text(canonical({k:v for k,v in m.items() if k!='evidence'}),encoding='utf-8',newline='\n')
 subprocess.run([str(binaries['pagefind']),'--site',str(destination),'--output-subdir','pagefind'],check=True)
 if not (destination/'pagefind/pagefind.js').is_file() or not list((destination/'pagefind').glob('*.pf_meta')):raise ValueError('Search index missing')
 (destination/'.nojekyll').write_bytes(b'')
 release={'format':'tw-wiki-build-v1','base_url':base_url,'bundle_sha256':manifest['bundle_sha256'],'upstream_sha256':b['upstream_sha256'],'entities':len(models),'toolchain':{n:s['version'] for n,s in lock.items()},'scope':b['scope']}
 release['files']={p.relative_to(destination).as_posix():sha(p.read_bytes()) for p in sorted(destination.rglob('*')) if p.is_file()}
 (destination/'release.json').write_text(json.dumps(release,indent=2)+'\n',encoding='utf-8',newline='\n')
 subprocess.run([sys.executable,'-B',str(ROOT/'scripts/check.py'),str(destination)],check=True)
 return release
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--base-url',default='https://loursentong.github.io/Codex-Thronewake/next/');ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 result=build(a.base_url,a.out);print(json.dumps({'entities':result['entities'],'files':len(result['files']),'out':str(a.out)}))

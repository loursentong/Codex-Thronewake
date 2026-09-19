"""Validate final artifact recursively, including prefix links and all local anchors."""
import argparse,hashlib,json,re
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
class Doc(HTMLParser):
 def __init__(self,raw):super().__init__();self.ids=[];self.links=[];self.tags=[];self.feed(raw)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags.append((tag,a))
  if 'id' in a:self.ids.append(a['id'])
  for key in ('src','href'):
   if key in a:self.links.append(a[key])
def check(root):
 root=root.resolve();release=json.loads((root/'release.json').read_bytes());prefix=urlsplit(release['base_url']).path
 files={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file() and p.name!='release.json'}
 if files!=release['files']:raise ValueError('Artifact differs from manifest')
 docs={p.resolve():Doc(p.read_text(encoding='utf-8')) for p in root.rglob('*.html')};links=0
 for path,d in docs.items():
  if len(d.ids)!=len(set(d.ids)):raise ValueError('Duplicate anchors: '+str(path))
  if sum(t=='h1' for t,a in d.tags)!=1:raise ValueError('Expected one H1: '+str(path))
  for t,a in d.tags:
   if t=='img' and 'alt' not in a:raise ValueError('Image lacks alt text')
  for value in d.links:
   u=urlsplit(value)
   if u.scheme or u.netloc:continue
   if u.path.startswith('/'):
    if not u.path.startswith(prefix):raise ValueError('Wrong base path: '+value)
    target=root/unquote(u.path[len(prefix):])
   else:target=path.parent/unquote(u.path) if u.path else path
   target=target.resolve()
   if not target.is_relative_to(root):raise ValueError('Link escapes artifact')
   if target.is_dir():target/='index.html'
   if not target.is_file():raise ValueError('Missing target: '+value+' in '+str(path))
   if u.fragment and unquote(u.fragment) not in docs[target].ids:raise ValueError('Missing anchor: '+value)
   links+=1
 for p in root.rglob('*'):
  if p.suffix not in ('.json','.html'):continue
  text=p.read_text(encoding='utf-8')
  for value in ('C:/Users/','C:\\Users\\','Latong','02_STRATEGIE_COMPTE','04_BASE_SERVEUR','@gmail.com'):
   if value in text:raise ValueError('Private material: '+str(p))
 if len(list((root/'data').glob('*.json')))!=9:raise ValueError('Entity count mismatch')
 return {'html_pages':len(docs),'local_links_checked':links,'files':len(files),'valid':True}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);a=ap.parse_args();print(json.dumps(check(a.root)))

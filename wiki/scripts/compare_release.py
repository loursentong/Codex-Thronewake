"""Exact content comparison; order-insensitive Pagefind 1.5.2 filter metadata.

Pagefind serializes filter values from an unordered map. We do not rewrite its
output or ignore its index. Only that ordering and its dependent hash references
are normalized for comparison. Each artifact still has its own exact manifest.
"""
import argparse,gzip,hashlib,json
from pathlib import Path
from check import check

def decode(raw):
 """Fail-closed subset of CBOR used by pinned Pagefind filter/meta arrays."""
 data=gzip.decompress(raw)
 if not data.startswith(b'pagefind_dcd'):raise ValueError('Unknown Pagefind envelope')
 data=data[12:];pos=0
 def read():
  nonlocal pos
  head=data[pos];pos+=1;major=head>>5;n=head&31
  if n>=24:
   size={24:1,25:2,26:4,27:8}.get(n)
   if not size:raise ValueError('Unsupported CBOR length')
   n=int.from_bytes(data[pos:pos+size],'big');pos+=size
  if major==0:return n
  if major==3:
   s=data[pos:pos+n].decode('utf-8');pos+=n;return s
  if major==4:return [read() for _ in range(n)]
  raise ValueError('Unsupported Pagefind CBOR type')
 result=read()
 if pos!=len(data):raise ValueError('Trailing CBOR bytes')
 return result

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def comparable(root):
 check(root)
 r=json.loads((root/'release.json').read_bytes());files=r['files'];filters={}
 for p in sorted((root/'pagefind/filter').glob('*.pf_filter')):
  value=decode(p.read_bytes())
  if len(value)!=2 or not isinstance(value[0],str):raise ValueError('Unexpected filter shape')
  name,items=value
  if len({x[0] for x in items})!=len(items):raise ValueError('Duplicate filter value')
  filters[p.stem]=(name,sorted(items,key=lambda x:x[0]))
  del files[p.relative_to(root).as_posix()]
 entry_path=root/'pagefind/pagefind-entry.json';entry=json.loads(entry_path.read_bytes())
 if entry.get('version')!='1.5.2':raise ValueError('Unreviewed Pagefind metadata version')
 used=set()
 for lang,info in entry['languages'].items():
  p=root/'pagefind'/('pagefind.'+info['hash']+'.pf_meta');meta=decode(p.read_bytes())
  if len(meta)!=6 or meta[0]!='1.5.2':raise ValueError('Unexpected Pagefind metadata shape')
  bound=[]
  for name,ref in meta[3]:
   if ref not in filters or filters[ref][0]!=name:raise ValueError('Invalid filter binding')
   used.add(ref);bound.append(filters[ref])
  meta[3]=sorted(bound,key=lambda x:x[0]);info['hash']=digest(meta)
  del files[p.relative_to(root).as_posix()]
 if used!=set(filters):raise ValueError('Unreferenced filter')
 files['pagefind/pagefind-entry.json']=digest(entry)
 return r

def compare(expected,actual):
 one=comparable(expected);two=comparable(actual)
 if one!=two:
  changed=sorted(k for k in one['files'].keys()|two['files'].keys() if one['files'].get(k)!=two['files'].get(k))
  raise ValueError('Rebuilt content differs: '+repr(changed))
 return {'equivalent':True,'comparison':'Exact content and search index; filter value order normalized only','entities':one['entities']}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('expected',type=Path);ap.add_argument('actual',type=Path);a=ap.parse_args()
 print(json.dumps(compare(a.expected,a.actual)))

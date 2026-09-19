"""Install pinned build binaries locally; no npm scripts or system changes."""
import base64,hashlib,io,json,os,platform,tarfile,urllib.request,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def install():
 system=platform.system().lower()
 if system not in ('windows','linux') or platform.machine().lower() not in ('amd64','x86_64'):raise RuntimeError('Pinned binaries cover Windows/Linux x64 only')
 lock=json.loads((ROOT/'toolchain.json').read_text());dest=ROOT/'.tools';dest.mkdir(exist_ok=True)
 for name,spec in lock.items():
  filename=name+('.exe' if system=='windows' else '');target=dest/filename;receipt=dest/(name+'.json')
  if target.exists() and receipt.exists():
   old=json.loads(receipt.read_text())
   if old.get('version')==spec['version'] and old.get('sha256')==hashlib.sha256(target.read_bytes()).hexdigest():continue
  source=spec[system];request=urllib.request.Request(source['url'],headers={'User-Agent':'Codex-Thronewake-build'})
  raw=urllib.request.urlopen(request,timeout=60).read()
  if 'sha256' in source:assert hashlib.sha256(raw).hexdigest()==source['sha256'],'Archive checksum mismatch'
  else:assert base64.b64encode(hashlib.sha512(raw).digest()).decode()==source['sha512'],'Archive integrity mismatch'
  if source['url'].endswith('.zip'):
   with zipfile.ZipFile(io.BytesIO(raw)) as archive:data=archive.read(filename)
  else:
   with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as archive:
    member_names={filename,name+'_extended'+('.exe' if system=='windows' else '')}
    matches=[m for m in archive.getmembers() if m.isfile() and Path(m.name).name in member_names]
    if len(matches)!=1:raise ValueError('Binary member is ambiguous')
    data=archive.extractfile(matches[0]).read()
  target.write_bytes(data);target.chmod(0o755)
  receipt.write_text(json.dumps({'version':spec['version'],'sha256':hashlib.sha256(data).hexdigest()},indent=2)+'\n')
  print(name,spec['version'],'verified')
if __name__=='__main__':install()

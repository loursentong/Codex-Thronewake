"""Import only approved unit artwork from the checksum-pinned supplied archive."""
import hashlib,json,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main(archive):
 assets=json.loads((ROOT/'ASSETS.json').read_bytes())
 if hashlib.sha256(archive.read_bytes()).hexdigest()!=assets['archive_sha256']:raise ValueError('Unreviewed artwork archive')
 bundle=json.loads((ROOT/'knowledge/bundle.json').read_bytes())
 with zipfile.ZipFile(archive) as z:
  for entity in bundle['entities'].values():
   if entity['kind']!='unit':continue
   key=entity['id'].removeprefix('unit.');name=key+'.png'
   raw=z.read('thronewake-compendium-master/static/images/units/'+name)
   if not raw.startswith(b'\x89PNG\r\n\x1a\n'):raise ValueError('Unexpected asset format')
   (ROOT/'static/images'/name).write_bytes(raw)
   assets['files'][name]={'sha256':hashlib.sha256(raw).hexdigest()}
 assets['files']=dict(sorted(assets['files'].items()))
 (ROOT/'ASSETS.json').write_text(json.dumps(assets,indent=2)+'\n',encoding='utf-8',newline='\n')
 print(json.dumps({'approved_assets':len(assets['files'])}))
if __name__=='__main__':main(Path(sys.argv[1]))

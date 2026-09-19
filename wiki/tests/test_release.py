"""Static and negative tests; isolated copies only, never mutation of TW."""
import copy,gzip,hashlib,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import build,check,import_tw,compare_release
class Release(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.bundle,cls.manifest=build.checked_bundle()
 def test_scope(self):self.assertEqual(len(self.bundle['entities']),9)
 def test_names(self):self.assertEqual(self.bundle['names']['building.main'],'Town Hall');self.assertEqual(self.bundle['names']['unit.raider'],'Raider')
 def test_resource_names(self):self.assertEqual([r['name'] for r in self.bundle['resources']],['Lumber','Stone','Metal','Food'])
 def test_raider_cost(self):
  fact=next(r for r in self.bundle['entities']['unit.raider']['facts'] if r['predicate']=='training_cost');self.assertEqual(fact['value'],dict(wood=95,clay=75,iron=40,crop=40))
 def test_no_inferred_training_building(self):
  for key in import_tw.UNIT_KEYS:self.assertIsNone(self.bundle['entities']['unit.'+key]['detail']['training_building'])
 def test_siege_qualification(self):self.assertIn('rule.J17_C_PATCH_RAM',[r['id'] for r in self.bundle['entities']['unit.war_ram']['rules']])
 def test_workshop_prerequisite(self):
  reqs=self.bundle['entities']['building.workshop']['detail']['requirements'];self.assertIn({'entity_id':'building.academy','kind':'required','level':10,'presence_flag':None},reqs)
 def test_workshop_level_one(self):
  levels=self.bundle['entities']['building.workshop']['catalogue']['levels'];one=next(r for r in levels if r['level']==1);self.assertEqual(one['cost'],dict(wood=460,clay=510,iron=600,crop=320));self.assertEqual(levels[-1]['level'],22)
 def test_full_provenance(self):
  for m in self.bundle['entities'].values():
   proofs=build.gather_proofs(m);self.assertTrue(proofs)
   for e in proofs:self.assertTrue(e['entity_key']);self.assertTrue(e['fields'])
 def test_bad_proof_rejected(self):
  with self.assertRaises(ValueError):build.gather_proofs({'evidence':[dict(source_id='x',entity_key='x',sha256='wrong',fields=['x'])]})
 def modified(self,mutator,reseal=False):
  (ROOT/'artifacts').mkdir(exist_ok=True)
  temp=tempfile.TemporaryDirectory(dir=ROOT/'artifacts',prefix='test-');root=Path(temp.name);(root/'knowledge').mkdir();b=copy.deepcopy(self.bundle);mutator(b);raw=import_tw.canonical(b).encode();m=dict(self.manifest)
  if reseal:m['bundle_sha256']=build.sha(raw)
  (root/'knowledge/bundle.json').write_bytes(raw);(root/'knowledge/manifest.json').write_text(json.dumps(m));return temp,root
 def test_changed_value_requires_review(self):
  temp,root=self.modified(lambda b:b['entities']['unit.raider']['detail']['stats'].update(attack=99))
  with temp,patch.object(build,'ROOT',root),self.assertRaises(ValueError):build.checked_bundle()
 def test_dangling_requirement_rejected(self):
  temp,root=self.modified(lambda b:b['entities']['building.workshop']['detail']['requirements'][0].update(entity_id='building.missing'),True)
  with temp,patch.object(build,'ROOT',root),self.assertRaises(ValueError):build.checked_bundle()
 def test_official_name_mismatch_rejected(self):
  temp,root=self.modified(lambda b:b['entities']['unit.raider'].update(name='Pillager'),True)
  with temp,patch.object(build,'ROOT',root),self.assertRaises(ValueError):build.checked_bundle()
 def test_path_traversal_rejected(self):
  temp,root=self.modified(lambda b:b['entities']['unit.raider'].update(path='../account/'),True)
  with temp,patch.object(build,'ROOT',root),self.assertRaises(ValueError):build.checked_bundle()
 def test_source_format_rejected(self):
  with self.assertRaises(ValueError):import_tw.project({'format':'wrong'})
 def test_raw_html_disabled(self):self.assertIn('unsafe = false',(ROOT/'hugo.toml').read_text())
 def test_no_default_page_approval(self):self.assertIn('not a new live account measurement',(ROOT/'layouts/_default/single.html').read_text())
 def test_generator_versions_pinned(self):
  lock=json.loads((ROOT/'toolchain.json').read_text());self.assertEqual(lock['hugo']['version'],'0.166.0');self.assertEqual(lock['pagefind']['version'],'1.5.2')
 def test_filter_decoder(self):
  raw=b'pagefind_dcd\x82dType\x82\x82dUnit\x82\x07\x08\x82hBuilding\x81\x01'
  self.assertEqual(compare_release.decode(gzip.compress(raw)),['Type',[['Unit',[7,8]],['Building',[1]]]])
 def test_filter_comparison_preserves_membership(self):
  a=['Type',sorted([['Unit',[7,8]],['Building',[1]]])]
  b=['Type',sorted([['Building',[1]],['Unit',[7,8]]])]
  self.assertEqual(compare_release.digest(a),compare_release.digest(b))
  b[1][1][1].append(9)
  self.assertNotEqual(compare_release.digest(a),compare_release.digest(b))
 def test_unknown_search_format_fails_closed(self):
  with self.assertRaises(ValueError):compare_release.decode(gzip.compress(b'wrong format'))
  with self.assertRaises(ValueError):compare_release.decode(gzip.compress(b'pagefind_dcd\xa0'))
 def test_artwork_credits_and_hashes(self):
  assets=json.loads((ROOT/'ASSETS.json').read_bytes())
  self.assertIn('credits',assets['authorization'])
  for name,info in assets['files'].items():self.assertEqual(build.sha((ROOT/'static/images'/name).read_bytes()),info['sha256'])
if __name__=='__main__':
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(Release);result=unittest.TextTestRunner(verbosity=2).run(suite)
 print(json.dumps({'success':result.wasSuccessful(),'tests':result.testsRun,'failed':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped)}));raise SystemExit(0 if result.wasSuccessful() else 1)

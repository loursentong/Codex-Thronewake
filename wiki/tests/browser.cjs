const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const base=process.env.TW_BASE||'http://127.0.0.1:8766/Codex-Thronewake/next/';
const out=process.env.TW_QA_DIR||path.join(__dirname,'..','artifacts','qa');fs.mkdirSync(out,{recursive:true});
function luminance(c){return c.map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4}).reduce((s,x,i)=>s+x*[.2126,.7152,.0722][i],0)}
function contrast(a,b){const x=luminance(a),y=luminance(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)}
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});const ctx=await browser.newContext({viewport:{width:1440,height:1000}});const page=await ctx.newPage();
 const errors=[],failed=[],checks=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)failed.push(r.url()+' '+r.status())});
 await ctx.route('**/*',r=>r.request().url().startsWith(base)?r.continue():r.abort());
 const raider=base+'reference/units/raider/';await page.goto(raider);
 assert.equal(await page.locator('h1').textContent(),'Raider');assert.deepEqual(await page.locator('#costs .cost-item strong').allTextContents(),['95','75','40','40']);checks.push('Source-backed Raider cost and name');
 const colors=await page.evaluate(()=>{const c=getComputedStyle(document.body);return [c.color,c.backgroundColor]});assert(contrast(...colors.map(s=>s.match(/\d+/g).map(Number)))>=7);checks.push('Body text contrast exceeds 7:1');
 await page.screenshot({path:path.join(out,'desktop.png'),fullPage:true});
 for(const width of [1440,1024,768,390,320]){
  await page.setViewportSize({width,height:900});await page.goto(raider);
  assert(!await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),'overflow '+width);
  for(const d of await page.locator('details.disclosure').all())await d.locator('summary').click();
  assert(!await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),'expanded overflow '+width);
  await page.evaluate(()=>scrollTo(0,document.body.scrollHeight));
  if(width===390){await page.goto(raider);await page.screenshot({path:path.join(out,'mobile.png'),fullPage:true});}
  checks.push('Full page/details at '+width+'px');
 }
 await page.getByRole('link',{name:'Suggest a correction'}).click();await page.locator('#change').fill('<img src=x onerror=alert(1)> Test only');await page.locator('#source').fill('Source verification test.');await page.getByRole('button',{name:'Prepare GitHub proposal'}).click();
 assert.equal(await page.locator('#proposal-text img').count(),0);
 const issue=new URL(await page.locator('#github-proposal').getAttribute('href'));assert.equal(issue.origin,'https://github.com');assert.equal(issue.pathname,'/loursentong/Codex-Thronewake/issues/new');assert(issue.searchParams.get('body').includes('unit.raider'));assert(issue.searchParams.get('body').includes('Data revision:'));assert(!await page.locator('dialog').evaluate(e=>e.scrollWidth>e.clientWidth));checks.push('Targeted GitHub draft URL, escaped input, mobile form; no submission');
 await page.keyboard.press('Escape');assert(await page.getByRole('link',{name:'Suggest a correction'}).evaluate(e=>e===document.activeElement));checks.push('Dialog focus returns');
 await page.goto(base+'reference/units/war-ram/');await page.getByRole('link',{name:'Workshop',exact:true}).click();assert.equal(await page.locator('h1').textContent(),'Workshop');await page.goto(base+'reference/buildings/workshop/#building.workshop.level.10');assert(await page.locator('#level-table').evaluate(e=>e.open));checks.push('Unit/prerequisite connection and nested level deep link');
 assert(!await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth));assert(await page.locator('#level-table tbody tr').count()===23);checks.push('All 23 building levels accessible at 320px without page overflow');
 await page.setViewportSize({width:1440,height:1000});await page.goto(base+'search/');
 await page.locator('.pagefind-ui__search-input').fill('Raider');await page.locator('.pagefind-ui__result-link').filter({hasText:'Raider'}).first().waitFor();
 const result=page.locator('.pagefind-ui__result-link').filter({hasText:'Raider'}).first();assert((await result.getAttribute('href')).includes('/Codex-Thronewake/next/reference/units/raider/'));await result.click();assert.equal(await page.locator('h1').textContent(),'Raider');checks.push('Real Pagefind result under production prefix');
 await page.goto(base+'search/');await page.locator('.pagefind-ui__search-input').fill('Workshop');await page.locator('.pagefind-ui__result-link').first().waitFor();
 await page.locator('summary').filter({hasText:/^Type$/}).click();await page.locator('#Type-Building').check();await page.waitForFunction(()=>{const a=[...document.querySelectorAll('.pagefind-ui__result-link')];return a.length===1&&a[0].textContent.trim()==='Workshop';});checks.push('Real Type filter narrows results to Workshop');
 await page.locator('#Type-Building').uncheck();await page.locator('.pagefind-ui__search-input').fill('zzzzzznotaword');await page.locator('.pagefind-ui__message').filter({hasText:/No results/i}).waitFor();checks.push('Search empty-result state');
 await page.goto(base+'search/');await page.locator('.pagefind-ui__search-input').fill('defence');await page.locator('.pagefind-ui__result-link').first().waitFor();checks.push('Pagefind indexes collapsed detail text');
 const searchColors=await page.locator('.pagefind-ui__search-input').evaluate(e=>{const c=getComputedStyle(e);return[c.color,c.backgroundColor]});
 assert(contrast(...searchColors.map(s=>s.match(/\d+/g).slice(0,3).map(Number)))>=4.5);assert(luminance(searchColors[1].match(/\d+/g).slice(0,3).map(Number))<.1);checks.push('Search input retains dark background and readable contrast');
 await page.screenshot({path:path.join(out,'search.png'),fullPage:true});
 await page.goto(raider+'?highlight=defence');assert(await page.locator('#combat-statistics').evaluate(e=>e.open));checks.push('Search query reveals matching collapsed content');
 const plainCtx=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:900}});const plain=await plainCtx.newPage();await plain.goto(raider);assert.equal(await plain.locator('h1').textContent(),'Raider');await plain.locator('#combat-statistics summary').click();assert(await plain.locator('#combat-statistics').evaluate(e=>e.open));await plain.getByRole('link',{name:'Suggest a correction'}).click();assert((await plain.locator('h1').textContent()).includes('accurate'));checks.push('No-JavaScript reference and correction fallback');
 assert.deepEqual(errors,[]);assert.deepEqual(failed,[]);checks.push('No browser errors or missing HTTP assets');
 await browser.close();fs.writeFileSync(path.join(out,'browser.json'),JSON.stringify({success:true,base,checks,errors,failed,submission:'Draft URL tested; no issue submitted'},null,2));console.log(JSON.stringify({success:true,checks:checks.length}));
})().catch(e=>{console.error(e);process.exit(1)});

'use strict';
(() => {
  const base=document.body.dataset.base;
  const nav=document.querySelector('.mobile-nav'),mq=matchMedia('(max-width:950px)');
  function navMode(){nav.open=!mq.matches;}navMode();mq.addEventListener('change',navMode);
  document.addEventListener('keydown',e=>{if(e.key==='/'&&!e.ctrlKey&&!e.metaKey&&!e.altKey&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)&&!document.querySelector('dialog[open]')){e.preventDefault();location.href=base+'search/';}});
  function reveal(){let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{return;}const target=id&&document.getElementById(id);if(target){for(let n=target;n;n=n.parentElement)if(n.tagName==='DETAILS')n.open=true;requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));}
    const terms=(new URLSearchParams(location.search).get('highlight')||'').toLowerCase().split(/\s+/).filter(Boolean);
    if(terms.length)document.querySelectorAll('details.disclosure').forEach(d=>{if(terms.some(t=>d.textContent.toLowerCase().includes(t)))d.open=true;});
  }addEventListener('hashchange',reveal);reveal();
  if(document.getElementById('search'))window.addEventListener('load',()=>{
    if(typeof PagefindUI==='undefined'){document.getElementById('search').textContent='Search could not load. Please browse the reference sections or try again.';return;}
    new PagefindUI({element:'#search',bundlePath:base+'pagefind/',showSubResults:true,showImages:false,resetStyles:false,highlightParam:'highlight'});
  });
  const dialog=document.getElementById('correction-dialog');let opener;
  document.querySelectorAll('.suggest').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();opener=a;dialog.showModal();document.getElementById('change').focus();}));
  dialog.querySelector('[data-close]').addEventListener('click',()=>dialog.close());dialog.addEventListener('close',()=>opener?.focus());
  document.getElementById('correction-form').addEventListener('submit',e=>{
    e.preventDefault();const article=document.querySelector('[data-entity]');
    const body=['Page: '+document.querySelector('h1').textContent,'Entity: '+article.dataset.entity,'Data revision: '+article.dataset.revision,'Section: '+(location.hash||'not specified'),'Area: '+document.getElementById('field').value,'','Proposed correction:',document.getElementById('change').value.trim(),'','Source and context:',document.getElementById('source').value.trim()].join('\n');
    document.getElementById('proposal-text').textContent=body;
    const url=new URL('https://github.com/loursentong/Codex-Thronewake/issues/new');url.searchParams.set('title','Correction: '+document.querySelector('h1').textContent);url.searchParams.set('body',body);
    const link=document.getElementById('github-proposal');link.href=url.href;
    document.getElementById('copy-status').textContent=url.href.length>7500?'Long proposal: copy the text and paste it into the GitHub issue if the prefill is unavailable.':'';
    document.getElementById('proposal-preview').hidden=false;document.getElementById('proposal-preview').scrollIntoView({block:'nearest'});
  });
  document.getElementById('copy-proposal').addEventListener('click',async()=>{try{await navigator.clipboard.writeText(document.getElementById('proposal-text').textContent);document.getElementById('copy-status').textContent='Copied. Nothing has been submitted.';}catch{document.getElementById('copy-status').textContent='Select and copy the text above. Clipboard access is unavailable.';}});
})();

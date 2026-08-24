(()=>{
  const mount=document.querySelector('[data-case-library]');
  const zh=(document.documentElement.lang||'').toLowerCase().startsWith('zh');
  const t=(c,en,cn)=>zh?c[cn]:c[en];
  const esc=s=>String(s??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const idx=document.querySelector('[data-case-index]');
  const filters=document.querySelector('[data-case-filters]');
  const labels=zh?{profile:'客户类型',pseudo:'客户化名',category:'产品品类',market:'市场',challenge:'客户问题',work:'工作内容',control:'控制节点',commercial:'商务关注',result:'代表性结果',all:'全部案例',commercialText:'供应商匹配、报价口径、MOQ、模具、样品、交期、包装与出口准备度分别作为独立决策项保持可见。'}:{profile:'Client profile',pseudo:'Pseudonym',category:'Product category',market:'Market',challenge:'Buyer challenge',work:'Our work package',control:'Control gate',commercial:'Commercial focus',result:'Representative result',all:'All cases',commercialText:'Supplier fit, quotation basis, MOQ, tooling, sample status, lead time, packaging and export readiness were kept visible as separate decision points.'};
  const sectors=[...new Map(CASE_LIBRARY.map(c=>[c.sector,zh?c.zhSector:c.sector])).entries()];
  let active='all';
  const visible=()=>active==='all'?CASE_LIBRARY:CASE_LIBRARY.filter(c=>c.sector===active);
  const renderIndex=()=>{if(idx) idx.innerHTML=visible().map(c=>`<a href="#case-${esc(c.n)}">${esc(c.n)} ${esc(t(c,'industry','zhIndustry'))}</a>`).join('');};
  const render=()=>{
    const data=visible(); renderIndex(); if(!mount)return;
    mount.innerHTML=data.map(c=>`<article class="case-study" id="case-${esc(c.n)}"><div class="case-study-media"><img loading="lazy" src="/assets/photos/${esc(c.photo)}" alt="${esc(t(c,'title','zhTitle'))}"><div class="case-study-head"><div class="case-study-no">${zh?'案例':'Case'} ${esc(c.n)}</div><div class="eyebrow">${esc(t(c,'industry','zhIndustry'))} · ${esc(c.market)}</div><h2>${esc(t(c,'title','zhTitle'))}</h2><p>${esc(t(c,'challenge','zhChallenge'))}</p><div class="case-client"><div><span>${labels.profile}</span><strong>${esc(t(c,'profile','zhProfile'))}</strong></div><div><span>${labels.pseudo}</span><strong>${esc(c.client)}</strong></div><div><span>${labels.category}</span><strong>${esc(t(c,'industry','zhIndustry'))}</strong></div><div><span>${labels.market}</span><strong>${esc(c.market)}</strong></div></div><div class="case-tags">${c.tags.map(tag=>`<span class="case-tag">${esc(tag)}</span>`).join('')}</div></div></div><div class="case-study-body"><div class="case-detail-grid"><div class="case-detail"><h3>${labels.challenge}</h3><p>${esc(t(c,'challenge','zhChallenge'))}</p></div><div class="case-detail"><h3>${labels.work}</h3><p>${esc(t(c,'work','zhWork'))}</p></div><div class="case-detail"><h3>${labels.control}</h3><p>${esc(t(c,'control','zhControl'))}</p></div><div class="case-detail"><h3>${labels.commercial}</h3><p>${labels.commercialText}</p></div></div><div class="case-result"><strong>${labels.result}</strong><p>${esc(t(c,'result','zhResult'))}</p></div></div></article>`).join('');
  };
  if(filters){filters.innerHTML=[`<button type="button" data-sector="all" class="active">${labels.all} <span>${CASE_LIBRARY.length}</span></button>`,...sectors.map(([key,label])=>`<button type="button" data-sector="${esc(key)}">${esc(label)} <span>${CASE_LIBRARY.filter(c=>c.sector===key).length}</span></button>`)].join('');filters.addEventListener('click',e=>{const b=e.target.closest('button[data-sector]');if(!b)return;active=b.dataset.sector;filters.querySelectorAll('button').forEach(x=>x.classList.toggle('active',x===b));render();window.scrollTo({top:mount.offsetTop-110,behavior:'smooth'});});}
  render();
})();

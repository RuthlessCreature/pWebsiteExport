const CONTACT={name:'Yusuf',email:'abd.yusuf.ibrahim.mustafa@gmail.com',phoneDisplay:'+86 132 4269 4270',phone:'+8613242694270'};

(()=>{
  const nav=document.querySelector('[data-nav]');
  if(!nav) return;
  [...nav.querySelectorAll('a')].forEach(a=>{const h=a.getAttribute('href')||'';if(['/zh/','/en/','/ja/','/ru/','/es/','/pt/'].includes(h)&&!a.classList.contains('nav-cta'))a.remove();});
  const path=location.pathname;let active='EN';if(path.startsWith('/zh/'))active='中文';else if(path.startsWith('/ja/'))active='日本語';else if(path.startsWith('/ru/'))active='RU';else if(path.startsWith('/es/'))active='ES';else if(path.startsWith('/pt/'))active='PT';
  const lang=document.createElement('details');lang.className='lang-menu';lang.innerHTML=`<summary>${active}</summary><div class="lang-popover"><a href="/zh/">中文</a><a href="/en/">English</a><a href="/ja/">日本語</a><a href="/ru/">Русский</a><a href="/es/">Español</a><a href="/pt/">Português</a></div>`;
  const cta=nav.querySelector('.nav-cta');nav.insertBefore(lang,cta||null);
})();

const menuButton=document.querySelector('[data-menu]');const nav=document.querySelector('[data-nav]');if(menuButton&&nav){menuButton.addEventListener('click',()=>nav.classList.toggle('open'));}

function trackEvent(event,target=''){
  const payload=JSON.stringify({event,page:location.pathname,target,language:document.documentElement.lang||''});
  try{
    if(navigator.sendBeacon){const blob=new Blob([payload],{type:'application/json'});if(navigator.sendBeacon('/api/event',blob))return;}
    fetch('/api/event',{method:'POST',headers:{'content-type':'application/json'},body:payload,keepalive:true,credentials:'same-origin'}).catch(()=>{});
  }catch(_e){}
}

document.addEventListener('click',(e)=>{
  const a=e.target.closest&&e.target.closest('a');if(!a)return;
  const href=a.getAttribute('href')||'';
  if(href.startsWith('https://wa.me/'))trackEvent('whatsapp_click','whatsapp');
  else if(href.startsWith('mailto:'))trackEvent('email_click','email');
  else if(href.startsWith('tel:'))trackEvent('phone_click','phone');
  else if(/^\/resources\/.*\.(?:csv|xlsx|pdf)(?:$|\?)/i.test(href))trackEvent('resource_download',href.split('?')[0]);
  else if(href==='/contact/'||href.startsWith('/contact/?'))trackEvent('contact_click','/contact/');
},true);

const inquiry=document.querySelector('[data-inquiry-form]');
if(inquiry){
  trackEvent('rfq_open','contact-form');
  inquiry.addEventListener('submit',(e)=>{
    e.preventDefault();
    const data=new FormData(inquiry);
    trackEvent('rfq_mailto_submit','contact-form');
    const lines=['Hello Pomerol International,','',`Name: ${data.get('name')||''}`,`Company: ${data.get('company')||''}`,`Email: ${data.get('email')||''}`,`Country/Market: ${data.get('market')||''}`,`Product / Category: ${data.get('product')||''}`,`Estimated quantity: ${data.get('quantity')||''}`,`Target timing: ${data.get('timing')||''}`,'',String(data.get('message')||'')];
    const subject=encodeURIComponent(`Sourcing inquiry — ${data.get('product')||data.get('company')||'new project'}`);
    const body=encodeURIComponent(lines.join('\n'));
    window.location.href=`mailto:${CONTACT.email}?subject=${subject}&body=${body}`;
  });
}

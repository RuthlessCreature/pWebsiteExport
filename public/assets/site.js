(()=>{for(const href of ['/assets/photo-cases.css','/assets/locale.css']){if(!document.querySelector(`link[href="${href}"]`)){const l=document.createElement('link');l.rel='stylesheet';l.href=href;document.head.appendChild(l);}}})();

const CONTACT={name:'Yusuf',email:'abd.yusuf.ibrahim.mustafa@gmail.com',phoneDisplay:'+86 132 4269 4270',phone:'+8613242694270'};

(()=>{
  const nav=document.querySelector('[data-nav]');
  if(!nav) return;
  [...nav.querySelectorAll('a')].forEach(a=>{const h=a.getAttribute('href')||'';if(['/zh/','/en/','/ja/','/ru/','/es/','/pt/'].includes(h)&&!a.classList.contains('nav-cta'))a.remove();});
  const path=location.pathname;let active='EN';if(path.startsWith('/zh/'))active='中文';else if(path.startsWith('/ja/'))active='日本語';else if(path.startsWith('/ru/'))active='RU';else if(path.startsWith('/es/'))active='ES';else if(path.startsWith('/pt/'))active='PT';
  const lang=document.createElement('details');lang.className='lang-menu';lang.innerHTML=`<summary>${active}</summary><div class="lang-popover"><a href="/zh/">中文</a><a href="/en/">English</a><a href="/ja/">日本語</a><a href="/ru/">Русский</a><a href="/es/">Español</a><a href="/pt/">Português</a></div>`;
  const cta=nav.querySelector('.nav-cta');nav.insertBefore(lang,cta||null);
})();

(()=>{
  const replacements=[['Nicole',CONTACT.name],['13923387986@163.com',CONTACT.email],['+86 139 2338 7986',CONTACT.phoneDisplay],['+8613923387986',CONTACT.phone]];
  const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=walker.nextNode()){for(const [a,b] of replacements){if(n.nodeValue&&n.nodeValue.includes(a))n.nodeValue=n.nodeValue.split(a).join(b);}}
  document.querySelectorAll('a[href]').forEach(a=>{let h=a.getAttribute('href')||'';h=h.replace('mailto:13923387986@163.com','mailto:'+CONTACT.email).replace('tel:+8613923387986','tel:'+CONTACT.phone).replace('https://wa.me/8613923387986','https://wa.me/'+CONTACT.phone.replace('+',''));a.setAttribute('href',h);});
})();

const menuButton=document.querySelector('[data-menu]');const nav=document.querySelector('[data-nav]');if(menuButton&&nav){menuButton.addEventListener('click',()=>nav.classList.toggle('open'));}
const inquiry=document.querySelector('[data-inquiry-form]');if(inquiry){inquiry.addEventListener('submit',(e)=>{e.preventDefault();const data=new FormData(inquiry);const lines=['Hello Pomerol International,','',`Name: ${data.get('name')||''}`,`Company: ${data.get('company')||''}`,`Email: ${data.get('email')||''}`,`Country/Market: ${data.get('market')||''}`,`Product / Category: ${data.get('product')||''}`,`Estimated quantity: ${data.get('quantity')||''}`,`Target timing: ${data.get('timing')||''}`,'',String(data.get('message')||'')];const subject=encodeURIComponent(`Sourcing inquiry — ${data.get('product')||data.get('company')||'new project'}`);const body=encodeURIComponent(lines.join('\n'));window.location.href=`mailto:${CONTACT.email}?subject=${subject}&body=${body}`;});}

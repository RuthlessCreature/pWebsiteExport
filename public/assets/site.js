(()=>{const href='/assets/photo-cases.css';if(!document.querySelector(`link[href="${href}"]`)){const l=document.createElement('link');l.rel='stylesheet';l.href=href;document.head.appendChild(l);}})();
const menuButton=document.querySelector('[data-menu]');const nav=document.querySelector('[data-nav]');
if(menuButton&&nav){menuButton.addEventListener('click',()=>nav.classList.toggle('open'));}
const inquiry=document.querySelector('[data-inquiry-form]');
if(inquiry){inquiry.addEventListener('submit',(e)=>{e.preventDefault();const data=new FormData(inquiry);const lines=[
  'Hello Pomerol International,','',`Name: ${data.get('name')||''}`,`Company: ${data.get('company')||''}`,`Email: ${data.get('email')||''}`,`Country/Market: ${data.get('market')||''}`,`Product / Category: ${data.get('product')||''}`,`Estimated quantity: ${data.get('quantity')||''}`,`Target timing: ${data.get('timing')||''}`,'',String(data.get('message')||'')
];const subject=encodeURIComponent(`Sourcing inquiry — ${data.get('product')||data.get('company')||'new project'}`);const body=encodeURIComponent(lines.join('\n'));window.location.href=`mailto:13923387986@163.com?subject=${subject}&body=${body}`;});}

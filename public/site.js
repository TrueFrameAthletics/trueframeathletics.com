(function(){
 const toggle=document.getElementById('nav-toggle'),nav=document.getElementById('nav-menu');
 function close(){nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');toggle.textContent='Menu';}
 toggle?.addEventListener('click',()=>{const open=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open));toggle.textContent=open?'Close':'Menu';});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav?.classList.contains('open')){close();toggle.focus();}});
 document.getElementById('yr').textContent=new Date().getFullYear();
 const form=document.getElementById('contact-form');if(!form)return;
 const alias={sideline:'Sideline Support',practice:'Practice Integration',ongoing:'Ongoing Team Support',individual:'Individual Athlete Coaching',workshop:'Team Workshop',team:'Ongoing Team Support',coach:'Coach Development',college:'College Athletic Program Collaboration',general:'General Business Inquiry'};
 const key=new URLSearchParams(location.search).get('inquiry');if(alias[key])form.elements.inquiry_type.value=alias[key];
 if(key==='film')form.elements.message.value='Interested in film and pressure review.\n\n';
 const status=document.getElementById('f-status'),button=document.getElementById('f-submit');
 function show(type,message){status.className='form-status '+type;status.textContent=message;status.hidden=false;}
 form.addEventListener('submit',async e=>{e.preventDefault();if(!form.reportValidity())return;
 const raw=Object.fromEntries(new FormData(form));
 const data={name:raw.name.trim(),email:raw.email.trim(),phone:raw.phone,role:raw.role,sport:raw.sport,organization:raw.organization,company_website:raw.company_website,services:[raw.inquiry_type],message:[`Location: ${raw.location||'-'}`,`Athlete: ${raw.athlete_name||'-'}`,`Age or grade: ${raw.athlete_age||'-'}`,`Challenge: ${raw.concern||'-'}`,'',raw.message||''].join('\n')};
 button.disabled=true;show('','Sending your request…');
 try{const response=await fetch('/api/contact',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});if(!response.ok)throw new Error('send');const result=await response.json();if(!result.ok)throw new Error('send');form.reset();show('ok','Request received. Richard will follow up to discuss your team and the support you’re looking for.');}
 catch{show('err','Your request could not be sent. Please email rich@trueframeathletics.com or call 402-506-3816. Your entries are still here so you can try again.');}
 finally{button.disabled=false;}
 });
})();

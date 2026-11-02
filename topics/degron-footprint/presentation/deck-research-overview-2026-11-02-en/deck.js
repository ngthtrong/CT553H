(() => {
  const slides=[...document.querySelectorAll('.slide')], mainCount=34;
  const deck=document.getElementById('deck'), counter=document.getElementById('counter');
  const overview=document.getElementById('overview'), notes=document.getElementById('notes'), help=document.getElementById('help');
  let index=0, chart;
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  document.body.classList.toggle('reduced-motion',reduced.matches);
  reduced.addEventListener('change',e=>document.body.classList.toggle('reduced-motion',e.matches));
  function resize(){const v=document.getElementById('viewport');const scale=Math.min(v.clientWidth/1280,v.clientHeight/720);deck.style.transform=`translate(-50%,-50%) scale(${scale})`;}
  function getIndex(){const m=location.hash.match(/slide-(\d+)/);return m?Number(m[1])-1:0;}
  function syncGif(){slides.forEach((s,i)=>s.querySelectorAll('img.animated-gif').forEach(img=>{if(i===index&&!document.body.classList.contains('motion-paused')&&!reduced.matches){if(img.dataset.gif)img.src=img.dataset.gif;}else if(img.dataset.poster)img.src=img.dataset.poster;}));}
  function show(n,writeHash=true){index=Math.max(0,Math.min(slides.length-1,n));slides.forEach((s,i)=>{s.classList.toggle('active',i===index);s.setAttribute('aria-hidden',i===index?'false':'true');s.inert=i!==index;});
    counter.textContent=index<mainCount?`${index+1} / ${mainCount}`:`Appendix ${index-mainCount+1} / ${slides.length-mainCount}`;
    document.getElementById('progress').style.width=((index+1)/slides.length*100)+'%';
    document.getElementById('status').textContent=slides[index].dataset.title;
    if(writeHash)history.replaceState(null,'',`#slide-${index+1}`);syncGif();if(slides[index].querySelector('#recipeChart'))initChart();
  }
  function openOverview(){const grid=document.getElementById('overview-grid');grid.replaceChildren();slides.forEach((s,i)=>{const b=document.createElement('button');b.className=i===index?'current':'';const n=document.createElement('span');n.className='num';n.textContent=i<mainCount?String(i+1).padStart(2,'0'):`Appendix ${i-mainCount+1}`;b.append(n,document.createTextNode(s.dataset.title));b.addEventListener('click',()=>{overview.close();show(i)});grid.append(b)});overview.showModal();grid.querySelector('.current')?.focus();}
  function openNotes(){document.getElementById('notes-title').textContent=slides[index].dataset.title;document.getElementById('notes-body').innerHTML=slides[index].querySelector('.speaker-notes').innerHTML;notes.showModal();}
  function pause(){const paused=document.body.classList.toggle('motion-paused');const b=document.getElementById('motion');b.setAttribute('aria-pressed',String(paused));b.textContent=paused?'Resume motion':'Pause motion';syncGif();}
  function initChart(metric='mae'){
    const canvas=document.getElementById('recipeChart');if(!canvas||!window.Chart)return;
    if(chart)chart.destroy();const rows=DECK_DATA.explorer;
    const labels={mae:'MAE (PSI) · lower is better',auroc:'Positive-event AUROC · higher is better',ap:'Positive-event AP · higher is better'};
    chart=new Chart(canvas,{type:'bar',data:{labels:rows.map(r=>r.name),datasets:[{data:rows.map(r=>r[metric]),backgroundColor:rows.map(r=>r.name.includes('ESM + CNN')?'#18974c':'#a9b7a8'),borderRadius:2}]},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,animation:reduced.matches?false:{duration:350},plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>`${labels[metric]}: ${c.raw.toFixed(6)}`}}},scales:{x:{beginAtZero:true,max:metric==='mae'?.5:1,title:{display:true,text:labels[metric],font:{family:'Be Vietnam Pro',size:16}},grid:{color:'#e3e8df'},ticks:{font:{family:'Be Vietnam Pro',size:13}}},y:{grid:{display:false},ticks:{font:{family:'Be Vietnam Pro',size:15},color:'#193a2b'}}}}});
    document.querySelectorAll('[data-metric]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.metric===metric)));
  }
  document.getElementById('prev').onclick=()=>show(index-1);document.getElementById('next').onclick=()=>show(index+1);
  document.getElementById('overview-button').onclick=openOverview;document.getElementById('notes-button').onclick=openNotes;
  document.getElementById('motion').onclick=pause;document.getElementById('help-button').onclick=()=>help.showModal();
  document.getElementById('full-button').onclick=()=>document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen?.();
  document.querySelectorAll('dialog .close').forEach(b=>b.onclick=()=>b.closest('dialog').close());
  document.querySelectorAll('[data-metric]').forEach(b=>b.onclick=()=>initChart(b.dataset.metric));
  document.addEventListener('keydown',e=>{if(document.querySelector('dialog[open]')||/INPUT|SELECT|TEXTAREA/.test(e.target.tagName)||e.ctrlKey||e.metaKey||e.altKey)return;
    if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();show(index+1)}
    if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();show(index-1)}
    if(e.key==='Home'){e.preventDefault();show(0)}if(e.key==='End'){e.preventDefault();show(mainCount-1)}
    if(e.key.toLowerCase()==='o')openOverview();if(e.key.toLowerCase()==='n')openNotes();if(e.key.toLowerCase()==='m')pause();
    if(e.key.toLowerCase()==='f')document.getElementById('full-button').click();
  });
  let touchX=0,touchY=0;document.getElementById('viewport').addEventListener('touchstart',e=>{touchX=e.changedTouches[0].clientX;touchY=e.changedTouches[0].clientY},{passive:true});
  document.getElementById('viewport').addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-touchX,dy=e.changedTouches[0].clientY-touchY;if(Math.abs(dx)>60&&Math.abs(dx)>Math.abs(dy))show(index+(dx<0?1:-1))},{passive:true});
  addEventListener('resize',resize);addEventListener('hashchange',()=>show(getIndex(),false));document.fonts.ready.then(resize);resize();show(getIndex(),false);
  window.DECK={show,resize,get index(){return index},mainCount,total:slides.length};
})();

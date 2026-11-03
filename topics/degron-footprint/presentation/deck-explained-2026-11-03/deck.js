(() => {
  const slides = [...document.querySelectorAll('.slide')];
  const mainCount = slides.filter(s => s.dataset.appendix === 'false').length;
  const deck = document.getElementById('deck');
  const overview = document.getElementById('overview');
  const notes = document.getElementById('notes');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let index = 0, step = 0, chart, metric = 'mae';
  const maxStep = () => Math.max(0, ...[...slides[index].querySelectorAll('[data-step]')].map(e => +e.dataset.step));
  const paused = () => document.body.classList.contains('motion-paused') || reduced.matches;
  function resize() {
    const v = document.getElementById('viewport');
    deck.style.transform = `translate(-50%,-50%) scale(${Math.min(v.clientWidth/1280,v.clientHeight/720)})`;
  }
  function syncMedia() {
    document.body.classList.toggle('reduced-motion',reduced.matches);
    slides.forEach((s,i) => {
      s.querySelectorAll('video').forEach(video => {
        if (i===index && !paused() && !video.dataset.userPaused) video.play().catch(() => {});
        else video.pause();
      });
      s.querySelectorAll('.animated-gif').forEach(img => {
        if (!img.dataset.gif) img.dataset.gif=img.getAttribute('src');
        img.src = i===index && !paused() ? img.dataset.gif : 'assets/fam188a-poster.png';
      });
    });
    if (chart) chart.options.animation=paused()?false:{duration:300};
  }
  function syncSteps() {
    slides[index].querySelectorAll('[data-step]').forEach(e=>e.classList.toggle('future',+e.dataset.step>step));
    const count = index<mainCount ? `${index+1} / ${mainCount}` : `Phụ lục ${index-mainCount+1} / ${slides.length-mainCount}`;
    document.getElementById('counter').textContent=count+(maxStep()?` · bước ${step+1}/${maxStep()+1}`:'');
  }
  function show(n,all=false,writeHash=true) {
    index=Math.max(0,Math.min(slides.length-1,n));
    slides.forEach((s,i)=>{s.classList.toggle('active',i===index);s.setAttribute('aria-hidden',String(i!==index));s.inert=i!==index;});
    step=all?maxStep():0;syncSteps();syncMedia();
    document.getElementById('progress').style.width=`${(index+1)/slides.length*100}%`;
    document.getElementById('status').textContent=slides[index].dataset.title;
    if(writeHash) history.replaceState(null,'',`#slide-${index+1}`);
    if(slides[index].querySelector('#recipeChart')) initChart(metric);
  }
  function next(skip=false){if(!skip && step<maxStep()){step++;syncSteps();}else show(index+1);}
  function prev(skip=false){if(!skip && step>0){step--;syncSteps();}else show(index-1,true);}
  function openOverview(){
    const grid=document.getElementById('overview-grid');grid.replaceChildren();
    slides.forEach((s,i)=>{const b=document.createElement('button');b.className=i===index?'current':'';
      const label=document.createElement('span');label.className='num';label.textContent=i<mainCount?String(i+1).padStart(2,'0'):`Phụ lục ${i-mainCount+1}`;
      b.append(label,document.createTextNode(s.dataset.title));b.onclick=()=>{overview.close();show(i);};grid.append(b);});
    overview.showModal();grid.querySelector('.current')?.focus();
  }
  function openNotes(){document.getElementById('notes-title').textContent=slides[index].dataset.title;document.getElementById('notes-body').innerHTML=slides[index].querySelector('.speaker-notes').innerHTML;notes.showModal();}
  function toggleMotion(){
    const value=document.body.classList.toggle('motion-paused'),button=document.getElementById('motion');
    button.setAttribute('aria-pressed',String(value));button.textContent=value?'Tiếp tục chuyển động':'Dừng chuyển động';syncMedia();
  }
  function initChart(selected='mae'){
    metric=selected;const canvas=document.getElementById('recipeChart');if(!canvas || !window.Chart)return;
    if(chart)chart.destroy();const rows=DECK_DATA.explorer;
    const labels={mae:'MAE (PSI) · thấp hơn tốt hơn',auroc:'AUROC dương · cao hơn tốt hơn',ap:'AP dương · cao hơn tốt hơn'};
    chart=new Chart(canvas,{type:'bar',data:{labels:rows.map(r=>r.name),datasets:[{data:rows.map(r=>r[metric]),backgroundColor:['#a9b7a8','#477ca7','#18974c','#0a5032','#c76242'],borderRadius:3}]},
      options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,animation:paused()?false:{duration:300},layout:{padding:{right:80}},
      plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>`${labels[metric]}: ${c.raw.toFixed(6)}`}}},
      scales:{x:{beginAtZero:true,max:metric==='mae'?.5:1,title:{display:true,text:labels[metric],font:{family:'Be Vietnam Pro',size:17}},ticks:{font:{family:'Be Vietnam Pro',size:15}},grid:{color:'#e3e8df'}},
      y:{ticks:{font:{family:'Be Vietnam Pro',size:19},color:'#193a2b'},grid:{display:false}}}},
      plugins:[{id:'valueLabels',afterDatasetsDraw(c){const ctx=c.ctx;ctx.save();ctx.font='600 18px "Be Vietnam Pro"';ctx.fillStyle='#193a2b';ctx.textBaseline='middle';c.getDatasetMeta(0).data.forEach((bar,i)=>ctx.fillText(rows[i][metric].toFixed(4).replace('.',','),bar.x+12,bar.y));ctx.restore();}}]});
    document.querySelectorAll('[data-metric]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.metric===metric)));
  }
  document.getElementById('prev').onclick=()=>prev();document.getElementById('next').onclick=()=>next();
  document.getElementById('overview-button').onclick=openOverview;document.getElementById('notes-button').onclick=openNotes;
  document.getElementById('motion').onclick=toggleMotion;
  document.getElementById('full-button').onclick=()=>document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen?.();
  document.getElementById('help-button').onclick=()=>document.getElementById('help').showModal();
  document.querySelectorAll('dialog .close').forEach(b=>b.onclick=()=>b.closest('dialog').close());
  document.querySelectorAll('[data-metric]').forEach(b=>b.onclick=()=>initChart(b.dataset.metric));
  document.querySelectorAll('.video-toggle').forEach(b=>b.onclick=()=>{const v=b.parentElement.querySelector('video');if(v.paused){delete v.dataset.userPaused;if(!paused())v.play().catch(()=>{});}else{v.dataset.userPaused='true';v.pause();}});
  document.addEventListener('keydown',e=>{
    if(document.querySelector('dialog[open]')||/INPUT|SELECT|TEXTAREA/.test(e.target.tagName)||e.ctrlKey||e.metaKey||e.altKey)return;
    // Keep native activation of focused controls with Space/Enter.
    if(/BUTTON|A/.test(e.target.tagName) && [' ','Enter'].includes(e.key))return;
    if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();next(e.shiftKey);}
    if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();prev(e.shiftKey);}
    if(e.key==='Home'){e.preventDefault();show(0);}if(e.key==='End'){e.preventDefault();show(mainCount-1,true);}
    if(e.key.toLowerCase()==='o')openOverview();if(e.key.toLowerCase()==='n')openNotes();
    if(e.key.toLowerCase()==='m')toggleMotion();if(e.key.toLowerCase()==='f')document.getElementById('full-button').click();
  });
  let touchX=0,touchY=0;document.getElementById('viewport').addEventListener('touchstart',e=>{touchX=e.changedTouches[0].clientX;touchY=e.changedTouches[0].clientY;},{passive:true});
  document.getElementById('viewport').addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-touchX,dy=e.changedTouches[0].clientY-touchY;if(Math.abs(dx)>60&&Math.abs(dx)>Math.abs(dy))dx<0?next():prev();},{passive:true});
  reduced.addEventListener('change',syncMedia);addEventListener('resize',resize);
  const hashIndex=()=>{const m=location.hash.match(/slide-(\d+)/);return m?+m[1]-1:0;};
  addEventListener('hashchange',()=>show(hashIndex(),false,false));
  addEventListener('beforeprint',()=>{slides.forEach(s=>s.querySelectorAll('video').forEach(v=>v.pause()));});
  addEventListener('afterprint',syncMedia);
  window.DECK={show,next,prev,resize,get index(){return index;},get step(){return step;},get metric(){return metric;},mainCount,total:slides.length};
  resize();show(hashIndex(),false,false);document.fonts.ready.then(()=>{resize();if(chart)initChart(metric);});
})();

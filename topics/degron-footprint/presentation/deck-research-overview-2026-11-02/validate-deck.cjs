const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:900},deviceScaleFactor:1});
 await page.context().setOffline(true);
 const errors=[],networkRequests=[];page.on('pageerror',e=>errors.push(e.message));
 page.on('request',r=>{if(/^https?:/.test(r.url()))networkRequests.push(r.url())});
 const out=path.join(__dirname,'previews');fs.mkdirSync(out,{recursive:true});
 await page.goto(pathToFileURL(path.join(__dirname,'index.html')).href);await page.evaluate(()=>document.fonts.ready);
 const results=[];
 for(let i=0;i<50;i++){
  await page.evaluate(i=>window.DECK.show(i),i);await page.waitForTimeout(100);
  const r=await page.evaluate(()=>{
   const s=document.querySelector('.slide.active'),bounds=s.getBoundingClientRect(),bad=[];
   const visible=e=>{const x=getComputedStyle(e);return x.display!=='none'&&x.visibility!=='hidden'&&e.getBoundingClientRect().width>0};
   for(const e of s.querySelectorAll('h1,h2,p,.insight,.context,.table,.table td,svg text')){
    if(e.closest('.speaker-notes')||!visible(e))continue;const b=e.getBoundingClientRect();
    if(b.left<bounds.left-1||b.right>bounds.right+1||b.top<bounds.top-1||b.bottom>bounds.bottom+1)bad.push({tag:e.tagName,text:e.textContent.slice(0,85),rect:{x:b.x,y:b.y,w:b.width,h:b.height}});
   }
   const words=[...s.querySelectorAll('header,.body,.insight')].map(e=>e.innerText).join(' ').split(/\s+/).filter(Boolean).length;
   const broken=[...s.querySelectorAll('img')].filter(e=>!e.complete||e.naturalWidth===0).map(e=>e.getAttribute('src'));
   const text=[...s.querySelectorAll('header,.body,.insight')].map(e=>e.innerText).join(' ');
   const forbidden=text.match(/\b(?:R\d+|[A-E][−–-][A-E]|Arm\s+[A-E]|W5|M3|P0)\b/g)||[];
   return {title:s.dataset.title,overflow:bad,brokenImages:broken,words,forbiddenLabels:forbidden};
  });
  r.slide=i+1;results.push(r);
  await page.locator('#deck').screenshot({path:path.join(out,`slide-${String(i+1).padStart(2,'0')}.png`),animations:'disabled'});
 }
 await page.evaluate(()=>window.DECK.show(1));await page.waitForTimeout(400);
 const motionBefore=await page.evaluate(()=>document.getAnimations().filter(a=>a.playState==='running').length);
 await page.locator('#motion').click();
 const motionAfter=await page.evaluate(()=>document.getAnimations().filter(a=>a.playState==='running').length);
 await page.locator('#overview-button').click();const overviewCount=await page.locator('#overview-grid button').count();
 await page.keyboard.press('Escape');await page.locator('#notes-button').click();const hasNotes=(await page.locator('#notes-body').innerText()).length>50;
 await page.keyboard.press('Escape');await page.keyboard.press('Home');await page.keyboard.press('ArrowRight');
 const keyboardIndex=await page.evaluate(()=>DECK.index);
 await page.evaluate(()=>DECK.show(42));await page.locator('[data-metric="ap"]').click();
 const chartWorks=await page.evaluate(()=>{const c=Chart.getChart(document.getElementById('recipeChart'));return c?.data.datasets[0].data[0]===DECK_DATA.explorer[0].ap;});
 await page.emulateMedia({reducedMotion:'reduce'});await page.evaluate(()=>DECK.show(1));
 const reducedMotion=await page.evaluate(()=>getComputedStyle(document.querySelector('.slide.active .animated-gif')).display==='none');
 const screens=[];
 for(const size of [{width:1280,height:720},{width:1920,height:1080},{width:390,height:844},{width:844,height:390}]){
  await page.setViewportSize(size);await page.evaluate(()=>DECK.show(4));await page.waitForTimeout(80);
  screens.push(await page.evaluate(size=>({size,documentOverflow:document.documentElement.scrollWidth>innerWidth,deckRect:document.querySelector('#deck').getBoundingClientRect().toJSON()}),size));
 }
 const links=await page.evaluate(()=>[...document.querySelectorAll('a[href]')].map(e=>e.getAttribute('href')).filter(u=>!/^https?:|^#/.test(u)));
 const brokenLinks=[...new Set(links)].filter(u=>!fs.existsSync(path.resolve(__dirname,u)));
 await page.emulateMedia({media:'print'});
 const printSlideCount=await page.evaluate(()=>[...document.querySelectorAll('.slide')].filter(s=>getComputedStyle(s).display==='flex').length);
 const report={slides:results,scriptErrors:errors,offline:true,networkRequests,printSlideCount,motion:{running:motionBefore,afterPause:motionAfter,reducedMotion},overviewCount,hasNotes,keyboardIndex,chartWorks,screens,brokenLinks};
 const bad=results.filter(r=>r.overflow.length||r.brokenImages.length||r.forbiddenLabels.length);
 report.pass=!bad.length&&!errors.length&&!brokenLinks.length&&overviewCount===50&&printSlideCount===50&&!networkRequests.length&&hasNotes&&keyboardIndex===1&&chartWorks&&motionAfter===0&&reducedMotion&&!screens.some(s=>s.documentOverflow);
 fs.writeFileSync(path.join(__dirname,'validation.json'),JSON.stringify(report,null,2));await browser.close();
 console.log(JSON.stringify({pass:report.pass,problemSlides:bad,scriptErrors:errors,brokenLinks,motion:report.motion,overviewCount,chartWorks,offline:true,networkRequests,printSlideCount},null,2));
 if(!report.pass)process.exitCode=1;
})().catch(e=>{console.error(e);process.exit(1)});

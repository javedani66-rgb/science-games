/* D217: وضوح کاراکترها (ماژول مشترک ماکت‌ها). تصویر منبع برای هر نمایش چندمرحله‌ای (نصف‌نصف) تا اندازهٔ واقعیِ روی صفحه × چگالی پیکسل کوچک می‌شود و تیز‌کنندهٔ ملایم می‌گیرد؛ کوچک‌کردن یک‌مرحله‌ایِ مرورگر خطوط نازک را گل‌آلود می‌کند. استفاده: crispEl(<img> یا <image> SVG, منبع) */
const CR=new Map();
function crisp(url,cssH,done){const dpr=Math.max(1,devicePixelRatio||1),H=Math.max(60,Math.min(640,Math.round(cssH*dpr))),key=url.length+':'+url.slice(-40)+':'+H;if(CR.has(key)){done(CR.get(key));return}
 const im=new Image();im.onload=()=>{try{let src=im,w0=im.naturalWidth,h0=im.naturalHeight;if(h0<=H*1.05){CR.set(key,url);done(url);return}const W=Math.round(w0*H/h0);
  while(h0/2>=H){const c=document.createElement('canvas');c.width=Math.round(w0/2);c.height=Math.round(h0/2);const x=c.getContext('2d');x.imageSmoothingEnabled=true;x.imageSmoothingQuality='high';x.drawImage(src,0,0,c.width,c.height);src=c;w0=c.width;h0=c.height}
  const c=document.createElement('canvas');c.width=W;c.height=H;const x=c.getContext('2d');x.imageSmoothingEnabled=true;x.imageSmoothingQuality='high';x.drawImage(src,0,0,W,H);
  const d=x.getImageData(0,0,W,H),o=d.data,s=new Uint8ClampedArray(o);const A=.55;
  for(let y=1;y<H-1;y++)for(let q=1;q<W-1;q++){const k=(y*W+q)*4;if(s[k+3]<200)continue;for(let ch=0;ch<3;ch++){let m=0;for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++){const kk=((y+dy)*W+q+dx)*4;m+=s[kk+3]<200?s[k+ch]:s[kk+ch]}m/=9;o[k+ch]=Math.max(0,Math.min(255,s[k+ch]+A*(s[k+ch]-m)))}}
  x.putImageData(d,0,0);const u=c.toDataURL('image/webp',.95);CR.set(key,u);done(u)}catch(e){done(url)}};im.src=url}
function crispEl(el,src){const isSvg=el.tagName.toLowerCase()==='image',set=u=>isSvg?el.setAttribute('href',u):(el.src=u);crisp(src,el.getBoundingClientRect().height||el.offsetHeight||80,set)}

// Read-only inventory of the checked-in game definitions. Never mounts a scene.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const dir=path.join(root,'src/simple-machines');
const files=['core.js','machines.js','st_force.js','st_fric.js','st_scale.js','st_lever.js','st_ramp.js','st_pulley.js','st_wheel.js','st_wedge.js','st_sort.js','content.js','quiz.js','harbor-content.js','app.js','harbor-routes.js','journey.js'];
const sources=Object.fromEntries(files.map(f=>[f,fs.readFileSync(path.join(dir,f),'utf8')]));
// The environment is deliberately inert: definitions/generators only, no storage/UI.
const context=vm.createContext({window:{__TEST:true},document:{querySelector:()=>null,addEventListener:()=>{}},localStorage:{getItem:()=>null},matchMedia:()=>({matches:true})});
for(const f of files){
 let source=sources[f];
 if(f==='app.js')source=source.slice(0,source.indexOf('function setC('));
 if(f==='journey.js')source=source.slice(0,source.indexOf('/* ---------- وضعیت بازیکن'));
 vm.runInContext(source,context,{filename:f,timeout:3000});
}
const data=vm.runInContext(`(()=>{
 const tracks=['a','b','c','d'], levels=[],stations=[];
 const types=(generate,tr,d)=>{S.track=tr;const seen=new Set();for(let seed=1;seed<=64;seed++){
  const specs=d==null?generate(rng(seed)): [generate(rng(seed),d)];
  for(const sp of specs)seen.add(sp.t||'unspecified');
 }return [...seen].sort();};
 for(const k of ORDER){const st=ST[k],byId=new Map();
  for(const tr of tracks){S.track=tr;for(const lv of levelsFor(k,tr)){
   if(!byId.has(lv.id))byId.set(lv.id,{id:lv.id,station:k,title:lv.title,description:lv.desc,tracks:[],challengeIds:lv.ch||[],typesByTrack:{}});
   const row=byId.get(lv.id);row.tracks.push(tr);row.typesByTrack[tr]=types(lv.gen,tr);
  }}levels.push(...byId.values());
  stations.push({id:k,name:st.name,labInstructions:KIDLAB[k],hasLab:typeof st.lab==='function',endless:{hasGenerator:typeof st.endless==='function',kidRuntimeCap:1.9,samples:['a','b','c'].map(tr=>({track:tr,bands:[0,1,1.9,2,2.6,3.5,5,6].map(d=>({difficulty:d,effectiveDifficulty:tr==='a'?Math.min(d,1.9):d,types:types(st.endless,tr,tr==='a'?Math.min(d,1.9):d)}))}))}});
 }
 const challenges=Object.values(CH).map(ch=>({id:ch.id,station:ch.st,legacyDifficulty:ch.d,phase:ch.phase||null,terms:ch.terms,teach:ch.teach||'',typesByTrack:Object.fromEntries(tracks.map(tr=>[tr,types(r=>[ch.mk(r)],tr)]))}));
 const questions=QBANK.map(q=>({id:q.id,term:q.term,tracks:[...q.lv],type:q.type,after:q.after??null,eligibleAt:tracks.flatMap(tr=>QUIZ_AT.filter(at=>q.lv.includes(tr)&&(q.after==null||q.after<=at.after)&&QTERMS[tr].slice(0,at.after+1).some(ts=>ts.includes(q.term))).map(at=>({track:tr,afterStop:at.after+1})))}));
 return {routeActivities:HARBOR_CONTENT.routes.flatMap(route=>route.activities.map(a=>({id:a.id,routeId:route.id,regionId:HARBOR_CONTENT.regionId,title:a.title,grades:HARBOR_CONTENT.grades.map(g=>g+2),goals:a.goals,prerequisiteGoals:a.prerequisiteGoals,type:a.make(rng(1)).t}))),tracks:{active:['a','b','c'],historicalOnly:['d']},stations,levels,challenges,questions,stops:STOPS.map((s,i)=>({id:'stop.'+(i+1),number:i+1,title:s.n,sideStation:s.side,missions:s.m,home:HOME[i],learn:LEARN[i]})),terms:QTERMS,definitionTerms:Object.keys(QDEF),quizSchedule:QUIZ_AT,sideGoals:SIDEG,definitionStations:Object.keys(DEFS),formulaCards:FORMULAS.map(x=>({station:x.k,title:x.t,trackGate:x.g,example:x.ex,rule:x.rule})),videoReferences:Object.entries(V).map(([id,x])=>({id,title:x[0],url:x[1]}))};
})()`,context,{timeout:10000});
const payload={schemaVersion:1,method:{kind:'definition-extraction-and-deterministic-generator-sampling',seedsPerBand:64,limits:'Spec type sampling is not exhaustive over random parameters. Does not mount UI, validate physics or infer textbook alignment. eligibleAt is eligibility, not a guaranteed quiz draw.'},sourceHashes:Object.fromEntries(files.map(f=>[f,crypto.createHash('sha256').update(sources[f]).digest('hex')])),...data};
const output=JSON.stringify(payload,null,2)+'\n';
if(process.argv[2])fs.writeFileSync(path.resolve(process.argv[2]),output);else process.stdout.write(output);

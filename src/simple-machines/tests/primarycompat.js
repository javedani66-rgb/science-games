'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'..','journey.js'),'utf8');
const ctx=vm.createContext({DB:{profiles:[]},migrateS:s=>{s.ls=s.ls||{};},useProfile:()=>{},save:()=>{},applyNums:()=>{}});
vm.runInContext(source.slice(0,source.indexOf('DB.profiles.forEach(fixProfile);'))+source.slice(source.indexOf('function switchLevel('),source.indexOf('function teacherMsg(')),ctx);
for(const name of ['canOfferLevel','trk','maxLevel'])ctx[name]=vm.runInContext(name,ctx);
assert.equal(vm.runInContext('GRADES.length',ctx),8); // Never shift serialized grade slots.
assert.equal(vm.runInContext('TRK',ctx),'abcd');
for(const t of ['a','b','c'])assert.equal(ctx.canOfferLevel(t),true);
for(const t of ['d','','x',null])assert.equal(ctx.canOfferLevel(t),false);
for(const g of [5,6,7]){
  const p=ctx.newProfile('historical',g,2);p.S.ls={'d:force.2':2};p.done='abcd';p.quiz=[1,0,0,0,0];p.quizEvidence={d:{kept:true}};
  ctx.fixProfile(p);assert.equal(p.g,g);assert.equal(ctx.trk(p),'d');
  const code=ctx.makeCode(p),r=ctx.readCode(code);assert.equal(r.g,g);assert.equal(r.lvl,'d');assert.equal(r.st[0][0],2);
  assert.equal(ctx.maxLevel(p),2);
  ctx.switchLevel(p,'c');assert.equal(ctx.trk(p),'c');assert.equal(p.S.ls['d:force.2'],2);assert.equal(p.stash.d.quiz[0],1);assert.equal(p.quizEvidence.d.kept,true);
  const before=JSON.stringify(p);assert.equal(ctx.switchLevel(p,'d'),false);assert.equal(JSON.stringify(p),before);
  // Direct historical-code import still restores the authentic old grade/track.
  ctx.applyCode(p,r);assert.equal(p.g,g);assert.equal(ctx.trk(p),'d');assert.equal(p.S.ls['d:force.2'],2);
}
const p=ctx.newProfile('primary',4,0);p.done='abc';assert.equal(ctx.maxLevel(p),2);assert.equal(ctx.switchLevel(p,'d'),false);assert.equal(ctx.trk(p),'c');
console.log('primarycompat: active choices, legacy grade indices/codes/save data and blocked d switching passed');

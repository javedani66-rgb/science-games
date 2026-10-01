/* Source-level persistence/report regression; no game build required. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync(path.join(__dirname,'..','journey.js'),'utf8');
const names=['quizEvidence','quizEvidenceStart','quizEvidenceAnswer','quizEvidenceFinish','quizEvidenceText'];
const helpers=source.split('\n').filter(line=>names.some(name=>line.startsWith('function '+name+'('))).join('\n');
const ctx=vm.createContext({fa:String});vm.runInContext(helpers,ctx);
const p={},q1={id:'mass',q:'Compare mass?',term:'جرم'},q2={id:'weight',q:'Compare weight?',term:'وزن'};
let run=ctx.quizEvidenceStart(p,'b',0,2);
ctx.quizEvidenceAnswer(run,q1,false);
assert.match(ctx.quizEvidenceText(p,'b'),/اجرای ناتمام/);
assert.equal(run.latest.complete,false);
ctx.quizEvidenceAnswer(run,q2,true);
ctx.quizEvidenceAnswer(run,{...q1,again:1,slot:0},true);
ctx.quizEvidenceFinish(run);
const restored=JSON.parse(JSON.stringify(p));
assert.equal(restored.quizEvidence.b[0].first.items[0].first,false);
assert.equal(restored.quizEvidence.b[0].first.items[0].corrected,true);
assert.match(ctx.quizEvidenceText(restored,'b'),/پاسخ اول 1 از 2 درست/);
assert.match(ctx.quizEvidenceText(restored,'b'),/پس از دیدن پاسخ 1 اصلاح شد/);
assert.match(ctx.quizEvidenceText(restored,'b'),/برای مرور: جرم/);
// Repetition cannot replace original evidence with previously disclosed answers.
run=ctx.quizEvidenceStart(restored,'b',0,2);
ctx.quizEvidenceAnswer(run,q1,true);ctx.quizEvidenceAnswer(run,q2,true);ctx.quizEvidenceFinish(run);
assert.equal(restored.quizEvidence.b[0].first.items[0].first,false);
assert.equal(restored.quizEvidence.b[0].latest.items[0].first,true);
// Track and profile isolation, including older profiles with only completion flags.
ctx.quizEvidenceStart(restored,'c',0,3);
assert.equal(restored.quizEvidence.b[0].first.total,2);
const old={quiz:[1,0,0,0,0]};assert.match(ctx.quizEvidenceText(old,'b'),/ثبت نشده/);
assert.equal(old.quiz[0],1);
assert.match(ctx.quizEvidenceText({},'b'),/ثبت نشده/);
// Wrong correction is not represented as a correct first response.
run=ctx.quizEvidenceStart({},'a',0,1);ctx.quizEvidenceAnswer(run,q1,false);
ctx.quizEvidenceAnswer(run,{...q1,again:1,slot:0},false);ctx.quizEvidenceFinish(run);
assert.equal(run.first.items[0].first,false);assert.equal(run.first.items[0].corrected,false);
// Live callback wiring saves answers and preserves existing completion/final gate.
assert.match(source,/quizEvidenceAnswer\(evidence,q,ok\);save\(\);/);
assert.match(source,/function finish\(\)\{quizEvidenceFinish\(evidence\);p.quiz\[qi\]=1;/);
assert.match(source,/کد پیشرفت، جزئیات پاسخ‌ها را منتقل نمی‌کند/);
console.log('quizevidence: first answers, corrections, restore, replay, old saves and isolation passed');

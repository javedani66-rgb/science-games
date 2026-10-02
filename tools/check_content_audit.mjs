// Checks coverage/provenance and source drift, not educational validity.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const inv=read('design/content/source-inventory.json'),audit=read('design/content/content-audit.json'),assets=read('design/routes/assets.json'),plan=read('design/routes/harbor-plan.json');
const sameIds=(a,b,label)=>{assert.equal(new Set(a).size,a.length,`${label}: duplicate IDs`);assert.deepEqual([...a].sort(),[...b].sort(),`${label}: coverage mismatch`);};
sameIds(audit.stations.flatMap(s=>s.levels.map(x=>x.id)),inv.levels.map(x=>x.id),'levels');
sameIds(audit.questions.map(x=>x.id),inv.questions.map(x=>x.id),'questions');
sameIds(audit.challengeReviews.map(x=>x.id),inv.challenges.map(x=>x.id),'catalog');
if(inv.routeActivities)sameIds((audit.routeActivityReviews||[]).map(x=>x.id),inv.routeActivities.map(x=>x.id),'route activities');
assert.deepEqual(audit.sourceHashes,inv.sourceHashes);
for(const [file,expected] of Object.entries(inv.sourceHashes))assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'src/simple-machines',file))).digest('hex'),expected,`source drift: ${file}; re-export and re-review`);
const placements=new Set(['core','challenge','extension','mixed']);
for(const row of [...audit.stations.flatMap(s=>s.levels),...audit.questions]){
 assert(placements.has(row.placement),`placement: ${row.id}`);
 assert(Array.isArray(row.grades)&&row.grades.every(g=>Number.isInteger(g)&&g>=1&&g<=12),`grades: ${row.id}`);
 for(const key of ['concept','calculation','reading','controls'])assert(Number.isInteger(row.difficulty[key])&&row.difficulty[key]>=0&&row.difficulty[key]<=3,`difficulty: ${row.id}/${key}`);
}
for(const ch of audit.challengeReviews){assert.equal(ch.unreviewedTypes.length,0,`missing family ${ch.id}`);const s=audit.stations.find(s=>s.station===ch.station);for(const n of ch.familyReviewIndices)assert(s.families[n]);}
const visit=x=>{if(Array.isArray(x))x.forEach(visit);else if(x&&typeof x==='object'){if(x.document)assert(fs.existsSync(path.join(root,x.document)),`missing source reference ${x.document}`);Object.values(x).forEach(visit);}};visit(audit);
assert.equal(audit.support.home.length,inv.stops.length);assert.equal(audit.support.learn.length,inv.stops.length);
const qmap=new Map(inv.questions.map(q=>[q.id,q]));for(const q of audit.questions)assert.deepEqual([...q.tracks].sort(),[...qmap.get(q.id).tracks].sort(),`question tracks: ${q.id}`);
assert.equal(new Set(assets.assets.map(a=>a.id)).size,assets.assets.length);
for(const a of assets.assets)assert(fs.existsSync(path.resolve(root,'design/routes',a.path)),`missing asset ${a.id}`);
for(const r of plan.routes)assert(assets.assets.some(a=>a.id===r.environmentAssetId),`unknown route asset ${r.id}`);
console.log(`content audit valid: ${inv.levels.length} levels, ${inv.challenges.length} catalog links, ${inv.questions.length} questions; ${assets.assets.length} asset paths exist; source hashes match`);

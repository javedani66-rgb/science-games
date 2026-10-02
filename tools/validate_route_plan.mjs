// Planning validator, not a shipped game engine. Any number of routes is allowed.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

export function validateRoutePlan(plan, inventory){
 const errors=[];
 if(plan.schemaVersion!==1)errors.push('unsupported schemaVersion');
 if(plan.status!=='draft')errors.push('only draft plans are supported; no runtime approval is implied');
 const arrays=['objectives','activities','regions','routes'];
 for(const key of arrays)if(!Array.isArray(plan[key]))errors.push(`${key} must be an array`);
 if(errors.length)return errors;
 const index=(items,label)=>{const out=new Map();for(const item of items){
  if(!item||typeof item.id!=='string'||!item.id)errors.push(`${label}: missing id`);
  else if(out.has(item.id))errors.push(`${label}: duplicate ${item.id}`);else out.set(item.id,item);
 }return out;};
 const objectives=index(plan.objectives,'objective'),activities=index(plan.activities,'activity'),regions=index(plan.regions,'region');
 index(plan.routes,'route');
 const content=new Set([...inventory.levels,...inventory.challenges,...inventory.questions].map(x=>x.id));
 const refs=(value,ids,label)=>{if(!Array.isArray(value))errors.push(`${label} must be an array`);else for(const id of value)if(!ids.has(id))errors.push(`${label}: unknown ${id}`);};
 for(const a of plan.activities){
  if(!a)continue;
  refs(a.sourceContentIds,content,`${a.id}.sourceContentIds`);
  refs(a.proposedGoals,objectives,`${a.id}.proposedGoals`);
  refs(a.prerequisiteGoals,objectives,`${a.id}.prerequisiteGoals`);
  if(a.reviewStatus!=='pending')errors.push(`${a.id}: this draft cannot claim approved activity coverage`);
 }
 for(const region of plan.regions){
  if(!region)continue;
  refs(region.requiredGoals,objectives,`${region.id}.requiredGoals`);
  if(region.nextRegionId!==null&&!regions.has(region.nextRegionId))errors.push(`${region.id}: unknown next region`);
  if(!plan.routes.some(r=>r?.regionId===region.id&&r.role==='alternative'))errors.push(`${region.id}: no alternative route`);
 }
 for(const route of plan.routes){
  if(!route)continue;
  const region=regions.get(route.regionId);
  if(!region)errors.push(`${route.id}: unknown region`);
  if(!['alternative','side'].includes(route.role))errors.push(`${route.id}: invalid role`);
  refs(route.activityIds,activities,`${route.id}.activityIds`);
  if(!route.activityIds?.length)errors.push(`${route.id}: empty activity list`);
  if(route.returnAllowed!==true)errors.push(`${route.id}: return must be allowed`);
  if(!route.difficulty||!['concept','calculation','reading','controls'].every(k=>Number.isInteger(route.difficulty[k])&&route.difficulty[k]>=0&&route.difficulty[k]<=3))errors.push(`${route.id}: invalid difficulty axes`);
  if(typeof route.environmentAssetId!=='string'||!route.environmentAssetId)errors.push(`${route.id}: missing environment asset`);
  const covered=new Set((route.activityIds||[]).flatMap(id=>activities.get(id)?.proposedGoals||[]));
  if(route.role==='alternative'&&region)for(const g of region.requiredGoals||[])if(!covered.has(g))errors.push(`${route.id}: missing required goal ${g}`);
  // Side rewards never grant main-region completion merely by being harder.
  if(route.role==='side'&&route.grantsRegionCompletion!==false)errors.push(`${route.id}: side route cannot grant region completion`);
  if(route.role==='alternative'&&route.grantsRegionCompletion!==true)errors.push(`${route.id}: alternative must declare proposed completion coverage`);
 }
 // Session progression stays acyclic. Returning inside a region is separate.
 const visiting=new Set(),visited=new Set();
 const visit=id=>{if(visiting.has(id)){errors.push('region progression cycle');return;}if(visited.has(id))return;
  visiting.add(id);const next=regions.get(id)?.nextRegionId;if(next&&regions.has(next))visit(next);visiting.delete(id);visited.add(id);};
 for(const id of regions.keys())visit(id);
 return errors;
}

if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
 const plan=JSON.parse(fs.readFileSync(process.argv[2]||path.join(root,'design/routes/harbor-plan.json'),'utf8'));
 const inventory=JSON.parse(fs.readFileSync(path.join(root,'design/content/source-inventory.json'),'utf8'));
 const errors=validateRoutePlan(plan,inventory);if(errors.length){console.error(errors.join('\n'));process.exitCode=1;}else console.log(`draft route plan valid: ${plan.routes.length} routes; educational approval and runtime integration pending`);
}

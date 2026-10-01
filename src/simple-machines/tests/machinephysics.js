/* Independent ideal-machine work/units regression. Run: node machinephysics.js */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const context = vm.createContext({});
vm.runInContext(fs.readFileSync(path.join(__dirname, '..', 'machines.js'), 'utf8') + '\nthis.model = MACHINE;', context);
const M = context.model;
let seed = 0x51a7e, checks = 0;
function random(min, max) {
  seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
  return min + (max - min) * seed / 4294967296;
}
function equal(actual, expected, name) {
  checks++;
  assert.ok(Number.isFinite(actual), `${name}: non-finite output`);
  assert.ok(Math.abs(actual - expected) <= 1e-10 * Math.max(1, Math.abs(expected)),
    `${name}: ${actual} differs from ${expected}`);
}
for (let i = 0; i < 1000; i++) {
  const weight = random(1, 500), height = random(.1, 3);
  const length = random(height, 10), ratio = random(1, 8);
  const supports = [1, 2, 4, 6][i % 4], turns = random(.1, 12);
  // Work is compared in joules; force and path are independently specified.
  equal(M.ramp(weight, height, length) * length, weight * height, 'ramp work');
  equal(M.pulley(weight, supports) * M.rope(supports, height), weight * height, 'pulley work');
  const axleCircumference = random(.1, 1);
  equal(M.wheel(weight, ratio) * M.hand(ratio, turns, axleCircumference),
    weight * turns * axleCircumference, 'wheel work');
  // Wedge dimensions are cm; screw dimensions are mm. Convert both sides.
  const resistance = random(1, 1000), widthCm = random(.5, 3);
  const travelCm = random(widthCm, 12), pitchMm = random(.5, 8);
  const handMm = random(50, 250), depthMm = random(1, 30);
  equal(M.wedge(resistance, travelCm, widthCm) * travelCm / 100,
    resistance * widthCm / 100, 'wedge work / cm');
  equal(M.screw(resistance, pitchMm, handMm) * handMm / 1000,
    resistance * pitchMm / 1000, 'screw work / mm');
  equal(M.turns(depthMm, pitchMm) * pitchMm, depthMm, 'screw advance');
  // Scaling both geometrical distances must leave mechanical advantage unchanged.
  equal(M.ramp(weight, height * 100, length * 100), M.ramp(weight, height, length), 'ramp units');
  equal(M.screw(resistance, pitchMm / 1000, handMm / 1000),
    M.screw(resistance, pitchMm, handMm), 'screw units');
  equal(M.wedge(resistance, travelCm / 100, widthCm / 100),
    M.wedge(resistance, travelCm, widthCm), 'wedge units');
}
// Exact equilibrium can hold a load but cannot start its rise in this model.
assert.equal(M.minimum([1, 2, 4, 6], n => M.pulley(120, n), 30), 6);
assert.equal(M.minimum([1, 2, 3, 4], r => M.wheel(60, r), 20), 4);
assert.equal(M.minimum([2, 4, 6, 8], l => M.wedge(60, l), 30), 6);
assert.equal(M.minimum([6, 4, 3, 2], p => M.screw(600, p), 20), 3);
assert.equal(M.minimum([1, 2], n => M.pulley(60, n), 30), undefined);
assert.equal(M.minimum([1, 2], n => M.pulley(60, n), 30.01), 2);
assert.equal(M.minimum([1, 2], n => M.pulley(60, n), 29.99), undefined);
// Current scene defaults: 2 cm wedge back, 120 mm screw hand path, .5 m axle circumference.
equal(M.wedge(90, 6), 30, 'default wedge width');
equal(M.screw(600, 3), 15, 'default screw circumference');
equal(M.hand(4, 2), 4, 'default axle circumference');
console.log(`machinephysics: ${checks + 7} deterministic checks passed`);

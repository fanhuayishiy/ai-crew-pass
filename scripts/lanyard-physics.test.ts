import test from 'node:test';
import assert from 'node:assert/strict';
import { createSim } from '../src/scripts/lanyard-physics.ts';

const create = () => createSim({
  segments: 16, ropeLength: 320, cordLength: 120, pinX: 0, pinY: 0,
  gravity: 4000, chainInvMass: 20, bendStiffness: 0.025,
  frictionPerFrame: 0.985, iterations: 40, fixedDt: 1/120, maxSubSteps: 8,
  maxAngle: 88*Math.PI/180, returnStrength: 0,
});
const advance = (sim: ReturnType<typeof create>, seconds: number, rate=120) => {
  for (let i=0;i<Math.round(seconds*rate);i++) sim.step(1/rate);
};

test('the strap is substantially lighter than the badge by default', () => {
  const points=createSim({}).state().points;
  assert.ok(points[1].w >= points.at(-1)!.w*10, 'rope nodes must have higher inverse mass than the card');
});

test('the grabbed badge stays at its pointer target while the rope solves', () => {
  const sim=create();
  sim.grab(0,440);
  sim.dragTo(140,280,1/60);
  sim.step(1/60);
  const {com}=sim.state();
  assert.ok(Math.hypot(com.x-140,com.y-280)<0.1, `drag drift: ${JSON.stringify(com)}`);
});

test('a lifted badge leaves slack in the original-length strap', () => {
  const sim=create();
  sim.grab(0,440);
  sim.dragTo(90,240,1/60);
  advance(sim,2);
  const {points,clip,com}=sim.state();
  const rope=points.slice(0,-1);
  const arc=rope.slice(1).reduce((s,p,i)=>s+Math.hypot(p.x-rope[i].x,p.y-rope[i].y),0);
  assert.ok(Math.hypot(com.x-90,com.y-240)<0.1, 'held badge drifted away');
  assert.ok(arc>Math.hypot(clip.x,clip.y)+35,'lifted strap stayed a taut shrinking line');
  assert.ok(arc<340,`rope stretched excessively: ${arc}`);
});

test('release accelerates downward, crosses the centre and loses energy naturally', () => {
  const sim=create();
  sim.grab(0,440);
  sim.dragTo(120,250,1/60);
  advance(sim,1.5);
  const start=sim.state().com;
  sim.release();
  advance(sim,.2);
  assert.ok(sim.state().com.y>start.y+20,'badge did not fall under gravity');
  let crossed=false;
  for(let i=0;i<480;i++) { sim.step(1/120); if(sim.state().com.x< -5) crossed=true; }
  assert.ok(crossed,'badge never swung past the anchor');
  advance(sim,12);
  const end=sim.state();
  assert.ok(Math.abs(end.com.x)<8,`did not settle near anchor: ${end.com.x}`);
  assert.ok(Math.hypot(end.velocity.x,end.velocity.y)<8,'residual energy did not decay');
  assert.ok(Math.abs(Math.hypot(end.com.x-end.clip.x,end.com.y-end.clip.y)-120)<0.2,'card detached from clip');
});

test('fixed time steps produce the same trajectory at 30 and 120 fps', () => {
  const a=create(), b=create();
  a.swing(.25,.4); b.swing(.25,.4);
  advance(a,3,30); advance(b,3,120);
  assert.ok(Math.hypot(a.state().com.x-b.state().com.x,a.state().com.y-b.state().com.y)<1);
});

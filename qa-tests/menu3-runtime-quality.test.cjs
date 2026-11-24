'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const test=require('node:test');

const runtime=fs.readFileSync(path.join(__dirname,'..','menu3-pinyin-fix-v42.10.23.js'),'utf8');

function loadRuntime(){
  const syllables=new Set(['zuo','tian','zou','ti','an','ni','qing','wo','he','cha','le','nv','nu','nve','lve','lu']);
  const listeners={};
  const host={hidden:false,replaceChildren(){},appendChild(){}};
  const status={textContent:''};
  const query={value:''};
  const originalSelector=(items)=>items;
  const windowObject={
    pinyin18Key(value){
      return String(value||'').normalize('NFD').toLowerCase()
        .replace(/u\u0308/g,'v').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z]/g,'');
    },
    getPinyin18SourceIndex(){return {syllables};},
    pinyin18SelectToneDiverse:originalSelector,
    setTimeout(callback){callback();}
  };
  const documentObject={
    documentElement:{dataset:{}},
    head:{appendChild(){}},
    createElement(){return {style:{},classList:{add(){},remove(){}},setAttribute(){}};},
    addEventListener(type,callback){(listeners[type]||=[]).push(callback);},
    getElementById(id){
      if(id==='homework3x-candidates')return host;
      if(id==='homework3x-status')return status;
      if(id==='homework3x-query')return query;
      return null;
    },
    querySelector(){return null;}
  };
  const context=vm.createContext({window:windowObject,document:documentObject,navigator:{},console,Map,Set});
  vm.runInContext(runtime,context,{timeout:10000});
  return {window:windowObject,context,listeners,query,status,host};
}

test('compact zuotian is resolved as zuo+tian, not zou+ti+an; original spacing is preserved',()=>{
  const {window}=loadRuntime();
  const actual=window.formatByInputSpacing(
    'zuotian ni qing wo he cha le',
    'zuó tiān nǐ qǐng wǒ hē chá le'
  );
  assert.equal(actual,'zuótiān ni qǐng wo he cha le'.replace('ni','nǐ').replace('qing','qǐng').replace('wo','wǒ').replace('he','hē').replace('cha','chá'));
  assert.equal(actual,'zuótiān nǐ qǐng wǒ hē chá le'.replace('qing','qǐng'));
});

test('source syllables, not an ambiguous raw alias, determine whether ü is displayed',()=>{
  const {window}=loadRuntime();
  assert.equal(window.formatByInputSpacing('nü','nǚ'),'nǚ');
  assert.equal(window.formatByInputSpacing('nv3','nǚ'),'nǚ');
  assert.equal(window.formatByInputSpacing('nu','nǔ'),'nǔ');
  assert.equal(window.formatByInputSpacing('lu','lù'),'lù');
});

test('strict umlaut matching splits multi-syllable input and candidate readings on whitespace',async()=>{
  const {window}=loadRuntime('nv3 lv4');
  // The runtime installs its strict selector when the result renderer is first invoked.
  await window.renderHomework3xCandidatesV421023([]);
  const candidates=[{zh:'A',py:'nü lǚ'},{zh:'B',py:'nü lu'}];
  const result=window.pinyin18SelectToneDiverse(candidates,'nv3 lv4',30);
  assert.deepEqual(Array.from(result,x=>x.zh),['A']);
});

test('multi-row composed glosses are never trusted; whole Hanzi sentence translation is used',()=>{
  assert.match(runtime,/const composed=Array\.isArray\(item\.sourceRows\)&&item\.sourceRows\.length>1/);
  assert.match(runtime,/let vi=composed\?'':cleanMeaning\(item\.preferredMeaning\|\|item\.vi\|\|''\)/);
  assert.match(runtime,/window\.machineTranslate3x\(String\(item\.zh\),'zh-CN','vi'\)/);
});

test('cards are inserted before asynchronous Vietnamese meaning lookup completes',()=>{
  const start=runtime.indexOf('const renderPage=async()=>{');
  const end=runtime.indexOf('await renderPage();return source[0]||null;',start);
  const block=runtime.slice(start,end);
  assert.ok(start>=0&&end>start);
  assert.ok(block.indexOf('host.appendChild(grid)')<block.indexOf('await mapLimit(rawItems,3,translateFullSentence)'));
  assert.match(block,/Đang xác minh nghĩa tiếng Việt/);
});

test('runtime has real whitespace regexes, not literal backslash-s matching',()=>{
  assert.ok(runtime.includes("split(/[\\s,，、;；]+/)"));
  assert.ok(runtime.includes("split(/\\s+/)"));
  assert.ok(!runtime.includes("split(/[\\\\s,"));
  assert.ok(!runtime.includes("split(/\\\\s+/"));
});

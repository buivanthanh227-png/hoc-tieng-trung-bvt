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
  const query={value:'',addEventListener(){}};
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

test('multi-row composed glosses are translated from complete Hanzi with a secondary translator',()=>{
  assert.match(runtime,/const composed=Array\.isArray\(item\.sourceRows\)&&item\.sourceRows\.length>1/);
  assert.match(runtime,/const direct=\[item\.preferredMeaning,item\.vi\]\.map\(cleanMeaning\)/);
  assert.match(runtime,/if\(!composed&&direct\)return \{\.\.\.item,vi:direct\}/);
  assert.match(runtime,/translators\.push\(\(\)=>window\.machineTranslate3x\(hanzi,'zh-CN','vi'\)\)/);
  assert.match(runtime,/translators\.push\(\(\)=>window\.machineTranslate\(hanzi,'zh-CN','vi'\)\)/);
});

test('resolved Vietnamese meanings survive invalid preferred glosses and translator fallback',()=>{
  assert.match(runtime,/const direct=\[item\.preferredMeaning,item\.vi\]\.map\(cleanMeaning\)/);
  assert.match(runtime,/!isPinyinEchoMeaning\(value,item\.py\)/);
  assert.match(runtime,/translators\.push\(\(\)=>window\.machineTranslate3x\(hanzi,'zh-CN','vi'\)\)/);
  assert.match(runtime,/translators\.push\(\(\)=>window\.machineTranslate\(hanzi,'zh-CN','vi'\)\)/);
  assert.match(runtime,/result\.translation\?\?result\.translatedText/);
  assert.match(runtime,/meaning:validMeaning\(modalVi\)&&!isPinyinEchoMeaning\(modalVi,item\?\.py\)/);
  assert.match(runtime,/if\(!values\.hanzi\|\|!values\.pinyin\|\|!values\.meaning\)return/);
});

test('Vietnamese meanings are resolved before any result card is rendered',()=>{
  assert.match(runtime,/Đang hoàn thiện nghĩa tiếng Việt cho các kết quả/);
  assert.match(runtime,/const resolved=await mapLimit\(source,3,translateFullSentence\)/);
  assert.match(runtime,/const complete=resolved.filter\(item=>item&&item\.zh&&item\.py&&validMeaning\(item\.vi\)\)/);
  assert.ok(!runtime.includes("Đang xác minh nghĩa tiếng Việt…"));
});

test('runtime has real whitespace regexes, not literal backslash-s matching',()=>{
  assert.ok(runtime.includes("split(/[\\s,，、;；]+/)"));
  assert.ok(runtime.includes("split(/\\s+/)"));
  assert.ok(!runtime.includes("split(/[\\\\s,"));
  assert.ok(!runtime.includes("split(/\\\\s+/"));
});


test('unknown but clause-like dictionary compositions are retained for full-sentence Vietnamese translation',()=>{
  assert.match(runtime,/function menu3CanTranslateWholeSentence\(entries\)/);
  assert.match(runtime,/if\(!vi&&!menu3CanTranslateWholeSentence\(path\.entries\)\)continue/);
  assert.match(runtime,/results\.push\(\{zh:path\.zh,py:path\.entries\.map\(entry=>String\(entry\.py\|\|''\)\.trim\(\)\)\.filter\(Boolean\)\.join\(' '\),vi:vi\|\|'',score:path\.score\}\)/);
  assert.match(runtime,/const resolved=await mapLimit\(source,3,translateFullSentence\)/);
});

test('modal applies three isolated colors to the actual Hanzi, Pinyin and Vietnamese values',()=>{
  assert.match(runtime,/homework3x-modal-value-hanzi/);
  assert.match(runtime,/homework3x-modal-value-pinyin/);
  assert.match(runtime,/homework3x-modal-value-meaning/);
  assert.match(runtime,/color:#7b3fa1!important;-webkit-text-fill-color:#7b3fa1!important/);
  assert.match(runtime,/color:#2563a6!important;-webkit-text-fill-color:#2563a6!important/);
  assert.match(runtime,/color:#21805b!important;-webkit-text-fill-color:#21805b!important/);
});

test('modal speech bypasses shared auto speech and reads only the selected field',()=>{
  assert.match(runtime,/Bypass shared auto-speech helpers/);
  assert.match(runtime,/utterance\.text=text/);
  assert.match(runtime,/synth\.cancel\(\)/);
  assert.match(runtime,/language==='zh'\?'zh-CN':'vi-VN'/);
  assert.doesNotMatch(runtime,/window\.bvtSpeakLocale\(text,locale\)/);
  assert.doesNotMatch(runtime,/window\.speakMandarinSentence\(text\)/);
});

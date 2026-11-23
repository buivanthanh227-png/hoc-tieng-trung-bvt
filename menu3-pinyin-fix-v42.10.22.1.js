/* Menu 3 Pinyin composer fix · V42.10.22.1 */
(function(){
 'use strict';
 if(!document.getElementById('homework3x-query'))return;
 if(typeof getPinyin18SourceIndex!=='function'||typeof pinyin18InputToken!=='function'||
    typeof pinyin18InputInfosMatchSource!=='function'||typeof pinyin18ToneFromInput!=='function')return;
 try{pinyin3xComposerSourceIndex=null;pinyin3xComposerIndex=null;}catch(_){}

 function segmentToken(rawToken,syllables,maxResults,groupIndex){
  const parsed=pinyin18InputToken(rawToken),base=parsed.base;
  if(!base||base.length>24)return [];
  const results=[];
  const walk=(offset,path)=>{
   if(results.length>=maxResults)return;
   if(offset===base.length){results.push(path.slice());return;}
   for(let next=Math.min(base.length,offset+6);next>offset;next--){
    const part=base.slice(offset,next);if(!syllables.has(part))continue;
    const tones=parsed.tones.filter(mark=>mark.numeric?mark.offset===next:mark.offset>=offset&&mark.offset<next).map(mark=>({...mark,offset:mark.offset-offset}));
    path.push({base:part,tones,group:groupIndex});walk(next,path);path.pop();
    if(results.length>=maxResults)return;
   }
  };
  walk(0,[]);return results;
 }

 function buildInputOptions(raw,syllables,maxOptions){
  const source=String(raw||''),matches=[...source.matchAll(/[^\s,，、;；.!?！？]+/g)];
  if(!matches.length)return [];
  let combined=[[]];
  for(let index=0;index<matches.length;index++){
   const choices=segmentToken(matches[index][0],syllables,64,index);
   if(!choices.length)return [];
   const next=[];
   for(const prefix of combined){
    for(const choice of choices){next.push(prefix.concat(choice));if(next.length>=maxOptions)break;}
    if(next.length>=maxOptions)break;
   }
   combined=next;
  }
  const seen=new Set();
  return combined.filter(option=>{
   const key=option.map(item=>item.base+':'+item.tones.map(t=>t.offset+'-'+t.tone).join(',')+'@'+item.group).join('|');
   if(seen.has(key))return false;seen.add(key);return true;
  });
 }

 function getComposerIndex(){
  const sourceIndex=getPinyin18SourceIndex();
  if(pinyin3xComposerSourceIndex===sourceIndex&&pinyin3xComposerIndex)return pinyin3xComposerIndex;
  const seedRows=[...(typeof seed!=='undefined'&&Array.isArray(seed)?seed:[]),...(typeof extraSeed!=='undefined'&&Array.isArray(extraSeed)?extraSeed:[])];
  const seedByKey=new Map();
  for(const row of seedRows){
   const zh=String(row?.[0]||'').trim(),py=String(row?.[2]||'').trim();if(!zh||!py)continue;
   const compact=py.split(/\s+/).map(pinyin18Key).join('');if(compact)seedByKey.set(zh+'|'+compact,{level:String(row?.[4]||''),py});
  }
  const byCompact=new Map(),dedupe=new Map();
  for(const item of sourceIndex.entries){
   const zh=String(item.zh||'').trim(),py=String(item.py||'').trim();
   if(!/^[\u3400-\u9fff\uf900-\ufaff]{1,6}$/.test(zh)||!py)continue;
   if(typeof homework3xValidVietnameseMeaning==='function'&&!homework3xValidVietnameseMeaning(item))continue;
   const tokens=py.split(/\s+/).filter(Boolean),compact=tokens.map(pinyin18Key).join('');
   if(!compact||compact.length>30||tokens.some(token=>!pinyin18Key(token)))continue;
   const chars=[...zh],seedData=seedByKey.get(zh+'|'+compact),seedExact=!!seedData,level=seedData?.level||'';
   const levelBonus=/HSK\s*1|HSK1/i.test(level)?100:/HSK\s*2|HSK2/i.test(level)?75:/HSK\s*3|HSK3/i.test(level)?50:/HSK\s*4|HSK4/i.test(level)?25:0;
   const score=(chars.length>1?180+Math.min(chars.length,6)*28:24)+(seedExact?160+levelBonus:0)+(item.priority===100?12:0);
   const identity=zh+'|'+compact,previous=dedupe.get(identity);
   const entry={...item,zh,py:seedData?.py||py,compact,score,seedExact,chars:chars.length};
   if(!previous||entry.score>previous.score)dedupe.set(identity,entry);
  }
  for(const entry of dedupe.values()){if(!byCompact.has(entry.compact))byCompact.set(entry.compact,[]);byCompact.get(entry.compact).push(entry);}
  for(const entries of byCompact.values()){entries.sort((a,b)=>b.score-a.score||a.zh.localeCompare(b.zh));if(entries.length>96)entries.length=96;}
  pinyin3xComposerSourceIndex=sourceIndex;pinyin3xComposerIndex={byCompact,entryCount:dedupe.size};return pinyin3xComposerIndex;
 }

 function applyTone(rawSyllable,tone){
  const original=String(rawSyllable||'').trim();if(!original)return original;
  const normalized=original.replace(/u:/gi,'ü').replace(/v/gi,'ü').normalize('NFD'),hasUmlaut=normalized.includes('\u0308');
  let base=normalized.replace(/[\u0300-\u036f]/g,'');if(hasUmlaut)base=base.replace(/u/g,'ü');
  if(!tone||tone===5||tone<1||tone>4)return base;
  let at=base.indexOf('a');if(at<0)at=base.indexOf('e');if(at<0&&base.includes('ou'))at=base.indexOf('o');
  if(at<0)for(let i=base.length-1;i>=0;i--)if('aeiouü'.includes(base[i])){at=i;break;}
  if(at<0)return base;
  const map={a:['ā','á','ǎ','à'],e:['ē','é','ě','è'],i:['ī','í','ǐ','ì'],o:['ō','ó','ǒ','ò'],u:['ū','ú','ǔ','ù'],ü:['ǖ','ǘ','ǚ','ǜ']};
  const marked=map[base[at]]?.[tone-1];if(!marked)return base;
  const output=base.slice(0,at)+marked+base.slice(at+1);
  return /^[A-Z]/.test(original)?output.charAt(0).toUpperCase()+output.slice(1):output;
 }

 function renderPinyinPreservingInput(raw,input,entries){
  const source=String(raw||''),matches=[...source.matchAll(/[^\s,，、;；.!?！？]+/g)];
  if(!matches.length||!input.length)return '';
  const units=[];for(const entry of entries)units.push(...String(entry.py||'').trim().split(/\s+/).filter(Boolean));
  if(units.length!==input.length)return '';
  for(let i=0;i<input.length;i++)if(pinyin18Key(units[i])!==input[i].base)return '';
  const groups=Array.from({length:matches.length},()=>[]);
  for(let i=0;i<input.length;i++){
   const entered=input[i].tones?.[0]?.tone,canonical=pinyin18ToneFromInput(units[i]),tone=entered===undefined?canonical:entered,group=input[i].group;
   if(!Number.isInteger(group)||group<0||group>=groups.length)return '';
   groups[group].push(applyTone(units[i],tone));
  }
  const leading=source.slice(0,matches[0].index),last=matches[matches.length-1];
  const trailing=source.slice(last.index+last[0].length);
  let output=leading+groups[0].join('');
  for(let i=1;i<groups.length;i++)output+=source.slice(matches[i-1].index+matches[i-1][0].length,matches[i].index)+groups[i].join('');
  output+=trailing;
  return output.replace(/^(\s*)([a-zü])/i,(whole,prefix,first)=>prefix+first.toUpperCase());
 }

 function composeSentence(raw){
  const sourceIndex=getPinyin18SourceIndex(),composer=getComposerIndex(),options=buildInputOptions(raw,sourceIndex.syllables,128);
  if(!options.length)return {status:'none'};
  const resultsByHanzi=new Map();
  for(const input of options){
   const states=Array.from({length:input.length+1},()=>[]);states[0]=[{score:0,zh:'',entries:[]}];
   const add=(pos,candidate)=>{
    const bucket=states[pos],prior=bucket.find(item=>item.zh===candidate.zh);
    if(prior){if(candidate.score>prior.score)Object.assign(prior,candidate);}else bucket.push(candidate);
    bucket.sort((a,b)=>b.score-a.score||a.zh.localeCompare(b.zh));if(bucket.length>32)bucket.length=32;
   };
   for(let start=0;start<input.length;start++){
    if(!states[start].length)continue;
    for(let end=start+1;end<=Math.min(input.length,start+6);end++){
     const span=input.slice(start,end),compact=span.map(item=>item.base).join('');
     for(const entry of composer.byCompact.get(compact)||[]){
      if(!pinyin18InputInfosMatchSource(entry,span))continue;
      for(const path of states[start])add(end,{score:path.score+entry.score-4,zh:path.zh+entry.zh,entries:path.entries.concat(entry)});
     }
    }
   }
   for(const path of states[input.length]){
    const py=renderPinyinPreservingInput(raw,input,path.entries);if(!py)continue;
    const prior=resultsByHanzi.get(path.zh);if(!prior||path.score>prior.score)resultsByHanzi.set(path.zh,{...path,py});
   }
  }
  const results=[...resultsByHanzi.values()].sort((a,b)=>b.score-a.score||a.zh.localeCompare(b.zh));
  if(!results.length)return {status:'none'};
  const best=results[0].score,top=results.filter(item=>best-item.score<=12).slice(0,6);
  const final=top.map(item=>{
   let zh=item.zh;if(/[?？]$/.test(String(raw||'').trim())||/[吗呢]$/.test(zh))zh=zh.replace(/[。.!?！？]*$/,'')+'？';
   return {zh,py:item.py,score:item.score};
  });
  return final.length===1?{status:'ok',...final[0]}:{status:'ambiguous',options:final};
 }

 window.pinyin3xSegmentInputToken=segmentToken;
 window.pinyin3xBuildInputOptions=(raw,syllables,maxOptions=128)=>buildInputOptions(raw,syllables,maxOptions);
 window.getPinyin3xComposerIndex=getComposerIndex;
 window.composePinyinSentence3x=composeSentence;
 window.formatHomework3xPinyinByWord=function(zh,py){return String(py||'');};
 const intro=document.querySelector('#panel-translate3 .quick-translate-intro');
 if(intro)intro.textContent='Nhập tiếng Việt, chữ Hán hoặc Pinyin. Pinyin được tra cứu nguyên cụm trước; nếu không có mục từ/câu hoàn chỉnh, hệ thống sẽ phân tích âm tiết và ghép câu từ các mục từ có trong từ điển.';
 document.documentElement.dataset.menu3PinyinFix='42.10.22.1';
})();
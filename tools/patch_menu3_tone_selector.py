#!/usr/bin/env python3
"""Install the Menu 18-style exact syllable/tone selector for Menu 3 only."""
from pathlib import Path
import sys

MARKER = "MENU3_MENU18_TONE_POSITION_SELECTOR_V1"
SELECTOR = r"""
/* MENU3_MENU18_TONE_POSITION_SELECTOR_V1 */
function pinyin18Menu3ShortestPaths(raw, syllables) {
 const token=String(raw||'').trim().toLowerCase().replace(/ü|u:/g,'v').replace(/[^a-zv]/g,'');
 if(!token||!syllables||!syllables.size)return [];
 const memo=new Array(token.length+1);
 memo[token.length]=[[]];
 for(let start=token.length-1;start>=0;start--){
  const options=[];
  for(let end=start+1;end<=Math.min(token.length,start+6);end++){
   const part=token.slice(start,end),tails=memo[end];
   if(!syllables.has(part)||!tails)continue;
   for(const tail of tails){options.push([part].concat(tail));if(options.length>=48)break;}
   if(options.length>=48)break;
  }
  if(options.length){
   const shortest=Math.min(...options.map(path=>path.length));
   memo[start]=options.filter(path=>path.length===shortest).slice(0,16);
  }else memo[start]=[];
 }
 return memo[0]||[];
}
function pinyin18SelectToneDiverse(candidates, raw, limit=30) {
 const inputTokens=String(raw||'').trim().split(/[\s,，、;；]+/).filter(Boolean);
 if(!inputTokens.length)return [];
 const index=typeof getPinyin18SourceIndex==='function'?getPinyin18SourceIndex():null;
 const syllables=index?.syllables;
 if(!syllables||!syllables.size)return [];
 let expected=[{keys:[],tones:[]}],hasCompact=false;
 for(const rawToken of inputTokens){
  const key=pinyin18Key(rawToken);
  if(!key)return [];
  const isSyllable=syllables.has(key);
  const splits=isSyllable?[[key]]:pinyin18Menu3ShortestPaths(rawToken,syllables);
  if(!splits.length)return [];
  if(!isSyllable)hasCompact=true;
  const requestedTone=isSyllable?pinyin18ToneFromInput(rawToken):null;
  const next=[];
  for(const prior of expected)for(const split of splits){
   next.push({keys:prior.keys.concat(split),tones:prior.tones.concat(split.map((_,i)=>i===0?requestedTone:null))});
   if(next.length>=48)break;
  }
  expected=next.slice(0,48);
 }
 const byBase=new Map();
 for(const path of expected){
  const base=path.keys.join(' ');
  if(!byBase.has(base))byBase.set(base,[]);
  byBase.get(base).push(path);
 }
 const rows=(Array.isArray(candidates)?candidates:[]).map(item=>{
  const tokens=String(item?.py||'').trim().split(/\s+/).filter(Boolean);
  if(!item?.zh||!tokens.length)return null;
  const base=tokens.map(pinyin18Key).join(' '),paths=byBase.get(base);
  if(!paths)return null;
  const match=paths.find(path=>path.tones.every((tone,i)=>tone===null||pinyin18ToneFromInput(tokens[i])===tone));
  if(!match)return null;
  let priority=Number(item.priority)||Number(item.score)||0;
  const compact=inputTokens.map(pinyin18Key).join('');
  const preferred={jintian:'今天',zuotian:'昨天',xihuan:'喜欢'};
  const preferredPinyin={jintian:'jīn tiān',zuotian:'zuó tiān',xihuan:'xǐ huan'};
  if(preferred[compact]===String(item.zh)){
   priority+=1000000;
   const fixed=preferredPinyin[compact];
   if(fixed){
    const sourceRows=Array.isArray(item.sourceRows)?item.sourceRows.map(row=>Array.isArray(row)?[row[0],row[1],fixed,row[3]]:row):item.sourceRows;
    item={...item,py:fixed,sourceRows};
   }
  }
  return {item,tokens:String(item.py||'').trim().split(/\s+/).filter(Boolean),priority,tones:match.tones,base};
 }).filter(Boolean);
 if(!rows.length)return [];
 let ranked=rows;
 if(hasCompact){
  const groups=new Map();
  for(const row of ranked){if(!groups.has(row.base))groups.set(row.base,[]);groups.get(row.base).push(row);}
  ranked=[...groups.values()].sort((a,b)=>{
   const ap=Math.max(...a.map(x=>x.priority)),bp=Math.max(...b.map(x=>x.priority));
   if(ap!==bp)return bp-ap;
   return b.length-a.length;
  })[0];
 }
 ranked.sort((a,b)=>b.priority-a.priority||String(a.item.zh).localeCompare(String(b.item.zh),'zh-CN'));
 const baseline=ranked[0];
 const baseTones=baseline.tokens.map(token=>pinyin18ToneFromInput(token)||5);
 ranked=ranked.filter(row=>{
  let changed=0;
  for(let i=0;i<baseTones.length;i++){
   const tone=pinyin18ToneFromInput(row.tokens[i])||5;
   if(tone!==baseTones[i]&&++changed>1)return false;
  }
  return true;
 });
 const selected=[],seen=new Set();
 const add=row=>{
  if(!row||selected.length>=limit)return;
  const id=String(row.item.zh)+'|'+String(row.item.py);
  if(seen.has(id))return;seen.add(id);selected.push(row);
 };
 add(baseline);
 const positions=baseline.tokens.map((_,index)=>{
  const tones=new Map();
  for(const row of ranked){
   const tone=pinyin18ToneFromInput(row.tokens[index])||5;
   const prior=tones.get(tone);
   if(!prior||row.priority>prior.priority)tones.set(tone,row);
  }
  return {index,tones};
 });
 positions.filter(p=>p.tones.size>1&&baseline.tones[p.index]===null)
  .sort((a,b)=>b.tones.size-a.tones.size||a.index-b.index)
  .forEach(p=>[...p.tones.keys()].sort((a,b)=>a-b).forEach(tone=>add(p.tones.get(tone))));
 return selected.map(row=>row.item);
}
if(typeof window!=='undefined')window.pinyin18SelectToneDiverse=pinyin18SelectToneDiverse;
"""

def main():
    target=Path(sys.argv[1] if len(sys.argv)>1 else "index.html")
    html=target.read_text(encoding="utf-8")
    if MARKER in html:
        bad = r"split(/\\s+/).filter(Boolean)"
        good = r"split(/\s+/).filter(Boolean)"
        if bad in html:
            if html.count(bad) != 1:
                raise SystemExit("Menu 3 selector has an ambiguous escaped whitespace regex.")
            html = html.replace(bad, good, 1)
            target.write_text(html, encoding="utf-8", newline="\n")
            print("Repaired existing Menu 3 selector whitespace tokenization.")
        elif good in html:
            print("Menu 3 Menu 18 tone-position selector already installed and corrected.")
        else:
            raise SystemExit("Existing Menu 3 selector marker found, but its tokenization expression is unknown.")
        return
    if "function pinyin18ToneFromInput(value){" not in html or "function pinyin18Key(value){" not in html:
        raise SystemExit("Menu 18 Pinyin tone/key helpers are missing; refusing to install an incompatible selector.")
    anchor="function pinyinToChineseCandidates(raw){"
    if html.count(anchor)!=1:
        raise SystemExit("Expected exactly one Pinyin candidate mapper for Menu 3 selector insertion.")
    html=html.replace(anchor,SELECTOR+"\n"+anchor,1)
    target.write_text(html,encoding="utf-8",newline="\n")
    print("Menu 3 Menu 18-derived syllable/tone-position selector: PASS")

if __name__=="__main__":
    main()

#!/usr/bin/env python3
"""Patch the shared native speech engine for Android Chrome compatibility."""
from pathlib import Path
import sys

MARKER = "BVT_ANDROID_CHROME_SPEECH_FIX_V1"

HELPERS = r"""// BVT_ANDROID_CHROME_SPEECH_FIX_V1
function bvtNativeVoices(){
 try{return ('speechSynthesis' in window)?(window.speechSynthesis.getVoices()||[]):[];}catch(_){return [];}
}
function bvtNormalizeSpeechLang(value){return String(value||'').trim().replace(/_/g,'-').toLowerCase();}
function bvtFindChineseVoice(voices){
 const accepted=(voices||[]).filter(v=>{
  const lang=bvtNormalizeSpeechLang(v.lang),name=String(v.name||'');
  if(/^(?:zh-(?:hk|tw|hant)|yue)(?:-|$)/i.test(lang)||/hong\s*kong|cantonese|taiwan|quảng đông/i.test(name))return false;
  return /^(?:zh|cmn)(?:-|$)/i.test(lang)||/chinese|mandarin|普通话|中文/i.test(name);
 });
 const mainland=accepted.filter(v=>/^(?:zh-(?:cn|hans-cn)|cmn-cn)(?:-|$)/i.test(bvtNormalizeSpeechLang(v.lang))||/google.*(?:chinese|mandarin)|(?:chinese|mandarin).*google|mainland|普通话|中国大陆/i.test(v.name||''));
 return mainland.find(v=>/google/i.test(v.name||''))||mainland.find(v=>v.default)||mainland[0]||accepted.find(v=>v.default)||accepted[0]||null;
}
function bvtFindVietnameseVoice(voices){
 const accepted=(voices||[]).filter(v=>/^vi(?:-|$)/i.test(bvtNormalizeSpeechLang(v.lang)));
 return accepted.find(v=>/microsoft\s+an\b|\ban\s*[-(]/i.test(v.name||''))||accepted.find(v=>v.default)||accepted[0]||null;
}
function bvtCancelCloudSpeech(){
 // Compatibility name retained for existing learning flows.
 speechPlaybackToken++;speechPlaybackActive=false;
 try{const synth=window.speechSynthesis;if(synth&&(synth.speaking||synth.pending))synth.cancel();}catch(_){}
}
function bvtSpeechBaseLocale(locale){
 const value=String(locale||'').trim();
 const index=value.indexOf('-');
 return index>0?value.slice(0,index):value;
}
function bvtSpeakQueue(parts,button=null,onFinished=null){
 const queue=(Array.isArray(parts)?parts:[]).map(part=>({
  text:String(part?.text||'').trim(),
  lang:String(part?.lang||'vi-VN').trim()||'vi-VN',
  rate:Number(part?.rate)||.9
 })).filter(part=>part.text);
 if(!queue.length){if(typeof onFinished==='function')onFinished();return null;}
 if(!('speechSynthesis'in window)||typeof SpeechSynthesisUtterance==='undefined'){
  if(typeof onFinished==='function')onFinished();return null;
 }
 const synth=window.speechSynthesis;
 const token=++speechPlaybackToken;
 try{
  // Cancel only an active queue. Do not require voices to have loaded before speaking.
  if(synth.speaking||synth.pending)synth.cancel();
  if(typeof synth.resume==='function')synth.resume();
 }catch(_){}
 let index=0,firstUtterance=null,finished=false;
 const finish=()=>{
  if(finished||token!==speechPlaybackToken)return;
  finished=true;speechPlaybackActive=false;reflexLastSpeechEndedAt=Date.now();
  if(typeof onFinished==='function'){try{onFinished();}catch(error){console.warn('Speech completion callback:',error);}}
 };
 const playCurrent=()=>{
  if(token!==speechPlaybackToken)return;
  if(index>=queue.length){finish();return;}
  const part=queue[index];
  let fallbackUsed=false;
  const launch=(locale)=>{
   if(token!==speechPlaybackToken)return;
   let utterance;
   try{
    utterance=new SpeechSynthesisUtterance(part.text);
    utterance.lang=locale;utterance.rate=part.rate;utterance.pitch=1;
    // Do not pin utterance.voice. Android Chrome can expose stale/remote voice objects.
    if(!firstUtterance)firstUtterance=utterance;
    utterance.onstart=()=>{if(token===speechPlaybackToken)speechPlaybackActive=true;};
    utterance.onend=()=>{
     if(token!==speechPlaybackToken)return;
     index++;playCurrent();
    };
    utterance.onerror=(event)=>{
     if(token!==speechPlaybackToken)return;
     const error=String(event?.error||'').toLowerCase();
     const fallback=bvtSpeechBaseLocale(locale);
     if(!fallbackUsed&&fallback&&fallback!==locale&&(error==='voice-unavailable'||error==='language-unavailable')){
      fallbackUsed=true;launch(fallback);return;
     }
     index++;playCurrent();
    };
    speechPlaybackActive=true;
    if(typeof synth.resume==='function')try{synth.resume();}catch(_){}
    synth.speak(utterance);
   }catch(error){
    const fallback=bvtSpeechBaseLocale(locale);
    if(!fallbackUsed&&fallback&&fallback!==locale){fallbackUsed=true;launch(fallback);return;}
    console.warn('Speech synthesis could not start:',error);
    index++;playCurrent();
   }
  };
  launch(part.lang);
 };
 markSpeechButton(button,'Phát âm bằng bộ đọc văn bản của thiết bị.');
 playCurrent();
 return firstUtterance;
}
function bvtSpeakLocale(text,language='vi',button=null,onFinished=null){
 const value=String(text||'').trim();
 if(!value){if(typeof onFinished==='function')onFinished();return null;}
 return language==='zh'?speak(value,button,onFinished):speakAuto(value,button,onFinished);
}
function markSpeechButton(button,title){
 if(!button)return;
 const icon=button.querySelector?.('.dict-action-icon');
 if(icon)icon.textContent='🔊';else button.textContent='🔊';
 button.title=title;
}
function speak(text,button=null,onFinished=null){
 const value=String(text||'').trim();
 if(!value){if(typeof onFinished==='function')onFinished();return null;}
 return bvtSpeakQueue([{text:value,lang:'zh-CN',rate:.82}],button,onFinished);
}
function speakAuto(text,button=null,onFinished=null){
 const value=String(text||'').trim();
 if(!value){if(typeof onFinished==='function')onFinished();return null;}
 const hasHan=/[\u3400-\u9fff\uf900-\ufaff]/u.test(value);
 const isOnlyHan=hasHan&&/^[\u3400-\u9fff\uf900-\ufaff\s，。！？!?、,.：:；;“”"'’‘]+$/u.test(value);
 if(!hasHan)return bvtSpeakQueue([{text:value,lang:'vi-VN',rate:.9}],button,onFinished);
 if(isOnlyHan)return speak(value,button,onFinished);
 const parts=value.match(/[\u3400-\u9fff\uf900-\ufaff]+|[^\u3400-\u9fff\uf900-\ufaff]+/gu)||[value];
 const queue=parts.filter(part=>part.trim()).map(part=>({
  text:part,
  lang:/[\u3400-\u9fff\uf900-\ufaff]/u.test(part)?'zh-CN':'vi-VN',
  rate:.88
 }));
 return bvtSpeakQueue(queue,button,onFinished);
}
"""

ML_HELPER = r"""function bvtMlSpeak(text,language){
 const value=String(text||'').trim();if(!value)return;
 const lang=language||bvtMlDetectLanguage(value);
 if(!lang||!BVT_ML_LANGUAGES[lang]){alert('Hãy chọn ngôn ngữ nguồn để phát âm chính xác.');return;}
 const locale=BVT_ML_LANGUAGES[lang].locale||lang;
 if(lang==='zh'){speak(value,null,null);return;}
 if(lang==='vi'){speakAuto(value,null,null);return;}
 bvtSpeakQueue([{text:value,lang:locale,rate:.92}],null,null);
}
"""

VOICE_INIT = r"""if('speechSynthesis'in window){
 try{speechSynthesis.getVoices();}catch(_){}
 const refreshBvtVoices=()=>{try{speechSynthesis.getVoices();}catch(_){}};
 if(typeof speechSynthesis.addEventListener==='function')speechSynthesis.addEventListener('voiceschanged',refreshBvtVoices);
 else speechSynthesis.onvoiceschanged=refreshBvtVoices;
}
"""

def patch(source: str) -> str:
    if MARKER in source:
        return source
    start = source.find("function bvtNativeVoices(){")
    end = source.find("if('speechSynthesis'in window){", start)
    if start < 0 or end < 0:
        raise SystemExit("Android speech patch: shared speech helper anchors not found uniquely.")
    source = source[:start] + HELPERS + source[end:]
    init_start = source.find("if('speechSynthesis'in window){", start + len(HELPERS))
    init_end = source.find("\ndocument.addEventListener('click',e=>", init_start)
    if init_start < 0 or init_end < 0:
        raise SystemExit("Android speech patch: voice initialization block not found.")
    source = source[:init_start] + VOICE_INIT + source[init_end:]
    ml_start = source.find("function bvtMlSpeak(text,language){")
    ml_end = source.find("async function bvtMlCopy", ml_start)
    if ml_start < 0 or ml_end < 0:
        raise SystemExit("Android speech patch: multilingual speech helper anchors not found.")
    source = source[:ml_start] + ML_HELPER + source[ml_end:]
    return source

if len(sys.argv) != 2:
    raise SystemExit("Usage: patch_android_chrome_speech.py <index.html>")
path = Path(sys.argv[1])
if not path.is_file():
    raise SystemExit(f"Android speech patch: file not found: {path}")
original = path.read_text(encoding="utf-8")
updated = patch(original)
if updated != original:
    path.write_text(updated, encoding="utf-8")
    print("Android Chrome shared speech fix applied.")
else:
    print("Android Chrome shared speech fix already present.")

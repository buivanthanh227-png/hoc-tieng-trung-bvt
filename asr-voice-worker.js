// BVT v42: multilingual Whisper worker for Vietnamese/Chinese voice translation.
// Uses automatic language detection first; only retries with explicit languages if detection gives no useful text.
let transformersModulePromise=null,transcriber=null,transcriberPromise=null,activeSession=null;
function postForActive(type,session,payload={}){if(activeSession===session)self.postMessage({type,session,...payload});}
async function loadTransformers(){
 if(!transformersModulePromise){
  transformersModulePromise=import('https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.8.1').catch(error=>{
   transformersModulePromise=null;throw new Error('Không tải được Transformers.js: '+String(error?.message||error));
  });
 }
 return transformersModulePromise;
}
async function getTranscriber(session){
 if(transcriber)return transcriber;
 if(!transcriberPromise){
  transcriberPromise=(async()=>{
   const {pipeline,env}=await loadTransformers();
   env.allowLocalModels=false;env.allowRemoteModels=true;env.useBrowserCache=true;env.useWasmCache=true;env.cacheKey='bvt-whisper-tiny-v42-voice-multilingual';
   try{if(env.backends?.onnx?.wasm)env.backends.onnx.wasm.numThreads=1;}catch(_){}
   postForActive('status',session,{text:'Đang tải bộ nhận diện đa ngôn ngữ Whisper lần đầu…'});
   return await pipeline('automatic-speech-recognition','onnx-community/whisper-tiny',{
    device:'wasm',dtype:'q8',progress_callback:info=>{
     if(activeSession!==session||!info||info.status!=='progress')return;
     const name=String(info.file||'tệp mô hình').split('/').pop();
     const pct=Number.isFinite(info.progress)?` ${Math.round(info.progress)}%`:'';
     postForActive('progress',session,{text:`Đang tải mô hình nhận diện: ${name}${pct}`});
    }
   });
  })().catch(error=>{transcriberPromise=null;throw error;});
 }
 transcriber=await transcriberPromise;return transcriber;
}
function tidy(value){return String(value||'').replace(/[\u0000-\u001f]/g,' ').replace(/\s+/g,' ').trim();}
function countMatches(text,regex){return (String(text||'').match(regex)||[]).length;}
function hasTargetScript(text){
 const t=String(text||'');
 return /[\u3400-\u9fff\uf900-\ufaff]/.test(t)||/[ăâđêôơưàáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ]/i.test(t);
}
function scoreForced(text,language){
 const t=String(text||'');const han=countMatches(t,/[\u3400-\u9fff\uf900-\ufaff]/g);const latin=countMatches(t,/[A-Za-zÀ-ỹ]/g);
 const marks=countMatches(t,/[ăâđêôơưàáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ]/gi);
 return language==='chinese'?(han*5-latin*0.15):(latin+marks*3-han*5);
}
async function run(pipe,audio,options){
 const out=await pipe(audio,{task:'transcribe',return_timestamps:false,chunk_length_s:30,stride_length_s:5,...options});
 return tidy(out?.text);
}
async function transcribe(pipe,audio,session){
 let text=await run(pipe,audio,{});if(activeSession!==session)return '';
 if(hasTargetScript(text))return text;
 postForActive('status',session,{text:text?'Đang kiểm tra lại ngôn ngữ để tránh nhận sai tiếng Việt/Trung…':'Đang thử nhận diện riêng tiếng Việt và tiếng Trung…'});
 let vi='',zh='';
 try{vi=await run(pipe,audio,{language:'vietnamese'});}catch(_){}
 if(activeSession!==session)return '';
 try{zh=await run(pipe,audio,{language:'chinese'});}catch(_){}
 if(activeSession!==session)return '';
 const candidates=[{text,score:hasTargetScript(text)?1000:0},{text:vi,score:scoreForced(vi,'vietnamese')},{text:zh,score:scoreForced(zh,'chinese')}].filter(x=>x.text);
 candidates.sort((a,b)=>b.score-a.score||b.text.length-a.text.length);
 return candidates[0]?.text||'';
}
self.addEventListener('message',async event=>{
 const message=event.data||{};
 if(message.type==='cancel'){if(activeSession===message.session)activeSession=null;return;}
 if(message.type!=='transcribe')return;
 const session=message.session;activeSession=session;
 try{
  const pipe=await getTranscriber(session);if(activeSession!==session)return;
  const audio=message.audio instanceof Float32Array?message.audio:new Float32Array(message.audio);
  if(audio.length<8000)throw new Error('Bản ghi quá ngắn hoặc không có âm thanh.');
  let peak=0;for(let i=0;i<audio.length;i++)peak=Math.max(peak,Math.abs(audio[i]));
  if(peak<0.0015)throw new Error('Micro không thu được tiếng nói rõ ràng.');
  postForActive('status',session,{text:'Đang nhận diện tự động tiếng Việt hoặc tiếng Trung…'});
  const text=await transcribe(pipe,audio,session);
  postForActive('result',session,{text});
 }catch(error){postForActive('error',session,{message:String(error?.message||error||'Không nhận dạng được âm thanh.')});}
});

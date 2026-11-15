#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
index_path=ROOT/'index.html'
html=index_path.read_text(encoding='utf-8')
changes=[]

def rep(old,new,label):
    global html
    count=html.count(old)
    if count!=1:
        raise RuntimeError(f'{label}: expected 1 match, got {count}')
    html=html.replace(old,new,1)
    changes.append(label)

# BVT-07: common meaning of 鱼/魚.
rep(
" ['饿','餓','è','Đói','HSK1'],['渴','渴','kě','Khát','HSK1'],['疼','疼','téng','Đau; đau nhức','HSK2'],['痛','痛','tòng','Đau; đau đớn','HSK2'],['生病','生病','shēngbìng','Bị bệnh; ốm','HSK2'],['生气','生氣','shēngqì','Tức giận; giận','HSK2'],['开心','開心','kāixīn','Vui; vui vẻ','HSK2'],['难过','難過','nánguò','Buồn; khó chịu','HSK2'],['想念','想念','xiǎngniàn','Nhớ (ai đó); nhớ nhung','HSK3']",
" ['饿','餓','è','Đói','HSK1'],['渴','渴','kě','Khát','HSK1'],['疼','疼','téng','Đau; đau nhức','HSK2'],['痛','痛','tòng','Đau; đau đớn','HSK2'],['生病','生病','shēngbìng','Bị bệnh; ốm','HSK2'],['生气','生氣','shēngqì','Tức giận; giận','HSK2'],['开心','開心','kāixīn','Vui; vui vẻ','HSK2'],['难过','難過','nánguò','Buồn; khó chịu','HSK2'],['想念','想念','xiǎngniàn','Nhớ (ai đó); nhớ nhung','HSK3'],['鱼','魚','yú','Cá; họ [Yu2]','']",
"BVT-07 nghĩa 鱼/魚")

# BVT-14: do not interpret a normalized-empty emoji as an empty dictionary query.
rep(
"function applyFilter(){const q=norm($('dict-search').value);filteredIndices=[];if(!q){filteredIndices=Array.from({length:dictionary.length},(_,i)=>i);}else{const found=[];for(let i=0;i<dictionary.length;i++){const score=searchScoreForRow(i,q);if(score>0)found.push({i,score});}found.sort((a,b)=>b.score-a.score||a.i-b.i);filteredIndices=found.map(x=>x.i);}currentPage=1;renderDictionary();}",
"function applyFilter(){const raw=String($('dict-search').value||'').trim(),q=norm(raw);filteredIndices=[];if(!raw){filteredIndices=Array.from({length:dictionary.length},(_,i)=>i);}else if(q){const found=[];for(let i=0;i<dictionary.length;i++){const score=searchScoreForRow(i,q);if(score>0)found.push({i,score});}found.sort((a,b)=>b.score-a.score||a.i-b.i);filteredIndices=found.map(x=>x.i);}currentPage=1;renderDictionary();}",
"BVT-14 emoji từ điển")

# BVT-13: same guard for radicals.
rep(
"function renderRadicals(){const raw=String($('radical-search')?.value||'').trim(),q=norm(raw).replace(/^bo/,'');const st=$('radical-stroke-filter')?.value||'all';const rows=RADICALS.filter(r=>(st==='all'||r.strokes===Number(st)||r.variantStrokes===Number(st))&&(!q||radicalSearchText(r).includes(q)));",
"function renderRadicals(){const raw=String($('radical-search')?.value||'').trim(),normalized=norm(raw),q=normalized.replace(/^bo/,''),invalidQuery=Boolean(raw&&!normalized);const st=$('radical-stroke-filter')?.value||'all';const rows=RADICALS.filter(r=>(st==='all'||r.strokes===Number(st)||r.variantStrokes===Number(st))&&!invalidQuery&&(!q||radicalSearchText(r).includes(q)));",
"BVT-13 emoji bộ thủ")

# BVT-04: readable wrapping for Menu 7 search result rows on phones.
style_start=html.find('<style>')
style_end=html.find('</style>',style_start)
if style_start<0 or style_end<0:
    raise RuntimeError('BVT-04: first CSS block not found')
css="""
/* v42.9.1 QA fix BVT-04: readable, wrapping vocabulary matches in handwriting search. */
#write-vocab-results .combine-suggestion{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:start;gap:5px 10px;min-width:0;}
#write-vocab-results .suggestion-hanzi{grid-column:1;grid-row:1;min-width:0;white-space:normal;overflow-wrap:anywhere;}
#write-vocab-results .suggestion-meta{grid-column:1;grid-row:2;display:grid;grid-template-columns:minmax(0,1fr);gap:3px;min-width:0;white-space:normal;}
#write-vocab-results .suggestion-pinyin,#write-vocab-results .suggestion-meaning{display:block;white-space:normal;overflow:visible;text-overflow:clip;overflow-wrap:anywhere;line-height:1.4;}
#write-vocab-results .suggestion-add{grid-column:2;grid-row:1 / span 2;position:static;align-self:center;white-space:nowrap;}
"""
html=html[:style_end]+css+html[style_end:]
changes.append('BVT-04 CSS mobile')

# BVT-01: CSV parser, preserving header and already translated cells.
csv_code=r"""
function parseCsvRows(source){
 const text=String(source||'').replace(/^\uFEFF/,'');
 const rows=[];let row=[],field='',quoted=false;
 for(let i=0;i<text.length;i++){
  const ch=text[i];
  if(quoted){if(ch==='"'&&text[i+1]==='"'){field+='"';i++;}else if(ch==='"')quoted=false;else field+=ch;}
  else if(ch==='"'&&field.length===0)quoted=true;
  else if(ch===','){row.push(field);field='';}
  else if(ch==='\n'){row.push(field);field='';if(row.some(cell=>String(cell).trim()))rows.push(row);row=[];}
  else if(ch!=='\r')field+=ch;
 }
 if(field.length||row.length){row.push(field);if(row.some(cell=>String(cell).trim()))rows.push(row);}
 return rows;
}
function serializeCsvRows(rows){
 const quote=cell=>{const value=String(cell??'');return /[",\r\n]/.test(value)?'"'+value.replace(/"/g,'""')+'"':value;};
 return rows.map(row=>row.map(quote).join(',')).join('\n');
}
function isCsvLanguageHeader(row){
 const labels=new Set(['vi','vn','vietnamese','tiengviet','zh','zhcn','zhtw','cn','chinese','tiengtrung','hanzi','pinyin','id','key']);
 const cells=(row||[]).map(cell=>norm(cell).replace(/[\s_-]/g,''));
 return cells.length>=2&&cells.some(cell=>['vi','vn','vietnamese','tiengviet'].includes(cell))&&cells.some(cell=>['zh','zhcn','zhtw','cn','chinese','tiengtrung','hanzi'].includes(cell))&&cells.every(cell=>labels.has(cell));
}
function containsChineseText(value){return /[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]/.test(String(value||''));}
async function translateCsvText(source,target,statusEl,resultEl){
 const rows=parseCsvRows(source);if(!rows.length)throw new Error('Tệp CSV không có dòng dữ liệu.');
 const sourceIsVietnamese=target.startsWith('zh'),firstDataRow=isCsvLanguageHeader(rows[0])?1:0,tasks=[];
 for(let r=firstDataRow;r<rows.length;r++)for(let c=0;c<rows[r].length;c++){
  const value=String(rows[r][c]||'').trim();if(!value||/^[\d\s.,;:%+\-()/]+$/.test(value))continue;
  const hasChinese=containsChineseText(value);
  if(sourceIsVietnamese){if(hasChinese||!/[A-Za-zÀ-ỹ]/.test(value))continue;}else if(!hasChinese)continue;
  tasks.push({row:r,column:c});
 }
 if(tasks.length>200)throw new Error('Tệp CSV có hơn 200 ô cần dịch trong một lượt. Hãy chia tệp thành các phần nhỏ hơn để tránh giới hạn dịch vụ.');
 if(!tasks.length){resultEl.textContent=serializeCsvRows(rows);resultEl.dataset.translationLanguage=target;setTranslationResultActions(resultEl.id,true);statusEl.textContent='Không có ô nguồn cần dịch. Đã giữ nguyên tiêu đề và dữ liệu CSV.';return;}
 const sourceLanguage=sourceIsVietnamese?'vi':'zh-CN';
 for(let i=0;i<tasks.length;i++){const task=tasks[i];statusEl.textContent='Đang dịch ô '+(i+1)+'/'+tasks.length+' trong tệp CSV…';rows[task.row][task.column]=await machineTranslate(rows[task.row][task.column],sourceLanguage,target);}
 resultEl.textContent=serializeCsvRows(rows);resultEl.dataset.translationLanguage=target;setTranslationResultActions(resultEl.id,!!resultEl.textContent.trim());statusEl.textContent='Đã dịch xong CSV ('+tasks.length+' ô). Hàng tiêu đề và các ô đã ở ngôn ngữ đích được giữ nguyên.';
}
"""
rep("async function runFileTranslation(target){",csv_code+"\nasync function runFileTranslation(target){","BVT-01 CSV parser")
rep(
"try{out.textContent='Đang đọc tệp '+file.name+'…';const content=await readTranslationFile(file);if(!content.trim())throw new Error('Tệp không có văn bản để dịch.');await translateLongText(content,target,status,out);}catch(e)",
"try{out.textContent='Đang đọc tệp '+file.name+'…';const content=await readTranslationFile(file);if(!content.trim())throw new Error('Tệp không có văn bản để dịch.');const ext=(file.name.split('.').pop()||'').toLowerCase();if(ext==='csv')await translateCsvText(content,target,status,out);else await translateLongText(content,target,status,out);}catch(e)",
"BVT-01 CSV route")

# BVT-09: exact local matching only for Pinyin conversion.
rep(
"function tryLocalTranslation(raw){\n const key=norm(raw);",
"function tryExactLocalTranslation(raw){\n const key=norm(raw);if(OFFLINE_SENTENCE_TRANSLATIONS[key])return {...OFFLINE_SENTENCE_TRANSLATIONS[key],source:'Câu mẫu tích hợp sẵn'};\n const exact=sentenceDeck.find(r=>[r.zh,r.py,r.vi].some(x=>norm(x)===key));return exact?{zh:exact.zh,py:exact.py,vi:exact.vi,source:'Câu mẫu khớp chính xác'}:null;\n}\nfunction tryLocalTranslation(raw){\n const key=norm(raw);",
"BVT-09 exact Pinyin match")
rep("const exactLocal=tryLocalTranslation(converted.zh)||tryLocalTranslation(raw);","const exactLocal=tryExactLocalTranslation(converted.zh);","BVT-09 no near Pinyin match")

# BVT-05: accept the report's evidenced synonym for 茶.
rep(
"score=scoreAnswer(user,expected,[simpleGloss(r[3]),r[0]])",
"score=scoreAnswer(user,expected,[simpleGloss(r[3]),r[0],...((r[0]==='茶'||r[1]==='茶')?['chè','chè khô']:[])])",
"BVT-05 chè synonym")

# BVT-02: completed stroke quiz should count once.
rep("let practiceStrokeCount = 0;","let practiceStrokeCount = 0;\nlet practiceStrokeScoreRecorded = false;","BVT-02 score guard")
rep("practiceStrokeQuizWriter=null;practiceStrokeCount=0;practiceStrokeMistakes=0;","practiceStrokeQuizWriter=null;practiceStrokeCount=0;practiceStrokeMistakes=0;practiceStrokeScoreRecorded=false;","BVT-02 reset on reset")
rep("practiceStrokeCount=0;practiceStrokeMistakes=0;\n $('practice-free-wrap').hidden=true;","practiceStrokeCount=0;practiceStrokeMistakes=0;practiceStrokeScoreRecorded=false;\n $('practice-free-wrap').hidden=true;","BVT-02 reset on start")
rep(
"$('practice-stroke-feedback').textContent='Hoàn thành chữ '+practiceTraceChar+'! Điểm: '+score+'/100 · Số lần viết sai: '+mistakes+' · Tổng số nét: '+practiceStrokeCount+'.';\n    $('practice-grade-strokes').textContent='↻ Luyện lại';",
"$('practice-stroke-feedback').textContent='Hoàn thành chữ '+practiceTraceChar+'! Điểm: '+score+'/100 · Số lần viết sai: '+mistakes+' · Tổng số nét: '+practiceStrokeCount+'.';\n    if(!practiceStrokeScoreRecorded){practiceStrokeScoreRecorded=true;saveStats(score);updateStats();}\n    $('practice-grade-strokes').textContent='↻ Luyện lại';",
"BVT-02 save score")

# BVT-03: swap respondent pronouns for auto-generated Q&A pairs.
rep(
"if(statement){const key='dialogue|'+clean+'|'+statement.zh;if(!seen.has(key)){seen.add(key);pairs.push({qZh:clean+'？',aZh:String(statement.zh).replace(/[。！？!?]+$/,'')+'。',qVi:s.vi||'Hãy trả lời câu hỏi này bằng tiếng Trung.',aVi:statement.vi||'',kind:'dialogue',py:statement.py||pinyinForChinese(statement.zh)});}}",
"if(statement){const key='dialogue|'+clean+'|'+statement.zh;if(!seen.has(key)){seen.add(key);const answerZh=String(statement.zh||'').replace(/[。！？!?]+$/,'').replace(/你/g,'__BVT_YOU__').replace(/我/g,'你').replace(/__BVT_YOU__/g,'我');const answerVi=String(statement.vi||'').replace(/Tôi/g,'__BVT_TOI__').replace(/Bạn/g,'Tôi').replace(/__BVT_TOI__/g,'Bạn').replace(/tôi/g,'__BVT_toi__').replace(/bạn/g,'tôi').replace(/__BVT_toi__/g,'bạn');pairs.push({qZh:clean+'？',aZh:answerZh+'。',qVi:s.vi||'Hãy trả lời câu hỏi này bằng tiếng Trung.',aVi:answerVi,kind:'dialogue',py:pinyinForChinese(answerZh+'。')});}}",
"BVT-03 Q&A pronouns")

# BVT-08: localize invalid JSON errors.
rep(
"}catch(error){status('Không nhập được bản sao lưu: '+(error?.message||String(error)));}",
"}catch(error){const parseFailure=error instanceof SyntaxError||error?.name==='SyntaxError'||error?.name==='InvalidCharacterError';const message=parseFailure?'Tệp JSON không hợp lệ hoặc đã bị hỏng. Hãy chọn bản sao lưu JSON được xuất từ ứng dụng BVT. Thư viện hiện tại vẫn được giữ nguyên.':(error?.message==='Tệp không đúng định dạng bản sao lưu của BVT.'?error.message:'Không nhập được bản sao lưu. Vui lòng kiểm tra tệp và thử lại.');status('Không nhập được bản sao lưu: '+message);}",
"BVT-08 Vietnamese JSON error")

# BVT-12: clamp and write back timer settings.
rep(
"function trainingSeconds(id,fallback,min=0,max=120){const n=Number($(id)?.value);return Number.isFinite(n)?Math.max(min,Math.min(max,n)):fallback;}",
"function trainingSeconds(id,fallback,min=0,max=120){const field=$(id),raw=String(field?.value??'').trim(),parsed=raw===''?NaN:Number(raw);const value=Number.isFinite(parsed)?Math.max(min,Math.min(max,Math.trunc(parsed))):fallback;if(field&&String(field.value)!==String(value))field.value=String(value);return value;}\n[['vocab-training-show-seconds',5,1,120],['vocab-training-next-seconds',2,0,60]].forEach(([id,fallback,min,max])=>{const field=$(id);if(field){const normalize=()=>trainingSeconds(id,fallback,min,max);field.addEventListener('change',normalize);field.addEventListener('blur',normalize);}});",
"BVT-12 timer fields")

# BVT-10: never copy placeholder/pending/failed translation.
rep(
"async function bvtMlCopy(elementId){\n const element=$(elementId);const value=String(element&&('value'in element)?element.value:element?.textContent||'').trim();if(!value)return;",
"async function bvtMlCopy(elementId){\n const element=$(elementId);if((elementId==='bvt-mi-result'||elementId==='bvt-mv-result')&&element?.dataset?.bvtTranslationReady!=='true'){const status=$(elementId.replace('-result','-status'));if(status)status.textContent='Chưa có kết quả dịch để sao chép.';return;}const value=String(element&&('value'in element)?element.value:element?.textContent||'').trim();if(!value)return;",
"BVT-10 copy guard")
# BVT-15: empty input does not overwrite a live recording state.
rep(
"if(!text){result.textContent='Bản dịch sẽ hiển thị tại đây.';if(status)status.textContent='Sẵn sàng.';return;}",
"if(!text){result.textContent='Bản dịch sẽ hiển thị tại đây.';result.dataset.bvtTranslationReady='false';const recordingActive=prefix==='bvt-mv'&&typeof bvtMvRecorder!=='undefined'&&bvtMvRecorder?.state==='recording';if(status)status.textContent=recordingActive?'Đang ghi âm… chạm lại để kết thúc.':'Sẵn sàng.';return;",
"BVT-15 live recording state")
rep("result.textContent='Đang dịch…';\n try{","result.textContent='Đang dịch…';result.dataset.bvtTranslationReady='false';\n try{","BVT-10 pending marker")
rep("result.textContent=translated.text;\n  if(field&&translated.source)","result.textContent=translated.text;result.dataset.bvtTranslationReady='true';\n  if(field&&translated.source)","BVT-10 success marker")
rep("result.textContent='Chưa dịch được nội dung.';\n  if(status)","result.textContent='Chưa dịch được nội dung.';result.dataset.bvtTranslationReady='false';\n  if(status)","BVT-10 failed marker")
rep(
"const result=$(prefix+'-result');if(result)result.textContent='Bản dịch sẽ hiển thị tại đây.';",
"const result=$(prefix+'-result');if(result){result.textContent='Bản dịch sẽ hiển thị tại đây.';result.dataset.bvtTranslationReady='false';}",
"BVT-10 clear marker")

# BVT-11: update image count after removing one preview.
rep(
"button.addEventListener('click',()=>{bvtMiFiles.splice(index,1);bvtMiRenderFiles();});",
"button.addEventListener('click',()=>{bvtMiFiles.splice(index,1);bvtMiRenderFiles();const status=$('bvt-mi-status');if(status)status.textContent=bvtMiFiles.length?'Đã chọn '+bvtMiFiles.length+' ảnh.':'Chưa chọn ảnh.';});",
"BVT-11 image count")

# BVT-16: filter the OCR no-text sentinel before translation.
rep(
"async function bvtMiScan(){\n if(!bvtMiFiles.length)",
"function bvtMiIsNoTextDetected(value){const text=String(value||'').trim().replace(/^[*\\s]+|[*\\s]+$/g,'').replace(/^\\[|\\]$/g,'').trim().toLowerCase();return !text||['no text detected','no text was detected','no text found'].includes(text);}\nasync function bvtMiScan(){\n if(!bvtMiFiles.length)",
"BVT-16 OCR sentinel helper")
rep(
"$('bvt-mi-text').value='';$('bvt-mi-result').textContent='Bản dịch sẽ hiển thị tại đây.';",
"$('bvt-mi-text').value='';$('bvt-mi-result').textContent='Bản dịch sẽ hiển thị tại đây.';$('bvt-mi-result').dataset.bvtTranslationReady='false';",
"BVT-16 reset old result")
rep(
"if(!response.ok)throw new Error(data.error||('OCR trả về lỗi '+response.status));if(data.text)results.push(String(data.text).trim());",
"if(!response.ok)throw new Error(data.error||('OCR trả về lỗi '+response.status));const recognizedText=String(data.text||'').trim();if(recognizedText&&!bvtMiIsNoTextDetected(recognizedText))results.push(recognizedText);",
"BVT-16 ignore sentinel")
rep(
"const recognized=results.join('\\n\\n').trim();if(!recognized)throw new Error('Không nhận diện được nội dung trong ảnh.');",
"const recognized=results.join('\\n\\n').trim();if(!recognized)throw new Error('Ảnh không có văn bản để nhận diện. Hãy chọn ảnh khác có chữ.');",
"BVT-16 stop empty image")

# BVT-06: recompute the tile positions on resize without restarting the active round.
rep(
"   box.style.height=Math.max(300,y+rowH+pad)+'px';\n }\n function pickDifferent(list,previous)",
"   box.style.height=Math.max(300,y+rowH+pad)+'px';\n }\n let hmResizeTimer=null;\n function hmReflowActiveBoard(){if(!started||!['observe','answer'].includes(clockMode))return;const board=$hm('hm-board');if(!board)return;const tiles=[...board.querySelectorAll('.hm-tile')];if(tiles.length)scatterTiles(board,tiles);}\n window.addEventListener('resize',()=>{if(!started||clockMode!=='observe')return;clearTimeout(hmResizeTimer);hmResizeTimer=setTimeout(hmReflowActiveBoard,120);});\n window.addEventListener('orientationchange',()=>{if(!started||clockMode!=='observe')return;clearTimeout(hmResizeTimer);hmResizeTimer=setTimeout(hmReflowActiveBoard,180);});\n function pickDifferent(list,previous)",
"BVT-06 memory board resize")
rep("<title>HỌC TIẾNG TRUNG · V42.9</title>","<title>HỌC TIẾNG TRUNG · V42.9.1</title>","version title")
rep("<strong>HỌC TIẾNG TRUNG · Phiên bản v42.9</strong>","<strong>HỌC TIẾNG TRUNG · Phiên bản v42.9.1</strong>","version footer")

index_path.write_text(html,encoding='utf-8')
manifest_path=ROOT/'manifest.webmanifest'
manifest=manifest_path.read_text(encoding='utf-8').replace('HỌC TIẾNG TRUNG BVT · V42.9','HỌC TIẾNG TRUNG BVT · V42.9.1')
manifest_path.write_text(manifest,encoding='utf-8')
sw_path=ROOT/'sw.js'
sw=sw_path.read_text(encoding='utf-8')
sw=sw.replace('hoc-trung-app-shell-v42-9-bugfix-20261115','hoc-trung-app-shell-v42-9-1-20261115')
sw=sw.replace('bvt-pinyin-audio-assets-v42-9','bvt-pinyin-audio-assets-v42-9-1')
sw_path.write_text(sw,encoding='utf-8')
release=ROOT/'RELEASE_NOTES_v42.9.1.md'
release.write_text(
"# HỌC TIẾNG TRUNG BVT v42.9.1\n\n"
"Đã xử lý các phát hiện trong báo cáo QA 42.9: CSV; thống kê hoàn thành luyện nét; đổi ngôi hỏi–đáp; bố cục kết quả luyện viết trên màn hình nhỏ; chấm đồng nghĩa 茶/chè; sắp xếp lại bảng nhớ chữ khi resize; nghĩa 鱼; thông báo JSON backup; đối chiếu Pinyin chính xác; chặn copy placeholder; cập nhật bộ đếm ảnh; giới hạn thời gian luyện từ; tìm emoji trong từ điển/bộ thủ; trạng thái micro; và ảnh OCR không có chữ.\n\n"
"Không thay đổi nội dung dữ liệu CVDICT đã nhúng hoặc các worker ASR/OCR. Những mục bị BLOCKED trong báo cáo gốc không được xem là đã kiểm thử lại.\n",
encoding='utf-8')
print(json.dumps({"version":"42.9.1","changes":changes,"html_bytes":index_path.stat().st_size},ensure_ascii=False,indent=2))

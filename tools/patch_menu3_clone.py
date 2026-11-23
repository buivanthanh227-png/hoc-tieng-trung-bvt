#!/usr/bin/env python3
"""Create an independent Menu 3 copy of Menu 18 on the deploy artifact."""
from pathlib import Path
import re, sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: patch_menu3_clone.py <site/index.html>")
p=Path(sys.argv[1]); html=p.read_text(encoding='utf-8')
MARK='MENU3_INDEPENDENT_COPY_OF_MENU18_V1'
if MARK in html: raise SystemExit('Menu 3 clone already applied; refusing duplicate patch.')

# Remove only Pinyin playback, retaining Pinyin display/copy and Chinese/Vietnamese speech.
py_button='<button type="button" data-homework18-speak="py">🔊 Nghe Pinyin</button>'
if html.count(py_button)!=1: raise SystemExit('Expected exactly one Menu 18 Pinyin speaker button.')
html=html.replace(py_button,'',1)
modal_start=html.find('function openHomework18CandidateModal(item,index,total){')
modal_end=html.find('\nasync function renderHomework18Candidates(candidates){',modal_start)
if modal_start<0 or modal_end<0: raise SystemExit('Cannot locate Menu 18 candidate modal source.')
modal=html[modal_start:modal_end]
py_start=modal.find(" // Recorded Pinyin syllable audio grouped by the user's original word boundaries.")
py_end=modal.find(" modal.querySelectorAll('[data-homework18-speak]')",py_start)
if py_start<0 or py_end<0: raise SystemExit('Cannot isolate Menu 18 Pinyin audio function.')
modal=modal[:py_start]+modal[py_end:]
modal=modal.replace("if(kind==='py'){playPinyinWords();return;}",'')
html=html[:modal_start]+modal+html[modal_end:]
if 'const playPinyinWords=async()=>{' in html or 'data-homework18-speak="py"' in html:
    raise SystemExit('Pinyin playback removal incomplete.')

# Clone the complete Menu 18 panel, with a fully separate DOM/state namespace.
panel_start=html.find('<section id="panel-translate-experimental"')
panel_end=html.find('\n<section id="',panel_start+1)
if panel_start<0 or panel_end<0: raise SystemExit('Cannot locate complete Menu 18 panel.')
panel=html[panel_start:panel_end]
clone=panel.replace('id="panel-translate-experimental"','id="panel-translate3"',1)
clone=clone.replace('id="experimental-quick-translate-card"','id="quick-translate-card3"',1)
clone=clone.replace('id="homework18-','id="homework3x-')
clone=clone.replace('id="long-translate-18-','id="long-translate-3x-')
clone=clone.replace('id="translate-file-18-','id="translate-file-3x-')
clone=clone.replace('id="file-translate-18-','id="file-translate-3x-')
clone=clone.replace('data-function-number="18"','data-function-number="3"')
clone=clone.replace('MENU 18 – DỊCH NHANH VIỆT ⇄ TRUNG (THỬ NGHIỆM)','MENU 3 – DỊCH NHANH VIỆT ⇄ TRUNG')
clone=clone.replace('MENU 18 – DỊCH NHANH VIỆT ⇄ TRUNG','MENU 3 – DỊCH NHANH VIỆT ⇄ TRUNG')
clone=clone.replace(' (THỬ NGHIỆM)','')
if 'id="homework18-' in clone or 'id="long-translate-18-' in clone:
    raise SystemExit('Menu 18 HTML IDs remain in cloned panel.')

# Duplicate Menu 18's full candidate/result logic; shared dictionary and Pinyin index stay read-only.
logic_start=html.find("function renderHomework18Card(result,sourceLabel=''){")
logic_end=html.find('async function machineTranslate(text,source,target){',logic_start)
if logic_start<0 or logic_end<0: raise SystemExit('Cannot locate complete Menu 18 lookup/render logic.')
logic=html[logic_start:logic_end]
logic=re.sub(r'\bhomework18([A-Za-z0-9_]*)',r'homework3x\1',logic)
logic=re.sub(r'\b([A-Za-z]+Homework)18([A-Za-z0-9_]*)',r'\g<1>3x\2',logic)
logic=logic.replace('looksLikePinyin18','looksLikePinyin3x')
logic=logic.replace("$('homework18-","$('homework3x-")
logic=logic.replace('data-homework18-','data-homework3x-')
if 'playPinyinWords' in logic or "$('homework18-" in logic:
    raise SystemExit('Cloned Menu 3 logic still contains Pinyin playback or Menu 18 DOM references.')

# Clone Menu 18's dedicated visual rules, retaining shared result/modal classes.
style_start=html.find('<style id="menu18-experimental-styles">')
style_end=html.find('</style>',style_start)
if style_start<0 or style_end<0: raise SystemExit('Cannot locate Menu 18 visual style block.')
style=html[style_start:style_end+8]
style=style.replace('menu18-experimental-styles','menu3-independent-styles')
style=style.replace('#panel-translate-experimental','#panel-translate3')
style=style.replace('#experimental-quick-translate-card','#quick-translate-card3')
style=style.replace('#long-translate-18-','#long-translate-3x-')
style=style.replace('#translate-file-18-','#translate-file-3x-')
style=style.replace('#file-translate-18-','#file-translate-3x-')
# Rename every Menu 18 result/modal class selector to the cloned Menu 3 namespace.
# The cloned HTML already uses homework3x; keeping these CSS selectors aligned
# makes result cards and the candidate popup visually identical to Menu 18.
style=style.replace('homework18','homework3x')
html=html[:style_end+8]+'\n'+style+html[style_end+8:]

# Preserve the old Menu 3 practice panel; the new Menu 3 gets its own panel.
practice_pos=html.find('<section id="panel-practice"')
if practice_pos<0: raise SystemExit('Cannot locate original Menu 3/practice panel.')
html=html[:practice_pos]+clone+'\n'+html[practice_pos:]

old_tab='<button class="tab" data-tab="translate" type="button"><span class="tab-number" aria-hidden="true">3</span><span class="tab-main"><span class="tab-icon translate-icon" aria-hidden="true">文 ⇄ A</span><span class="tab-label">DỊCH NHANH VIỆT ⇄ TRUNG</span></span></button>'
if html.count(old_tab)!=1: raise SystemExit('Could not uniquely locate Menu 3 navigation button.')
html=html.replace(old_tab,old_tab.replace('data-tab="translate"','data-tab="translate3"'),1)
html=html.replace('DỊCH NHANH VIỆT ⇄ TRUNG (THỬ NGHIỆM)','DỊCH NHANH VIỆT ⇄ TRUNG')

switch_marker="function switchTab(tab){"
if html.count(switch_marker)!=1: raise SystemExit("switchTab function marker is ambiguous.")
html=html.replace(switch_marker,"BVT_FUNCTION_COLORS.translate3=BVT_FUNCTION_COLORS.translate;\n"+switch_marker,1)

old="const panelTab=(tab==='translate'||PRACTICE_NAV_MODES.has(tab))?'practice':tab;"
new="const panelTab=tab==='translate3'?'translate3':((tab==='translate'||PRACTICE_NAV_MODES.has(tab))?'practice':tab);"
if html.count(old)!=1: raise SystemExit('switchTab panel routing marker is ambiguous.')
html=html.replace(old,new,1)
if html.count("const translating=tab==='translate';")!=1: raise SystemExit('switchTab visibility marker is ambiguous.')
html=html.replace("const translating=tab==='translate';","const translating=tab==='translate'||tab==='translate3';",1)
old="else if(tab==='translate')bvtSyncFunctionHeading($('quick-translate-card').querySelector('.section-title'),'translate');\n else bvtSyncActiveFunctionHeading(tab);"
new="else if(tab==='translate')bvtSyncFunctionHeading($('quick-translate-card').querySelector('.section-title'),'translate');\n else if(tab==='translate3')bvtSyncFunctionHeading($('quick-translate-card3').querySelector('.section-title'),'translate');\n else bvtSyncActiveFunctionHeading(tab);"
if html.count(old)!=1: raise SystemExit('switchTab heading marker is ambiguous.')
html=html.replace(old,new,1)

css='''<style id="menu3-independent-color">\n.app-shell #main-tabs .tab[data-tab="translate3"]{--menu-color:#0891b2}\n#panel-translate3{--red:#0891b2;--red2:#0e7490}\n#panel-translate3 .section-title{color:var(--red)}\n#panel-translate3 .btn:not(.secondary){background:var(--red)}\n</style>\n'''
html=html.replace('</head>',css+'</head>',1)

extra=r'''
<script id="menu3-independent-translation-handlers">
async function runLongTranslation3x(target){
 const status=$('long-translate-3x-status'),out=$('long-translate-3x-result');
 setTranslationResultActions(out.id,false);out.dataset.translationLanguage='';
 try{out.textContent='Đang chuẩn bị dịch…';await translateLongText($('long-translate-3x-input').value,target,status,out);}catch(error){status.textContent='Không dịch được: '+(error.message||error);out.textContent='';setTranslationResultActions(out.id,false);}
}
$('long-translate-3x-to-zh')?.addEventListener('click',()=>runLongTranslation3x('zh-CN'));
$('long-translate-3x-to-vi')?.addEventListener('click',()=>runLongTranslation3x('vi'));
async function runFileTranslation3x(target){
 const file=$('translate-file-3x-input').files?.[0],status=$('file-translate-3x-status'),out=$('file-translate-3x-result');
 if(!file){status.textContent='Hãy chọn tệp TXT, MD, CSV hoặc DOCX trước.';return;}
 setTranslationResultActions(out.id,false);out.dataset.translationLanguage='';
 try{out.textContent='Đang đọc tệp '+file.name+'…';const content=await readTranslationFile(file);if(!content.trim())throw new Error('Tệp không có văn bản để dịch.');await translateLongText(content,target,status,out);}catch(error){status.textContent='Không xử lý được tệp: '+(error.message||error);out.textContent='';setTranslationResultActions(out.id,false);}
}
$('file-translate-3x-to-zh')?.addEventListener('click',()=>runFileTranslation3x('zh-CN'));
$('file-translate-3x-to-vi')?.addEventListener('click',()=>runFileTranslation3x('vi'));
$('long-translate-3x-copy')?.addEventListener('click',()=>copyTranslationOutput('long-translate-3x-result','long-translate-3x-status'));
$('long-translate-3x-speak')?.addEventListener('click',()=>speakTranslationOutput('long-translate-3x-result','long-translate-3x-status'));
$('file-translate-3x-copy')?.addEventListener('click',()=>copyTranslationOutput('file-translate-3x-result','file-translate-3x-status'));
$('file-translate-3x-speak')?.addEventListener('click',()=>speakTranslationOutput('file-translate-3x-result','file-translate-3x-status'));
</script>
'''
insert='\n<script id="menu3-independent-lookup-logic">\n'+logic+'\n</script>\n'+extra+'\n'
if '</body>' not in html: raise SystemExit('Missing body close.')
html=html.replace('</body>',insert+'<!-- '+MARK+' -->\n</body>',1)
if re.search(r"\$\('homework18-",logic) or re.search(r"\bhomework18[A-Za-z0-9_]+",logic) or 'homework3x-query' not in html or 'panel-translate3' not in html:
    raise SystemExit('Independent Menu 3 verification failed.')
p.write_text(html,encoding='utf-8')
print('Created independent Menu 3; preserved original Menu 3 panel and Menu 18; Pinyin playback removed.')

#!/usr/bin/env python3
"""Apply the verified Menu 18 Pinyin ranking patch to the deploy artifact only.

The source index.html is intentionally left untouched by this overlay because
it is a very large embedded-dictionary file. The exact transformations are
version-controlled here and are applied deterministically during Pages build.
"""
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: patch_menu18_ranking.py <site/index.html>")

target = Path(sys.argv[1])
if not target.is_file():
    raise SystemExit(f"Menu 18 patch target not found: {target}")

source = target.read_text(encoding="utf-8")
original = source
changes = []

def replace_once(old: str, new: str, label: str) -> None:
    global source
    count = source.count(old)
    if count == 1:
        source = source.replace(old, new, 1)
        changes.append(label)
        return
    if count == 0 and source.count(new) == 1:
        return  # Already patched; keep the build idempotent.
    raise SystemExit(f"Menu 18 patch aborted: expected exactly one {label}; found {count}")

# Add a common-character fallback for the third syllable in "san ge ren".
replace_once(
    "shi:'是',you:'有'",
    "shi:'是',san:'三',you:'有'",
    "san → 三 fallback"
)

# A preferred word may have a valid dictionary row with no Vietnamese gloss.
# Keep the verified phrase gloss available to both direct lookup and sentence DP.
words_start = source.find("const PINYIN18_COMMON_WORDS={")
words_end_marker = "\n};\nlet pinyin18IndexSource"
words_end = source.find(words_end_marker, words_start)
if words_start < 0 or words_end < 0:
    raise SystemExit("Menu 18 patch aborted: preferred-word dictionary block not found.")

new_words = """const PINYIN18_COMMON_WORDS={
 'jin tian':['今天','jīn tiān','hôm nay'],'ming tian':['明天','míng tiān','ngày mai'],'zuo tian':['昨天','zuó tiān','hôm qua'],'tian qi':['天气','tiān qì','thời tiết'],
 'peng you':['朋友','péng you','bạn bè'],'zhong guo':['中国','zhōng guó','Trung Quốc'],'xue xi':['学习','xué xí','học tập'],'xue xiao':['学校','xué xiào','trường học'],'xue sheng':['学生','xué sheng','học sinh'],
 'lao shi':['老师','lǎo shī','giáo viên'],'gong zuo':['工作','gōng zuò','công việc'],'chi fan':['吃饭','chī fàn','ăn cơm'],'he shui':['喝水','hē shuǐ','uống nước'],'ke ren':['客人','kè rén','khách'],
 'shen me':['什么','shén me','cái gì'],'zen me':['怎么','zěn me','thế nào'],'xian zai':['现在','xiàn zài','bây giờ'],'zai jian':['再见','zài jiàn','tạm biệt'],'xie xie':['谢谢','xiè xie','cảm ơn'],
 'dui bu qi':['对不起','duì bu qǐ','xin lỗi'],'mei guan xi':['没关系','méi guān xi','không sao'],'bu ke qi':['不客气','bú kè qi','không có gì'],
 'ni hao':['你好','nǐ hǎo','xin chào'],'ni hao ma':['你好吗','nǐ hǎo ma','bạn khỏe không?'],'bu zhi dao':['不知道','bù zhī dào','không biết'],'wo bu zhi dao':['我不知道','wǒ bù zhī dào','tôi không biết'],
 'xi huan':['喜欢','xǐ huan','thích'],'jia li':['家里','jiā lǐ','trong nhà'],'hui jia':['回家','huí jiā','về nhà'],'shang ke':['上课','shàng kè','vào học'],'xia ke':['下课','xià kè','tan học'],
 'duo shao qian':['多少钱','duō shao qián','bao nhiêu tiền'],'qing wen':['请问','qǐng wèn','xin hỏi'],'yi dian':['一点','yì diǎn','một chút'],'you yi dian':['有一点','yǒu yì diǎn','có một chút'],
 'san ge ren':['三个人','sān ge rén','ba người'],'zhong wen':['中文','zhōng wén','tiếng Trung']
};"""
old_words = source[words_start:words_end + 3]
if old_words != new_words:
    if old_words.count("const PINYIN18_COMMON_WORDS={") != 1:
        raise SystemExit("Menu 18 patch aborted: preferred-word block is ambiguous.")
    source = source[:words_start] + new_words + source[words_end + 3:]
    changes.append("preferred words and offline Vietnamese glosses")

replace_once(
    "  const rawMeaning=String(candidate.vi||'').split(/[;；]/)[0].replace(/^[\\s·,，;:：-]+/,'').trim();",
    "  const rawMeaning=String(candidate.preferredMeaning||candidate.vi||'').split(/[;；]/)[0].replace(/^[\\s·,，;:：-]+/,'').trim();",
    "preferred Vietnamese gloss selection"
)

replace_once(
    """  const matches=index.get(key),existing=matches.findIndex(item=>item.row[0]===zh);
  const item=existing>=0?matches.splice(existing,1)[0]:{row:[zh,zh,pronunciation,''],rowIndex:rows.length+syllables.size};
  item.preferredWord=true;matches.unshift(item);""",
    """  const matches=index.get(key),existing=matches.findIndex(item=>item.row[0]===zh),meaning=String(entry[2]||'').trim();
  const item=existing>=0?matches.splice(existing,1)[0]:{row:[zh,zh,pronunciation,meaning],rowIndex:rows.length+syllables.size};
  item.preferredWord=true;item.preferredMeaning=meaning||item.preferredMeaning||String(item.row[3]||'');
  if(meaning&&!String(item.row[3]||'').trim())item.row=[item.row[0],item.row[1],item.row[2],meaning];
  matches.unshift(item);""",
    "preferred gloss storage"
)

replace_once(
    "  addCandidate({zh:item.row[0],trad:item.row[1],py:item.row[2],vi:item.row[3],source:'Từ điển hiện có'},150+Math.min([...String(item.row[0]||'')].length,8)-Math.log(item.rowIndex+1)*.01);",
    "addCandidate({zh:item.row[0],trad:item.row[1],py:item.row[2],vi:item.preferredMeaning||item.row[3],preferredMeaning:item.preferredMeaning,source:'Từ điển hiện có'},150+Math.min([...String(item.row[0]||'')].length,8)-Math.log(item.rowIndex+1)*.01+(item.preferredWord?500:0));",
    "preferred-word ranking"
)

replace_once(
    """       const commonCharBoost=PINYIN18_COMMON_CHARACTERS[syllable]===item.row[0]?5:0;
       const commonWordBoost=PINYIN18_COMMON_WORDS[syllable]?.[0]===item.row[0]?22:0;""",
    """const commonCharBoost=PINYIN18_COMMON_CHARACTERS[syllable]===item.row[0]?15:0;
       const commonWordBoost=PINYIN18_COMMON_WORDS[syllable]?.[0]===item.row[0]?50:0;""",
    "contextual sentence scoring"
)

required = [
    "'ke ren':['客人','kè rén','khách']",
    "'tian qi':['天气','tiān qì','thời tiết']",
    "'xian zai':['现在','xiàn zài','bây giờ']",
    "'ming tian':['明天','míng tiān','ngày mai']",
    "'shen me':['什么','shén me','cái gì']",
    "'san ge ren':['三个人','sān ge rén','ba người']",
    "'zhong wen':['中文','zhōng wén','tiếng Trung']",
    "item.preferredMeaning=meaning",
    "item.preferredWord?500:0",
    "commonWordBoost=PINYIN18_COMMON_WORDS[syllable]?.[0]===item.row[0]?50:0"
]
missing = [needle for needle in required if needle not in source]
if missing:
    raise SystemExit("Menu 18 patch verification failed; missing: " + ", ".join(missing))

if source != original:
    target.write_text(source, encoding="utf-8", newline="\n")

print("Menu 18 ranking patch: verified")
print("Updated: " + (", ".join(changes) if changes else "already current"))
print("Required regression phrases/glosses: 7/7 present")

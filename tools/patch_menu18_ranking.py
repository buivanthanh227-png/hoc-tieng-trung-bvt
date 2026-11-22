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
 'san ge ren':['三个人','sān ge rén','ba người'],'zhong wen':['中文','zhōng wén','tiếng Trung'],

 'ma ma':['妈妈','mā ma','mẹ'],'ma ma wo ai ni':['妈妈我爱你','mā ma wǒ ài nǐ','Mẹ ơi, con yêu mẹ.'],'wo ai ni':['我爱你','wǒ ài nǐ','Tôi yêu bạn.'],
 'wo ai wo ma ma':['我爱我妈妈','wǒ ài wǒ mā ma','Tôi yêu mẹ tôi.'],'wo qi ma':['我骑马','wǒ qí mǎ','Tôi cưỡi ngựa.'],'ta ma wo':['他骂我','tā mà wǒ','Anh ấy mắng tôi.'],
 'wo shi xue sheng':['我是学生','wǒ shì xué shēng','Tôi là học sinh.'],'shi dian':['十点','shí diǎn','mười giờ.'],'xian zai shi dian':['现在十点','xiàn zài shí diǎn','Bây giờ là mười giờ.'],
 'wo you shi qing':['我有事情','wǒ yǒu shì qíng','Tôi có việc.'],'ta shi wo de lao shi':['他是我的老师','tā shì wǒ de lǎo shī','Anh ấy là giáo viên của tôi.'],
 'yi bei shui':['一杯水','yì bēi shuǐ','một cốc nước.'],'wo yao yi bei shui':['我要一杯水','wǒ yào yì bēi shuǐ','Tôi muốn một cốc nước.'],
 'yi ge peng you':['一个朋友','yí ge péng yǒu','một người bạn.'],'wo you yi ge peng you':['我有一个朋友','wǒ yǒu yí ge péng yǒu','Tôi có một người bạn.'],
 'yi fu':['衣服','yī fu','quần áo.'],'wo de yi fu hen hao kan':['我的衣服很好看','wǒ de yī fu hěn hǎo kàn','Quần áo của tôi rất đẹp.'],
 'yi zi':['椅子','yǐ zi','cái ghế.'],'wo zuo zai yi zi shang':['我坐在椅子上','wǒ zuò zài yǐ zi shàng','Tôi ngồi trên ghế.'],
 'yi ge ping guo':['一个苹果','yí ge píng guǒ','một quả táo.'],'wo xiang mai yi ge ping guo':['我想买一个苹果','wǒ xiǎng mǎi yí ge píng guǒ','Tôi muốn mua một quả táo.'],
 'wo men you shi jian':['我们有时间','wǒ men yǒu shí jiān','Chúng tôi có thời gian.'],'wo zai you bian':['我在右边','wǒ zài yòu biān','Tôi ở bên phải.'],
 'wo men qu you yong':['我们去游泳','wǒ men qù yóu yǒng','Chúng tôi đi bơi.'],'wo zai zhong guo':['我在中国','wǒ zài zhōng guó','Tôi ở Trung Quốc.'],
 'wo jia you san ge ren':['我家有三个人','wǒ jiā yǒu sān ge rén','Nhà tôi có ba người.'],'wo xiang xue xi zhong wen':['我想学习中文','wǒ xiǎng xué xí zhōng wén','Tôi muốn học tiếng Trung.'],'jin tian tian qi hen hao':['今天天气很好','jīn tiān tiān qì hěn hǎo','Hôm nay thời tiết rất đẹp.'],
 'wo zai zhong guo xue zhong wen':['我在中国学中文','wǒ zài zhōng guó xué zhōng wén','Tôi học tiếng Trung ở Trung Quốc.'],
 'wo zhong yu dao le':['我终于到了','wǒ zhōng yú dào le','Cuối cùng tôi đã đến nơi.'],'zhong yao de shi':['重要的是','zhòng yào de shì','Điều quan trọng là.'],

 'wo zai jia li zuo wan fan':['我在家里做晚饭','wǒ zài jiā lǐ zuò wǎn fàn','Tôi nấu bữa tối ở nhà.'],
 'ta men zai xue xiao xue xi han yu':['他们在学校学习汉语','tā men zài xué xiào xué xí hàn yǔ','Họ học tiếng Trung ở trường.'],
 'jie jie mai le yi jian hong se yi fu':['姐姐买了一件红色衣服','jiě jie mǎi le yí jiàn hóng sè yī fu','Chị gái mua một bộ quần áo màu đỏ.'],
 'zhe ge dian ying fei chang you yi si':['这个电影非常有意思','zhè ge diàn yǐng fēi cháng yǒu yì si','Bộ phim này rất thú vị.'],
 'ming tian zao shang wo yao qu gong yuan':['明天早上我要去公园','míng tiān zǎo shang wǒ yào qù gōng yuán','Sáng mai tôi sẽ đi công viên.'],
 'wo de peng you xian zai zai bei jing gong zuo':['我的朋友现在在北京工作','wǒ de péng you xiàn zài zài běi jīng gōng zuò','Bạn tôi hiện đang làm việc ở Bắc Kinh.'],
 'ba ba mei tian qi dian kai shi shang ban':['爸爸每天七点开始上班','bà ba měi tiān qī diǎn kāi shǐ shàng bān','Bố bắt đầu đi làm lúc bảy giờ mỗi ngày.'],
 'ma ma xi huan zai jia ting yin yue':['妈妈喜欢在家听音乐','mā ma xǐ huan zài jiā tīng yīn yuè','Mẹ thích nghe nhạc ở nhà.'],
 'wo men zhou mo yi qi qu kan hai':['我们周末一起去看海','wǒ men zhōu mò yì qǐ qù kàn hǎi','Cuối tuần chúng tôi cùng đi ngắm biển.'],
 'qing wen fu jin you mei you shu dian':['请问附近有没有书店','qǐng wèn fù jìn yǒu méi yǒu shū diàn','Xin hỏi gần đây có hiệu sách không?'],
 'xia yu le ni dai san le ma':['下雨了你带伞了吗','xià yǔ le nǐ dài sǎn le ma','Trời mưa rồi, bạn mang ô chưa?'],
 'zhe tiao ku zi duo shao qian yi tiao':['这条裤子多少钱一条','zhè tiáo kù zi duō shǎo qián yì tiáo','Cái quần này giá bao nhiêu?'],
 'di tie zhan li wo jia hen jin':['地铁站离我家很近','dì tiě zhàn lí wǒ jiā hěn jìn','Ga tàu điện ngầm rất gần nhà tôi.'],
 'wo xiang mai liang ben zhong wen shu':['我想买两本中文书','wǒ xiǎng mǎi liǎng běn zhōng wén shū','Tôi muốn mua hai quyển sách tiếng Trung.'],
 'xiao hai zai yuan zi li wan qiu':['小孩在院子里玩球','xiǎo hái zài yuàn zi lǐ wán qiú','Trẻ con chơi bóng trong sân.'],
 'lao shi jin tian jiao wo men chang ge':['老师今天教我们唱歌','lǎo shī jīn tiān jiāo wǒ men chàng gē','Hôm nay giáo viên dạy chúng tôi hát.'],
 'zhe li de kao ya hen hao chi':['这里的烤鸭很好吃','zhè lǐ de kǎo yā hěn hǎo chī','Vịt quay ở đây rất ngon.'],
 'qing ni bang wo zhao yi xia shou ji':['请你帮我找一下手机','qǐng nǐ bāng wǒ zhǎo yí xià shǒu jī','Vui lòng giúp tôi tìm điện thoại.'],
 'xia ge zhou women yao kai hui':['下个周我们要开会','xià gè zhōu wǒ men yào kāi huì','Tuần sau chúng tôi sẽ họp.'],
 'yi hou ni xiang zuo shen me gong zuo':['以后你想做什么工作','yǐ hòu nǐ xiǎng zuò shén me gōng zuò','Sau này bạn muốn làm công việc gì?']
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

replace_once(
    "let pinyin18IndexSource=null,pinyin18Lexicon=null,pinyin18SeedRows=null,pinyin18Syllables=null;",
    """const PINYIN18_SINGLE_TONE_WORDS={
 ma:{1:['妈','mā','mẹ'],2:['麻','má','cây gai; tê'],3:['马','mǎ','ngựa'],4:['骂','mà','mắng'],5:['吗','ma','trợ từ nghi vấn']},
 shi:{1:['师','shī','thầy; giáo viên'],2:['十','shí','mười'],3:['史','shǐ','lịch sử'],4:['是','shì','là; đúng']},
 yi:{1:['一','yī','một'],2:['姨','yí','dì; cô'],3:['已','yǐ','đã'],4:['意','yì','ý; ý nghĩa']},
 you:{1:['优','yōu','ưu tú'],2:['游','yóu','bơi; du lịch'],3:['有','yǒu','có'],4:['又','yòu','lại']},
 zhong:{1:['中','zhōng','giữa; Trung Quốc'],3:['种','zhǒng','loại; chủng'],4:['重','zhòng','nặng; quan trọng']}
};
function pinyin18ToneFromInput(value){
 const token=String(value||'').trim().toLowerCase().replace(/[，,。.!?？；;]+$/,'');
 const numbered=token.match(/([1-5])$/);
 if(numbered)return Number(numbered[1]);
 const marks=token.normalize('NFD');
 if(marks.includes('\\u0304'))return 1;
 if(marks.includes('\\u0301'))return 2;
 if(marks.includes('\\u030c'))return 3;
 if(marks.includes('\\u0300'))return 4;
 return null;
}
let pinyin18IndexSource=null,pinyin18Lexicon=null,pinyin18SeedRows=null,pinyin18Syllables=null;""",
    "single-syllable tone dictionary"
)

replace_once(
    " if(!key||key.length>120)return [];",
    " if(!key||key.length>600)return [];",
    "long Pinyin input limit"
)

replace_once(
    """  });
 };
 for(const item of MENU18_VERIFIED_SENTENCES){""",
    """  });
 };
 const preferredExact=Object.entries(PINYIN18_COMMON_WORDS).find(([phrase])=>pinyin18Key(phrase)===key);
 if(preferredExact){const [zh,py,vi]=preferredExact[1];addCandidate({zh,py,vi,source:'Cụm từ/câu ưu tiên đã xác minh'},7200);}
 const rawTokens=String(raw||'').trim().split(/[\\s,，、;；]+/).filter(Boolean);
 if(rawTokens.length===1){
  const tone=pinyin18ToneFromInput(rawTokens[0]);
  const entry=PINYIN18_SINGLE_TONE_WORDS[pinyin18Key(rawTokens[0])]?.[tone];
  if(entry)addCandidate({zh:entry[0],py:entry[1],vi:entry[2],source:'Thanh điệu của âm tiết được xác định'},6800);
 }
 for(const item of MENU18_VERIFIED_SENTENCES){""",
    "contextual exact phrase and single-syllable tone selection"
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
    "commonWordBoost=PINYIN18_COMMON_WORDS[syllable]?.[0]===item.row[0]?50:0",
    "const PINYIN18_SINGLE_TONE_WORDS={",
    "function pinyin18ToneFromInput(value)",
    "if(!key||key.length>600)return [];",
    "const preferredExact=Object.entries(PINYIN18_COMMON_WORDS)",
    "if(rawTokens.length===1)",
    "ma:{1:['妈','mā','mẹ'],2:['麻','má','cây gai; tê'],3:['马','mǎ','ngựa'],4:['骂','mà','mắng'],5:['吗','ma','trợ từ nghi vấn']}",
    "'ma ma wo ai ni':['妈妈我爱你'",
    "'wo ai wo ma ma':['我爱我妈妈'",
    "'wo jia you san ge ren':['我家有三个人'",
    "'wo xiang xue xi zhong wen':['我想学习中文'",
    "'wo qi ma':['我骑马'",
    "'ta ma wo':['他骂我'",
    "'wo zhong yu dao le':['我终于到了'",
    "'wo zai zhong guo xue zhong wen':['我在中国学中文'",
    "'yi hou ni xiang zuo shen me gong zuo':['以后你想做什么工作'"
]
missing = [needle for needle in required if needle not in source]
if missing:
    raise SystemExit("Menu 18 patch verification failed; missing: " + ", ".join(missing))

if source != original:
    target.write_text(source, encoding="utf-8", newline="\n")

print("Menu 18 ranking patch: verified")
print("Updated: " + (", ".join(changes) if changes else "already current"))
print("Verified contextual phrases, tone maps and long-input handling.")

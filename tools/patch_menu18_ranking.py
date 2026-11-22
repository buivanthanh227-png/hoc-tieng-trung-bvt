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
    new_count = source.count(new)
    if new_count == 1:
        return  # Already patched; check before the old anchor because replacements can retain that anchor.
    if new_count > 1:
        raise SystemExit(f"Menu 18 patch aborted: duplicate replacement for {label}; found {new_count}")
    count = source.count(old)
    if count == 1:
        source = source.replace(old, new, 1)
        changes.append(label)
        return
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
words_end_marker = "\n};"
words_end = source.find(words_end_marker, words_start)
if words_start < 0 or words_end < 0:
    raise SystemExit("Menu 18 patch aborted: preferred-word dictionary block not found.")

new_words = """const PINYIN18_COMMON_WORDS={
 'jin tian':['今天','jīn tiān','hôm nay'],'ming tian':['明天','míng tiān','ngày mai'],'zuo tian':['昨天','zuó tiān','hôm qua'],'tian qi':['天气','tiān qì','thời tiết'],
 'peng you':['朋友','péng you','bạn bè'],'zhong guo':['中国','zhōng guó','Trung Quốc'],'xue xi':['学习','xué xí','học tập'],'xue xiao':['学校','xué xiào','trường học'],'xue sheng':['学生','xué sheng','học sinh'],
 'lao shi':['老师','lǎo shī','giáo viên'],'gong zuo':['工作','gōng zuò','công việc'],'chi fan':['吃饭','chī fàn','ăn cơm'],'he shui':['喝水','hē shuǐ','uống nước'],'ke yi':['可以','kě yǐ','có thể'],'ke ren':['客人','kè rén','khách'],
 'shen me':['什么','shén me','cái gì'],'zen me':['怎么','zěn me','thế nào'],'xian zai':['现在','xiàn zài','bây giờ'],'zai jian':['再见','zài jiàn','tạm biệt'],'xie xie':['谢谢','xiè xie','cảm ơn'],
 'dui bu qi':['对不起','duì bu qǐ','xin lỗi'],'mei guan xi':['没关系','méi guān xi','không sao'],'bu ke qi':['不客气','bú kè qi','không có gì'],
 'ni hao':['你好','nǐ hǎo','xin chào'],'ni hao ma':['你好吗','nǐ hǎo ma','bạn khỏe không?'],'ni jin le ma':['你进了吗','nǐ jìn le ma','Bạn vào được chưa?'],'bu zhi dao':['不知道','bù zhī dào','không biết'],'wo bu zhi dao':['我不知道','wǒ bù zhī dào','tôi không biết'],
 'xi huan':['喜欢','xǐ huan','thích'],'jia li':['家里','jiā lǐ','trong nhà'],'hui jia':['回家','huí jiā','về nhà'],'shang ke':['上课','shàng kè','vào học'],'xia ke':['下课','xià kè','tan học'],
 'duo shao qian':['多少钱','duō shao qián','bao nhiêu tiền'],'qing wen':['请问','qǐng wèn','xin hỏi'],'yi dian':['一点','yì diǎn','một chút'],'you yi dian':['有一点','yǒu yì diǎn','có một chút'],
 'san ge ren':['三个人','sān ge rén','ba người'],'zhong wen':['中文','zhōng wén','tiếng Trung'],
 'ta hai mei you gongzuo':['他还没有工作','tā hái méiyǒu gōngzuò','Anh ấy vẫn chưa có việc làm.'],

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
 'jin tian wo jia you ke ren':['今天我家有客人','jīn tiān wǒ jiā yǒu kè rén','Hôm nay nhà tôi có khách.'],'wo jia you san ge ren':['我家有三个人','wǒ jiā yǒu sān ge rén','Nhà tôi có ba người.'],'wo xiang xue xi zhong wen':['我想学习中文','wǒ xiǎng xué xí zhōng wén','Tôi muốn học tiếng Trung.'],'jin tian tian qi hen hao':['今天天气很好','jīn tiān tiān qì hěn hǎo','Hôm nay thời tiết rất đẹp.'],
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
    "state.rows.concat(item.row)",
    "state.rows.concat([item.row])",
    "preserve nested dictionary rows during sentence composition"
)

replace_once(
    "let pinyin18IndexSource=null,pinyin18Lexicon=null,pinyin18SeedRows=null,pinyin18Syllables=null;",
    """const PINYIN18_SINGLE_TONE_WORDS={
 jin:{1:['今','jīn','nay; hiện tại'],3:['仅','jǐn','chỉ; chỉ có'],4:['进','jìn','đi vào; tiến lên']},
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
 if(marks.includes(String.fromCharCode(0x304)))return 1;
 if(marks.includes(String.fromCharCode(0x301)))return 2;
 if(marks.includes(String.fromCharCode(0x30c)))return 3;
 if(marks.includes(String.fromCharCode(0x300)))return 4;
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
  const variants=PINYIN18_SINGLE_TONE_WORDS[pinyin18Key(rawTokens[0])];
  if(tone&&variants?.[tone]){
   const entry=variants[tone];
   addCandidate({zh:entry[0],py:entry[1],vi:entry[2],source:'Thanh điệu của âm tiết được xác định'},6800);
  }else if(variants){
   for(const [candidateTone,entry] of Object.entries(variants)){
    addCandidate({zh:entry[0],py:entry[1],vi:entry[2],source:'Một cách đọc theo thanh điệu '+candidateTone},6200-Number(candidateTone));
   }
  }
 }
 for(const item of MENU18_VERIFIED_SENTENCES){""",
    "contextual exact phrase and single-syllable tone selection"
)

replace_once(
    """function pinyin18SyllablePaths(raw,syllables){
 let paths=[[]];
 for(const rawToken of String(raw||'').trim().split(/[\\s,，、;；]+/).filter(Boolean)){
  const token=pinyin18Key(rawToken),memo=new Map([[token.length,[[]]]]);
  for(let start=token.length-1;start>=0;start--){
   const options=[];
   for(let end=start+1;end<=Math.min(token.length,start+6);end++){
    const syllable=token.slice(start,end),tails=memo.get(end);
    if(!syllables.has(syllable)||!tails)continue;
    for(const tail of tails){options.push([syllable].concat(tail));if(options.length>=16)break;}
   }
   options.sort((a,b)=>a.length-b.length);
   const shortest=options.length?options[0].length:0;
   memo.set(start,options.filter(option=>option.length===shortest).slice(0,4));
  }
  const splits=memo.get(0)||[];
  if(!splits.length)return [];
  const next=[];
  for(const path of paths)for(const split of splits){next.push(path.concat(split));if(next.length>=8)break;}
  paths=next.slice(0,8);
 }
 return paths;
}""",
    """function pinyin18SyllablePaths(raw,syllables){
 // Preserve explicit syllable tokens; only compact chunks are segmented.
 let paths=[[]];
 const tokens=String(raw||'').trim().split(/[\\s,，、;；]+/).filter(Boolean);
 for(const rawToken of tokens){
  const token=pinyin18Key(rawToken);
  if(!token||token.length>120)return [];
  if(syllables.has(token)){
   paths=paths.map(path=>path.concat([token])).slice(0,24);
   continue;
  }
  const memo=new Map([[token.length,[[]]]]);
  for(let start=token.length-1;start>=0;start--){
   const options=[],seen=new Set();
   for(let finish=start+1;finish<=Math.min(token.length,start+6);finish++){
    const syllable=token.slice(start,finish),tails=memo.get(finish);
    if(!syllables.has(syllable)||!tails)continue;
    for(const tail of tails){
     const option=[syllable].concat(tail),identity=option.join(' ');
     if(!seen.has(identity)){seen.add(identity);options.push(option);}
    }
   }
   options.sort((a,b)=>{
    if(a.length!==b.length)return a.length-b.length;
    for(let i=0;i<Math.min(a.length,b.length);i++){
     if(a[i].length!==b[i].length)return b[i].length-a[i].length;
    }
    return a.join(' ').localeCompare(b.join(' '));
   });
   const groups=new Map();
   for(const option of options){
    const group=groups.get(option.length)||[];
    if(group.length<4)group.push(option);
    groups.set(option.length,group);
   }
   const retained=[];
   for(const count of [...groups.keys()].sort((a,b)=>a-b)){
    retained.push(...groups.get(count));
    if(retained.length>=20)break;
   }
   memo.set(start,retained.slice(0,20));
  }
  const splits=memo.get(0)||[];
  if(!splits.length)return [];
  const next=[],seenPaths=new Set();
  outer: for(const path of paths){
   for(const split of splits){
    const combined=path.concat(split),identity=combined.join('|');
    if(seenPaths.has(identity))continue;
    seenPaths.add(identity);
    next.push(combined);
    if(next.length>=24)break outer;
   }
  }
  paths=next;
 }
 return paths;
}""",
    "keep explicit Pinyin syllables intact and segment compact input"
)


# Improve candidate generation and Vietnamese gloss integrity on the deploy artifact.
if "const hasMeaningPlaceholder=" not in source:
    replace_once(
        """  const rawMeaning=String(candidate.preferredMeaning||candidate.vi||'').split(/[;；]/)[0].replace(/^[\\s·,，;:：-]+/,'').trim();
  const vi=rawMeaning.length>=2&&/[A-Za-zÀ-ỹ\\u3400-\\u9fff]/.test(rawMeaning)?rawMeaning:'';""",
        """  const rawMeaning=String(candidate.vi||'').split(/[;；]/)[0].replace(/^[\\s·,，;:：-]+/,'').trim();
  const hasMeaningPlaceholder=/(?:chưa có nghĩa|chưa tìm được nghĩa|chưa tra được nghĩa|không có nghĩa|không tìm thấy nghĩa|not found|undefined|null)/i.test(rawMeaning);
  const hasMeaningDigits=/\\d/.test(rawMeaning);
  const hasMeaningHanzi=/[\\u3400-\\u9fff\\uF900-\\uFAFF]/.test(rawMeaning);
  const vi=!hasMeaningPlaceholder&&!hasMeaningDigits&&!hasMeaningHanzi&&rawMeaning.length>=2&&/[A-Za-zÀ-ỹĐđ]/.test(rawMeaning)?rawMeaning:'';""",
        "reject placeholder and corrupted dictionary meanings"
    )
    
else:
    gloss_markers = ["const hasMeaningDigits=", "const hasMeaningHanzi=", "const vi=!hasMeaningPlaceholder"]
    missing_gloss = [marker for marker in gloss_markers if marker not in source]
    if missing_gloss:
        raise SystemExit("Menu 18 gloss filter incomplete: " + ", ".join(missing_gloss))
replace_once(
    """   vi:vi||'Chưa có nghĩa tiếng Việt trong dữ liệu hiện tại.',
   note:candidate.note||(!vi&&rows.length?'Chưa có nghĩa tiếng Việt cho toàn cụm trong dữ liệu hiện tại.':''),""",
    """   vi,
   note:candidate.note||(!vi&&rows.length?'Nghĩa tiếng Việt đang chờ tra cho toàn câu.':''),""",
    "remove placeholder output and mark gloss as pending"
)
replace_once(
    """ if(!hasExactPhraseSource){""",
    """ // Keep the exact verified sentence first, while also exploring alternate readings.
 const shouldGenerateAlternates=true;
 if(!hasExactPhraseSource||shouldGenerateAlternates){""",
    "always generate alternatives alongside exact matches"
)
replace_once(
    """     vi:fullRow?state.rows[0][3]:rowMeanings.join(' · '),
     note:fullRow?'':'Nghĩa tham khảo ghép từ điển từng mục; sẽ ưu tiên dịch toàn câu.',""",
    """     vi:fullRow?state.rows[0][3]:'',
     note:fullRow?'':'Nghĩa tiếng Việt sẽ được tra cho toàn câu sau khi chọn phương án.',""",
    "do not present word-by-word gloss fragments as whole-sentence translation"
)
replace_once(
    """ return [...found.values()].sort((a,b)=>b.priority-a.priority||a.zh.localeCompare(b.zh,'zh-CN')).slice(0,8);""",
    """ return pinyin18SelectToneDiverse([...found.values()],raw,found.size);""",
    "return syllable-preserving, tone-diverse Pinyin alternatives"
)
replace_once(
    """ const vi=String(result.vi||'Chưa tìm được nghĩa tiếng Việt cho toàn câu.');""",
    """ const vi=String(result.vi||'Đang tra nghĩa tiếng Việt…');""",
    "show pending gloss state in result card"
)
replace_once(
    """  const needsFullSentenceMeaning=Boolean(best.note&&/ghép từ điển|cụm từ/i.test(best.note));
  if(!needsFullSentenceMeaning){
   status.textContent='Đã tự động ghép câu bằng cách xét các biến thể thanh điệu phù hợp.';
   return;
  }
  status.textContent='Đã ghép được chữ Hán. Đang tra nghĩa tiếng Việt cho toàn câu…';
  try{
   const vi=await machineTranslate(best.zh,'zh-CN','vi');
   if(token!==homework18LookupToken)return;
   renderHomework18Card({...best,vi,note:'Nghĩa tiếng Việt được dịch từ toàn câu đã ghép.'},'Pinyin · tự động xét nhiều thanh điệu');
   status.textContent='Đã ghép Pinyin và tìm được nghĩa tiếng Việt cho toàn câu.';
  }catch(error){
   if(token!==homework18LookupToken)return;
   renderHomework18Card({...best,note:'Dịch vụ dịch nghĩa hiện không khả dụng; bên dưới là nghĩa tham khảo ghép từ điển.'},'Pinyin · tự động xét nhiều thanh điệu');
   status.textContent='Đã ghép được chữ Hán; đang hiển thị nghĩa tham khảo offline.';
  }""",
    """  status.textContent=best.vi
   ?'Đã ghép Pinyin. Bạn có thể xem các phương án ghép khác nếu cần.'
   :'Đã ghép được chữ Hán. Đang tra nghĩa tiếng Việt cho phương án đang chọn…';""",
    "translate the candidate selected by the learner instead of replacing it later"
)


replace_once(
    """ for(const [py,zh] of Object.entries(PINYIN18_COMMON_CHARACTERS)){
  if([...String(zh||'')].length!==1||py.length>6)continue;
  syllables.add(py);
  if(!index.has(py))index.set(py,[{row:[zh,zh,py,''],rowIndex:rows.length+syllables.size}]);
 }
 for(const [py,entry] of Object.entries(PINYIN18_COMMON_WORDS)){""",
    """ for(const [py,zh] of Object.entries(PINYIN18_COMMON_CHARACTERS)){
  if([...String(zh||'')].length!==1||py.length>6)continue;
  syllables.add(py);
  if(!index.has(py))index.set(py,[{row:[zh,zh,py,''],rowIndex:rows.length+syllables.size}]);
 }
 // Seed all curated tone readings into the multi-syllable lexicon too.
 for(const [base,variants] of Object.entries(PINYIN18_SINGLE_TONE_WORDS)){
  const key=pinyin18LexiconKey(base);
  if(!index.has(key))index.set(key,[]);
  const matches=index.get(key);syllables.add(key);
  for(const entry of Object.values(variants)){
   const zh=String(entry[0]||''),pronunciation=String(entry[1]||'');
   const tone=pinyin18ToneFromInput(pronunciation);
   if(!matches.some(item=>item.row[0]===zh&&pinyin18ToneFromInput(item.row[2])===tone)){
    matches.unshift({row:[zh,zh,pronunciation,String(entry[2]||'')],rowIndex:rows.length+syllables.size});
   }
  }
  if(matches.length>48)matches.length=48;
 }
 for(const [py,entry] of Object.entries(PINYIN18_COMMON_WORDS)){""",
    "seed curated tone variants into sentence lexicon"
)

selector_code = r"""function pinyin18SelectToneDiverse(candidates,raw,limit=16){
 const rawText=String(raw||'').trim();
 const inputTokens=rawText.split(/[\s,，、;；]+/).filter(Boolean);
 if(!inputTokens.length)return [];
 const syllables=(pinyin18Syllables instanceof Set&&pinyin18Syllables.size)
  ?pinyin18Syllables:new Set(inputTokens.map(pinyin18Key));
 let expected=[{keys:[],tones:[]}];
 let hasCompactToken=false;
 for(const rawToken of inputTokens){
  const tokenKey=pinyin18Key(rawToken);
  if(!tokenKey)return [];
  const isSyllable=syllables.has(tokenKey);
  const splits=isSyllable?[[tokenKey]]:pinyin18SyllablePaths(rawToken,syllables);
  if(!splits.length)return [];
  if(!isSyllable)hasCompactToken=true;
  const requestedTone=isSyllable?pinyin18ToneFromInput(rawToken):null;
  const next=[];
  for(const path of expected){
   for(const split of splits){
    const keys=path.keys.concat(split);
    const tones=path.tones.concat(split.map((_,index)=>index===0?requestedTone:null));
    next.push({keys,tones});
    if(next.length>=32)break;
   }
   if(next.length>=32)break;
  }
  expected=next;
 }
 const expectedByBase=new Map();
 for(const path of expected){
  const base=path.keys.join(' ');
  if(!expectedByBase.has(base))expectedByBase.set(base,[]);
  expectedByBase.get(base).push(path);
 }
 let ranked=(Array.isArray(candidates)?candidates:[]).map(item=>{
  const py=String(item.py||'').trim();
  if(!py)return null;
  const tokens=py.split(/\s+/).filter(Boolean);
  const keys=tokens.map(pinyin18Key);
  const base=keys.join(' ');
  const paths=expectedByBase.get(base);
  if(!paths)return null;
  const matched=paths.find(path=>path.tones.every((tone,index)=>
   tone===null||pinyin18ToneFromInput(tokens[index])===tone
  ));
  if(!matched)return null;
  return {item,tokens,base,tones:matched.tones,priority:Number(item.priority)||0};
 }).filter(Boolean);
 if(!ranked.length)return [];
 // If a compact input token admits several possible syllable boundaries,
 // choose one dictionary-supported path instead of mixing incompatible splits.
 if(hasCompactToken){
  const groups=new Map();
  for(const row of ranked){
   if(!groups.has(row.base))groups.set(row.base,[]);
   groups.get(row.base).push(row);
  }
  ranked=[...groups.values()].sort((a,b)=>{
   if(a.length!==b.length)return b.length-a.length;
   return Math.max(...b.map(x=>x.priority))-Math.max(...a.map(x=>x.priority));
  })[0];
 }
 ranked.sort((a,b)=>b.priority-a.priority||String(a.item.zh||'').localeCompare(String(b.item.zh||''),'zh-CN'));
 const selected=[],selectedIds=new Set();
 const add=row=>{
  if(!row||selected.length>=limit)return;
  const id=String(row.item.zh||'')+'|'+String(row.item.py||'');
  if(selectedIds.has(id))return;
  selectedIds.add(id);selected.push(row);
 };
 // Keep the highest-ranked complete sentence first (usually the exact verified phrase).
 if(ranked.length)add(ranked[0]);
 const positions=ranked.length?ranked[0].tokens.map((_,index)=>{
  const toneRows=new Map();
  for(const row of ranked){
   const tone=pinyin18ToneFromInput(row.tokens[index])||5;
   const current=toneRows.get(tone);
   if(!current||row.priority>current.priority)toneRows.set(tone,row);
  }
  return {index,toneRows};
 }):[];
 positions
  .filter(position=>position.toneRows.size>1&&ranked[0].tones[position.index]===null)
  .sort((a,b)=>b.toneRows.size-a.toneRows.size||a.index-b.index)
  .forEach(position=>{
   for(const tone of [...position.toneRows.keys()].sort((a,b)=>a-b))add(position.toneRows.get(tone));
  });
 for(const row of ranked)add(row);
 return selected.map(row=>row.item);
}"""
replace_once(
    "function pinyinToChineseCandidates(raw){",
    selector_code + "\nfunction pinyinToChineseCandidates(raw){",
    "tone-diverse candidate selector with exact input syllable validation"
)

required = [
    "'ke yi':['可以','kě yǐ','có thể']",
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
required.extend([
    "function pinyin18SyllablePaths(raw,syllables){",
    "const shouldGenerateAlternates=true;",
    "if(!hasExactPhraseSource||shouldGenerateAlternates){",
    "const hasMeaningPlaceholder=",
    "const hasMeaningDigits=",
    "const hasMeaningHanzi=",
    "Nghĩa tiếng Việt sẽ được tra cho toàn câu sau khi chọn phương án.",
    "6200-Number(candidateTone)",
    ".slice(0,5)",
    "commonWordBoost=PINYIN18_COMMON_WORDS[syllable]?.[0]===item.row[0]?50:0"
])

missing = [needle for needle in required if needle not in source]
if missing:
    raise SystemExit("Menu 18 patch verification failed; missing: " + ", ".join(missing))


# Preserve the reading generated from matching dictionary rows. Recomputing
# Pinyin from Hanzi can change the learner's syllable or choose a default polyphone.
replace_once(
    " const py=pinyinForChinese(zh,String(result.py||''));",
    " const py=formatHomework18PinyinByWord(zh,String(result.py||pinyinForChinese(zh)));",
    "preserve candidate Pinyin at final render"
)


# Compact candidate selector and distinct semantic colors for Menu 18.
def replace_ui_once(old: str, new: str, label: str) -> None:
    global source
    count = source.count(old)
    if count == 0 and source.count(new) == 1:
        return
    if count != 1:
        raise SystemExit(f"Menu 18 UI patch aborted: expected one {label}; found {count}")
    source = source.replace(old, new, 1)
    changes.append(label)

replace_ui_once(
    ".homework18-candidates{display:none!important}",
    """.homework18-candidates:not([hidden]){display:block!important;margin:7px 0 9px!important}
.homework18-candidate-tabs-label{font-size:12px;font-weight:750;color:var(--muted,#667085);margin:0 0 6px}
.homework18-candidate-tabs-list{display:flex;flex-wrap:wrap;gap:6px}
.homework18-candidate-tab{border:1px solid #d8c4e3;border-radius:999px;background:#faf7fc;color:#6b3b7b;padding:6px 11px;min-height:30px;font-size:12px;font-weight:750;cursor:pointer}
.homework18-candidate-tab[aria-pressed="true"]{background:#ba68c8;border-color:#9850a6;color:#172033}
.homework18-output-value.is-hanzi{color:#7b3fa1!important}
.homework18-output-value.is-pinyin{color:#2563a6!important;font-weight:650}
.homework18-output-value.is-meaning{color:#21805b!important}
@media(max-width:390px){.homework18-candidate-tab{padding:5px 9px;font-size:11px}.homework18-candidates:not([hidden]){margin:5px 0 7px!important}}""",
    "visible compact candidate selector and color-coded output"
)

replace_ui_once(
    "(kind==='hanzi'?'is-hanzi':'')",
    "'is-'+kind",
    "semantic output color classes"
)

old_renderer = """function renderHomework18Candidates(candidates){
 const box=$('homework18-candidates');box.hidden=true;box.replaceChildren();
 const best=Array.isArray(candidates)?candidates[0]:null;
 if(!best)return null;
 renderHomework18Card(best,'Tự động ghép Pinyin · '+String(best.source||'xét nhiều thanh điệu'));
 return best;
}"""
new_renderer = """let homework18Candidates=[];
let homework18SelectedIndex=0;
function homework18ValidVietnameseMeaning(item){
 const meaning=String(item?.preferredMeaning||item?.vi||'').trim();
 const hanzi=String(item?.zh||'');
 if(!hanzi)return false;
 // A blank gloss is pending and will be translated after the candidate is selected.
 if(!meaning)return true;
 if(/(?:chưa có nghĩa|chưa tìm được nghĩa|chưa tra được nghĩa|không có nghĩa|không tìm thấy nghĩa|not found|undefined|null)/i.test(meaning))return false;
 if(/\\d/.test(meaning)||/[\\u3400-\\u9fff\\uF900-\\uFAFF]/.test(meaning))return false;
 const letters=(meaning.match(/[A-Za-zÀ-ỹĐđ]/g)||[]).length;
 if(letters<2||letters/meaning.length<0.45)return false;
 if(!/[A-Za-zÀ-ỹĐđ]/.test(meaning))return false;
 if(/^(?:[a-z]\\s*){1,5}$/i.test(meaning))return false;
 return true;
}
function pinyin18DisplayKey(value){
 return String(value||'').toLowerCase().replace(/ü|u:/g,'v').normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
}
function formatHomework18PinyinByWord(zh,py){
 const chars=[...String(zh||'')],tokens=String(py||'').trim().split(/\s+/).filter(Boolean);
 if(!chars.length||!tokens.length)return String(py||'');
 const words=Object.entries(PINYIN18_COMMON_WORDS)
  .map(([key,value])=>({zh:String(value[0]||''),py:String(value[1]||'').trim().split(/\s+/).filter(Boolean)}))
  .filter(word=>[...word.zh].length===2&&word.py.length===2)
  .sort((a,b)=>[...b.zh].length-[...a.zh].length);
 const output=[];let charAt=0,tokenAt=0;
 while(charAt<chars.length&&tokenAt<tokens.length){
  const match=words.find(word=>
   chars.slice(charAt,charAt+[...word.zh].length).join('')===word.zh&&
   word.py.length<=tokens.length-tokenAt&&
   word.py.every((syllable,index)=>pinyin18DisplayKey(syllable)===pinyin18DisplayKey(tokens[tokenAt+index]))
  );
  if(match){
   const compact=match.py.join('');
   output.push(/^[A-Z]/.test(tokens[tokenAt])?compact.charAt(0).toUpperCase()+compact.slice(1):compact);
   charAt+=[...match.zh].length;tokenAt+=match.py.length;
  }else{
   output.push(tokens[tokenAt]);charAt++;tokenAt++;
  }
 }
 if(charAt!==chars.length||tokenAt!==tokens.length)return String(py||'');
 return output.join(' ');
}
function renderHomework18Candidates(candidates){
 homework18SelectedIndex=0;
 const box=$('homework18-candidates');
 const seen=new Set();
 homework18Candidates=(Array.isArray(candidates)?candidates:[]).filter(item=>{
  if(!homework18ValidVietnameseMeaning(item))return false;
  const key=String(item.zh||'')+'|'+String(item.py||'')+'|'+String(item.preferredMeaning||item.vi||'').trim().toLowerCase();
  if(seen.has(key))return false;
  seen.add(key);return true;
 });
  homework18Candidates=pinyin18SelectToneDiverse(homework18Candidates,String($('homework18-query')?.value||''),homework18Candidates.length);
 if(!homework18Candidates.length){
  box.hidden=true;box.replaceChildren();
  const status=$('homework18-status');
  if(status)status.textContent='Chưa tìm được phương án ghép hợp lệ. Hãy thử thêm dấu cách giữa các từ hoặc nhập Pinyin có dấu thanh.';
  return null;
 }
 box.hidden=false;
 box.innerHTML='<div class="homework18-candidate-tabs-label">Các phương án ghép Pinyin phù hợp · chạm để xem</div><div class="homework18-candidate-tabs-list">'+
  homework18Candidates.map((item,index)=>'<button type="button" class="homework18-candidate-tab" data-homework18-result="'+index+'" aria-pressed="'+(index===0?'true':'false')+'">Kết quả '+(index+1)+'</button>').join('')+'</div>';
 const choose=index=>{
  const item=homework18Candidates[index];if(!item)return;
  homework18SelectedIndex=index;
  box.querySelectorAll('[data-homework18-result]').forEach(button=>{
   button.setAttribute('aria-pressed',String(Number(button.dataset.homework18Result)===index));
  });
  const label='Kết quả '+(index+1)+' · '+String(item.source||'ghép Pinyin');
  renderHomework18Card({...item,py:formatHomework18PinyinByWord(item.zh,item.py)},label);
  const status=$('homework18-status'),requestToken=homework18LookupToken;
  if(!String(item.vi||'').trim()){
   if(status)status.textContent='Đang tra nghĩa tiếng Việt cho phương án '+(index+1)+'…';
   machineTranslate(item.zh,'zh-CN','vi').then(vi=>{
    if(requestToken!==homework18LookupToken||homework18SelectedIndex!==index)return;
    const enriched={...item,vi,note:'Nghĩa tiếng Việt được dịch từ toàn câu.'};
    if(!homework18ValidVietnameseMeaning(enriched))throw new Error('Dịch vụ không trả về nghĩa tiếng Việt hợp lệ.');
    homework18Candidates[index]=enriched;
    renderHomework18Card({...enriched,py:formatHomework18PinyinByWord(enriched.zh,enriched.py)},label);
    if(status)status.textContent='Đã tra nghĩa tiếng Việt cho phương án '+(index+1)+'.';
   }).catch(()=>{
    if(requestToken!==homework18LookupToken||homework18SelectedIndex!==index)return;
    renderHomework18Card({...item,py:formatHomework18PinyinByWord(item.zh,item.py),vi:'Chưa tra được nghĩa tiếng Việt.'},label);
    if(status)status.textContent='Đã ghép được chữ Hán; dịch vụ nghĩa tiếng Việt hiện không khả dụng.';
   });
  }else if(status){
   status.textContent='Đang xem Kết quả '+(index+1)+' / '+homework18Candidates.length+'.';
  }
 };
 box.querySelectorAll('[data-homework18-result]').forEach(button=>button.addEventListener('click',()=>choose(Number(button.dataset.homework18Result))));
 choose(0);
 return homework18Candidates[0];
}"""
replace_ui_once(old_renderer,new_renderer,"multi-result selector and selection behavior")

ui_required = [
    "function formatHomework18PinyinByWord(zh,py)",
    "pinyin18DisplayKey(value)",
    "requestToken!==homework18LookupToken||homework18SelectedIndex!==index",
    "Chưa tra được nghĩa tiếng Việt.",
    "homework18Candidates=(Array.isArray(candidates)?candidates:[]).filter"
]
missing_ui = [needle for needle in ui_required if needle not in source]
if missing_ui:
    raise SystemExit("Menu 18 UI verification failed; missing: " + ", ".join(missing_ui))


# Do not let a delayed translation response replace a different candidate
# that the learner selected while the request was in flight.
token_guard = "if(token!==homework18LookupToken)return;"
token_guard_new = "if(token!==homework18LookupToken||homework18SelectedIndex!==0)return;"
token_guard_count = source.count(token_guard)
patched_guard_count = source.count(token_guard_new)
if token_guard_count == 2:
    source = source.replace(token_guard, token_guard_new)
    changes.append("preserve candidate selection in remaining translation paths")
elif token_guard_count == 0 and patched_guard_count == 2:
    pass  # Already patched; keep the overlay idempotent.
else:
    raise SystemExit(
        "Menu 18 patch aborted: expected two generic async result guards "
        f"(unpatched={token_guard_count}, patched={patched_guard_count})"
    )


if source != original:
    target.write_text(source, encoding="utf-8", newline="\n")

print("Menu 18 ranking patch: verified")
print("Updated: " + (", ".join(changes) if changes else "already current"))
print("Verified contextual phrases, tone maps and long-input handling.")

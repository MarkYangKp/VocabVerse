WORD2PASSAGE = """
角色:
你是语言能力极强且具有深厚写作技巧的英语写作家。你不仅具备良好的文字表达能力，能够迅速生成高质量、优美的文章，而且具有
较强的适应能力，能够根据不同的写作要求调整风格和难度。你能够根据给定的词汇或主题迅速构思并组织文章内容，并且对受众的需求有
很强的敏感度，能够根据受众的阅读水平、考试要求、甚至特定的语言考点调整写作的深度和语言难度。
###########################################################################
任务:
请你根据提供的词汇、文章要求、文章类型、字数要求写出一篇包含提供的词汇，且内容完整的英文文章,确保读者读后对提供的词汇的记忆加深。
词汇:{{words}}
文章要求:{{passage_needs}}
文章类型:{{passage_type}}
字数要求:{{word_num}}
###########################################################################
输出要求:
你要输出的有:1.文章
这是大致的输出格式，如果不清楚，可以参考下面的示例。
输出格式:
```json
{
  "article": "文章用 Markdown 排版，注意要给提供的词汇加粗。",
  "word_count": "文章字数",
  "passage_type": "文章类型",
  "passage_needs": "文章要求"
}
```
###########################################################################
示例:
输入:
词汇:jealous,creature,consulate,jockey,ore,declare,divine,obese,gymnasium,chapter,filter,rust,domain,hurdle,testify,standpoint,violent,liver,petition,salesmman
文章要求:研究生入学考试英语阅读文章难度
文章类型:搞笑
字数要求:100-150
输出:
```json
{
  "article": "**Chapter** 12 of Sir Reginald's absurd quest began at the **consulate** of Eldorado, where he **declared** his mission to steal the **divine** dragon's **ore**. The **obese** dragon, named Sparkles, was last seen napping atop a **gymnasium**\-turned\-treasure vault. \"I must **filter** through this bureaucratic **hurdle** first,\" sighed Reginald, clutching a **petition** signed by **jealous** knights who claimed the dragon's **liver** held immortality secrets. \n\nAs he approached Sparkles' lair, a **violent** snore shook the walls. \"This is my **domain**,\" boomed the dragon, waking suddenly. Reginald's **salesman** charm failed when Sparkles sneezed **rust** particles. \"From my **standpoint**, you're trespassing,\" the dragon growled. Just then, a **jockey** riding a armored **creature** burst in, screaming about \"dragon tax evasion.\" Reginald facepalmed. This quest was getting more ridiculous by the minute.",
  "word_count": "150",
  "passage_type": "搞笑",
  "passage_needs": "研究生入学考试英语阅读文章难度"
}
```
###########################################################################
正式输入:
词汇:{{words}}
文章要求:{{passage_needs}}
文章类型:{{passage_type}}
字数要求:{{word_num}}
###########################################################################
输出:
"""


WORD2TRANSLATION = """
请你把这些单词在文章中的具体含义给解释出来，如果涉及词组着给出词组搭配的含义。并给出文章翻译
单词:{{words}}
文章:{{passage}}
########################################################################
请你按如下格式输出:
```json
{
    "language_points":[
        "word":"单词的翻译或者词组搭配说明"
    ],
    "translation":"文章翻译"
}
```
########################################################################
示例输入:
单词:ideal,gauge,rarely,usage,bag,December,album,she,bounce,recede,commodity,parade,permeate
文章:**December** has always been a critical **commodity** sales season, but this year's shopping **parade** reveals shifting consumer priorities. Retail analysts use the **gauge** of foot traffic and online clicks to track spending patterns, noting that **she**-economy demographics are driving **rarely** seen purchasing behaviors. \"The **ideal** gift is now experiential rather than material,\" explained Dr. Ellis, pointing to surging bookings for Antarctic tours over traditional luxury **bag** purchases.\n\nMusic **album** sales, however, defy this trend. Vinyl records have made a remarkable **bounce** back, with collectors **recede**-ing from digital platforms to embrace tactile nostalgia. This resurgence permeates even niche markets - jazz albums in **usage** for yoga studios have tripled since 2022. Meanwhile, environmental campaigns **permeate** the holiday discourse: major retailers now charge for festive wrapping paper, steering customers toward reusable solutions.\n\n\"Consumer behavior isn't just changing - it's undergoing a seismic shift,\" said retail consultant Marco Lee. As snow blankets Manhattan's Fifth Avenue, the question remains: will these trends crystallize into permanent market transformations, or melt away come January's thaw?\
########################################################################
示例输出:
```json
{
    "language_points":[
        {"word":"December", "explanation":"十二月（指具体月份）"},
        {"word":"commodity", "explanation":"商品（与sales搭配指商品销售）"},
        {"word":"parade", "explanation":"热潮（shopping parade指购物热潮）"},
        {"word":"gauge", "explanation":"衡量指标（与foot traffic搭配指客流量衡量标准）"},
        {"word":"she", "explanation":"她经济（she-economy指女性消费经济）"},
        {"word":"rarely", "explanation":"罕见地（修饰seen表示前所未见）"},
        {"word":"ideal", "explanation":"理想的（ideal gift指完美礼物）"},
        {"word":"bag", "explanation":"包袋（指奢侈品包袋产品）"},
        {"word":"album", "explanation":"专辑（特指音乐唱片）"},
        {"word":"bounce", "explanation":"反弹（bounce back表示恢复活力）"},
        {"word":"recede", "explanation":"撤退（指消费者从数字平台回归实体）"},
        {"word":"usage", "explanation":"使用场景（指瑜伽工作室的实际应用）"},
        {"word":"permeate", "explanation":"渗透（指环保理念深入假日话题）"}
    ],
    "translation":"十二月一直是关键的商品销售季，但今年的购物热潮揭示了消费者优先事项的转变。零售分析师通过客流量和线上点击量等指标追踪消费模式，指出'她经济'人群正推动前所未见的购买行为。'理想礼物已从物质转向体验'，埃利斯博士解释道，指出南极旅游预订量已超过传统奢侈品包袋购买量。\n\n然而音乐专辑销售逆势而上。黑胶唱片强势反弹，收藏家们从数字平台回归，拥抱触感怀旧。这种复苏甚至渗透到小众市场——自2022年以来，瑜伽工作室使用的爵士乐专辑增加了三倍。与此同时，环保运动渗透假日话题：主要零售商开始对节日包装纸收费，引导顾客使用可重复利用方案。\n\n'消费者行为不仅是改变——而是正在经历地震式转变'，零售顾问马可·李表示。当积雪覆盖曼哈顿第五大道时，问题依然存在：这些趋势会固化为永久的市场转型，还是随着一月回暖消融？"
}
```
########################################################################
正式输入:
单词:{{words}}
文章:{{passage}}
########################################################################
输出:
"""


PASSAGE2QUESTION = """
请你把结合单词和文章，出4个选择题综合考察读者对文章和单词的理解。
单词:{{words}}
文章:{{passage}}
难度:{{difficulty}}
########################################################################
请你按如下格式输出:
```json
[
    {
      "question":"问题",
      "answer":"答案选项",
      "option":{
        "A":"A选项",
        "B":"B选项",
        "C":"C选项",
        "D":"D选项",
      },
      "explanation":{
        "chinese_exp":"中英文混合解析",
        "english_exp":"纯英文解析"
      }
    }
]
```
########################################################################
示例输入:
单词:ideal,gauge,rarely,usage,bag,December,album,she,bounce,recede,commodity,parade,permeate
文章:**December** has always been a critical **commodity** sales season, but this year's shopping **parade** reveals shifting consumer priorities. Retail analysts use the **gauge** of foot traffic and online clicks to track spending patterns, noting that **she**-economy demographics are driving **rarely** seen purchasing behaviors. \"The **ideal** gift is now experiential rather than material,\" explained Dr. Ellis, pointing to surging bookings for Antarctic tours over traditional luxury **bag** purchases.\n\nMusic **album** sales, however, defy this trend. Vinyl records have made a remarkable **bounce** back, with collectors **recede**-ing from digital platforms to embrace tactile nostalgia. This resurgence permeates even niche markets - jazz albums in **usage** for yoga studios have tripled since 2022. Meanwhile, environmental campaigns **permeate** the holiday discourse: major retailers now charge for festive wrapping paper, steering customers toward reusable solutions.\n\n\"Consumer behavior isn't just changing - it's undergoing a seismic shift,\" said retail consultant Marco Lee. As snow blankets Manhattan's Fifth Avenue, the question remains: will these trends crystallize into permanent market transformations, or melt away come January's thaw?\
难度:适中
########################################################################
示例输出:
```json
[
    {
        "question": "The word 'gauge' in the article most likely means:",
        "answer": "A",
        "option": {
            "A": "Measurement tool",
            "B": "Estimation method",
            "C": "Promotion strategy",
            "D": "Economic model"
        },
        "explanation": {
            "chinese_exp": "文中提到零售分析师使用'gauge'来追踪消费模式，结合后文foot traffic和online clicks的描述，应理解为'测量工具'。'gauge'在此处表示衡量指标，如A选项所示。",
            "english_exp": "The term 'gauge' refers to metrics used by analysts to track spending patterns, aligning with 'measurement tool' as the correct interpretation."
        }
    },
    {
        "question": "The pronoun 'she' in 'she-economy' refers to:",
        "answer": "B",
        "option": {
            "A": "Female entrepreneurs",
            "B": "Female consumer groups",
            "C": "Economic policies",
            "D": "Retail companies"
        },
        "explanation": {
            "chinese_exp": "文中'she-economy demographics'指代女性消费群体，与B选项一致。此术语常用于描述女性主导的消费趋势。",
            "english_exp": "'She-economy' typically describes economic activities driven by female consumers, making B the correct choice."
        }
    },
    {
        "question": "The word 'bounce' in the context of music albums implies:",
        "answer": "C",
        "option": {
            "A": "Sudden decline",
            "B": "Gradual increase",
            "C": "Strong recovery",
            "D": "Temporary fluctuation"
        },
        "explanation": {
            "chinese_exp": "文中'bounce back'表示黑胶唱片的显著复苏，C选项'强劲复苏'符合语境。'bounce back'为固定搭配，表示回升。",
            "english_exp": "'Bounce back' indicates a recovery, so 'strong recovery' (C) matches the context of vinyl records' resurgence."
        }
    },
    {
        "question": "The word 'permeate' in the last paragraph is used to describe environmental campaigns that:",
        "answer": "D",
        "option": {
            "A": "Replace traditional practices",
            "B": "Generate controversy",
            "C": "Require government approval",
            "D": "Spread through multiple areas"
        },
        "explanation": {
            "chinese_exp": "文中'permeate'指环保活动渗透到假日讨论中，D选项'扩散至多个领域'准确表达其含义。例如，零售商收取包装费即体现这种渗透。",
            "english_exp": "'Permeate' suggests widespread influence, aligning with D ('spread through multiple areas') as seen in retailers' sustainable practices."
        }
    }
]
```
########################################################################
正式输入:
单词:{{words}}
文章:{{passage}}
难度:{{difficulty}}
########################################################################
输出:
"""
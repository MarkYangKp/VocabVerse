WORD2PASSAGE = """
你是一位专业的文章生成助手。请根据以下要求创作一篇包含指定单词的文章：

单词列表: {{ words }}
文章类型: {{ article_type }}
难度级别: {{ difficulty_level }}
文章风格: {{ tone_style }}
文章长度: {% if word_count %}{{ word_count }}词{% else %}{% if article_length == "short" %}100-200词{% elif article_length == "medium" %}300-500词{% elif article_length == "long" %}600-1000词{% else %}300-500词{% endif %}{% endif %}
主题领域: {{ topic }}
句子复杂度: {{ sentence_complexity }}（0-1之间，越高越复杂）

请确保:
1. 自然地使用所有给定单词，必要时可灵活变化词形
2. 符合指定的文章类型、难度级别和风格
3. 达到指定的文章长度
4. 围绕指定主题展开
5. 控制句子复杂度符合指定值

请以JSON格式返回结果:
{
  "article": "生成的文章内容, markdown格式,对给出单词加粗体处理",
  "word_count": "实际字数统计",
  "article_type": "{{ article_type }}",
  "difficulty_level": "{{ difficulty_level }}",
  "tone_style": "{{ tone_style }}",
  "topic": "{{ topic }}"
}
#########################################################################
示例输入:
单词列表: ideal,gauge,rarely,usage,bag,December,album,she,bounce,recede,commodity,parade,permeate
文章类型:short_story
难度级别: intermediate
文章风格:humorous
文章长度: medium
主题领域: general
句子复杂度: 0.5
###########################################################################
示例输出:
```json
{
  "article": "## The **Ideal** Cookie Catastrophe  \n\nIt was **December** 15th, and Mrs. Pettigrew had **gauged** this to be the **ideal** time for holiday baking. **She** pulled out her grandmother's recipe **album**, determined to make gingerbread cookies shaped like **commodity** trucks. \"The town **parade** needs edible decorations!\" she declared, ignoring her cat Mr. Whiskers batting at the flour **bag**.  \n\nHer first batch **rarely** looked like trucks. More like mutant blobs. \"Must've messed up the butter **usage**,\" she muttered as dough lumps **bounce**d off the rolling pin. Suddenly, the oven timer dinged.  \n\n**She** yanked open the oven door just as the cookie sheet slipped. Twenty burnt truck-shaped projectiles shot across the kitchen. One hit Mr. Whiskers' tail, making him **recede** under the sofa faster than holiday discounts. Another knocked over the sugar canister, creating a snowstorm effect that **permeate**d every surface.  \n\nOutside, the town mayor practicing his **parade** wave got hit by a flying cookie through the window. \"These taste terrible,\" he complained, spitting crumbs, \"but they make **ideal** eco-friendly confetti!\"  \n\nMrs. Pettigrew surveyed the disaster. \"Next year,\" she sighed, brushing flour from her hair, \"I'm buying cookies and calling it **'commodity** outsourcing'.\"  \n\nThe moral? Sometimes the **ideal** holiday spirit involves knowing when to **bounce** straight to the grocery store.",
  "word_count": 248,
  "article_type": "short_story",
  "difficulty_level": "intermediate",
  "tone_style": "humorous",
  "topic": "general"
}
```
#########################################################################
正式输出:
单词列表: {{ words }}
文章类型: {{ article_type }}
难度级别: {{ difficulty_level }}
文章风格: {{ tone_style }}
文章长度: {% if word_count %}{{ word_count }}词{% else %}{% if article_length == "short" %}100-200词{% elif article_length == "medium" %}300-500词{% elif article_length == "long" %}600-1000词{% else %}300-500词{% endif %}{% endif %}
主题领域: {{ topic }}
句子复杂度: {{ sentence_complexity }}（0-1之间，越高越复杂）
##########################################################################
输出:
"""


WORD2TRANSLATION = """
【文本分析任务说明】
请根据提供的单词和文章内容，完成以下深度解析：

一、单词语境解析
请为每个目标单词提供：

基本信息 - 词性/音标（标注重音）/基础词义

语境义项 - 结合上下文的具体含义及引申义

搭配分析 - 该词在文中出现的搭配结构（标注出现段落）
例：
[Resilience]
▶ 词性：n. /rɪˈzɪliəns/
▶ 文中含义：指经济体系在遭受冲击后的恢复能力（第3段）
▶ 典型搭配：demonstrate remarkable resilience（展现非凡韧性）

二、关键词组提取
请识别文章中5-8个具有学习价值的词组：

专业术语

惯用表达

高频搭配
每个词组提供：

结构解析

语用功能

仿写例句

三、精准翻译
请提供符合"信达雅"原则的全文翻译，要求：

专业领域术语准确

长难句逻辑清晰

文学性文本保持韵律美

待解析单词：{{words}}
原文内容：{{passage}}
########################################################################
请你按如下格式输出:
```json
{
    "language_points":[
        "word":"单词的翻译或者词组搭配说明,用markdown格式"
    ],
    "translation":"文章翻译"
}
########################################################################
```
########################################################################
示例输入:
待解析单词:ideal,gauge,rarely,usage,bag,December,album,she,bounce,recede,commodity,parade,permeate
原文内容:**December** has always been a critical **commodity** sales season, but this year's shopping **parade** reveals shifting consumer priorities. Retail analysts use the **gauge** of foot traffic and online clicks to track spending patterns, noting that **she**-economy demographics are driving **rarely** seen purchasing behaviors. \"The **ideal** gift is now experiential rather than material,\" explained Dr. Ellis, pointing to surging bookings for Antarctic tours over traditional luxury **bag** purchases.\n\nMusic **album** sales, however, defy this trend. Vinyl records have made a remarkable **bounce** back, with collectors **recede**-ing from digital platforms to embrace tactile nostalgia. This resurgence permeates even niche markets - jazz albums in **usage** for yoga studios have tripled since 2022. Meanwhile, environmental campaigns **permeate** the holiday discourse: major retailers now charge for festive wrapping paper, steering customers toward reusable solutions.\n\n\"Consumer behavior isn't just changing - it's undergoing a seismic shift,\" said retail consultant Marco Lee. As snow blankets Manhattan's Fifth Avenue, the question remains: will these trends crystallize into permanent market transformations, or melt away come January's thaw?\
########################################################################
示例输出:
```json
{
    "language_points": [
        {
            "word": "December",
            "explanation": "n. /dɪˈsembər/ 十二月（第1段）\n - 文中含义：作为关键销售季的时间坐标\n - 搭配结构：critical commodity sales season（关键大宗商品销售季）"
        },
        {
            "word": "commodity",
            "explanation": "n. /kəˈmɑːdəti/ 大宗商品（第1段）\n - 语境引申：具有季节属性的消费类产品\n - 搭配结构：critical commodity sales season（关键大宗商品销售季）"
        },
        {
            "word": "parade",
            "explanation": "n. /pəˈreɪd/ 购物季活动（第1段）\n - 隐喻用法：指系列促销活动的有序展开\n - 搭配结构：shopping parade（购物狂欢季）"
        },
        {
            "word": "gauge",
            "explanation": "v. /ɡeɪdʒ/ 测量指标（第1段）\n - 专业术语：零售业流量监测参数\n - 搭配结构：gauge of foot traffic（客流量监测指标）"
        },
        {
            "word": "she-economy",
            "explanation": "专业术语（第1段）\n - 结构解析：复合名词'she'+连字符+经济领域\n - 语用功能：描述女性主导的消费经济形态\n - 仿写：The rise of silver-economy reflects aging population trends"
        },
        {
            "word": "tactile nostalgia",
            "explanation": "惯用表达（第2段）\n - 结构解析：形容词+抽象名词的非常规搭配\n - 语用功能：表达实体物品带来的怀旧触感\n - 仿写：Visual nostalgia drives the revival of film cameras"
        },
        {
            "word": "seismic shift",
            "explanation": "高频搭配（第3段）\n - 结构解析：地质隐喻+名词\n - 语用功能：强调变革的根本性与颠覆性\n - 仿写：The AI revolution brings seismic changes to education"
        },
        {
            "word": "crystallize into",
            "explanation": "动词短语（第3段）\n - 结构解析：物质状态变化隐喻\n - 语用功能：描述趋势固化的动态过程\n - 仿写：Online learning may crystallize into mainstream education"
        }
    ],
    "translation": "十二月向来是大宗商品销售的关键战役，然今岁购物狂欢季却显露出消费优先级的悄然转向。零售分析师通过监测实体客流量与线上点击量的复合指标，追踪消费图谱之变，发现'她经济'群体正催生前所未有的采购模式。'理想礼品已从物质载体转向体验经济，'埃利斯博士阐释道，指出南极科考游预订量激增，而传统奢侈品手袋采购式微。\n\n然音乐黑胶唱片却逆势而起，演绎绝地反弹的商界传奇。藏家们如潮水退离数字平台，拥抱实体唱片的触觉乡愁。此番复兴甚至渗透至利基市场——瑜伽馆专用的爵士乐专辑使用量自2022年来已翻三倍。与此同时，环保倡议漫染节日话语体系：主流零售商开始对礼品包装纸收费，引导消费者拥抱可持续方案。\n\n'消费行为之变，非止涟漪，实为地壳运动。'零售顾问马可·李如是说。当皑雪覆满纽约第五大道，悬疑犹存：此般趋势将凝为永恒的市场晶构，抑或随正月暖阳消融无形？"
}
```
########################################################################
正式输入:
待解析单词:{{words}}
原文内容:{{passage}}
########################################################################
输出:
"""


PASSAGE2QUESTION = """
Please design 5 high-quality English reading comprehension multiple-choice questions based on the following elements to comprehensively assess readers' mastery of vocabulary in context and deep text understanding:

Question Design Principles:

Competency Dimensions Coverage:

2 questions focusing on vocabulary application (word meaning differentiation/collocation usage/contextual inference)

2 questions testing discourse structure comprehension (main idea/paragraph function/logical cohesion)

1 question evaluating inferential judgment (implied meaning/author's perspective/text extension)

Option Design Specifications:
√ Each option length: 5-15 words
√ Distractors must include plausible alternatives (e.g., near-synonyms, context mismatches, partially correct information)
√ Avoid "none of the above" or trick options
√ Randomize answer positions

Question Integration Requirements:

Each question must link both textual content and target vocabulary

Stem must clearly indicate assessment focus (e.g., "The word 'ephemeral' in paragraph 3 most nearly means...")

Questions ordered according to text sequence

########################################################################
Output Format:
```json
[
    {
      "question":"question stem",
      "answer":"answer option",
      "option":{
        "A":"A option",
        "B":"B option",
        "C":"C option",
        "D":"D option"
      },
      "explanation":{
        "chinese_exp":"中英文混合解析",
        "english_exp":"ENGLISH explanation"
      }
    }
]
```
########################################################################
Example Input:
word list:ideal,gauge,rarely,usage,bag,December,album,she,bounce,recede,commodity,parade,permeate
article:**December** has always been a critical **commodity** sales season, but this year's shopping **parade** reveals shifting consumer priorities. Retail analysts use the **gauge** of foot traffic and online clicks to track spending patterns, noting that **she**-economy demographics are driving **rarely** seen purchasing behaviors. \"The **ideal** gift is now experiential rather than material,\" explained Dr. Ellis, pointing to surging bookings for Antarctic tours over traditional luxury **bag** purchases.\n\nMusic **album** sales, however, defy this trend. Vinyl records have made a remarkable **bounce** back, with collectors **recede**-ing from digital platforms to embrace tactile nostalgia. This resurgence permeates even niche markets - jazz albums in **usage** for yoga studios have tripled since 2022. Meanwhile, environmental campaigns **permeate** the holiday discourse: major retailers now charge for festive wrapping paper, steering customers toward reusable solutions.\n\n\"Consumer behavior isn't just changing - it's undergoing a seismic shift,\" said retail consultant Marco Lee. As snow blankets Manhattan's Fifth Avenue, the question remains: will these trends crystallize into permanent market transformations, or melt away come January's thaw?\
dificulty:simple
########################################################################
Example Output:
```json
[
    {
      "question":"What emerging consumer trend contradicts traditional December commodity sales according to the article?",
      "answer":"A",
      "option":{
        "A":"Experiential gifts replacing material items",
        "B":"Increased luxury bag purchases",
        "C":"Digital music platform dominance",
        "D":"Free festive wrapping paper promotions"
      },
      "explanation":{
        "chinese_exp":"文章指出'ideal gift is now experiential rather than material'，南极游预订超过传统奢侈品包，显示体验式礼物趋势。",
        "english_exp":"The article states the 'ideal gift is now experiential rather than material' with Antarctic tours surpassing luxury bag purchases, indicating a shift toward experiential gifting."
      }
    },
    {
      "question":"What does 'gauge' specifically refer to in the retail context of the article?",
      "answer":"B",
      "option":{
        "A":"Price measurement tools",
        "B":"Foot traffic and online engagement metrics",
        "C":"Product quality standards",
        "D":"Inventory management systems"
      },
      "explanation":{
        "chinese_exp":"文中明确使用'gauge of foot traffic and online clicks'指测量客流量和点击量的指标。",
        "english_exp":"The text explicitly uses 'gauge of foot traffic and online clicks' referring to metrics for tracking consumer engagement."
      }
    },
    {
      "question":"What demographic shift is indicated by the term 'she-economy' in the article?",
      "answer":"C",
      "option":{
        "A":"Male-dominated spending patterns",
        "B":"Gender-neutral marketing strategies",
        "C":"Female-driven consumer behaviors",
        "D":"Senior-focused retail campaigns"
      },
      "explanation":{
        "chinese_exp":"'she-economy'指女性主导的经济现象，后文提到'rarely seen purchasing behaviors'显示女性消费群体的影响力。",
        "english_exp":"The term 'she-economy' refers to female-driven economic patterns, with 'rarely seen purchasing behaviors' indicating women's growing consumer influence."
      }
    },
    {
      "question":"Which two words describe the paradoxical trends in music consumption?",
      "answer":"D",
      "option":{
        "A":"Bounce & Permeate",
        "B":"Recede & Usage",
        "C":"Album & Commodity",
        "D":"Bounce & Recede"
      },
      "explanation":{
        "chinese_exp":"黑胶唱片'remarkable bounce back'和收藏家'recede-ing from digital'形成数字撤退与实体复兴的对比。",
        "english_exp":"Vinyl's 'remarkable bounce back' contrasts with collectors 'recede-ing from digital platforms', showing analog resurgence versus digital withdrawal."
      }
    },
    {
      "question":"How does the article illustrate environmental campaigns' influence?",
      "answer":"C",
      "option":{
        "A":"Banning all holiday packaging",
        "B":"Promoting disposable decorations",
        "C":"Charging for wrapping paper to encourage reusables",
        "D":"Reducing vinyl production for sustainability"
      },
      "explanation":{
        "chinese_exp":"文中提到'charge for festive wrapping paper'推动可重复使用方案，体现环保渗透(permeate)节日话语。",
        "english_exp":"The article states retailers 'charge for festive wrapping paper, steering customers toward reusable solutions', demonstrating how environmental concerns permeate holiday practices."
      }
    }
]
```
########################################################################
Input:
word list:{{words}}
article:{{passage}}
difficulty:{{difficulty}}
########################################################################
Output:
"""
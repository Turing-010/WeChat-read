# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
三个关键词， 2026 ⾕歌 I / O ⼤会全说透了
May  20 , 2026 , 12 : 25  AM⼴东腾讯技术⼯程 81  listened
导语
"There are three areas where I want to go deeper today to show you the progress in
each: Models, coding, and agents."
这不是⽇程表，这是⾕歌交给  AI 下半场的答题卡。
⽽这三块拼图最令⼈振奋的地⽅在于：
模型： Gemini 3.5 Flash ⼀个  "Flash 级 " 的⼩模型，把⾕歌⾃⼰三个⽉前的旗舰  Gemini 3.1
Pro 在⼏乎所有基准上正⾯打穿；
编程： Antigravity ⽤  93 个⼦  Agent 、 12 ⼩时、不到  1000 美元，从零造了⼀个能跑  Doom
北京时间今天凌晨  1 点，⾕歌  I/O 2026 在  Shoreline 圆形剧场落幕。整场  keynote ⼤约
1 ⼩时  51 分钟，涉及⼗⼏款产品、三代模型、⼀个新  IDE 、⼀个新  Agent 、⼀套新搜索
范式
但如果只能记⼀句话，那就是⽪查伊（ Sundar Pichai ）在演讲第  16 分钟说的那⼀句。
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
的操作系统；
Agent： Search 直接进⼊ "Search agents" 时代 —— 它不再只回答你，它开始替你做。
这⼀夜， AI 第⼀次⼤规模地从 " 对话框 " ⾛进了 " ⽇常事 " 。
⼀、模型层： 3.5 Flash 把⾃家上⼀代  Pro ⼲翻了， Omni 让  AI 第⼀次会 " 改 " 视
频
1. 数据先⾏：每分钟  190 亿  tokens ， 13 个产品⽉活破  10 亿
讲模型之前，⽪查伊先甩了⼀组数据，定调 " 现在到底有多⼤ " ：
⾕歌每⽉处理  tokens ：从  9.7 万亿涨到  3.2 千万亿；
每分钟处理：190 亿  tokens；
全球开发者：850 万；
⽉活破  10 亿的⾕歌产品：13 个，其中  5 个超  30 亿；
AI Overviews ⽉活：25 亿；
AI Mode 上线⼀年，⽉活突破  10 亿；
Capex 投⼊：从  2022 年的  310 亿美元，飙到  2026 年的  1800–1900 亿美元—— 四年  6
倍。
这是  Gemini 3.5 出场前的全部底⽓。
2. Gemini 3.5 Flash ：今⽇全量上线，把⾃家上⼀代旗舰按在地上
接下来是模型层最⼤⼀块⽯头 ——Gemini 3.5 Flash 今⽇全量上线。
今天起在所有⾕歌产品和  API 中全量开放；
同时成为  Gemini App 与  Google Search AI Mode 的默认模型—— 没错，你今天打开  AI
Mode 搜的每⼀条，背后都已经是  3.5 Flash ；
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
Gemini 3.5 Pro  下个⽉跟上。
但真正让现场倒吸⼀⼝凉⽓的是数字：
速度：输出  289 tokens/ 秒，⽐  GPT-5.5 、Claude Opus 4.7  快  4 倍以上；
价格：⽐同级前沿模型便宜超过⼀半；
性能：在⼏乎所有基准上，与⾃家三个⽉前的旗舰  Gemini 3.1 Pro 正⾯对标并实现反
超。
最后这⼀条值得停下来再读⼀遍 —— 这是⼀个  Flash 级模型，在主要  benchmark 上全⾯对标
⾃家上⼀代  Pro。换算到外部世界，约等于：⼀辆刚出⼚的 " 经济款 " ，把⾃家三个⽉前的 " 性
能旗舰 " 按在地上摩擦。
四组关键基准成绩：
基准 项⽬ 3.5 Flash 成绩
Terminal-Bench 2.1 编码能⼒ 76.2%
GDPval-AA 真实世界  Agent 任务 1656 Elo
MCP Atlas ⼤规模⼯具使⽤ 83.6%
CharXiv Reasoning 多模态推理 84.2%
更暴⼒的是它对企业账单的杀伤⼒ —— ⽪查伊原话：⼤客户若把  80% 的⼯作切到  3.5
Flash ，⼀年能省下超过  10 亿美元的  API 成本。
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
这是⾕歌今晚扔在桌上的第⼀张牌：" 我⽤⼀个  Flash 级模型，把整个前沿模型市场的均衡价
格区间，向下⼜拉了⼀档。 "
3. Gemini Omni ： AI 第⼀次会 " 改 " ⼀段已经拍好的视频
如果说  3.5 Flash 是模型层的 " 性价⽐王炸 " ，那  Omni 就是模型层的 " 想象⼒天花板 " 。
Demis Hassabis 上台揭幕：Omni 是⼀个原⽣的视频⽣成与编辑模型家族，今晚发布的⾸款
成员叫  Gemini Omni Flash，更强的  Omni Pro 不久后跟上。
它最炸的地⽅，不是从零⽣成视频—— 这事  Veo 早能做。
"Just like Nano Banana redeﬁned image editing, Omni gives you a much more natural way to
edit video with conversational language."
（正如  Nano Banana 重新定义了图⽚编辑，Omni 让你能⽤对话式语⾔、⾃然地编辑视
频。）
—— Demis Hassabis
真正的跨越，是它能改⼀段已经存在的视频，⽽不破坏原有⼈物的表演。
你拍了⼀段  selﬁe ，⼀句  prompt + ⼀张参考图，它能：把背景换掉、加上特效、塞进⼀个新
⻆⾊ —— ⽽你脸上的表情、肢体语⾔、说话节奏，纹丝不动。
这⼀步是从 " ⽣成 " 迈向 " 编辑 "—— ⽽这⼀步，正是创作者真正在意的那⼀步。
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
发布会还顺⼿秀了⼀⼿原⽣⾳视频同步⽣成：画⾯、配乐、⾳效在同⼀次推理⾥出来，不再
需要三个模型接⼒配菜。
⾸发渠道： Omni Flash 今⽇正式上线，同时接⼊  Gemini App 、 Google Flow 和  YouTube
Shorts—— 其中  YouTube Shorts ⽤户可直接免费使⽤。 to-C 的扩散速度，⾕歌这次没省⼒
⽓。
顺带⼀提，⾕歌  AI 内容防伪⽔印  SynthID ⾃上线以来，已为  1000 亿张图像和视频、 6 万年
时⻓的⾳频打上⽔印—— 他们清楚  Omni 这种⼯具会带来什么。研究显示，⼈类只能正确识
别约  25% 的⾼质量深伪视频，⽔印这件事不再是 " 可选项 " 。
⼆、编程层： Antigravity 2.0—— ⼀个能跑  Doom 的操作系统
如果说模型层是地基，那今晚最让开发者⾎压升⾼的⼀段，全部发⽣在编程板块。
主讲⼈是  Varun Mohan—— 前  Codeium / Windsurf 创始⼈  CEO ，加⼊⾕歌后操盘
Antigravity 。他给  2.0 写下的定位只有⼀句：
1. ⼀组先扔出来的数据： Antigravity 内部已经 " ⻜起来 " 了
光是  Antigravity ⼀个产品，⾕歌内部处理  token 的速度 ——
从今年  3 ⽉的  5000 亿 / 天，飙到现在的  3 万亿 / 天。
两个⽉， 6 倍。  这是  Antigravity 在内部跑出来的真实加速度。
⽽开发者今天拿到的  Antigravity ⾥的  Flash ，是经过专项优化的  12× 加速版—— 也就是  3.5
Flash 在同等任务上吞吐能再翻  12 倍。
2. Antigravity 2.0 给开发者的三件⼤事
"Unabashedly agent ﬁrst." （毫不掩饰地， Agent 优先。）
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
全新独⽴桌⾯应⽤：抛开传统  IDE 的 " 编辑器 + 插件 " 思路，把  Agent 对话⾯板  / Agent 产
物⾯板  / 多  Agent 编排⾯板  做成⼀等公⺠；
CLI  + SDK + 原⽣语⾳：接⼊  Gemini audio 模型，可以直接⽤嘴和  Antigravity 谈需
求；
Android 、 Firebase 、 AI Studio 全栈原⽣集成；
底层引擎：Gemini 3.5 Flash × Antigravity Agent Harness，⾃带  sub-agents 、 hooks 、
async 三⼤原语。
3. 王炸时刻： 93 个⼦  Agent ， 12 ⼩时，造了⼀个能跑  Doom 的操作系统
Varun 在台上点开了⼀个不可思议的实验记录 ——
指标 数字
⼦  Agent 并⾏数 93 个
总耗时 12 ⼩时
模型请求次数 超  15,000 次
处理  tokens 26 亿
API 总成本 不到  1000 美元
产物 ⼀个能跑  Doom 的操作系统
（含调度器  / 内存管理  / ⽂件系统）
⽤⾕歌⾃⼰的话说 ——
现场演示更震惊： Varun 在⾃家  OS ⾥随⼿敲了个   sl（ Linux ⽼   ls  输错梗），跳出⼀只
⼩⽕⻋；接着试着跑  Doom—— 缺驱动；他随⼝让  Antigravity ⾃⼰去修 —— 修好了，全场⿎
掌。
"调度程序、内存管理、⽂件系统，每⼀⾏代码都是  Agent 写的、 Agent 测的、 Agent 审
计的。"
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
⼀件以前需要⼀整⽀系统团队做半年的事。
Varun 给这件事下的定调，是今晚开发者圈最值得被钉在墙上的⼀句话：
Antigravity 2.0 今天起全球开放。
三、 Agent 层： Spark + Search Agents ， AI ⾛出对话框的两条路径
到模块三，⽪查伊把这⼀年的  "agentic" 叙事钉死：
但  Agent 不是⼀个产品，⽽是两条铺设路径——
⼀条是  Gemini App ⾥的主控⼤脑  Spark；
⼀条是直接⻓在全球最⼤⼊⼝⾥的  Search Agents。
1. Gemini Spark ：你的  24×7 数字管家
Spark 是  Gemini App ⾥新冒出来的彗星图标。它的定位⾮常直⽩：
"Multiday engineering efforts are collapsing into hours, if not minutes." （以前要拉⼏天
的⼯程任务，正在被压缩成⼏⼩时，甚⾄⼏分钟。）
"We are ﬁrmly in our agentic Gemini era."
（我们已经稳稳进⼊  agentic Gemini 时代。）
"It's your personal AI agent that helps you navigate your digital life, taking action on your
behalf and under your direction. It runs on dedicated virtual machines on Google Cloud,
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
翻译成⼈话：它是⼀台  7×24 ⼩时不打烊、托管在⾕歌云上的 " 你 " 。
关键设计：
UI 是  Chat / Agent 双  Tab——Chat 还是问答， Agent 才是派活；
跨端：⽹⻚  / 桌⾯  / Android & iPhone 实时同步；接下来还会铺到  邮件  + IM；
能跑定时任务（ " 每周⼀  8 点把上周会议纪要整理给我 " ）；
通过  MCP 协议，未来⼏周打通第三⽅⼯具；
数据视野：连接的  Google 应⽤  + 聊天记录  + 已登录⽹站  + Personal Intelligence 个⼈画
像  + 实时位置；
下半年， Spark 将直接落地到  Chrome ⾥，成为  "agentic browser"—— 这就是去年传闻已
久的  "Chrome Auto Browse" 叙事的真正归宿；
同期还会推出  Android Halo—— ⼿机上专⻔为  Agent 准备的 " 基地 " 。
节奏与价格：
本周：仅对  trusted testers 灰度；
下周：向美国  Google AI Ultra 订阅⽤户开  Beta ；
AI Ultra 订阅同步调整：
新增  $100/ ⽉  ⼊⻔档—— 这是开通  Spark Beta 的最低⻔槛；
最⾼档  Ultra 计划从   降到200/ ⽉；
此外， Gemini App 同步改版（代号  Neural Expressive ），计费模式改为按算⼒计费。
and it is 24/7."
⚠  Spark ⾃带的诚实⾃⽩：Spark 是实验性产品。虽然它被设计成在敏感操作前征求许
可，但它可能在未询问的情况下分享你的信息或代你完成购买。请勿依赖它做医疗、法
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
2. Search 的  25 年最⼤改版：进⼊  "Search Agents" 时代
接下来上台的是  Liz Reid（⾕歌搜索负责⼈）。她甩出今晚  Agent 板块第⼆组震撼数据：
AI Mode 上线刚⼀年，⽉活突破  10 亿；
AI Mode 查询数⾃上线以来每季度翻倍；
已升级到  Gemini 3.5—— 现在打开  AI Mode ，你⽤的就是它。
然后她说出全⽂最值得划线的那句：
3. 三件具体的事
(1) 全新的  AI 搜索框 —— 25 年来最⼤的⼀次搜索框升级。原⽣⽀持⽂本  / 图像  / ⽂件  / 视
频混合输⼊， AI Overviews 与  AI Mode 之间⽆缝切换。
(2) Information Agents （信息智能体） —— 24×7 在后台替你 " 盯着 "
它主动监控你交代过的事：
demo 1 ：监控⽣物科技板块 " 市盈率 <15 、正现⾦流、低负债 " 的股票，命中即推送；
demo 2 ：租房—— 你随⼝讲⼀段需求，它持续在背后筛新房源；
demo 3 ：⼼仪球鞋⼀发售即时预警。
律、财务等专业决策。
—— 这段话是⾕歌⾃⼰写在产品安全说明⾥的。它不是免责声明，是当下所有  agentic
产品集体⾯对的真实⻛险。
"We're entering the era of Search agents."
（我们正在进⼊ " 搜索智能体 " 的时代。）
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
预计的上线时间：今年夏天。
(3) Generative UI in Search —— Antigravity 直接被嵌进  Search 后端
这是今晚  Search 部分最反直觉的⼀段。
demo 1 ：问⼀个关于⿊洞引⼒波的物理问题，Search 现场写出了⼀个交互式可视化
mini-app；
demo 2 ： Search 主动提议 ——" 要不要给你做个周末家庭计划器？ " 它结合  Gmail / Photos
/ Calendar ⾥的家庭画像，实时排出周末两天的⾏程，能转发给⽼婆、能⼀键同步到全家
共享⽇历。
预计上线时间：今年夏天免费向所有⼈开放。
4. 顺带的⼀颗⻓期变量： UCP （ Universal Commerce Protocol ）
Search 章节末尾， Vidhya Srinivasan 抛出了⼀个野⼼更⼤的东⻄ ——UCP 通⽤商业协议：
这意味着什么？ 意味着  Search 不再只是给你⼀个 " 答案⻚ "—— 它给你⼀个为你这个问题
专⻔⽣成的临时  App。
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
⾕歌  Shopping Graph 已收录  600 亿条商品，这是  UCP ⼀上来就能撑住的底盘。这⼀步如果
跑成， "AI 替你购物 " 就不再是各家⼚商各⾃的⼩作坊，⽽是整个互联⽹商业层的协议级重
构。
四、把三块拼图咬合起来看：⾕歌究竟在赌什么？
把今晚的三块板块叠在⼀起，会浮出⼀句异常清晰的判断：
模型  →  Omni 让  AI 第⼀次能改⼀段已经拍好的视频；
编程  →  Antigravity ⽤  1000 美元造了⼀个能跑  Doom 的操作系统；
Agent  →  Spark 24×7 替你跑后台， Search 边搜索边替你下单。
OpenAI 的  Agent 平台、 Anthropic 的  Conway 、微软的  Agent 365 都在路上。但⾕歌今晚交
出的这份答卷，差异化只有⼀句话 ——
这场  Agent 决赛的胜负⼿，可能不在谁的模型  benchmark ⾼⼀两个点。
它在 ——谁能把  AI 真的铺到  10 亿⼈的⽇常⾥。
⾕歌握着三个⼀般⼈⼀抬⼿就会⽤到的⼊⼝：Gemini App （ Spark ） + Google Search
（ Search Agents ） + Antigravity （开发者）—— 这是⼀道别家短期内复制不出来的分发护城
河。
⾄于另⼀⾯：当⼀个  24×7 的  Agent 拥有你的邮箱、相册、⽇历、位置和⽀付权限时，安全
边界谁来守？谁来负责？—— 这是⾕歌今晚没能给出完整答案的题，也是接下来⼀年所有⼤
⼚都绕不开的题。
五、写在最后
"UCP does for agentic commerce what HTTP did for the web: It gives agents and systems
a common language."
（UCP 之于  agentic 商业，正如  HTTP 之于  Web—— 它让所有  Agent 和系统说同⼀种语
⾔。）
AI 第⼀次⼤规模地，从 " 对话框 " ⾛进了 " ⽇常事 " 。
" 我把  Agent 直接装进了你每天必开的搜索框和  Gemini App 。 "
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
回头看⽪查伊那句开场⽩ ——"Models, coding, and agents."—— 它其实不是⽇程表，是⾕歌
交给  AI 时代下半场的答案：
模型继续往前推（更便宜、更多模态、能编辑⽽不只是⽣成）；
编程被  Agent 重写（⼀个⼈  + ⼀群⼦智能体  = ⼀个⼯程团队）；
Agent  借着搜索框和  App ⼊⼝，第⼀次真正⾛进了  10 亿⼈的⽇常。
你最期待哪⼀件事先发⽣在⾃⼰身上？ ——
☐  Spark 替你管收件箱和⽇程
☐  Search Agent 替你抢球鞋  / 监控租房  / 盯股票
☐  Antigravity 替你写下⼀个项⽬的代码
评论区聊聊。
⼀分钟视频速览
AI 不再只回答你，它开始替你做。
腾讯程序员
 195
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
作者提示: 内容由 AI ⽣成
阅读 9337修改于2026 年 5 ⽉ 20 ⽇
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
留⾔
还没有留⾔，来写⾸评
写留⾔
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
````

## 采集与转写核验记录（非原文）

以下说明由本次核验添加；上方逐页文本保持文本层原样，图片与布局以PDF为准。

- PDF物理页 8：抽取文本漏掉Ultra原价250；页8图可读250降到200/月，已据图补正
- PDF物理页 12,13,14：视频速览为静态封面，未读取视频；p.14空白页，正文结尾及评论可见，捕获完整性待复核

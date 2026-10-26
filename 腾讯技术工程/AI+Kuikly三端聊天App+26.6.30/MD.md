# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
AI + Kuikly ： 7 . 5 ⼩时 落地三端「多模态聊天 App 」实战
腾讯程序员 Jun  30 , 2026 , 2 : 44  AM贵州原创 腾讯技术⼯程 147  listened
⽤  28 轮对话、 740 字⾃然语⾔，⽣成约  3500 ⾏代码，完成⼀套三端可运⾏的多模态  AI 聊天
App 。全程零⼿写，不看代码， 1 天交付。
放在传统开发⾥，同样的功能  iOS 、 Android 、鸿蒙各写⼀遍，要  30 ⼈天；就算⽤  Kuikly ⼿
写，也得  7.5 ⼈天。这次⽤  AI 辅助，实际只花了  7.5 ⼩时。最终交付的  App ⽀持流式
Markdown 、拍照识图、相册选取、 SSE ⻓连接、本地会话管理，⼀套代码即可覆盖
Android 、 iOS 、鸿蒙三端。
这不是 “Vibe Coding” 的⽞学叙事，⽽是⼀次 “AI + Kuikly 跨端框架 ” 的实弹演习。 Skills 和  Rules
让  AI 始终保持在正确的技术上下⽂中，组件库开箱即⽤、三端模板⼀键⽣成，这套基础设施⽀
撑起了 “AI + Kuikly” 的协同效率。之前 搜狗输⼊法⽤  Spec Coding 把新⻚⾯开发从  3 天压到
1 天， QQ ⾳乐⽤  AI 智能转码实现  90%+ 代码采⽤率  ，效率红利正在被验证。
说到底，这次实验就想回答⼀个问题：纯靠对话，能把事情做到什么程度？⼀天之后，我有了
答案。
Kuikly  是腾讯开源的⾼性能跨端框架，基于 Kotlin  Multiplatform  技术，覆盖 Android 、 iOS 、
HarmonyOS 、 H5 、微信⼩程序、 Mac  六⼤平台，⽀撑业务⽇活⽤户超 5 亿。当 Kuikly  搭配真
正懂它的 AI ，开发会怎样——零⼿写代码，仅凭⾃然语⾔， 7 . 5  ⼩时交付⼀套⽀持 Android 、
iOS 、鸿蒙三端的 AI  聊天 App 。看 AI  如何调研组件、扩展原⽣模块、⾃⾏定位 Bug ，感受为
什么「 AI  + Kuikly 」是当下客户端开发效率最⾼的组合之⼀。
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
下⾯是这⼀天的真实⽇记。
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
AI Coding 全过程
先把这⼀天的节奏拉成⼀条时间线：
09:00 - 09:10 ｜ 环境准备：先把  AI 开发环境搭起来
动⼿写代码前，得先把  AI 的 “ ⼯作环境 ” 备⻬。
先跟着KuiklyUI GitHub 仓库的指引装好  IDE 和  Kuikly 插件。我本地早就配好了，直接跳过这
⼀步，开始创建模板⼯程。按向导填写信息、⼀路点下⼀步， Android 、 iOS 、鸿蒙三端的⼯程
⽂件就准备好了。
接着，按照官⽹AI 编程的指引在⼯程⾥安装  Kuikly AI 的  Skills 和  Rules 。
这⼀步很关键。 Kuikly  DSL  相对专有，通⽤⼤模型的训练语料覆盖并不充分，⽽
Skills  和 Rules  能把框架知识喂给模型，让 AI  像⼀个熟悉 Kuikly  的开发者⼀样⼯
作。
到这⾥， Kuikly 的  AI 开发环境就算准备好了，然后我切到  AI Coding 的主场：CodeBuddy 。
09:10 - 10:20 ｜ 需求分析与⽅案设计：先确定能复⽤什么，再决定⾃⼰写什
么
这是⼀个完整  App ⽽⾮单个⻚⾯，所以我没让它直接开写，⽽是先⽤  CodeBuddy
superpowers 插件⾥的  brainstorming技能把需求拆清楚。
给它的第⼀条指令：
觉得  Kuikly 有意思的话，欢迎给  KuiklyUI GitHub 仓库点个  ⭐  关注，以后好找。
1npx skills add Tencent-TDS/KuiklyUI-AI/skills
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
这条  Prompt 写得⽐较完整，关键是两点：明确 “ ⼀码三端 ” ，不是只跑  Android 的  Demo ；强调
“ 优先使⽤已有组件 ” ，避免它上来就造轮⼦。
组件查询
AI 随即调⽤查询第三⽅组件的技能，筛出⼀份匹配清单
（KuiklyChatUI、KuiklyMarkdown、KuiklyAlbum、KuiklyCamera、KuiklySQLite、Kuikly
Webview、KuiklyToast），接着并⾏访问它们的  GitHub 信息调研⽤法与平台⽀持。
有个细节挺有意思： AI 本来在清单⾥选了KuiklyMarkdown来做  Markdown 渲染，但调研后发
现  KuiklyChatUI⾥的AiMessageText已覆盖  AI 消息的  Markdown 渲染场景，于是不再单独引
⼊KuiklyMarkdown，最终落地  6 个组件。这就是  Skills 和  Rules 的第⼀个收益 ——AI 开始知道
什么时候不该写。
确定组件清单后， AI 还标出两个需要⽤  Kuikly 的  Module 机制扩展的能⼒缺⼝：
1. 现有Network不⽀持  SSE ⻓连接，需补⼀个SSEModule
2. 图⽚发给多模态模型前需统⼀压缩和  base64 编码，需补⼀个ImageModule
过去⽤  AI 写代码，最怕它把所有问题都包装成 " 没问题，我来实现 " ，然后⼀路写到编译报错。
这次  AI 则表现得像⼀个资深的  Kuikly 开发者，我知道这是  Kuikly AI 的  Skills 和  Rules 的功
劳。它们很好地充当了  AI 的缰绳，哪些⽤组件、哪些⾃研、⽤何种⽅式组织代码，都被框得很
清楚。
⽅案基本确定
聊天主体⽤  KuiklyChatUI
Markdown 能⼒复⽤  AiMessageText
拍照和相册分别⽤  KuiklyCamera 、KuiklyAlbum
会话历史⽤  KuiklySQLite
外链打开⽤  KuiklyWebview
轻提示⽤  KuiklyToast
SSE 和图⽚压缩编码⽤⾃研  Module 补⻬
AI 接着推演了架构、数据结构和交互设计，整体合理，我基本没打断，很快就拿到了第⼀版开
发   plan 。
/brainstorming 使⽤  Kuikly 实现⼀个多模态  AI 聊天  App ，⼀码三端，⽀持  Android 、
iOS 、鸿蒙。核⼼能⼒包括：发送⽂本 / 图⽚消息、拍照发图、相册选图、 AI 流式回复、
Markdown 渲染、打开消息中的⽹址、本地会话管理、历史会话恢复。优先使⽤  Kuikly
官⽅和社区已有组件。
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
10:20 - 11:10 ｜ 编码实现： AI 是怎么把代码写出来的
plan 确认后，我基本就让  AI ⾃⼰往下跑了，中途没有太多打断。
值得说⼀下的是它在不同环节调⽤的技能，这也是这次 "AI 真的懂  Kuikly" 的关键。
补两个框架没覆盖的能⼒时，它⽤的是[skill:kuikly-expand-api]—— 也就是  Kuikly 官⽅提
供的 " 扩展原⽣  API / ⾃定义  Module" 技能。SSEModule和  ImageModule这两个跨端  Module 都
是靠它⽣成的：从  commonMain 的接⼝定义，到三端  native 侧的桥接实现，技能⾥都有明确
的规范可循， AI 不⽤凭记忆去猜  Kuikly 的  Module 写法。
实现聊天主⻚⾯和历史会话列表⻚⾯时，它⽤的是[skill:kuikly-ui-framework]
和[skill:kuikly-reactive-observer]。前者负责  Kuikly DSL 的⻚⾯结构和组件⽤法，后者
负责响应式状态 —— 消息列表、流式回复这些需要随状态变化⾃动重渲染的地⽅，都是靠
observable把数据和  UI 绑起来的。
整个过程给我的感觉是： AI 不是在 " 硬写⼀种它半懂的  DSL " ，⽽是每到⼀个环节先加载对应
的  Kuikly 技能，再按规范动⼿。该⽤哪个组件、该扩展哪个  API 、状态怎么绑，基本没⾛偏。
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
11:10 - 12:30 ｜ 集成⾃测：上真机测试，发现⼀个图⽚加载缺陷
plan 执⾏完，我先在  Android 真机上跑。
⼀次编译就成功了。
App 起来，界⾯⼲净，输⼊框、消息列表、发送按钮都在。我发出了第⼀条⽂字消息， AI 流式
回复正常滚了出来， Markdown 也渲染对了。
对于⼀个⼀码三端、还⾃带  SSE ⻓连接和多模态结构的⼯程来说，第⼀次真机运⾏就直接跑通
⽂字链路，这个结果⽐我预期要好。
⽂字链路没问题，我接着试图⽚消息。
图⽚链路出问题：让  AI ⾃⼰定位
点开相册，选图⻚⾯正常打开了 —— 缩略图宫格布局也铺出来了，但每⼀格的缩略图都加载不
出来，整⽚宫格只有⼀个个空⽩格⼦，看不到图，⾃然也没法选。
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
我没有⾃⼰去翻代码，直接把现象和⽂件甩给  CodeBuddy ，让它⾃⼰查：
AI 按我说的先加⽇志、再⽤logcat抓⽇志，⽤adb注⼊操作复现，顺着⽇志⼀步步缩⼩范围。
很快它就定位到了根因：
定位清楚后，它在ImageAdapter加上了对  content URI 的识别，重新运⾏，相册缩略图全部正
常显示，选图、发送也都通了。模型能正确识别画⾯主体并给出对应回答，说明多模态理解链
路也跑通了。
@ImagePickerPage.kt  的图⽚加载不出来，请添加⽇志，⽤ adb ⾃⾏分析原因
相册组件给每张缩略图的图⽚地址是  content provider 格式（content://...），⽽模
板⼯程默认实现的  ImageAdapter  只处理了  base64 、 http 、 assets 、 ﬁle ⼏种来源，没有
认  content://这种  URI ，所以每张缩略图都解码失败、显示空⽩。
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
这个问题的链路其实很⻓：从  KuiklyAlbum组件取出缩略图信息，到跨端的  UI 组织，再到原
⽣图⽚控件上屏，每⼀步都可能是原因。但因为有  Kuikly AI 的知识库托底， AI 省去了研究框
架源码，我只给出问题现象、相关⽂件和分析要求，它就能⾃⼰加⽇志、⽤  logcat + adb 把根
因⼀路查到ImageAdapter这⼀层，就这样轻描淡写地把问题解决了。它再⼀次扮演了⼀个资深
Kuikly 开发的⻆⾊。
14:00 - 17:30 ｜ 迭代优化：把 " 能⽤ " 磨成 " 好⽤ "
⽂字和图⽚链路都通了，剩下的就是细节打磨。产品体验的反复推敲，在原⽣开发⾥最磨⼈，
也最容易出现平台不⼀致。⽽跨端框架的优势正在于此：⼀次修改，三端同步改好；配合
Kuikly AI ，很多修改进⼀步简化成了⼀句  Prompt 。
我基本是⼀条⼀条把问题丢给  AI ，它改完我真机验证，再提下⼀个。
1 ）键盘遮挡输⼊框
最先碰到的是⽼问题：键盘弹起来，把输⼊框挡住了。
我让  AI 监听  keyboardHeight，⽤外层容器的paddingBottom把输⼊区顶上去。它顺⼿还处理
了⼀个细节 ——Kuikly 的键盘事件要挂在Input / TextArea上，⽽ChatSession内部的输⼊框
不暴露这个事件，于是它在⻚⾯内挂⼀个代理  Input 承接  Kuikly 的键盘事件回调。这个绕法挺
地道，不是我提示的。
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
2 ）鸿蒙上新建会话不⽣效
在鸿蒙端验证时发现⼀个偏功能性的  bug ：新建会话后，历史列表⾥始终只有那⼀条旧会话。
把现象交给  AI ，它顺着路由链路定位到根因落在鸿蒙的RouterAdapter，这是  Kuikly 处理⻚⾯
跳转的模块，鸿蒙端默认的RouterAdapter没有考虑 " 先openPage再  closePage" 的边界场景。
因为有  Kuikly AI 的知识库托底，仅⼀轮对话就解决了问题。
3 ）拍照 / 相册⼊⼝：从  ActionSheet 改成宫格按钮
⼀开始点 "+" 弹的是系统  ActionSheet 。我觉得这不够 " 聊天  App" ，要求改成更常⻅的、类似微
信那种在输⼊框下⽅展开的宫格快捷⼊⼝。
这⼀条反⽽最折腾，⼀开始  AI 没意识到快捷⼊⼝⾯板和键盘抬升是互斥关系，从⾯板切到键盘
的⼀瞬间，输⼊框会抬升 " ⾯板  + 键盘 " 的双重距离，跳⼀下才落回正常位置。描述澄清了好⼏
轮， AI 才把⾯板和键盘收敛到同⼀套底部抬升逻辑⾥，共享同⼀个抬升量，保持输⼊框位置稳
定，问题彻底解决。
这也印证了⼀个共识： AI 从  0 到  1 很快，但从 " 能⽤ " 到 " 细腻 " ，还是得靠⼈⼀轮轮盯着调。
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
4 ）各⻚⾯  UI 统⼀
最后是收⼝。选图⻚、⽹⻚⻚这些后加的⻚⾯， UI ⻛格和主聊天⻚、会话列表⻚对不⻬。我直
接让  AI 把ImagePickerPage、WebViewPage  对⻬到  ChatPage、SessionListPage的设计规范
上。
它先⾃⼰读了两个主⻚⾯，提炼出⼀套规范 —— 紫⾊渐变背景、 44dp 透明导航栏、‹返回按
钮、 17sp ⽩⾊居中标题、浅⾊内容区 —— 再把另外两个⻚⾯逐项对⻬。这种 " 先归纳现有规
范、再套⽤到新⻚⾯ " 的做法，⽐我⼀条条描述样式⾼效得多。
17:30 - 18:00 ｜ 验收复盘：⼀天，⼀码三端，⼀个能⽤的  AI 聊天  App
到傍晚，这个  App 已经在  Android 、 iOS 、鸿蒙三端真机上都跑通了。
回看⼀下它最终具备的能⼒：
⽂本  / 图⽚消息发送
拍照、相册选图
AI 流式回复（ SSE ⻓连接）
Markdown 渲染、点链接打开⽹⻚
多模态图⽂理解
本地会话管理与历史恢复
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
这不是⼀个截图演示⽤的  demo ，⽽是⼀个交互完整、三端⼀致、真的能装到⼿机上聊起来的
应⽤。⽽这⼀切，⼀个⼈、⼀天就做完了。
思考总结
Kuikly 解决了什么
如果⽤传统三端原⽣开发这样⼀个  App——iOS 、 Android 、鸿蒙各派⼀⼈，设计只做⼀次，但
每块各端相关功能都要写三遍：
换成  Kuikly ⼀码三端，同样的功能只需⼀份代码：
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
从  30 ⼈天到  7.5 ⼈天， Kuikly 最直接节省的，是这种重复劳动的成本，这个成本可能是开发者
的⼯时，也可能是  AI 的  token 开销。
更深⼀层节省的，是重复决策。拿 "ActionSheet 改成宫格按钮 " 来说 —— 伴随布局调整，还要连
带解决键盘抬升与附件⾯板的冲突、 UI 配⾊不协调等⼀连串问题，来回调了好⼏轮才稳下来。
但所有这些轮次，都只在  shared 层发⽣了⼀次。如果没有  Kuikly ，就要在  Android 、 iOS 、鸿
蒙上各来⼀遍，还要额外确保三端⾏为对⻬。⼀码多端省掉的，正是这种 " 同⼀件事做三遍 " 的
乘数效应。
AI 解决了什么
7.5 ⼈天，是⼀个  Kuikly 熟⼿的⼯作量。⽽这次接上  AI 后，实际只花了约  7.5 ⼩时：
从  7.5 ⼈天压到  1 天，靠的不是  AI ⼀秒⽣成⼏千⾏，⽽是  Kuikly AI 让它真的 " 懂  Kuikly" 。这
⼀天最⼤的感受是：在  Kuikly AI 的  Skills 和  Rules 加持下， AI 不⽌是⼀个 " 会写  Kotlin 的通⽤
模型 " ，⽽更像⼀个熟悉  Kuikly 的资深开发。具体体现在⼏件事上：
⾃定义  Module 写得很地道。 SSE 和图⽚压缩这两个框架没覆盖的能⼒， AI ⽤kuikly-
expand-api技能补⻬ ——commonMain 定义接⼝、三端各实现  native 桥接，结构和官⽅
Module 如出⼀辙，不⽤我去纠正 "Kuikly 的  Module 到底该怎么写 " 。
DSL 和响应式理解到位。  ⻚⾯结构、组件⽤法、状态绑定都拿捏得准。消息列表、流式回
复这些要随状态⾃动重渲染的地⽅，它直接⽤observable把数据和  UI 绑起来，写法很贴合
Kuikly 的范式。
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
⾃定义组件、扩展原⽣也不在话下。  为了监听键盘，它⾃⼰加了⼀个零尺⼨的代
理Input；为了对接相册的content://地址，它改对了  ImageAdapter—— 这些都是要懂
Kuikly 渲染层和原⽣接缝才能下⼿的活。
知道什么时候复⽤、什么时候⾃⼰写。 该⽤AiMessageText就不再造  Markdown 轮⼦；该
扩展能⼒就⽼实补  Module ；遇到问题（相册缩略图）能⾃⼰logcat + adb把根因查
到ImageAdapter，⽽不是把报错原样丢回来。
这些恰恰是过去  AI 写客户端代码最容易翻⻋的地⽅ —— 凭记忆瞎猜私有  API 。 Kuikly AI 把框架
知识喂给模型，相当于补⻬了 " 资深  Kuikly 开发 " 的上下⽂，让它在正确的知识边界内⼯作。
"AI + Kuikly" 是当下客户端开发效率最⾼的组合之⼀。
这⼀天下来，我的体验是， Kuikly 消灭了跨端的重复劳动， AI 消灭了框架层⾯的样板劳动，剩
下留给⼈的是产品判断、体验打磨、⼯程把关。说得更具体⼀点 ——"AI + Kuikly" 让⼀个客户
端开发，真的有了 " ⼀个⼈顶⼀个三端⼩队 " 的体感。把繁琐交给  Kuikly 和  AI ，把判断⼒和创造
⼒留给⾃⼰。
关于  Kuikly
当前 Kuikly 已经开源，有兴趣和有需要的产品，可以通过以下⽅式访问  Kuikly 仓库和⽂档，欢
迎 Star 、 Watch 与体验：
👉  Github 仓库 | 📚官⽅⽂档
Kuikly 框架属于腾讯端服务联盟（ tds.qq.com ）的重要成员，欢迎关注及了解更多信息：
●腾讯端服务官⽹：TDS 腾讯端服务
●TDS Framework 官⽹：跨平台框架
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
阅读 7820
留⾔
还没有留⾔，来写⾸评
写留⾔
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
````


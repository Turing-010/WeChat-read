# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
AI 编程的下半场来了？学会⽤ Agent  Skill 解决编程的痛点问题
2026 年 3 ⽉ 2 ⽇ 01 : 36⼴东腾讯技术⼯程 164 ⼈
作者： bookerzhao
【推荐语】
最近我们在折腾  Agent Skills ，想把云开发（ CloudBase ）这些年攒下的经验打包给  AI 。实战
下来发现，最折磨⼈的不是  AI 不会写代码，⽽是它写的代码“ 只能活在本地 ”，以及它“ 总是不
听规矩 ”。
这篇⽂章主要分享两点实操复盘，希望能帮⼤家少⾛点弯路：
1. 让  AI ⽣成的代码能直接上线：⼤家可能都遇到过， AI 写的代码  Demo 感⼗⾜，但⼀上线
就全是安全隐患。我们尝试给  AI 注⼊底座感知，让它学会⽤底座原⽣认证代替脆弱的传
参，⽤安全规则代替接⼝ “ 裸奔 ” ，解决代码 “ 死在本地 ” 的尴尬。
2. 解决 “AI 有  Skill 却不爱⽤ ” 的⽑病：最让⼈头疼的是，明明配好了  Skills ， AI 却视⽽不
见，⾮要凭直觉盲⼲。我们会分享如何通过 “ 总纲 + 插件 ” 的结构，配合简单的⼯程拦截，把
AI 的技能激活率从  20% 硬拉到  84% 。
希望能给同样在研究  Skills 和  AI 开发的朋友⼀点参考，让  AI 交付的代码不再只是 “ 看着挺
美 ” ，⽽是真正稳健。
现状： Vibe Coding 的  " 本地舒适区 "
最近，开发者都在享受  Vibe Coding 的快感。在⽤户本地的   localhost  ⼀顿操作， UI 漂亮得
像成品，但魔法往往在 “ 上线 ” 瞬间戛然⽽⽌。
如何把  8 年云端经验装进你的  AI 开发⼯具，让 AI 从 " 实习⽣ " 变成 " 持证上岗的专家 " 。分
享如何⽤  Agent Skill 解决  AI Coding 领域的痛点问题，也分享如何解决  AI 不调⽤  Skill
等实践技巧。
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
AI 的代码逻辑还不错，但它⽆法感知真实的后端底座，导致⽣成的 “ 局部最优解 ” 难以落地，⽆
法简单的⽣成⽣产级可⽤的应⽤。
世界上最遥远的距离，是从   localhost 到真实访问的距离。 AI 填补了代码量的空⽩，却填补
不了⼯程底座的断层。
有什么办法可以解决这个问题吗？这⾥就需要提到  Skills 。
什么是  Skills
Skills 最早是  Anthropic 在  2025 年  10 ⽉给  Claude Code 加的⼀个功能，它是⼀套包含指
令、脚本和资源的能⼒包。把专业知识、步骤、代码打包成 “ 技能包 ”。
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
从本质上讲，⼀个  Skill 就是⼀个包含   SKILL.md  ⽂件的⽂件夹。该⽂件包含元数据（⾄少包
括   name 和   description）以及告诉  Agent 如何执⾏特定任务的指令。 Skills 还可以捆绑脚
本、模板和参考材料。
my-skill/
├── SKILL.md          # 核⼼：指令  + 元数据
├── scripts/          # 可选：可执⾏代码
├── references/       # 可选：参考⽂档
└── assets/           # 可选：模板、资源
如果把  AI ⽐作⾼材⽣， Skills 就是他的  “ 岗位操作⼿册 ” 。它不改变  AI 的智商，但它通过注⼊
程序性知识（ Procedural Knowledge ），让  AI 知道在你的特定环境下， “ 正确且⾼效 ” 的操作标
准是什么。
Agent Skill [1]在  2025 年  12 ⽉正式成为开放规范，⽬前已有包括  Claude 、 Cursor 、 VS
Code 、 GitHub Copilot 、 OpenCode 等主流 AI 开发⼯具宣布兼容⽀持。
Agent Skills 是⼀种轻量级、开放式的格式，⽤于通过专业知识和⼯作流扩展  AI Agent
的能⼒。
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
Skills 的⼯作原理：渐进式加载（ Progressive Disclosure ）
Skills 通过渐进式加载来⾼效管理上下⽂（ Context ），确保  Agent 在拥有强⼤能⼒的同时不会
因信息过载⽽变得迟钝：
1. Discovery （发现）：启动时， Agent 仅加载每个  Skill 的名称和描述。这⾜以让它在处理
请求时，判断哪些  Skill 可能与当前任务相关，⽽不会耗尽上下⽂窗⼝。
2. Activation （激活）：当任务与某个  Skill 的描述匹配时， Agent 才会按需将该  Skill 的完
整   SKILL.md  指令读⼊当前上下⽂。
3. Execution （执⾏）： Agent 遵循指令执⾏任务，并根据需要动态加载引⽤⽂件或运⾏捆绑
的脚本代码。
这种⽅法让  Agent 保持极⾼的响应速度，同时能够像 “ 随⾝携带百科全书 ” ⼀样，在需要时⽴即
获取深度专业知识。
⾏业⼤佬们已经在⾏动：
Vercel 发布了 `react-best-practices`[2]，解决  AI 乱写  React 导致的性能问题，将  React 专
家⼗余年经验你浓缩为最佳实践。
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
Remotion  推出视频制作  Skill[3]，让  AI 学会⽤代码 " 剪辑 " 视频
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
Vercel 推出了  skills 命令[4]来快速安装  Skills 到各个⼯具中，这是当前热门的  skills 列表。
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
这些  Skills 解决的核⼼问题是：让  AI 拥有特定领域的 " ⼯程直觉 " 。
那么，当你的应⽤需要落地到云端时，谁来给  AI 注⼊ " 后端直觉 " ？
CloudBase Skills ：把  8 年云端经验打包给  AI
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
云开发  CloudBase[5]  作为⾃  2018 年起就推出  Serverless 服务的团队，也推出CloudBase
Skills[6]。
Skills 是软件层⾯的 “ 岗位⼿册 ” ，⽽  CloudBase 则是承载代码落地的 “ 全栈底座 ” 。
许多  AI ⽣成的代码之所以 “ 死在本地 ” ，是因为  AI 往往只负责写逻辑，却不知道如何对接复杂
的⽣产环境。 CloudBase 为  AI 提供了⼀套⾼度抽象的基础设施，让  AI 写出的逻辑能⽆缝运
⾏在公⽹：
全栈托管与部署能⼒：⽀持前端静态⽹页与后端逻辑的快速部署，让项⽬从   localhost  真
正变成可访问的在线  URL 。
多端原⽣⾝份认证：打通了  Web 、⼩程序等多种⾝份源。 AI ⽆需⼿写复杂的登录逻辑，通
过  Skills 直接调⽤底座的认证能⼒，实现秒级接⼊。
数据库底座：同时提供⽂档型（ NoSQL ）与  SQL 型数据库能⼒。更重要的是，底座原⽣
集成了⾯向  C 端的权限控制机制，确保  AI ⽣成的每⼀⾏查询都运⾏在物理隔离的安全沙
箱中，从根源规避越权风险。
它将  CloudBase ⽀撑⽇均  10 亿次  API 调⽤、服务超过  330 万开发者的真实经验，翻译成了
AI 听得懂的指令。
举⼀些  CloudBase Skills 如何为  AI 注⼊⽣产级标准的场景：
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
场景⼀：⾝份认证 —— 拒绝 “ 相信前端输⼊ ”
错误做法
习惯于让前端通过   userId 传参给后端。
风险：这是典型的 “ 防君⼦不防⼩⼈ ” 。攻击者只需拦截请求并修改参数，即可实现横向越
权，访问任何⼈的私密数据。
正确做法
加载   auth-wechat Skill 后， AI 会被强制要求放弃前端传参，转⽽利⽤云底座的原⽣链路。
Before ( 脆弱逻辑 ):
// 实习⽣  AI ：相信⽤户传来的  ID
const { openid } = event.params; 
const user = await db.collection('users').doc(openid).get();
After ( ⽣产级标准 ):
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
// 专家  AI ：利⽤底座原⽣上下⽂，不可伪造
const { OPENID } = cloud.getWXContext(); 
const user = await db.collection('users').doc(OPENID).get();
场景⼆：数据安全 —— 从 “ 接⼝裸奔 ” 到 “ ⾏权限 ”
错误做法
倾向于直接暴露数据库接⼝。如果你的  API 逻辑稍有疏忽，数据库对攻击者⼏乎是 “ 裸奔 ” 状
态。
正确做法
Skill 会引导  AI 将权限校验  下沉到数据库⼊⼝，直接驱动底座的  安全规则（ Security
Rules ）。
实现改变：不再单纯写查询逻辑，⽽是为集合定义   auth.uid == doc._openid 规则。
价值：防御性编程的闭环。  即使业务逻辑代码出现  Bug ，底座依然能从物理层⾯拦截任何
⾮本⼈数据的越权修改。
场景三： AI 集成 —— 消灭  Hardcoded ，三⾏代码闭环
接⼊⼤模型是当前最热的需求，但  AI 往往给出的是 “Demo 级 ” 的代码，完全忽略了⽣产环境
的安全与⾼可⽤要求。
错误做法
将  API Key 硬编码在前端，写出⼀坨混乱的逻辑来处理流式输出（ Streaming ），既不安全也
不稳定。
⼯程准则：安全性应由底座的原⽣互信保证，⽽⾮依赖前端输⼊的⾃觉。
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
正确做法
Skill 注⼊了⽣产级  AI 接⼊规范，将复杂的封装逻辑简化为底层  SDK 的原⽣调⽤。
安全加固： Key ⾃动托管在云端环境变量，前端实现  “ 零泄露 ”。
⼏⾏代码调⽤  AI ⼤模型 ，⾃动处理流式响应。
// CloudBase Skills 实现的⽣产级  AI 调⽤
const model = wx.cloud.extend.AI.createModel("hunyuan-exp");
const res = await model.streamText({
data: {
    model: "hunyuan-turbos-latest",
    messages: [{ role: "user", content: " 介绍⼀下李⽩ " }],
  }
});
// 使⽤  textStream 获取增量⽂本
forawait (const text of res.textStream) {
console.log(" ⽂本⽚段 :", text);
}
核⼼价值
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
“AI 提供了逻辑的上限，⽽  CloudBase Skills 守住了⼯程的下限。 ”
安装  CloudBase Skills
在你的终端输⼊以下命令，为你的  AI 助⼿注⼊ “ ⽣产级直觉 ” ：
npx skills add tencentcloudbase/skills
即可安装我们提供的多个  Skills 到你的开发⼯具中。
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
CloudBase Skills 完整列表
我们将  Skills 按照实际开发中的职能进⾏了归类，确保  AI 在不同环境下调⽤正确的  SDK 和⼯
具。
这种分类不仅是为了⽅便开发者查阅，更是为了在  Discovery （发现阶段）降低  AI 的认知负
荷，实现精准的按需挂载。
核⼼理念：环境即边界（ Environment as Boundary ）
在展开列表前，我们需要阐述这套架构的底层设计：总纲路由，三端隔离。
物理隔离： Web 、⼩程序、 Node.js 的同名⽅法逻辑各异。我们将它们拆分为独⽴插件，
从物理层⾯杜绝  AI 在⼩程序⾥写出  Web SDK 语法的语义污染。
总纲引导： cloudbase-guidelines 是所有任务的默认⼊⼝。它像⼀个语义路由器，先判定
项⽬环境，再指引  AI 激活对应的⼦  Skill 。
完整技能矩阵
MCP vs Skills
在构建  AI 原⽣开发⽣态的道路上，我们始终坚持 “ 先打通，再优化 ” 的逻辑。
CloudBase MCP ：早已就绪的 “ ⼯程双⼿ ”
事实上，云开发  CloudBase 在  2025 年上半年的时候就推出了  CloudBase MCP[7]。作为
Anthropic 推出的⾏业标准协议， MCP 解决的是 “ 连接 ” 问题。
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
通过  MCP ，我们让  AI 助⼿真正拥有了操作腾讯云底座的结构化权限。它不再只是在对话框⾥
写代码，⽽是能直接查询云端状态、创建资源、拉取⽇志。⽬前， CloudBase MCP 已经⽀持
了包括  Cursor 、 Claude Desktop 、 VS Code 在内的多种主流⼯具，帮助⼤量开发者实现了  AI
与云端的物理连接，查看具体使⽤指引[8]。
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
CloudBase Skills ：后发制⼈的 “ 岗位⼿册 ”
既然有了  MCP 这双强有⼒的 “ ⼿ ” ，为什么我们还要推出  Skills ？
如果说  MCP 是让  AI “ 有权限 ” ⼲活，那么  Skills 就是让  AI “ 懂规矩 ” ⼲活。
在我们的规划中， Skills 是更上层的能⼒封装：
不仅仅是脚本：虽然  Skills 规范⽀持包含脚本（ Scripts ），但我们现阶段更侧重于“ 程序性
知识（ Procedural Knowledge ） ” 的注⼊。
更安全、更通⽤的专家直觉：正如前⽂提到的， AI 有了  MCP 虽然能执⾏脚本，但在云端
⽣产环境，盲⽬执⾏脚本不仅不安全，也不符合⼯程规范。 Skills 则是把我们  8 年的云端
填坑经验（如⾏权限隔离、原⽣上下⽂认证）变成  AI 的直觉。
为什么它们是黄⾦组合？
你可以单独使⽤其中之⼀，但组合使⽤才是  AI 编程的 “ 终极形态 ” ：
“MCP 提供了标准化的安全连接，⽽  Skills 提供了⽣产级的⼯程直觉。 ”
两者搭配，让  AI 从⼀个  “ ⼒⽓⼤但鲁莽的实习⽣ ” ，真正进化为⼀个“懂规矩、有权限 ” 的资
深云开发专家。
实战案例
CodeBuddy IDE 中已经内置了  CloudBase MCP 和  Skills ，在连接  CloudBase 之后会⾃动下
载  Skills 到你项⽬中。
````

## PDF 第 16 页

[原页](RAW.pdf#page=16)

````text
这⾥有⼀篇教程教你⽤免费云开发资源与混元 Token ，⼿把⼿教你⽤  AI 来开发⼀个  AI ⼩程
序。
````

## PDF 第 17 页

[原页](RAW.pdf#page=17)

````text
查看完整教程
还可以查看更多⼊门视频教程和⽂章[9]
````

## PDF 第 18 页

[原页](RAW.pdf#page=18)

````text
终章： Skills 落地踩坑与实战复盘
在做这套  Skills 的过程中，我们最⼤的感触是：现在的  AI 编程，其实处于⼀个 “ ⾼智商、低纪
律 ” 的阶段。 别看各⼤⼯具都号称⽀持  Skills ，真⽤起来全是坑。
以下是⼏个我们⾥跟  AI “ ⽃智⽃勇 ” 换来的经验教训：
1. 现状： AI 为什么会 “ 装死 ” ？
明明配了  Skill ， AI 还是视⽽不见。这背后的原因其实涉及⼤模型的两个底层逻辑：
注意⼒权重（ Attention Bias ）：在⼤模型的  Transformer 架构中，它会根据你的  Prompt
实时计算每个词的权重。当你聊得越深，你提的业务需求权重就会越⾼，⽽作为背景板的
外部  Skills 权重就会被 “ 稀释 ” 。
决策惰性（ Inference Laziness ）：调⽤  Skill 本质上是⼀次  Tool Use （⼯具调⽤）。模型
在推理时会进⾏ “ 路径评估 ” ：如果它觉得⾃⼰脑⼦⾥的预训练数据（通常是  Localhost 模
式）就能⽣成⼀段 “ 看起来正确 ” 的代码，它就会为了节省推理资源⽽跳过外部⼯具调⽤。
激活率落差：在我们的回归测试中，如果不加⼲预， AI 的主动调⽤率只有  20%  左右。它
宁愿 “ 盲⽬裸奔 ” ，也不愿意翻书。
2. “ 驯服 ” AI 的三套硬核解法
既然  AI 会产⽣决策惰性，我们就得⽤⼯程⼿段拉⾼它的 “ 警觉性 ” 。
⽅案  A ：最⼟但最稳的 “ ⾸⾏注⼊ ”
如果你的项⽬不容许犯错，就在提问的最开头带上这句 “ 咒语 ” ：
原理：利⽤  ⾸因效应（ Primacy Eﬀect ）。模型对输⼊序列最前端的信息具有天然的⾼关
注度。通过这种强⾏注⼊，能把  Skill 的激活率拉升。
强烈建议⼤家在试⽤过程中也带上这句  Prompt ，或者按照⽅案  B 来执⾏。
⽅案  B ：项⽬级的 “ 家法 ” (System Rules)
在项⽬根⽬录创建   CLAUDE.md  或   AGENT.md，增加项⽬级别的约束规则。这样就不⽤每
次都在  prompt 中  携带上⾯的咒语，不过这个⽅法也存在⼀定的缺陷，相⽐每次都⾸⾏注
⼊，随着对话的上下⽂越来越长，也会存在  AI 不遵循的情况，接下来就可以看看⽅案  3 的解
法。
# CloudBase Workflow
You MUST read the cloudbase-guidelines skill FIRST when working with
CloudBase projects.
````

## PDF 第 19 页

[原页](RAW.pdf#page=19)

````text
0. You MUST read the cloudbase-guidelines skill FIRST when working with CloudBase project
1. 评估：写代码前，必须显式评估可⽤  Skills 列表。
2. 承诺：必须在输出中陈述 “ 我需要调⽤某个  Skill” 的理由。
3. 执⾏：禁⽌跳过规矩直接写代码。
⽅案  3 ：⾃动化 “ 强制拦截 ” (Forced Eval Hook)
如果说前两个⽅案是靠 “ 嘴 ” 叮嘱  AI ，那⽅案  3 就是靠“ 物理拦截 ”
技术专家  Scott Spence 在他的实测中发现，最有效的⽅式是利⽤编辑器的  Hook （钩⼦）机
制。
它的本质是 “ 中间件 ”：这不再是你⼿动输⼊的  Prompt 。通过配置（如   .claude/settings.jso
n），脚本会在你按下回车的那⼀刻，⾃动拦截并 “ 魔改 ” 你的问题。
强制 “ 表态 ” 才能 “ ⼲活 ”：这个钩⼦会强制  AI 在输出任何代码前，必须先⽣成⼀段  评估报
告。 AI 必须逐⼀陈述：“当前有哪些  Skill 可⽤？针对这个需求，我需不需要调⽤它们？理
由是什么？ ”
消除 “ 决策惰性 ”： AI 有个⽑病，只要它觉得脑⼦⾥的旧数据能糊弄过去，它就不会翻书。
但这种  Hook 强迫  AI 必须⽩纸⿊字写下 “ 我要⽤这个⼯具 ” ，⼀旦它在开头表了态，后⾯的
代码⽣成就会严格遵守这个承诺。
激活率的质变：根据  Scott 的数据，这种 “ 拦截 + 评估 ” 的⼿段能将激活率从  20% 暴⼒拉升
到  84%
延伸阅读：How to Make Claude Code Skills Activate Reliably[10]
3. 架构复盘：为什么必须是 “ 总纲  + 独⽴插件 ” ？
在开发过程中，我们发现  AI 最⼤的⽑病是“ 端不分 ”。它分不清⼩程序、 Web 和  Node.js 的环
境边界。我们没有搞⼀个 “ 全家桶 ” Skill ，⽽是采⽤了  “1 个总纲  (Guidelines) Skill + 21 个独
⽴  Skill” 的分布式架构。这背后有三个核⼼逻辑：
A. 解决 “ 语义污染 ” 与环境误判
Web 、⼩程序、 Node.js 的  SDK ⽅法名极其相似（如都有   init,  callFunction）。
痛点：如果全塞进⼀个  Skill ， AI 经常在写⼩程序逻辑时，顺⼿掏出  Web 端的语法。这种
语义污染是造成代码⽆法上线的元凶。
解法：我们将  Skill 按端进⾏物理拆分。配合   cloudbase-guidelines  这种  “ ⼊⼝点 ” (Entry
Point) ，先指挥  AI 判定项⽬环境（如：识别到   app.json  即为⼩程序）。
收益：环境判定后， AI 只会加载相关的⼦  Skill 。这把⼲扰项直接屏蔽掉，搜索空间缩⼩了
90% ，推理精度⾃然⼤幅提升。
B. 开发者可以 “ 精准点菜 ”
痛点：全能包（单体架构）太重。当你想让  AI 专门解决 “ 微信⽀付 ” 或 “ 安全规则 ” 这种特定
问题时， AI 的注意⼒会被庞⼤的全量⼿册稀释。
````

## PDF 第 20 页

[原页](RAW.pdf#page=20)

````text
解法：独⽴插件⽀持局部强化。你可以直接下令：“调⽤   auth-web  检查实现⼿机号登
录 ”。
收益：这种设计允许开发者直接⼲预  AI 的决策路径。在  AI 逻辑混乱时，通过唤起特定⼦
Skill 强⾏把它的思维拉回到正确的窄道上。
未来规划
我们将持续推出：
⼩程序集成微信⽀付集成技能
⼩程序集成虚拟⽀付技能
⼩游戏集成云开发技能
云函数部署全栈后端应⽤技能
更多全栈应⽤开发模板和技能等
欢迎访问
CloudBase Skills GitHub 仓库[11]
CloudBase MCP GitHub 仓库[12]
了解更多详情！
写在最后：从 “ 代码⽣成 ” 到 “ ⽣产级交付 ” 的跨越
折腾了这么多  Skills 之后，我们最⼤的感触是：AI 编程的⽣产⼒，不取决于模型能写出多么
精妙的逻辑，⽽取决于你对它⽣成的代码具备多少 “ ⼯程约束⼒ ” 。
1. 核⼼本质：将 “ 隐性经验 ” 转化为 “ 程序性知识 ”
⽬前的  Agent 依然处于 “ ⾼智商、零经验 ” 的状态，它们是博学的 “ 实习⽣ ” ，却对真实的物理底
座缺乏敬畏。CloudBase Skills 的本质，是给  AI 注⼊⼀套⼯程化的 “ 肌⾁记忆 ” 。  通过   guide
lines 的语义导航和原⼦  Skill 的强约束，我们将云开发⼋年来沉淀的填坑经验（如⾏权限隔
离、多端原⽣上下⽂、⾼并发限流）转化为了  AI 的前置判定条件。这种程序性知识
（ Procedural Knowledge ）的注⼊，让  AI 真正理解了 “ 正确且安全 ” 的交付标准。
2. 范式转换： Agent 必须具备 “ 环境感知⼒ ”
Agent 进化的下⼀站，不仅仅是  Reasoning （推理）的增强，更是对  Infrastructure （基础设
施）感知⼒的补齐。
Skills 守住⼯程下限：它是⼀套 “ 防呆协议 ” 。通过场景化⼯作流和报错锚点，强制  AI 在编
写阶段就化解鉴权漏洞和多端环境差异，彻底终结 “ 代码只活在   localhost”的幻觉。
````

## PDF 第 21 页

[原页](RAW.pdf#page=21)

````text
CloudBase 承载逻辑上限：作为全栈底座，它让  AI 的逻辑输出不再是⽹页⾥的⽂本，⽽
是能直接部署、调通、并产⽣真实业务价值的⽣产级资源。
3. 确定性是  AI 开发的唯⼀度量衡
我们不应该期待  AI ⾃动变得 “ 完美 ” ，⽽应该通过⼯程⼿段让它变得 “ 稳定 ” 。AI 提供逻辑的上
限， Skills 守住⼯程的下限，⽽  CloudBase 则是承载这⼀切的物理底座。
我们正处于从 “ 氛围感编程  (Vibe Coding)” 向 “ ⽣产级交付 ” 跨越的节点。如果你也厌倦了在对话
框⾥修  Bug ，欢迎安装  CloudBase Skills 。给你的  AI ⽴个规矩，让它真正从⼀个 “ 聊天搭⼦ ”
进化为能帮你上线产品的 “ 资深合伙⼈ ” 。
如有问题或建议，欢迎在评论区交流。
名词解释
Vibe Coding：⼀种依赖  AI 直觉、快速⽣成原型但缺乏⼯程严谨性的编程⽅式。
Procedural Knowledge：程序性知识。指关于 “ 如何操作 ” 的知识，让  AI 掌握特定场景下
的标准作业流程（ SOP ）。
MCP：模型上下⽂协议。 AI 的“ 连接器 ”，让其能直接操作数据库、⽂件系统或云资源。
Agent Skills：能⼒插件包。 AI 的“ 专家⼿册 ”，注⼊特定领域的最佳实践和⼯程规范。
横向越权：安全漏洞。指攻击者通过篡改  ID 等参数，⾮法访问到同级别其他⽤户的数
据。
安全规则：底座级权限控制。在数据库⼊⼝处强制执⾏访问校验，是防御越权的核⼼⼿
段。
⽴即开始
在你的终端输⼊以下命令，为你的  AI 助⼿注⼊ “ ⽣产级直觉 ” ：
npx skills add tencentcloudbase/skills
参考资料
[1]  Agent Skill : https://agentskills.io/
[2]  react-best-practices: https://vercel.com/blog/introducing-react-best-practices
[3]  视频制作  Skill: https://x.com/Remotion/status/2013626968386765291
[4]  Vercel 推出了  skills 命令 : https://skills.sh/
[5]  云开发  CloudBase: https://tcb.cloud.tencent.com/
[6]  CloudBase Skills: https://github.com/TencentCloudBase/Skills
[7]  CloudBase MCP: https://github.com/TencentCloudBase/CloudBase-MCP
[8]  查看具体使⽤指引 : https://docs.cloudbase.net/ai/cloudbase-ai-toolkit/
[9]  查看更多⼊门视频教程和⽂章 : https://docs.cloudbase.net/ai/cloudbase-ai-toolkit/tutorials
[10]  How to Make Claude Code Skills Activate Reliably: https://scottspence.com/posts/how-to-make-clau
de-code-skills-activate-reliably
````

## PDF 第 22 页

[原页](RAW.pdf#page=22)

````text
阅读 1 . 3 万
[11]  CloudBase Skills GitHub 仓库 : https://github.com/TencentCloudBase/Skills
[12]  CloudBase MCP GitHub 仓库 : https://github.com/TencentCloudBase/CloudBase-MCP
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
留⾔
还没有留⾔，来写⾸评
写留⾔
````

## PDF 第 23 页

[原页](RAW.pdf#page=23)

````text
````


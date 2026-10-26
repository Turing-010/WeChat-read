# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
当整个团队开始 0  ⼈⼯ Coding ：⼀份万字 AI  Native 研发实战⼿册
腾讯程序员 2026 年 4 ⽉ 3 ⽇ 04 : 07⽇本原创 腾讯技术⼯程 473 ⼈
作者： binxiong
写在前⾯
如果你也在⽤  AI 写代码，你⼤概率经历过这样的场景：
打开  CodeBuddy ，对着对话框敲下⼀段需求描述， AI " 唰唰唰 " 吐出⼀段代码。你看了看，好
像对？复制粘贴，跑⼀下 —— 报错了。于是开始新⼀轮的 " 对话 - 调试 - 再对话 " 循环。
运⽓好的话，折腾半⼩时能搞定。运⽓不好，你发现  AI 写的代码和项⽬架构完全不搭，甚⾄
⽤了⼀个你们团队根本没有的库。
这不是  AI 的问题，是我们 " ⽤法 " 的问题。
我们团队在  2025 年就开始⼤规模使⽤  AI 辅助编码，标准软件、产品市场、极光平台都跑通
了实际案例。但随着使⽤深⼊，⼀个共识越来越清晰：
2026 年初，我们正式决定 ——全⾯转向  AI Native 研发模式，⽬标是 "0 ⼈⼯  Coding"。
这篇⽂章，就是这段旅程的全记录。
⼀、为什么要搞  AI Native ？ " 辅助编码 " 到底差在哪？
先说个残酷的事实：即便团队⾥的  AI ⽼⼿，⽤  AI 辅助编码的效率提升也很难超过  50%。原
因不是模型不够聪明，⽽是我们的协作⽅式有结构性缺陷。
导语： 2023 年我们开始⽤  AI 辅助解决问题， 2025 年我们验证了  AI Coding 的可⾏性，
2026 年我们决定更进⼀步 —— 不再让  AI 当 " 打字员 " ，⽽是让它当 " 施⼯队长 " 。这篇⽂章
记录了我们团队在  AI Native 研发模式落地过程中的思考、踩坑和最终形成的⼀套可复制
的⽅法论。
把  AI 当打字员⽤，天花板很低。把  AI 当施⼯队⽤，才有真正的效率⾰命。
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
当前研发⽤  AI 的真实画⾯
我总结了四⼤痛点，⼏乎每个⽤  AI 写代码的⼈都会踩到：
痛点 具体表现 根因
⼈机协作⽆
标准
效果完全取决于个⼈ " 提⽰词 " 功⼒，⽼⼿
提效明显，新⼿反⽽更慢
没有统⼀的  AI 交互规范，输⼊质量因⼈
⽽异
流程断点 ⼯程师变成了 " ⼈⾁翻译器 " ，在⽅案⽂档
和  IDE 之间来回搬运信息
设计⼯具和编码⼯具之间数据隔离，⽆法
⾃动传递上下⽂
上下⽂缺失AI 不认识你的项⽬，可能重复造轮⼦、
违反架构规范
AI ⽆法主动读取项⽬代码库和技术规范，
只能看到你⼿动喂的⽚段
⽂档脱节 ⽅案写进  iWiki 就再没更新过，新⼈⼊职
只能 " 考古 " 代码
⽂档和代码不在同⼀个版本控制系统⾥，
天然失同步
核⼼⽭盾就⼀句话：⼈与  AI 的交互缺乏规范，导致输出质量不可控。
所以我们需要的不是 " 更好的提⽰词技巧 " ，⽽是⼀套系统性的⽅法。
⼆、我们的回答： OpenSpec + CodeBuddy 全链路⽅案
什么是  OpenSpec ？
如果把开发⼀个功能⽐作盖⼀栋房⼦：
以前的做法：你（⼯程师）像个包⼯头，脑⼦⾥装着模糊的房⼦样⼦，跑到砖⼚（ AI ）
喊 " 来 100 块砖 " ，再跑到⽔泥⼚（另⼀个  AI ）喊 " 来两袋⽔泥 " 。 AI 不知道你要盖什么，只
能听你零散的指令，盖出来的东西千奇百怪。
OpenSpec 的做法：你的核⼼⼯作是和  AI ⼀起把建筑图纸画清楚。图纸审批通过后， AI
施⼯队就能根据这份唯⼀的、标准的图纸，全⾃动、⾼质量地完成施⼯。
本质上，OpenSpec 是⼀套机器和⼈都能理解的 " 研发契约 "。
⽬标态：⼈做什么， AI 做什么？
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
我们重新定义了  AI 时代研发⼈员的⾓⾊ ——从执⾏者变成指挥者：
阶段 AI 负责 ⼈负责
需求分析提炼需求、发现遗漏、结构化输出需求⽂档优先级判断，审批需求边界
⽅案设计 ⽣成技术⽅案、架构图、接⼝定义、风险清单技术选型拍板，安全审查
代码开发根据设计⽅案进⾏多⽂件编码、补充注释和单测评审关键代码，控制合并门禁
测试验证⽣成测试脚本、执⾏回归测试、分析失败原因审核⾼风险场景，最终放⾏决策
发布上线 校验实现是否与需求⼀致，提供发布清单审批发布窗⼝，处理事故升级
⼈的核⼼⾓⾊只有三个：决策、审批、把关。
其他的？让  AI 去⼲。
三、代码开发阶段的落地实践（我们是怎么做到 "0-Coding" 的）
3.1 核⼼⼯作流：三步⾛
我们把整个代码开发流程压缩到了三个指令：
Step 1 ： /opsx:propose — 先想清楚，再动⼿
/opsx:propose 帮我⽣成⼀个关于  [ 新增⽤户权限控制模块 ] 的变更
AI 会⾃动在  openspec/changes/[ 变更名 ]/  ⽬录下⽣成：
⽂件 作⽤ 通俗理解
proposal.md 需求背景与⽬标 " 为什么做 " 和 " 做什么 "
design.md 技术⽅案与架构决策 " 怎么做 "
tasks.md 带复选框的实施清单AI 的 " 施⼯单 "
specs/ 规范增量 本次变更的 " 差异记录 "
原则：严禁直接让  AI 写⼤段业务代码，必须先⽣成规划⽂档。
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
为什么这⼀步⾄关重要？  因为这些⽂件就是  AI 编码时的全部上下⽂。你在这⾥多花  10 分钟
审查，编码阶段能省  2 ⼩时的返⼯。
Step 2 ： /opsx:apply — 让  AI 按图施⼯
/opsx:apply [ 变更名称 ]
这⼀步  AI 会：
读取  tasks.md  中的清单
结合  design.md  和  proposal.md 的完整上下⽂
跨⽂件批量⽣成 / 修改代码
每完成⼀项⾃动在  tasks.md  ⾥打钩  ✓
开发者此时只需要做⼀件事： Code Review 。
Step 3 ： /opsx:archive — 让规范活起来
MR 通过后执⾏：
/opsx:archive [ 变更名称 ]
系统⾃动将本次规范增量合并到  openspec/specs  主⽬录，清空变更草稿。
这意味着什么？  你的项⽬⽂档永远和代码保持同步。没有 " 僵⼫  Wiki" ，没有 " 代码才是⽂
档 " 的⽆奈。
3.2 完整六步⼯作流
实际项⽬中，我们把核⼼三步扩展成了更严谨的六步：
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
关键卡点： Step 2 的  Review 是质量的⽣命线。tasks.md  建议控制在  15 项以内，避免  AI
因上下⽂过长产⽣幻觉。
3.3 前端页⾯开发的额外⼀步
如果变更涉及前端页⾯，我们在  Step 2 和  Step 4 之间加了⼀个原型审查环节：
在  With 平台上画好原型  →  团队确认  →  截图 / 链接贴回  design.md  →  再执⾏  /opsx:ap
ply
为什么？ Proposal 和  Design 解决的是 " 做什么 " 和 " 怎么做 " ，但对前端来说还缺 " 页⾯长什么
样 " 。跳过这步直接让  AI 写  UI ，返⼯成本远⼤于提前画⼀版原型。
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
四、让  AI " 懂 " 你的项⽬：三⼤武器库
光有⼯作流还不够。 AI 再聪明，如果不了解你的项⽬，写出来的代码也只是 " 通⽤代码 " ，不
是 " 你的代码 " 。
我们围绕  CodeBuddy 的三⼤机制，构建了⼀套完整的统⼀规范体系：
知识库  → 让  AI " 知道 "我们的项⽬
MCP   → 让  AI " 连接 "我们的⼯具   
Skills → 让  AI " 掌握 "我们的⽅法
4.1 知识库： AI 的项⽬记忆
知识库分两个通道注⼊  AI ：
通道⼀： OpenSpec specs/（核⼼记忆）
这就是项⽬的 " 活⽂档 " 。 AI 执⾏  /opsx:apply  时会⾃动读取，了解系统当前所有功能。每
次  /opsx:archive  后⾃动更新，始终与代码保持同步。
通道⼆： MCP 外部知识（辅助记忆）
通过  MCP 协议连接  Knot 知识库平台，存放⽆法⽤  specs ⽂件表达的内容：业务术语表、架
构决策历史、踩坑记录等。
知识类别 具体内容 来源
业务知识 产品功能说明、核⼼业务流程 iWiki ⽂档
架构知识 系统架构图、模块依赖、技术选型说明iWiki + Git
项⽬规范 ⽬录结构约定、数据模型定义、接⼝契约OpenSpec specs/
历史决策 技术选型原因、已知限制 iWiki + OpenSpec
常见问题 ⾼频问题及解决⽅案、排错指南 iWiki ⽂档
4.2 MCP ： AI 的⼯具连接层
MCP 让  AI 能直接访问团队的内部⼯具，消除 " 复制粘贴 " 式的跨⼯具搬运。
我们团队配置了以下  MCP ：
MCP ⼯具 连接⽬标 AI 获得的能⼒
TCS Component 前端组件库 查询组件使⽤规则，确保风格统⼀
TAPD MCP TAPD 需求平台 直接查询原始需求 /Bug 单
iWiki MCP ⽂档平台 直接检索设计⽂档、架构⽂档
极光流⽔线  MCP 部署平台 触发构建、查看部署状态
实际效果举例：以前⼯程师需要先打开  TAPD 看需求  →  理解  →  切到  IDE 描述给  AI 。现在  AI
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
通过  MCP 直接读  TAPD 原始需求，信息零损耗传递。
4.3 Skills ： AI 的专业技能包
Skills 是团队沉淀的标准化操作流程（ SOP ），封装成  AI 可复⽤的 " 技能包 " 。我们统⼀管理
在  ted.aurora/tcsc-skills  仓库中，按业务域分类，⽬前涵盖产品市场、前端组件库、⼯程实
践、运维中⼼、运营中⼼等多个领域。⼤家也可以通过  SkillHub 市场  来进⾏预览 , 后续我们也
会上架 Knot. 下⼀章会以  openspec-installer 为例，深度解剖⼀个⽣产级  Skill 的完整构造。
4.4 三⼤机制如何协同⼯作？
以⼀个典型的代码开发任务为例：
三者的关系可以⽤⼀句话概括：知识库让  AI " 知道 " 我们的项⽬， MCP 让  AI " 连接 " 我们的⼯
具， Skills 让  AI " 掌握 " 我们的⽅法。
五、深度解剖  openspec-installer ：⼀个  Skill 是怎么炼成的
5.1 这个  Skill 解决什么问题？
新⼈⼊职，或者团队开启⼀个新项⽬，⾸先要做的就是 " 搭环境 " 。在没有  openspec-installer
之前，这个过程是这样的：
1. 打开  Wiki ，找到安装指引（先找到正确的那篇  Wiki 就要  10 分钟）
2. 安装  Node.js （版本不对？换⼀个重来）
3. 全局安装  OpenSpec CLI （ npm 权限问题？ sudo ？ nvm ？）
前⾯提到  Skills 是团队经验的标准化封装。说起来容易，做起来呢？这⼀章我们拿
openspec-installer 这个  Skill 做⼀次完整的 " 庖丁解⽜ "—— 从⽂件结构到设计决策，从安
装流程到版本管理，让你看到⼀个⽣产级  Skill 的全貌。
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
4. 在项⽬中执⾏  openspec init（⽬录错了？重来）
5. ⼿动编辑  openspec/config.yaml（漏填了？ AI ⽣成的代码不符合规范）
6. 配置  MCP 服务（ iWiki 、⼯蜂的  URL 是什么？ Token 怎么拿？）
7. 安装项⽬需要的  Skills （装哪⼏个？从哪下载？版本对不对？）
8. 搭建知识库⽬录（ docs/ 下该有什么结构？）
⾄少  1 ⼩时，踩坑了可能半天。⽽且每个⼈踩的坑还不⼀样。
openspec-installer 把这  8 步压缩成了⼀句话：
请执⾏  curl -fsSL http: （内部 skill 命令 , 可以根据下⽂⽣成⼀个类似的安装指令即可）
AI 读到这个  SKILL.md 后，会⾃动完成所有步骤，全程不需要⼈⼯⼲预。
5.2 ⽂件结构：每个⽂件都有存在的理由
openspec-installer/
├── SKILL.md                          # 灵魂：600+ ⾏的完整安装  SOP
├── version.json                      # 版本控制元数据
├── scripts/
│   ├── INSTALL_MAC_LINUX.sh          # macOS/Linux 环境⾃动安装
│   ├── INSTALL_WINDOWS.ps1           # Windows 环境⾃动安装
│   ├── install_skills.sh             # 项⽬  Skills 批量安装
│   ├── check-skill-updates.sh        # 所有  Skills 版本检测
│   └── self_update.sh                # Skill ⾃身热更新
└── templates/
    ├── mcp-servers.json              # MCP 配置模板（含认证信息）
    ├── skill-bundle.json             # 项⽬默认  Skill 套装清单
    └── openspec-config-awareness.md  # Bridge Rule 模板
注意这不是⼀个简单的 " 安装脚本 "—— 它是⼀个包含  SOP 、⾃动化脚本、配置模板、版本管
理的完整系统。下⾯逐⼀拆解。
5.3 SKILL.md ： AI 的 " 施⼯蓝图 "
SKILL.md 是整个  Skill 的核⼼，它定义了  AI 应该按什么步骤做什么事。它的  frontmatter 使⽤
统⼀的元数据格式：
---
name: openspec-installer
description: 项⽬初始化⼯具。⾃动安装  OpenSpec 开发环境，同时配置  MCP 服务、
  批量安装  Skill 、搭建项⽬知识库⽬录、⽣成  OpenSpec 索引⽂件、检查  Skill 版本更新。
  当⽤户提到安装  OpenSpec 、配置  OpenSpec 环境、初始化项⽬、或  openspec init 时使⽤此  Skill 。
version: 0.4.3
author: binxiong
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
center: 公共
module: openspec-installer
tags: [openspec, setup, installation, initialization, mcp, skills]
---
description 字段的措辞经过仔细斟酌 —— 它同时承担两个职责：让⼈理解这个  Skill 做什么，
以及让  AI 知道什么时候该触发这个  Skill（通过关键词匹配）。
正⽂则是⼀套严格的分步  SOP （ Standard Operating Procedure ），包含  7 个主要步骤：
步骤 做什么 关键设计
Step 0 ⾃⾝版本检查 MCP 优先  →  静默跳过（不阻塞安装）
Step 1 检测操作系统 ⾃动识别  macOS/Linux/Windows
Step 2-4 安装  Node.js + OpenSpec CLI 跨平台脚本，幂等（已装不重装）
Step 5 补全  conﬁg.yaml 引导⽤户填写技术栈和业务背景
Step 6a openspec init ⽣成  OpenSpec 项⽬结构
Step 6a-1 ⽣成  Bridge Rule 解决 "AI 不知道要读  conﬁg.yaml" 的问题
Step 6b 配置  MCP 服务 Token 交互  + 安全防护（ .gitignore ）
Step 6c-6g 安装  Skills + 知识库  + 版本检测 批量操作，⼀步到位
Step 7 告知⽤户下⼀步 安装完成后的使⽤指引
每个步骤都是可执⾏的  bash 代码块， AI 读到后直接执⾏。同时每个步骤都设计了幂等性——
重复执⾏不会出问题。这意味着安装中断了可以随时重来。
5.4 三个关键设计决策
openspec-installer 的开发过程中，我们做了⼏个重要的设计决策，值得展开说说。
决策⼀： Bridge Rule—— 解决 " 链路断裂 " 问题
这是最有意思的⼀个设计。
OpenSpec 的  config.yaml  ⽀持⾃定义  rules 字段，⽐如：
# openspec/config.yaml
rules:
  archive:
    - 归档前检查：确认已创建  MR
    - 归档后更新：⾃动更新  INDEX.md 索引
问题是：AI 不知道要去读这个⽂件。
openspec init  ⽣成的  SKILL.md 是静态的，不包含 " 去读  conﬁg.yaml rules" 的指令。结
果就是：你⾟⾟苦苦在  conﬁg.yaml ⾥配了⼀堆规则， AI 执⾏  archive 的时候完全⽆视。
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
我们的解决⽅案是在安装时⾃动⽣成⼀个  Bridge Rule ⽂件：
# Step 6a-1：⽣成到  .codebuddy/rules/ ⽬录
cp "$SKILL_DIR/templates/openspec-config-awareness.md" \
   ".codebuddy/rules/openspec-config-awareness.md"
这个⽂件的内容⾮常短（只有  10 ⾏），但作⽤关键 —— 它像⼀个 " 指路牌 " ，告诉  AI ：
它使⽤  alwaysApply: true（每次会话⾃动加载）， context 开销可忽略不计。
这个设计背后的思想是：不把规则内容复制到  Bridge Rule ⾥（那样  conﬁg.yaml 改了  Bridge
Rule 也要改），⽽是只做 " 指路 "—— 保持  conﬁg.yaml 作为  single source of truth 。
这个看似简单的设计经历了两个版本迭代： v0.4.2 ⾸次引⼊时⽤了  alwaysApply: false
（ AI ⾃⾏判断是否加载），实测发现偶尔漏判； v0.4.3 改为  alwaysApply: true，问题彻
底解决。
决策⼆： Token 交互 —— 在  SKILL.md 指令层完成，⽽⾮  bash 脚本
MCP 服务需要  PAT Token 才能认证。怎么让⽤户配置  Token ？
直觉的做法是在  bash 脚本⾥⽤  read -p  提⽰⽤户输⼊。但  CodeBuddy 的  bash 执⾏环境
是⾮  TTY 的——read -p  会导致脚本挂起。
我们的解法是把  Token 交互写在  SKILL.md 的  SOP ⾥，让  AI 在对话中完成：
🔑  配置  MCP 服务需要你的个⼈访问令牌（ PAT ）。
请前往以下地址获取  Token ：
👉  https://token 申请⽹址
获取后请将  Token 粘贴到这⾥。
如果你想跳过此步骤，请直接回复" 跳过 "。
AI 获取到  Token 后，⽤  Python 脚本将  mcp-servers.json  模板中的  <your_token
>  占位符替换为真实  Token ，⽣成最终的  .mcp.json。
同时，在  Token 交互之前，还有⼀个安全防护步骤—— ⾃动将  .mcp.json  加⼊  .gitign
ore，防⽌含有  Token 的⽂件被意外提交到  Git 仓库。这个步骤⽆条件执⾏，即使⽤户跳过
了  Token 配置也会⽣效（因为⽤户之后可能⼿动配置）。
# Step 6b-0：幂等地将  .mcp.json 加⼊  .gitignore
if grep -qxF '.mcp.json' ".gitignore"; then
    echo "[INFO] .gitignore 已包含  .mcp.json ，跳过 "
" 当你执⾏  OpenSpec 操作时，先去读  openspec/config.yaml  中的  rules 。 "
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
else
    echo ".mcp.json" >> ".gitignore"
fi
决策三：版本检查的三级降级策略
openspec-installer ⾃⾝也有版本更新。怎么在安装时检测新版本？
直觉的做法是  curl git.woa.com 的  raw ⽂件。但该地址需要⾝份认证，在⾮交互环境下永
远  302 到登录页。
我们设计了三级降级策略：
1.  优先：通过⼯蜂  MCP 服务查询仓库中的  version.json （需已配置  Token ）
2.  降级：如果在仓库⽬录内，直接读取本地  version.json
3.  兜底：静默跳过版本检查，不阻塞安装
脚本通过环境变量  MCP_REMOTE_VERSION  接收  MCP 的查询结果（因为  bash 脚本⽆法直
接调⽤  MCP ，但  AI 可以在调⽤脚本前通过  MCP 获取版本信息并传⼊）：
# self_update.sh 中的版本获取逻辑
if [[ -n "${MCP_REMOTE_VERSION:-}" ]]; then
    remote_version="$MCP_REMOTE_VERSION"
    # MCP 查询成功，使⽤该版本
elif command -v git &>/dev/null; then
    # 降级： git clone --depth 1 获取
else
    # 兜底：静默跳过
fi
核⼼原则是：辅助功能的失败不应该阻塞核⼼功能。  版本检查是辅助功能，安装环境是核⼼
功能。
5.5 version.json ：不只是⼀个版本号
{
  "version": "0.4.3",
"name": "openspec-installer",
"description": " 项⽬初始化⼯具  — 安装  OpenSpec 环境、配置  MCP 服务、批量安装  Skill...",
"release_date": "2026-03-20",
"git_repo": "git@git.woa.com:ted.aurora/tcsc-skills.git",
"skill_path": "skills/ 公共 /openspec-installer",
"changelog": {
    "0.4.3": " 更新： bridge rule 改为  alwaysApply: true ，确保  100% 覆盖率 ",
    "0.4.2": " 新增： OpenSpec 配置感知  bridge rule ，修复  config.yaml rules 消费链路断裂问题 ",
    "0.4.1": " 更新：场景五  SOP 标注为兜底机制 ",
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
    "0.4.0": " 新增：归档后索引⾃动更新规则 ",
    "0.3.0": " 新增：归档前  MR 检查规则 ",
    "0.2.0": " 新增： MCP 配置与  Skill 批量安装 "
  }
}
这不只是给⼈看的  changelog——self_update.sh  会解析这个  JSON ，⽐较本地和远端
版本号，在发现新版本时展⽰精确到每个版本的变更内容。
5.6 skill-bundle.json ：项⽬的 "Skill 套装 "
每个项⽬需要安装哪些  Skills 不需要⼿动记忆：
{
  "skills": [
    { "name": "atomic", "type": "local", "centerPath": " 产品市场 /atomic" },
    { "name": "operation-template", "type": "local", "centerPath": " 产品市场 /operation-temp
    { "name": "bug-fix", "type": "local", "centerPath": " ⼯程实践 /bug-fix" }
  ]
}
install_skills.sh  读取这个清单，批量安装所有  Skill 。新⼈⼊职不需要问 " 这个项⽬需
要装什么  Skill" ，跑⼀次  installer 就全齐了。
5.7 迭代历史：⽤  OpenSpec 管理  Skill 本⾝
openspec-installer 的每⼀次改进，本⾝就是⽤  OpenSpec 的  propose →  apply →  archive 流
程来管理的。最近⼀周的迭代记录：
版本 ⽇期 变更 OpenSpec Change
v0.4.3 3 ⽉ 20 ⽇Bridge Rule 改  alwaysApply: true config-awareness-always-app
ly
v0.4.2 3 ⽉ 20 ⽇ 新增  Bridge Rule 解决链路断裂add-config-awareness-rule
v0.4.1 3 ⽉ 20 ⽇ 版本号同步、场景五  SOP 优化 sync-skill-version-and-auth
or
v0.4.0 3 ⽉ 20 ⽇ 归档后索引⾃动更新规则archive-index-auto-update
v0.3.0 3 ⽉ 19 ⽇归档前  MR 检查  + MCP Token 重
构 archive-require-mr
每个变更都有完整的  proposal.md（为什么改）、design.md（怎么改）、spec.md
（规范增量）和  tasks.md（实施清单）。
这就是  dogfooding 的⼒量—— 我们⽤⾃⼰的⼯具来改进⾃⼰的⼯具，既验证了流程的可⾏
性，也确保了每次变更都有据可查。
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
5.8 为什么这套做法值得推⼴？
openspec-installer 不只是⼀个安装⼯具，它展⽰了⼀个  Skill 应该怎么做：
做法 带来的价值
SKILL.md 定义完整  SOP AI 照着做就⾏，不需要⼈⼯解释上下⽂
每个步骤都幂等 中断了可以随时重来，不怕搞坏环境
跨平台脚本 macOS/Linux/Windows 统⼀⼀套流程
配置模板预填 减少⼿动配置，降低出错概率
Bridge Rule 解决  AI ⼯具链之间的 " 链路断裂 " 问题
Token 安全防护 .gitignore + 跳过机制，防⽌凭证泄漏
三级降级策略 辅助功能不阻塞核⼼功能
version.json + 热更新 团队成员⽆感升级，永远⽤最新版
⽤  OpenSpec 管理⾃⾝ 每次改进都有  proposal + design + spec
⼀句话总结：⼀个好的  Skill ，写⼀次，全团队永久受益。⽽  openspec-installer 就是这个理
念的最佳实践 —— 它让 " 搭环境 " 这件最枯燥的事，变成了⼀句话的事。
六、从  0 到  1 的上⼿指南
6.1 环境搭建（ 10 分钟搞定）
前置条件：已安装  CodeBuddy （ CLI 版或  IDE 插件版，推荐  CLI ）
Step 1 ：安装  OpenSpec Skill
请执⾏  curl -fsSL http://内部 skill 命令 , 可以根据下⽂⽣成⼀个类似的安装指令即可。
Step 2 ：执⾏⾃动化初始化
和  AI 对话： " 帮我初始化  OpenSpec 项⽬ "
AI 会⾃动完成：
1. 检测 / 安装  Node.js 环境
2. 全局安装  @fission-ai/openspec@latest
3. 在项⽬根⽬录执⾏  openspec init，⽣成配置⽬录
Step 3 ：补全配置
打开  openspec/config.yaml，填写：
配置项 说明 ⽰例
技术栈 当前项⽬使⽤的语⾔ / 框架 TS/JS 、 Go 、 React
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
配置项 说明 ⽰例
代码规范风格 团队约定的编码风格ESLint Standard 、 Airbnb
核⼼业务背景 简述项⽬的业务领域 "电商订单管理系统 "
6.2 CLI 与  IDE 的最佳搭配
推荐策略： CLI 主攻， IDE 辅助。
⼯具 适⽤场景
CodeBuddy CLI 执⾏  /opsx:propose、/opsx:apply 等核⼼指令，跨项⽬协同
CodeBuddy IDE 审查修改  proposal.md / design.md ，解决  Git 冲突，单⾏逻辑优化
6.3 多项⽬联动（前后端同时开发）
my-fullstack-workspace/         ←  ⽗⽬录：在此启动  CodeBuddy CLI
├── web-frontend/               ←  前端仓库
│   ├── openspec/
│   └── src/
└── api-backend/                 ←  后端仓库
    ├── openspec/
    └── src/
在⽗⽬录下启动  CLI ， AI 拥有全局视⾓，⼀条指令同时搞定前后端：
/opsx:propose 新增⼀个查询订单列表的  API ，并在前端编写对应的调⽤逻辑与表格渲染
七、扩展⼯作流：给⾼阶玩家的 " 精细操控 "
核⼼三步对⼤多数场景够⽤了。但遇到复杂需求时，你可能需要更精细的控制 ——
开启扩展⼯作流
openspec config profile
# 选择  "Workflows only" → 勾选扩展命令（new、 ff 、continue、 verify ）
扩展指令速查
指令 作⽤ 什么时候⽤
/opsx:new 只创建空脚⼿架，不⽣成内容想⾃⼰控制⽣成节奏
/opsx:continu
e 步进式⽣成（先  Proposal →  Review →  再  Design ） 逐步审查，适合复杂需
求
/opsx:ff 快进⽣成，⼀次补全所有规划需求明确，想快速推进
⚠  config.yaml  是  AI ⽣成代码时的基础 " 宪法 " ，请务必认真填写。
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
指令 作⽤ 什么时候⽤
/opsx:verify AI 代码审计，⽐对  design.md 写完代码想让  AI ⾃查
/opsx:explore 探索模式，和  AI 讨论需求 不知道怎么开始时
安全提⽰：/opsx:explore  只讨论和输出⽂档，绝对不会动代码，放⼼使⽤。
⼋、团队协同实践：踩过的坑和定下的规矩
原⼦化变更原则
规则 说明
⼀次变更解决⼀个需求每次  Change 只对应⼀个明确的业务需求或  Bug
tasks.md 控制在  15 项以内 避免  AI 因上下⽂过长产⽣遗忘或幻觉
⼩步快跑 确保⼈⼯  Code Review 在可控范围内
" 规范即⽂档 " 原则
要求 说明
禁⽌绕过  OpenSpec 不要绕过流程直接⼿写⼤量核⼼业务逻辑
原因 否则会破坏 " 规范与代码 " 的同步性， Spec 沦为 " 死⽂档 "
收益 全员坚持  SOP →  交付质量标准化  →  交接和维护成本最低
MR 审查的双重视⾓
Review ⼈员在审查  MR 时要同时看代码和规划⽂档：
审查维度 内容 对照⽂件
代码逻辑 AI ⽣成的代码是否遵守约束条件design.md
架构合规 技术⽅案是否符合团队底线 proposal.md
需求覆盖 所有规范中定义的⾏为是否已实现specs/
九、写在最后
回头看这半年的实践，最⼤的感悟不是技术上的，⽽是认知上的：
AI 不是来替代程序员的，⽽是来重新定义 " 程序员 " 这个⾓⾊的。
以前，我们的核⼼价值是 " 能写代码 " 。现在，我们的核⼼价值是 " 能指挥  AI 写出正确的代
码 " 。这听起来像是降级，但实际上是升级 —— 你的注意⼒从 " 怎么实现 " 转移到了 " 做什
么 " 和 " 为什么做 " 。
openspec/specs/  ⽬录就是永远与代码保持⼀致的 " 活体⽂档 " ，替代传统的沉睡
Wiki 。
````

## PDF 第 16 页

[原页](RAW.pdf#page=16)

````text
这像极了软件⼯程发展史上的⼀次次跃迁：
从机器码到汇编：我们不再关⼼寄存器
从汇编到⾼级语⾔：我们不再关⼼内存地址
从写代码到  AI Native ：我们不再关⼼具体的代码实现，⽽是关⼼需求定义和架构决策
如果你的团队也在探索  AI Native 研发，希望我们的经验能帮到你。也欢迎随时交流 —— 毕
竟，在这个  AI 飞速进化的时代，没有⼈是 " 到达 " 了的，我们都还在路上。
附录：指令总速查表
指令 阶段 ⼀句话说明
/opsx:explore 探索 与  AI 讨论需求，沉淀⽂档，不写代码
/opsx:propose 规划 ⼀键⽣成全套规划⽂档
/opsx:apply 编码 严格按  tasks.md 清单⾃动编码
/opsx:archive 归档 合并规范增量到主⼲，清空草稿
/opsx:new 准备 创建空脚⼿架（扩展版）
/opsx:continue步进 逐⽂件⽣成，逐步审查（扩展版）
/opsx:ff 快进 ⼀次性补全所有规划（扩展版）
/opsx:verify 审计 AI 代码审计，⽐对  design.md （扩展版）
附录：项⽬⽬录结构
项⽬根⽬录 /
└── openspec/
    ├── config.yaml               ←  项⽬配置（技术栈、规范⻛格、业务背景）
    ├── specs/                   ←  归档区：系统功能的" 活⽂档 "
    │   └── [ 功能名称 ]/
    │       └── spec.md
    └── changes/                 ←  ⼯作区：进⾏中的变更提案
        └── [ 任务名称 ]/
            ├── proposal.md       ←  为什么做、做什么
            ├── design.md         ←  怎么做
            ├── tasks.md         ←  AI 的施⼯清单
            └── specs/           ←  变更增量
附录：常见场景速查
场景 操作
新项⽬⾸次配置 安装  Skill →  " 帮我初始化  OpenSpec 项⽬ " →  补全  conﬁg.yaml
接到新需求 /opsx:propose
  →  Review →  /opsx:apply  →  测试  →  提  MR
复杂需求不知如何下⼿ /opsx:explore
  和  AI 讨论
````

## PDF 第 17 页

[原页](RAW.pdf#page=17)

````text
阅读 3 . 1 万
场景 操作
需要更细粒度控制 开启扩展⼯作流  →  new + continue/ff
写完想让  AI ⾃查 /opsx:verify
MR 通过后 /opsx:archive [ 变更名称 ]
前后端联动 ⽗⽬录启动  CLI →  /opsx:propose  ⼀次性规划
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
留⾔ 1
超级、⼩⼩宇⼴东4 ⽉ 3 ⽇
写留⾔
38
````

## PDF 第 18 页

[原页](RAW.pdf#page=18)

````text
⾸评
写这么多是 ai ⽣成的吗？@元宝
````

## 采集与转写核验记录（非原文）

以下说明由本次核验添加；上方逐页文本保持文本层原样，图片与布局以PDF为准。

- PDF物理页 8,12,13：p.12 skill-bundle代码长行右侧裁切；内部安装命令和完整脚本不随材料提供

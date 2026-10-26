# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
深⼊解析 Chromium 的 AI  Coding  开发体系
腾讯程序员 Jun  1 , 2026 , 2 : 36  AM⼴东原创 腾讯技术⼯程 310  listened
作者： QQ 浏览器团队出品
⼀、整体介绍
Chromium 是全球最⼤的开源  C++ 项⽬之⼀，代码量超过  3500 万⾏。⾯对如此庞⼤的代码
库， Chromium 团队在源码仓库中构建了⼀整套  AI Agent 基础设施—— 不只是 " ⽤  AI 写代
码 " ，⽽是建⽴了⼀套完整的提⽰词管理、技能系统、知识库、评估体系和⼤规模⾃动化项
⽬。
AI Coding 相关内容集中在   agents/  ⽬录下：
chromium/src/agents/
├── ai_policy.md             # AI 使⽤政策
├── prompts/                 # 🔥  提示词系统（分层组合设计）
│   ├── common.minimal.md    # 核⼼指令层
│   ├── common.md            # 完整⼯作流层
│   ├── knowledge_base.md    # RAG 知识库
│   ├── templates/           # 平台模板层（ desktop/android/ios... ）
│   └── eval/                # 评估⽤例（15+ 个场景）
├── skills/                  # 🔥  技能系统（18+ 个可复⽤技能）
├── extensions/              # MCP 扩展（⼯具能⼒增强）
├── projects/                # AI 驱动的⼤型项⽬
└── testing/                 # Prompt 评估测试框架
Chromium 同时⽀持  Gemini CLI 、 Claude Code 、 GitHub Copilot 三种  AI ⼯具，核⼼的
Prompts 和  Skills 设计为跨⼯具复⽤。 AI 使⽤政策（ai_policy.md）的核⼼原则是：AI
是辅助⼯具，⼈类开发者始终是最终责任⼈。如果某位开发者违反了原则，则可能被剥夺提交
代码的权限。
笔者作为 QQ 浏览器的开发，研究了⼀下 Chromium 的 AI Coding 开发体系，希望从中学习
到⼀些东西。
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
下⾯逐⼀介绍各核⼼机制：AI Policy （ AI 使⽤政策）、Prompts （提⽰词系统）、Skills （技能
系统）、Knowledge Base （知识库）、Eval （评估测试） 和  Projects （⼤规模项⽬）。
⼆、 AI Policy ：⼈类始终是最终责任⼈
agents/ai_policy.md  是整个  AI Coding 体系的底层约束，定义了⼈与  AI 的责任边界。
核⼼规则如下：
规则 要求 违规后果
⾃审义务 作者必须在发送  Review 前⾃⾏审查并理解所有
代码，确保正确性、设计、安全性和风格达标
提交不理解的代码  →  剥夺  Commi
tter 权限，再犯  →  封禁账号
原创声明 ⽆论是否使⽤  AI ，作者必须声明代码为⾃⼰的原
创作品 —
⼈类回复⼈
类
如果  AI Agent 创建的  CL 或  Bug 收到了⼈类的反
馈，必须由⼈类操作者亲⾃回复违反项⽬⾏为准则
此外， Policy 还给出了推荐做法：在  CL 描述中说明  AI ⼯具的使⽤⽅式（如附上  prompt ）；
如果是通过设计⽂档  + prompt 驱动  AI ⽣成的代码，可以将设计⽂档⼀并提交到代码库。
⼀句话概括：AI 是⼯具，不是作者 —— ⼈类开发者对每⼀⾏代码负全责。
三、 Prompts ：分层组合的提⽰词体系
Prompts 是整个  AI Coding 体系的基⽯。 Chromium 没有使⽤⼀个巨⼤的单体提⽰词，⽽是设
计了⼀套四层分层组合的架构，开发者按需组合。
3.1 四层架构
┌─────────────────────────────────────────────────┐
│   第四层： Task Prompts （任务提示词）                   │
│   ⼀次性任务指令，如  /cr:gerrit/cl-description       │
├─────────────────────────────────────────────────┤
│   第三层： Templates （平台模板）                        │
│  desktop.md / android.md / ios.md / rust.md      │
├─────────────────────────────────────────────────┤
│   第⼆层： common.md （完整⼯作流）                      │
│  8  步标准编辑流程  + 知识库引⽤                        │
├─────────────────────────────────────────────────┤
│   第⼀层： common.minimal.md （核⼼指令）                │
│   构建、测试、编码、 JNI 等基础规范                      │
└─────────────────────────────────────────────────┘
开发者通过创建本地   GEMINI.md  ⽂件，⽤   @  引⽤组合不同层级的  prompt ：
# 桌⾯开发者的配置
@agents/prompts/common.md          # ⾃动包含  common.minimal.md
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
@agents/prompts/templates/desktop.md
Chromium 会使⽤脚本解析引⽤的  prompt ，最终形成⼀个完整的  system instruction  注⼊
AI ：
┌─────────────────────────────────────────────┐
│  System Instruction （系统指令）                │   ←  GEMINI.md 递归展开后⽣成
│  common.minimal.md 的内容                     │
│  + common.md 追加的⼯作流                      │     每次对话隐式⽣效
│  + desktop.md 的平台规范                       │     对⽤户不可⻅
├─────────────────────────────────────────────┤
│  User Prompt （⽤户提示词）                     │   ←  开发者实际输⼊的任务
│  " 帮我在  TabStrip 中实现分屏功能 "              │     每次对话动态变化
└─────────────────────────────────────────────┘
3.2 第⼀层： common.minimal.md — 核⼼指令
这是所有开发者共享的最底层指令，定义了  AI 在  Chromium 中⼯作的基本规范：
规范领域 核⼼规则 设计意图
构建 必须先确认构建⽬录和⽬标，未确认前禁⽌构建AI 猜错构建⽬录的代价太⼤，强制
先确认
测试 使⽤  tools/autotest.py  运⾏测试，不要提前
调⽤  autoninja（ autotest 会⾃动构建）避免重复构建
编码 Stay on task ：不修⽆关的  TODO 和  code healt
h；注释只写 " 为什么 " 不写 " 做了什么 "
AI 有 " 顺⼿修  TODO" 和 " 写废话注
释 " 的倾向，需要明确约束
JNI 定义  Java ↔ C++ 的  JNI ⽅法识别规则（@Called
ByNative、@NativeMethods）
即使⾮  Android 开发者也可能遇到
JNI 代码，所以放在最底层
预提交 完成后运⾏  git cl format + git cl presub
mit，只修⾃⼰改动引⼊的问题避免  AI 修复不相关的预存警告
3.3 第⼆层： common.md — 8 步标准⼯作流
这是  Chromium AI Coding 的核⼼⼯作流定义，所有代码编辑任务都必须遵循。以下是完整的
8 步流程（摘⾃源⽂件）：
Step 1: 深度理解代码（强制第⼀步，不可跳过）
  ├── 1a. 定位核⼼⽂件
  ├── 1b. 完整审计（读取每个⽂件的完整源码，总结控制流和所有权语义）
  ├── 1c. 陈述理解（向开发者确认理解是否正确）
  └── 1d. 反模式规避：
        • 绝不从函数名猜测⾏为，必须读源码实现
        • 必须检查⾄少⼀个调⽤点来理解⽤法
Step 2: 编写代码
  └── 只做需求要求的事
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
Step 3: 编写 / 更新测试
  ├── 优先向已有测试⽂件添加⽤例
  └── 没有则创建新测试⽂件
Step 4: 构建
Step 5: 修复编译错误
  ├── 为每个错误⾄少读取⼀个新⽂件
  ├── 找到并理解所有相关⽂件
  ├── 检查历史对话中是否出现过相同错误
  └── 绝不做投机性修复
Step 6: 运⾏测试
Step 7: 修复测试错误
Step 8: 迭代（循环  Step 4-7  直到全部通过）
其中  Step 1 的设计尤为关键 —— 它强制  AI 在写任何代码之前，必须先完整阅读所有相关⽂件
并向开发者确认理解。使⽤过  AI 写代码的同学应该深有体会，充分的上下⽂理解是保证代码
质量的关键，也有助于减少幻觉问题。
3.4 第三层： Templates — 平台模板
平台模板为不同平台的开发者提供特定的上下⽂和构建指令。 Chromium 提供了  desktop 、
android 、 ios 三套模板，每套都精确定义了该平台的⽂件命名规范、构建⽬标、测试运⾏⽅
式，确保  AI 不会在平台特定的细节上犯错。
以桌⾯平台（ desktop.md ）为例，这是与  Windows/Mac/Linux 开发最相关的模板：
Before starting any tasks, you MUST read the following files:
  * //docs/chrome_browser_design_principles.md   ←  浏览器架构设计原则
  * //docs/ui/views/overview.md                   ←  Views UI 框架概览
Build Targets:
  * chrome                 - 桌⾯  Chrome 主⼆进制
  * unit_tests             - 单元测试
  * browser_tests          - 集成测试
  * interactive_ui_tests   - 需要独占窗⼝管理器的  UI 交互测试
模板的关键设计在于：强制  AI 在动⼿之前先阅读平台架构⽂档。这确保了  AI 理解  Views 框
架的  Widget/View 层级、 Browser/Proﬁle 的所有权模型等桌⾯平台核⼼概念，⽽不是凭猜测
写代码。
3.5 第四层： Task Prompts — ⾃定义命令
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
Chromium 在   .gemini/commands/  中预定义了⼀系列可直接调⽤的任务提⽰词。每个命
令本质上是⼀段预写好的  prompt ，封装了特定环节的完整操作步骤：
命令 功能 核⼼逻辑
/cr:gerrit/fix-review-
comments
⾃动修复  Review
意见
获取未解决评论  →  逐条判断是否有信⼼修复  →
修复或标记
/cr:test/gen-gtests⾃动⽣成单元测
试
分析  git diﬀ →  定位测试⽂件  →  读取现有  ﬁxtur
e →  ⽣成⽤例  →  验证
/cr:gerrit/cl-descript
ion ⾃动⽣成  CL 描述 分析  diﬀ →  按  Chromium 规范⽣成标题 / 正⽂ /B
ug/Test 标签
/cr:git/pre-upload-che
cklist ⼀键预提交检查同步依赖  →  风格检查  →  移除调试⽇志  →  格式
化  →  presubmit
/cr:test/disable-test禁⽤失败的测试定位测试  →  添加  DISABLED_ 前缀  →  更新  BUI
LD.gn
3.6 Prompt 的维护机制
Chromium 使⽤了⼀套模板  + 注释的维护机制：
源⽂件是   .tmpl.md（如   common.tmpl.md），包含  HTML 注释形式的设计意图说明
通过   process_prompts.py  脚本⾃动去除注释，⽣成最终的   .md  ⽂件
PRESUBMIT 检查确保   .md  ⽂件与   .tmpl.md 保持同步
这意味着每条  prompt 规则背后都有为什么这样写的记录，⽅便团队迭代优化。
四、 Skills ：按需激活的专业技能
Skills 是  Chromium AI Coding 体系中的专家模块。与  Prompts （始终加载的通⽤指令）不
同， Skills 是按需激活的 —— 只有当⽤户的请求与某个  Skill 相关时， AI Agent 才会⾃动加载
对应的   SKILL.md  ⽂件。
⽬前  Chromium 已有  18+ 个  Skill，覆盖开发中的各种专业场景：
Skill 功能
feature-flag-removal 移除  Feature Flag （ 17 步完整  checklist ）
fuzzing 编写  Fuzz 测试（含环境配置、代码模板、验证流程）
histograms 管理  UMA 指标（元数据、所有权、过期时间）
cl-description ⽣成  CL 描述
git-cl-helper Git CL 操作辅助
chromium-docs ⽂档搜索
network-traffic-annotations ⽹络流量注解
nullaway NullAway 空指针检查
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
Skill 功能
policy-creation 企业策略创建
webui-lit-migration WebUI Lit 迁移
trace-analysis 性能  Trace 分析
utr 通⽤测试运⾏器
... 还有  Java 内存泄漏、 JNI 类型转换、 Chromebook 调试等
五、 Knowledge Base ： Agentic RAG 知识增强
5.1 设计理念
Chromium 的知识库不是传统的向量数据库检索，⽽是⼀套Agentic RAG—— 通过  prompt 指
令让  AI ⾃主判断应该去读哪些⽂档。其核⼼原则写在   knowledge_base.md 的开头：
## Core Principle: Consult, then Answer
You MUST NOT answer from your general knowledge alone. The Chromium codebase is
vast and specific. Before answering any query, you must first consult the
relevant documents.
强制  AI 不依赖⾃⾝的通⽤知识，⽽是在回答前先去读源码中的权威⽂档。
5.2 三层知识增强架构
知识增强同样采⽤多层架构：
┌──────────────────────────────────────────────────────┐
│   第三层： MCP 扩展  — 外部知识源                           │
│  blink-spec （ GitHub API ） / build-information 等         │
├──────────────────────────────────────────────────────┤
│   第⼆层： chromium-docs Skill — 本地⽂档检索⼯具               │
│  2000+ md ⽂件索引， Python 脚本辅助  AI 定位⽂档               │
├──────────────────────────────────────────────────────┤
│   第⼀层： knowledge_base.md — 静态路由表                   │
│   任务关键词  → ⽂档路径的  if-then 规则引擎                  │
└──────────────────────────────────────────────────────┘
5.3 第⼀层： knowledge_base.md — 静态路由表
这是最核⼼的机制。knowledge_base.md 被引⽤在   common.md 的末尾，成为  AI 上下
⽂的⼀部分。它本质上是⼀个任务→⽂档的  if-then 规则引擎：
核⼼编程模式路由：
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
AI 检测到的任务特征 路由到的⽂档 / 动作
涉及进程间通信（ browser-to-r
enderer ） 查找对应的  .mojom  ⽂件，理解  Mojo IPC 接⼝
涉及异步操作或线程 读取  docs/threading_and_tasks.md
涉及回调（base::OnceCall
back 等） 读取  docs/callback.md
修改  third_party/blink/r
enderer/  下的代码
必须
使⽤  WTF 容器（blink::Vector、blink::String）和  Oilpan
GC （Member<>、Persistent<>），禁⽌使⽤  STL 容器
功能开发路由：
AI 检测到的任务特征 路由到的⽂档
涉及⽤户偏好（ pref 、 PrefService ） components/prefs/README.md
涉及  UMA 指标（ histograms ） docs/metrics/uma/README.md
涉及  UKM 指标 tools/metrics/ukm/README.md
修改  BUILD.gn ⽂件 docs/imported/gn/style_guide.md
调试路由（最精细的规则）：
* For a "header file not found" error:
    1. Verify `deps` in BUILD.gn
    2. Verify `#include` path
    3. Regenerate build files: `gn gen <out_dir>`
    4. Confirm GN sees the dependency: `gn desc <out_dir> //failing:target deps`
    5. Check for issues: `gn check <out_dir> //failing:target`
* For a linker error ("undefined symbol"):
    → Check deps (use `gn desc`) and `is_component_build` in args.gn
* For a visibility error:
    → Add depending target to the `visibility` list
执⾏流程⽰例：
当开发者说 " 帮我在  Blink 中添加⼀个  CSS 属性并追踪  UMA 指标 " 时：
1. AI 分析任务关键词
2.  检测到  "Blink" → 路由规则触发：必须⽤  WTF 容器  + Oilpan GC
   → AI 读取  Blink C++ Style Guide
3.  检测到  "UMA 指标 " → 路由规则触发
   → AI 读取  docs/metrics/uma/README.md
4. AI 基于读取的权威⽂档⽣成实现⽅案
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
5.4 第⼆层： chromium-docs Skill — 本地⽂档检索⼯具
当第⼀层的静态路由⽆法覆盖时（⽐如⽤户问了⼀个不在路由表中的话题）， AI 可以激活   ch
romium-docs skill 进⾏动态搜索。
这个  Skill 实际上是⼀个辅助  AI 定位⽂档的  Python 脚本⼯具（chromium_docs.py）。 AI
通过命令⾏调⽤它，脚本在本地  JSON 索引中做匹配，返回⽂档路径列表，然后  AI ⾃⼰去读
取这些⽂档。整个流程如下：
AI 判断需要查⽂档  → 调⽤  python chromium_docs.py "mojo ipc"
→ 脚本在本地  JSON  索引中做字符串匹配  + 关键词匹配
→ 按权重排序，返回⽂档路径列表
→ AI 拿到路径后，⾃⼰去读取这些⽂档⽂件
索引范围：覆盖   docs/**/*.md、*/README.md、*/docs/*.md 等路径下的  2000+
个  markdown ⽂件，⾸次构建索引约  30 秒。
本地  JSON 索引的结构：脚本在建索引阶段（--build-index）会扫描源码树中  2000+
个   .md  ⽂件，对每个⽂件提取元信息，保存为  3 个  JSON ⽂件：
索引⽂件 结构 ⽤途
doc_index.j
son
{ "docs/threading_and_tasks.md": { t
itle, summary, content, keywords, ca
tegory, mtime }, ... }
主索引
，存储每个⽂档的标题、摘
要、完整内容、关键词、分类
和修改时间
keyword_ind
ex.json
{ "mojo": ["docs/mojo/README.md",
...], "sandbox": [...], ... }
关键词倒排索引
， key 是  Chromium 专有术
语， value 是包含该术语的⽂档
列表
category_in
dex.json
{ "ui": ["docs/ui/views/overview.m
d", ...], "network": [...], ... }
分类索引
，按  13 个预定义分类（如  Net
work Stack 、 User Interface
等）归类⽂档
其中   doc_index.json  中每个⽂档的字段通过   _parse_document  ⽅法提取：标题取
⾃  markdown 的  H1/H2 标题，摘要截取前  300 字有意义⽂本，关键词从内容中提取
Chromium 专有术语（最多  20 个），分类根据⽂件路径和内容关键词⾃动判定。
搜索机制：搜索时脚本遍历   doc_index.json  中的每条记录，⽤纯字符串匹配  + 权重打分
（⾮向量语义检索）。标题匹配权重最⾼（ ×4.0 ），其次是路径匹配（ ×2.5 ）、关键词匹配
（ ×2.0 ）、内容匹配（ ×1.0-1.5 ），近期修改的⽂档也会获得⼩幅加分。
最终，脚本会找到最匹配的⽂档，返回给  AI 。
为什么需要  3 个索引⽽不是  1 个？
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
这种三分索引的设计借鉴了搜索引擎的倒排索引  + 正排索引架构，旨在优化不同场景下的查
询效率和内存使⽤：
索引类型 ⽤途 优势
doc_index.json
主⽂档索引
，存储完整元信息⽤于相关性打
分和结果展⽰
提供⽂档的标题、摘要、内容等完整信息
⽤于计算匹配分数
keyword_index.j
son
关键词倒排索引
，快速定位包含特定关键词的⽂
档
O(1) 时间查找
，避免遍历所有⽂档，速度快  1000+ 倍
category_index.
json
分类索引
，⽀持按分类浏览和过滤
O(1) 时间获取分类⽂档
，⽀持分类维度的快速聚合
内存效率考虑：如果只有⼀个巨⼤的索引包含所有信息，每次搜索都需要将  2000+ 个⽂档的
完整内容（可能⼏⼗ MB ）加载到内存。⽽三分⽅案：
搜索时先通过  keyword_index （很⼩）快速定位候选⽂档路径
然后只从  doc_index 中读取候选⽂档的元信息进⾏打分
内存使⽤量减少  90% 以上
这种设计在搜索效率和内存使⽤之间取得了最佳平衡，特别适合  Chromium 这种⽂档量⼤但
搜索频率相对较低的场景。
索引的持久化与复⽤：值得注意的是，并不需要每次搜索都重建索引。脚本采⽤ " ⼀次构建，
持久复⽤ " 的策略：
⾸次使⽤（约  30  秒）：
  python chromium_docs.py --build-index
  → 扫描  2000+ md ⽂件  → ⽣成  3  个  JSON  ⽂件  → 持久化到磁盘
后续每次搜索（毫秒级）：
  python chromium_docs.py "mojo ipc"
  → 直接从磁盘加载已有  JSON  索引  → 内存中匹配打分  → 返回结果
脚本在初始化时（__init__  →   _load_indexes()）会尝试从磁盘读取已有的  JSON
⽂件，如果存在就直接使⽤，不会重新扫描源码树。只有当索引⽂件不存在时，搜索才会返回
提⽰信息，要求开发者⼿动运⾏   --build-index。
不过，脚本⽬前没有增量更新机制—— 如果源码树中的⽂档发⽣了变化（新增、修改、删
除），已有索引不会⾃动感知，需要⼿动重新运⾏   --build-index  重建。但考虑到
Chromium 的⽂档变化频率远低于代码变化频率，偶尔重建⼀次即可。
5.5 第三层： MCP 扩展  — 外部知识源
对于需要实时外部信息的场景，通过  MCP （ Model Context Protocol ）扩展获取：
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
blink-spec：通过  GitHub API 查询  W3C/CSS 规范的  Issue 和讨论
build-information：查询当前构建配置和状态
depot-tools：获取  depot_tools 相关的命令帮助
5.6 与传统  RAG 的对⽐
维度 传统  RAG Chromium 的  Agentic RAG
检索⽅式⽤户  query →  向量检索  →  返回  chunks AI ⾃主判断  →  按规则读取⽂件  →  按需搜索
知识来源 预构建的向量数据库 源码树中的原始⽂档（实时读取）
路由机制 纯语义相似度 静态规则表  + 动态搜索  + MCP 外部查询
更新⽅式 需要重新  embedding ⽂档随代码同步更新，索引按需重建
核⼼理念 被动检索 AI 主动查阅
（ "Consult, then Answer" ）
六、 Eval ： AI Agent 的评估测试套件
Chromium 不仅构建了  AI Coding 的基础设施，还为其建⽴了⼀套回归测试体系——agent
s/prompts/eval/  ⽬录。当系统提⽰词（如   common.md）发⽣修改时，团队可以⽤这
些评估⽤例验证  AI Agent 的表现是否退化。
6.1 评估⽤例概览
eval  ⽬录下有  15 个⼦⽬录，每个代表⼀个独⽴的评估任务，覆盖了⽇常开发中的典型场
景：
评估⽤例 任务类型 说明
adapt_builder 构建配置 参照已有  LUCI builder 创建新  builder
add_browser_test_coverage测试⽣成 为代码添加浏览器测试覆盖
add_gtest_coverage测试⽣成 为指定⽅法添加单元测试
class_refactor 重构 将嵌套结构体重构为独⽴类
fix_broken_test 修复测试 编译、定位并修复失败的测试
fuzzing Fuzz 测试 编写  FUZZ_TEST
cl-description CL 描述 ⽣成符合规范的  CL 描述
feature_flags_addFeature Flag 添加新的  Feature Flag
find_function
 / search_class 代码搜索 查找函数定义、类定义
build_file
 / build_target 构建 构建指定⽂件或⽬标
6.2 ⽤例结构
每个评估⽤例由两个核⼼⽂件组成：
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
prompt.md — 模拟⽤户输⼊的任务指令。例如   fix_broken_test：
I have a broken test called "DummyTest" in
third_party/blink/renderer/core/css/css_math_expression_node_test.cc.
Can you compile and run the test to figure out why it is failing,
then attempt to fix it?
eval.md  或   eval.promptfoo.yaml — 评估标准。eval.md  记录预期结果（修改了
哪些⽂件、达成了什么效果），eval.promptfoo.yaml  则是基于  promptfoo  框架的⾃动化
断⾔配置，可以精细检查：
tests:
  - assert:
    # 检查是否修改了正确的⽂件
    - type: python
      value: check_files_changed
      config:
        files:
        - services/network/public/cpp/schemeful_site_mojom_traits_unittest.cc
    # 检查⽂件内容：必须包含  FUZZ_TEST ，不能包含旧式  API
    - type: python
      value: check_file_content
      config:
        files:
          - path: '...unittest.cc'
            present: ['FUZZ_TEST', 'SchemefulSite']
            absent: ['LLVMFuzzerTestOneInput']
    # 检查是否调⽤了正确的构建命令
    - type: python
      value: check_tool_used_with_args_match
      config:
        tool_names: [run_shell_command]
        args_regexes: ['autoninja', 'out/fuzz']
6.3 设计理念
eval  ⽬录的本质是⼀套  **AI Agent 的 " 单元测试 "** ：
回归测试：修改提⽰词后跑⼀遍所有  eval ⽤例，确保  AI ⾏为没有退化
可复现：每个⽤例绑定特定的   Git-Revision，可在同⼀代码版本上重复验证
⾃动化：通过  promptfoo 框架可在  CI 上⾃动运⾏，检查⽂件变更、内容断⾔、⼯具调⽤
等
参考模板：这些⽤例同时也是开发者的任务参考 —— 遇到类似任务时，可以直接参考对应
的   prompt.md
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
6.4 测试框架： agents/testing/
eval/  ⽬录存放的是测试⽤例，⽽   agents/testing/  则是执⾏这些⽤例的测试框架
—— 两者的关系类似于  test_*.py ⽂件与  pytest 框架。
核⼼组件：
组件 职责
eval_prompts.
py 主⼊⼝脚本，⼀键发现、过滤、调度、执⾏所有评估⽤例
gemini_provid
er.py
promptfoo ⾃定义  Provider ，驱动  Gemini CLI 执⾏测试（写⼊  GEMINI.md →  设
置  system prompt →  stdin 传⼊  user prompt →  流式捕获输出）
workers.py并⾏执⾏引擎，每个  Worker 创建独⽴的  WorkDir （ btrfs 快照秒级创建，确保测试
隔离）
asserts/ ⾃定义断⾔脚本（ check_changes.py 检查⽂件变更、 check_tool_calls.py 检查⼯
具调⽤等）
关键设计：
隔离执⾏：每个测试在独⽴的  WorkDir 中运⾏（ btrfs 快照或  gclient-new-workdir ），测试
之间互不⼲扰
Pass@K 机制：⼀个⽤例运⾏  N 次，只要  K 次通过就算成功，适应  LLM 输出的⾮确定性
CI 级基础设施：⽀持  Swarming 分⽚并⾏、 Docker 沙箱隔离、 ResultDB 上报、 Skia Perf
性能看板，可在  CI 上⾃动运⾏
Telemetry 采集：从  Gemini CLI 的  OpenTelemetry 输出中提取  token ⽤量和⼯具调⽤记
录，⽤于性能追踪和断⾔验证
七、 Projects ： AI 驱动的⼤规模代码改造
agents/projects/  ⽬录存放的不是实战案例，⽽是真正在⽣产中运⾏的  AI 驱动的⼤规
模⼯程项⽬。与  Skills （解决单个任务）不同， Projects ⾯向长期的⼯程治理⽬标，包含完整
的  SKILL.md + 参考⽂档  + Python 脚本  + ⾃动化流⽔线。
⽬前有  3 个项⽬：
项⽬ ⽬标 核⼼机制
bedrock/modula
rize-chrome-bro
wser
将  chrome/browse
r/ 的巨型单体构建⽬
标拆分为独⽴模块
6 阶段流程：盘点⽂件  →  选择构建模式  →  ⽣成  BUIL
D.gn →  更新⽗级  BUILD →  修复  include 错误  →  验证
提交。 SKILL.md 长达  344 ⾏
code-health/ 代码健康⾃动化治理框
架
含  Hub 调度中⼼  + ⼦任务（ histogram-cleanup 清理
过期指标、 lint-sync 添加枚举同步守卫）。 AI ⾃动发现
候选项  →  置信度评估  →  创建分⽀  →  修改代码  →  验
证  →  提交到  Gerrit
modernization/ 代码现代化⾃动修复Python 框架  AutoFixer，将错误信息喂给  Gemini ⾃
动修复，验证后重试，最多  3 轮循环
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
Projects 与  Skills 的定位差异：
维度 Skills Projects
粒度 单个任务（如 " 移除⼀个  Feature
Flag" ）
⼤规模⼯程项⽬（如 " 模块化整个  chrome/browse
r"）
⾃动化程
度 AI 辅助，⼈类确认⾼度⾃动化，含发现脚本、验证流⽔线、⾃动提交
复杂度 ⼀个  SKILL.md 完整项⽬结构（ SKILL.md + 参考⽂档  + Python 脚
本  + 测试）
⼋、具体案例：以 " 实现页⾯分屏 " 为例
下⾯以⼀个具体的产品需求 ——" 实现页⾯的分屏 "—— 来完整推演  Prompts 、 Skills 、
Knowledge 如何协同⼯作。
8.1 需求拆解（⼈类主导）
产品经理提出： " 在桌⾯版  Chrome 中，⽀持同⼀窗⼝内左右并排显⽰两个  Tab" 。
⼈类⼯程师将其拆解为多个  CL（ CL 即  ChangeList ，等同于  GitHub 的  Pull Request ）
CL 1: 添加  Feature Flag （ kSplitView ）
CL 2: 修改窗⼝布局模型（ BrowserView ⽀持双  ContentsWebView ）
CL 3: 实现分屏控制器（ SplitViewController ）
CL 4: 添加  UI ⼊⼝（ Tab 右键菜单  + ⼯具栏按钮）
CL 5: 添加  UMA 指标追踪
CL 6: 编写  Browser Tests
8.2 CL 1 ：添加  Feature Flag — Prompts + Skills 协同
开发者告诉  AI ：
帮我添加⼀个  feature flag 叫  kSplitView ，
放在  //chrome/browser 组件下，默认  DISABLED_BY_DEFAULT ，
需要暴露到  about:flags 。
Prompts 层⾯：common.md 的  8 步⼯作流启动， AI 先进⼊  Step 1 （深度理解）。
仅推演，不代表 Chromium 开发中的真实⼯作流。
以下  CL 拆解是从实际代码提交记录逆向推演的。实测中，直接将产品需求输⼊  AI ， AI
并不能⾃主完成这样的拆解。下⾯的内容记录的是 AI 如何处理这些 CL 的。
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
Knowledge 层⾯：knowledge_base.md  中没有直接的  Feature Flag 路由规则，但   eva
l/feature_flags_add/  ⽬录下有预定义的评估⽤例， AI 可以参考其中的  prompt 模式。
Skills 层⾯：虽然没有 " 添加  Feature Flag" 的  Skill ，但有   feature-flag-removal Skill
可以反向参考。 AI 知道最终需要修改的⽂件包括：
chrome/browser/about_flags.cc
chrome/browser/flag_descriptions.h / .cc
chrome/browser/flag-metadata.json
tools/metrics/histograms/enums.xml
8.3 CL 3 ：实现分屏控制器  — Knowledge 深度参与
开发者给  AI 技术描述后，三层知识增强机制同时⼯作：
第⼀层（ knowledge_base.md 静态路由）：
检测到的特征 触发的路由 AI 的动作
代码在  chrome/browse
r/ui/views/
desktop.md 模
板
读取  docs/ui/views/overview.md 和  docs/chr
ome_browser_design_principles.md
需要修改  BUILD.gn knowledge_bas
e 规则 读取  docs/imported/gn/style_guide.md
第⼆层（ chromium-docs 本地检索⼯具）：
如果  AI 需要了解  BrowserView 的布局机制但静态路由没有覆盖，它会调⽤脚本搜索：
python chromium_docs.py "BrowserView layout ContentsWebView"
# 脚本在本地索引中匹配，返回： chrome/browser/ui/views/frame/README.md 等
# AI 再⾃⾏读取这些⽂档
第三层（ Prompts ⼯作流）：
AI 按  8 步⼯作流执⾏：
1. 读取   browser_view.h、contents_web_view.h、tab_strip_model.h 的完
整源码
2. 向开发者陈述理解并确认
3. 编写   split_view_controller.h/.cc
4. 修改   browser_view.h/.cc 和   BUILD.gn
5. 构建  →  修复编译错误  →  测试  →  修复测试错误  →  迭代
8.4 CL 5 ：添加  UMA 指标  — Skills 主导
开发者说： " 给分屏功能添加  UMA 指标追踪 " 。
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
Skills 层⾯：histograms Skill ⾃动激活，指导  AI ：
1.  确定指标名称（如  SplitView.Activated ）
2.  定位元数据⽬录（ tools/metrics/histograms/metadata/split_view/ ）
3.  更新  histograms.xml （添加  <histogram> 条⽬）
4.  更新  enums.xml （定义枚举值）
5.  设置过期时间（3  个⽉后）
6.  添加⾄少两个  owner
Knowledge 层⾯：knowledge_base.md  检测到  "UMA" 关键词，路由到   docs/metric
s/uma/README.md， AI 读取后获得完整的  UMA 规范。
8.5 提交阶段  — Task Prompts 加速
/cr:git/pre-upload-checklist    → ⼀键执⾏预提交检查
/cr:gerrit/cl-description       → ⾃动⽣成  CL 描述
/cr:gerrit/fix-review-comments  → ⾃动修复  Review 意⻅
8.6 三⼤机制的协同关系
                    ┌─────────────┐
                    │   开发者需求    │
                    └──────┬──────┘
                           │
                    ┌────── ▼ ──────┐
                    │   Prompts    │   ←  定义" 怎么做 "（8  步⼯作流）
                    │  ( ⼯作流引擎 ) │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌────── ▼ ──────┐ ┌── ▼ ───┐ ┌────── ▼ ──────┐
       │  Knowledge   │ │Skills│ │    Task      │
       │  ( 知识增强 )   │ │( 专业  │ │   Prompts    │
       │              │ │ 技能 )│ │  ( 快捷命令 )   │
       │ 告诉  AI      │ │ 告诉 AI│ │   加速关键      │
       │ " 去哪找信息 "  │ │" 如何  │ │   环节执⾏      │
       │              │ │ 做特定 │ │              │
       │              │ │ 任务 " │ │              │
       └──────────────┘ └──────┘ └──────────────┘
总结
Chromium 的  AI Coding 体系建⽴在⼀条底线和三⼤机制的精密协同之上：
1. AI Policy （使⽤政策） — 明确⼈与  AI 的责任边界：⼈类开发者对每⼀⾏代码负全责， AI
是⼯具⽽⾮作者
````

## PDF 第 16 页

[原页](RAW.pdf#page=16)

````text
2. Prompts （提⽰词） — 四层分层组合架构，从核⼼指令到平台模板到任务命令，确保  AI
在任何场景下都有正确的⾏为规范
3. Skills （技能） — 18+ 个按需激活的专业模块，将复杂任务（如移除  Feature Flag 的  17
个步骤）编码为可复⽤的  checklist ，确保不遗漏
4. Knowledge Base （知识库） — 三层  Agentic RAG 架构，从静态路由表到动态⽂档搜索
到外部知识源，确保  AI 基于权威⽂档⽽⾮通⽤知识⼯作
此外，完善的  Eval 评估体系（ 15+ 个评估⽤例  + ⾃动化测试框架）确保了整套  AI Coding 基
础设施在持续迭代中保持稳定可靠，不会因提⽰词修改⽽导致  AI ⾏为退化。
Chromium 的⽂档如此详尽，也并⾮⼀天两天的事情。查看提交记录可以发现，⽂档从  2015
年开始积累，跨越  11 年，总计  6445 次提交，逐步沉淀⾄今。agents/  ⽬录于  2025 年  7
⽉  10 ⽇创建，⽽  chromium-docs 这个核⼼  Skill 则是  2026 年  1 ⽉由⼀位微软⼯程师提交
的。
对于我们团队⽽⾔，如何积累出同等深度的⽂档体系，是落地  AI Coding 的关键挑战。
需要说明的是，本⽂仅从⼯程代码层⾯进⾏分析，并⾮  Chromium 真实完整的开发流程。
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
````

## PDF 第 17 页

[原页](RAW.pdf#page=17)

````text
阅读 1 . 2 万
留⾔
还没有留⾔，来写⾸评
写留⾔
````


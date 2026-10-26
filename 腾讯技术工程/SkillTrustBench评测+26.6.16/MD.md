# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
谁是 Agent  最强守⻔员？⾸个 Agent  技能安全评测基准
SkillTrustBench  正式发布
2026 年 6 ⽉ 16 ⽇ 02 : 33⼴东腾讯技术⼯程 4 ⼈
作者：⾹港中⽂⼤学（深圳） & 腾讯朱雀实验室
导语
随着  Agent 技能（ Skills ）快速融⼊  AI 应⽤⽣态，它正逐步成为全新的安全边界与供应链攻
击⼊⼝。为了防范恶意  Skill 导致的数据泄露与  Agent 劫持，构建安全可信的  Skill 运⾏环境
已成为⾏业共识。尽管  ClawHub 等主流技能市场已上线检测机制，开源社区也涌现出⼤量
扫描⼯具，但在实际落地中，⽤户常⾯临两难境地。
⼀⽅⾯，部分扫描⽅案偏向⾼召回但频发误报，极易导致安全告警疲劳；另⼀⽅⾯，部分⽅
案虽判定精准，却在⾯对隐蔽的对抗⼿法时容易漏报。此外，基于  LLM 的扫描器在切换底层
模型时研判偏好差异显著。在缺乏系统性评估标准的当下，⾏业亟需客观的衡量标尺，既⽤
于度量安全⽅案的检测效能，也⽤于评估  Skill 本身的安全可信度。
针对这些痛点，腾讯朱雀实验室 联合⾹港中⽂⼤学（深圳）吴保元教授课题组正式发
布  SkillTrustBench —— ⾸个⾯向真实落地场景、兼顾  Agent Skills 安全可信度与外部扫描⽅
案检测效能的双重评测基准。该基准从主流技能市场的  62,652 个  Skill 中提炼出  5,520 个评
测⽤例，涵盖九⼤类常⻅安全威胁，为评估并提升  Agent 技能的安全性提供客观参考。
从⾸期评测数据中，我们总结了⼏个关键点：
⼤模型底座表现：在本次评测中，Claude Opus 4.6 与  GLM 5.1  在安全扫描场景下展现
出极强的语义推理与安全约束理解能⼒，处于第⼀梯队；DeepSeek V4 Flash 与  Hy3
preview 则在性能与成本之间取得了优异平衡，性价⽐优势显著。
开源⼯具效能：以  OpenClaw  + Skill Vetter 为代表的轻量级开源审计⽅案，已具备发现
多数恶意  Skill ⻛险的基础能⼒，但在复杂噪声⼲扰下的误报控制上仍有较⼤优化空间。
Skill 本身的安全可信度：评测发现⼤量⾮恶意  Skill 同样存在不可信隐患。诸如硬编码凭
证 、敏感权限滥⽤、以及易受命令注⼊等不安全编码缺陷⼴泛存在，这些⾏为虽主观⽆
害，却因其⾃身的安全脆弱性，极易成为供应链劫持的⼆次攻击⼊⼝。
项⽬官⽹（点击阅读原⽂）：https://matrix.tencent.com/skilltrustbench
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
HuggingFace Dataset ：https://huggingface.co/datasets/cuhk-zhuque/SkillTrustBench
HuggingFace Leaderboard ：https://huggingface.co/spaces/cuhk-zhuque/SkillTrustBench-Leaderboard
01 Agent Skills 的攻击⾯正在扩⼤
Agent Skills 的危险性来⾃它的复合性。 Skill 同时跨越⾃然语⾔、代码、依赖、权限和运⾏时
上下⽂。它既能在⽂档中直接向  Agent 下达指令、利⽤⽹络请求向外传输数据，也可以通过
执⾏本地脚本、安装外部依赖或篡改会话记忆来实施隐蔽攻击。
在  2026 年  1 ⽉底的  ClawHavoc 事件中， 1,184 个恶意  Skill 被上架到  ClawHub 市场，涉及
24.7 万次安装。随后  Snyk 发布的  ToxicSkills 报告显示市场中  36.82% 的  Skill ⾄少存在⼀个
安全问题；论⽂  SkillProbe 审计发现，⾼下载量并不等于更安全， ClawHub 中超过  90% 的
⾼热度  Skill 仍然存在⻛险。
2026 年  4 ⽉，腾讯朱雀实验室使⽤ A.I.G （ AI-Infra-Guard ：https://github.com/Tencent/AI-
Infra-Guard，腾讯朱雀实验室开源的⼀站式  AI 红队安全测试平台）对  ClawHub 上  Skill 进⾏
了全量扫描。研究显示， ClawHub 在  90 天内从不⾜  2,000 个  Skill 增⻓到超  50,000 个；即
便平台后续上线了安全检测机制，  Skill ⽣态中的⻛险信号仍然密集。
第⼀，恶意  Skill 已呈现出规模化、矩阵化的⽣产迹象。五万个  Skill 背后共有  15,427 名开发
者，但  Top 20 发布者合计发布  5,422 个  Skill ，占总量  12.9% ；极端账号  3 个⽉发布  955 个
Skill ，⽇均  10.6 个。多组命名相近、发布时间交替的账号矩阵说明， Skill ⽣态已经具备批量
制造、批量投放、批量伪装的条件。
第⼆，权限组合天然接近数据外泄链路。在近五万个  Skill 中， 27,818 个声明了⽹络请求权
限，占⽐  74.6% 。联⽹本身不是问题，但当读⽂件  + 联⽹成为⼤量  Skill 的常⻅组合时，恶
意外传就可以隐藏在正常功能流量中。
第三，外联通道已经⾮常分散。全量扫描共发现  246,378 条  URL ，指向  29,196 个不同域
名。它们既可能是正常  API 、⽂档、依赖源，也可能成为远程控制、数据回传、链上交互或
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
⼆阶段载荷下载的通道。
02 现有扫描与评测为什么不够
在年初的  ClawHavoc 事件之后， Skill 市场和安全⼚商已经开始建设扫描机制。以  ClawHub
为例，平台新增了内置的  LLM 安全评估和  VirusTotal 的外联检测。这类机制能有效拦截⼤部
分恶意指令直接写在  SKILL.md (https://SKILL.md) ⽂档⾥和直接下载运⾏⽊⻢程序的粗暴攻
击。
但攻击者很快进⼊下⼀阶段：不再把恶意逻辑写得明显，⽽是利⽤输⼊截断、⽂件类型盲
区、源码与分发产物不⼀致、企业合规话术和社会⼯程解释来绕过扫描。
2026 年  6 ⽉， Trail of Bits 针对  ClawHub 、 Cisco skill scanner 以及  skills.sh 集成的多个扫描器
进⾏了绕过测试。他们构造的样本包括：
这些不是极端⾼级攻击，⽽是利⽤了当前扫描⽅案的能⼒边界：⽂件是否完整读取，特殊⽂
件是否展开分析，字节码是否反编译， LLM 是否会被合理解释说服。
另⼀个问题是当前⾏业中众多开源  Skill 安全扫描⽅案之间缺少共识。
2026 年  5 ⽉底  OpenClaw 官⽅发布的  ClawHub Security Signals 数据集覆盖了  ClawHub 中
67,453 个公开  Skill ，并进⼀步对⽐分析了 ClawHub 官⽅市场原有内置静态分析结果、
VirusTotal 分析结果和  NVIDIA SkillSpector 扫描结果三类信号。结果显示，任意两类扫描的
阳性样本重合度最多只有  10.4% ；只有  0.69% 的恶意  Skill 被三类扫描⽅案同时发现； 81.9%
的被标记样本只被单⼀扫描⽅案发现。
这意味着，不同扫描⽅案看到的是不同⻛险切⾯，甚⾄对同⼀批样本的判断也缺少稳定共
识。因此，仅有众多的开源扫描器还不够，⾏业还需要⼀个公开、可复现、可持续更新的评
测基准，回答⼏个更基础的问题：
哪个⽅案更能发现恶意  Skill ？
哪个⽅案更容易误报正常  Skill ？
同⼀个⽅案换不同底层模型会怎样？
哪些攻击类型最容易漏掉？
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
哪些正常⾏为最容易被误伤？
SkillTrustBench 正是围绕这些问题设计的。
03 SkillTrustBench ：从真实 Skill ⽣态构建评测标尺
SkillTrustBench 当前版本从 62,652 个真实  Skill  出发，来源覆盖主流技能市场与开源社区。
经过清洗、去噪、平衡采样和攻击注⼊，最终形成 5,520 个评测⽤例，覆盖九⼤类  Skill 常⻅
威胁。
样本分布如下：
这⾥最关键的设计不是样本数量，⽽是样本结构。
如果⼀个评测集只包含显⽽易⻅的恶意样本，扫描⽅案很容易被引导为看到危险命令就告警
的规则系统。这样的⼯具在测试⾥可能很好看，但进⼊真实平台后会制造⼤量误报：系统管
理  Skill 需要调⽤  shell ，⽂档处理  Skill 可能使⽤临时共享库，官⽅安装脚本可能出现  curl |
bash ，开发⼯具  Skill 可能需要拉取依赖或访问外部  API 。
毕竟在实际场景中，调⽤敏感  API 不等于恶意，⽽看似合规的解释也可能是伪装。因此，
SkillTrustBench 同时评估三类能⼒：
是否能抓住恶意  Skill ；
是否能区分  suspicious 与  malicious ；
是否能控制对安全样本的误报。
在⻛险分类上， SkillTrustBench 采⽤按攻击⼿段划分的  T01-T09 体系，⽽不是只按攻击后果
分类：
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
此外，评估  Skill 本身的安全可信度，绝⾮简单的 “ ⾮⿊即⽩ ” 恶意检测，我们在⻛险类别中特
意引⼊了 “ T09 不安全编码⾏为 ” 。
我们发现在真实的  Agent ⽣态中，⼤量由正常⼯程⼈员开发的  Skill 主观上并⽆恶意，但由于
缺乏安全编码规范，其代码中往往伴随着硬编码凭证、敏感权限过度声明、缺乏输⼊校验等
不可信缺陷。这些缺陷如同软件供应链中的潜伏漏洞：即使开发者主观⽆害，其不安全的代
码仍可能被⿊客通过提示词注⼊或间接指令劫持，成为⼊侵系统的隐性通道。
04 ⾸期评测发现：⾼召回不等于可落地
SkillTrustBench ⾸期评测包含两组核⼼榜单：⼀组⽐较不同扫描⼯具，⼀组⽐较同⼀扫描流
程在不同底层模型上的表现。
⾸期横评对⽐了当前开源⽣态中关注度较⾼的⼏款开源  Skill 开源扫描⽅案：
1. Skill Vetter  (OpenClaw / Hermes Agent)：当前下载量最⾼的安全审计  Skill ，可以快速部
署在各类  Agent 框架中，在  Skill 安装前检查⻛险并在对话中提示⽤户。
(https://clawhub.ai/spclaudehome/skill-vetter)
2. Cisco Skill Scanner ： Cisco AI Defense 开源的检测⼯具，结合了静态规则、 LLM 语义分析
与⾏为数据流分析，重点扫描提示注⼊、数据泄露及恶意代码。 (https://github.com/cisco-
ai-defense/skill-scanner)
3. NVIDIA SkillSpector ：采⽤两阶段检测架构。第⼀阶段利⽤  AST ⾏为分析、依赖项校验、
污点追踪及  YARA 规则进⾏快速初筛；第⼆阶段引⼊  LLM 进⾏上下⽂语义分析，⽤以过
滤误报并输出解释。 (https://github.com/NVIDIA/skillspector)
在扫描器横评中，统⼀使⽤  DeepSeek v4 Flash 作为底座模型。最新公开结果如下：
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
在最新榜单中，Skill Vetter + OpenClaw 的组合召回率与综合分值（ F1 ）  最⾼；Skill Vetter +
Hermes Agent 组合综合排名第⼆，但误报最少。Cisco Skill Scanner的召回率不错，但误报率
达到 24% 。 NVIDIA SkillSpector 的误报较少，但漏报最多。
这组数据说明，安全检测不能只单看召回率或误报率。在真实  Skill 市场上架前审计、企业内
部  CI/CD 流程和  Agent 平台⾥，⾼误报会直接损害  Skill 的可⽤性。⼀个扫描⽅案  如果把⼤
量正常  Skill 标成恶意，最终结果往往不⼀定是更安全，⽽是被⽤户选择忽略提示。能抓住恶
意样本是第⼀步。能放过正常样本，才是进⼊⽣产流程的前提。
在模型底座评测中， SkillTrustBench 固定扫描器配置，仅替换底层推理模型，观察不同模型
在以  A.I.G 最新内测版作为  Skill 安全扫描⼯具时的表现：
能⼒最强之选  Claude Opus 4.6 与  GLM-5.1 。两者在⻛险推断、指令关联分析和意图识别
⽅⾯表现出较好的均衡性，综合分值最⾼；不过相⽐之下， GLM 5.1 的评测  Token 成本相
对更低（不到  Claude 4.6 Opus 的  10% ）。
性价⽐之选  DeepSeek-V4-Flash 与  Hy3 Preview 。整体表现相对均衡，误报控制较好，适
合作为低成本的安全评测参照基线。适合在  Skill 市场上架前扫描这种任务较⾼的场景中
落地使⽤。
偏向性特征表现：
Gemini 3.5 Flash  在本组评测中展现出较⾼的精确率与极低的误报率，但在复杂样本的
召回能⼒上相对保守，会有部分漏报。
GPT-5.5 表现出较⾼的召回率，但其误报率⾼达 18.67% ，在安全性研判上更偏向于宁可
误报、也不漏过的⻛格。
对于模型⼚商⽽⾔， SkillTrustBench 不仅测试了模型的语义理解，还考验其对代码逻辑、多
步指令的链式推理和敏感边界的划定能⼒。过去，这种垂类安全任务场景的能⼒⽐较⼀直缺
少⾜够全⾯权威的标尺， SkillTrustBench 旨在为⼤模型在此类安全任务类推理提供⼀个客观
的评估基准。
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
05 共建安全可信的  Agent Skills ⽣态
当前， Agent Skill 安全扫描的核⼼问题已从有没有⼯具，迈向如何证明有效的新阶段。由于
Skill 兼具代码与⾃然语⾔的双重属性，且攻防对抗动态演进，⾏业⻓期缺乏统⼀标尺，导致
各⽅的评估结果各说各话，企业难以选择合适的扫描⽅案。
我们希望  SkillTrustBench 的发布能够为⾏业提供  AI 技能安全检测的客观评估基准，推动检测
能⼒从定性⾛向定量。作为⼀项持续演进的项⽬，我们将紧跟最新的攻防实践，不断充实评
测集，也诚挚邀请各⽅加⼊共建：
⼤模型⼚商：提交新模型评测结果，评估模型在  Agent Skill 安全审查场景中的能⼒⽔位；
Agent 平台与  Skill 市场：评估并优化内置的安装前安全审计⽅案；
安全扫描⼯具：提交新版本扫描⽅案，横向⽐较检测能⼒演进；
安全研究者：提交真实攻击样本、绕过案例和良性⾼⻛险样本，共同完善  benchmark 覆盖
⾯。
联系与合作： zhuque@tencent.com
参考资料
腾讯朱雀实验室：我们扫描了五万个  Skill ，发现危险仍然存在
Snyk ： ToxicSkills: Agent Skills supply chain compromise
study(https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
SkillProbe ： Security Auditing for Emerging Agent Skill Marketplaces via Multi-Agent
Collaboration(https://arxiv.org/abs/2603.21019)
Trail of Bits ： The sorry state of skill distribution(https://blog.trailofbits.com/2026/06/03/the-
sorry-state-of-skill-distribution/)
ClawHub Security Signals ： When VirusTotal, Static Analysis, and SkillSpector
Disagree(https://huggingface.co/papers/2606.01494)
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
阅读 3360
关于腾讯朱雀实验室
腾讯朱雀实验室（ Tencent Zhuque Lab ）是腾讯安全平台部于  2019 年成⽴的顶尖  AI 安全实验室，专
注于  AI 安全领域的实战攻防与前沿技术研究，研究⽅向涵盖⼤模型安全、 AI 智能体安全、 AI 赋能安
全与  AI ⽣成检测等领域。团队多次协助英伟达、⾕歌、微软等知名⼚商以及 OpenClaw 、 Linux 、
Huggingface 等开源社区修复⼤量⾼危漏洞，并获得官⽅公开致谢。先后推出开源  AI 红队安全测试平
台  A.I.G （ AI-Infra-Guard ）及朱雀  AI 检测助⼿等 AI 安全产品。研究成果⼴泛发表于  Black Hat 、 DEF
CON 、 ICLR 、 CVPR 、 NeurIPS 、 ACL 等国际顶级安全与  AI 学术会议，并出版专著《 AI 安全：技术与
实战》。
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
留⾔
写留⾔
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
还没有留⾔，来写⾸评
````


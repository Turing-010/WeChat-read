# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
AI 代码⽣成率 94 %：我们⽤⼀个 Skill  跑通需求开发全流程
腾讯程序员 Jul  20 , 2026 , 2 : 36  AM⼴东原创 腾讯技术⼯程 1585  listened
作者：企业微信团队  - gomezlai
⼀、问题： AI 写业务代码为什么总是 " 差⼀⼜⽓ " ？
把 "AI 辅助编码 " 放到企业级真实项⽬⾥，我们很快撞上⼀堵墙。下⾯这⼏个场景，每个移动端
同学应该都不陌⽣：
真实痛点现象
上下⽂塞不下9000+ 源⽂件、跨  5~6 层调⽤，单轮对话喂不进去
物料分散 PRD 在  TAPD 、设计稿在  Figma 、协议在企微⽂档、 UI 改动还要看  Figma Token
命名不⼀致 ⽤户说 " 邮件点击⼊⼝ " ，代码⾥其实叫  didSelectRowAtIndexPath
模糊指令 ⽤户⼀句 " 按  PRD 改⼀下 " ， AI 直接跳过拆解开始改代码，越界、漏改、改错位
验证不闭环 AI 报 " 完成 " ，结果编译都没过；改完⼀处没顾上同步另⼀处
跨会话失忆 上⼀次的设计决策、改了哪些⽂件、为什么这么改，下⼀次会话全忘
⼀句话总结：AI 不是不会写代码，是不会 " 按⼯程规范 " 开发需求。
我们的解法不是换更⼤的模型，⽽是把 " 需求开发 " 这件事流程化、原⼦化、可校验化，然后把
每⼀步都喂给  AI 。
⼆、整体架构：把 " 需求开发 " 拆成  8 个语义化阶段
Skill 的核⼼是⼀条严格顺序的流⽔线。每个阶段输⼊清晰、产出明确、退出标准可机器校
验。结合⼈⽇常的开发的流程，⼤概可以分成以下的流程：
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
阶段 输⼊ 关键产出 灵魂动作
①  设计稿 Figma 链接 移动端候选稿清单  + PNG 概
览
脚本化直⽅图筛选
，绝不允许  LLM " ⼿感 " 分桶
②  拆解 PRD + 设计稿  + CGI
+ TAPD
五列需求清单  + subtasks.
json  接⼒台账
多源收料  + 归宿校验
（每张设计稿必须归到三类之
⼀）
③  定位 需求点 ⽂件  + ⾏号  + 调⽤链 五步定位法
（见下⽂）
④  实现 调⽤链  + 上下⽂ 代码改动
⾃底向上
：数据  →  解析  →  枚举  →  业
务  →  UI →  ⽇志
⑤  验证 源码改动 编译报告（退出码  0 ） bazel build
 + 最多  3 轮⾃修复
⑥  模拟器验
证 编译通过的产物装机后的截图  + ⽇志 " ⼈机秒级确认  + 阶段内重试
≤ 2 轮 "
⑦  沉淀 git diﬀ + 时间线 TECH_SPEC.md
 单⼀事实源 跨会话知识传承的载体
⼦步骤命名约定： Skill 内部统⼀采⽤「阶段 · 动作」式命名，例如   设计稿 · 脚本筛选、
实现 ·UI· 切图、拆解 ·TAPD 收料—— 这让  AI 在⾃报家门时永远清楚⾃⼰在哪⼀格上。
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
阶段 输⼊ 关键产出 灵魂动作
⑧  提交 全部产物 git commit + 分⽀ 三段式  commit + AI 署名  + 代
码⽣成率
三、第⼀性原理： Skill 为什么这样设计？
整条流⽔线背后只回答⼀个问题：怎样让⼀个没参与过原始实现的AI ，在新会话⾥像 " 参与过
的⽼同事 " ⼀样把活⼲完？
围绕这个⽬标， Skill 的设计原则可以收敛成四条公理：
下⾯把这四个公理逐个拆开看。
四、公理  Ⅰ ：每⼀步都在 " 缩⼩范围 "—— 五步定位法
⼤模型不是搜索引擎，把整个项⽬   find .  丢给它毫⽆意义。 Skill 把 " 在  9000+ ⽂件⾥找到改
动点 " 这件事拆成  5 个收敛步骤，每步  Token 消耗严格控制。
步骤 给  LLM 的输⼊量 输出
1. 意图消歧 项⽬概述  ~2K + ⽤户原话 「这个⽬标可能对应  4 种技术解读」
2. 模块定位 ⽬录树  + 解读结果 2-3 个候选⽂件路径
3. 关键词搜索（不进  LLM ）rg  直接跑 函数声明  + 位置
4. 调⽤链追踪单个⽂件相关⽚段  ~10K 完整调⽤链
5. 验证确认 函数实现  ~5K 最终改动点  + 理由
但这⾥还有⼀个前置问题没解决 —— 五步定位法的第  1 、第  2 步都依赖⼀个东西：项⽬本⾝得
有⼀张 "AI 看得懂 " 的地图。否则 " 项⽬概述  ~2K" 从哪⼉来？ " ⽬录树  + 解读 " 凭什么这么准？
真正的窍门：前  2 步只看⽬录和⽂件名，第  3 步才让脚本  grep ，到第  4 步才真正读代
码。⼀路漏⽃下来，模型从来不会被整个代码库淹死。
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
下⼀节我们就讲：这张地图是怎么造出来、怎么维护、并且如何永不过时的。
五、代码知识库：让  AI 拥有项⽬的 " 地图 "
定位精准的前提，是  AI ⼿⾥要有⼀份结构化、最新、可索引的项⽬知识。 Skill 在这⼀层下了
重注 —— 我们构建了⼀套三级⾦字塔知识库，并配套了⼀个漂移⾃动检测机制，确保地图永远
跟得上代码。
5.1 三级⾦字塔：从总览到字段，按需展开
级别 ⽂件 粒度 加载时机
L1 总览 project_wiki/overv
iew.md 模块名  + ⼀句话职责 「定位」阶段默认  preload
（ < 5KB ）
L2 模块 project_wiki/<modu
le>.md
每个  .h/.mm  ⽂件  + 功能说
明 命中模块后按需加载
L3 语义桥
figma_token_mappin
g.md
 / ui_components_wik
i.md
Figma Token →  ⼯程  API 的
精确映射 「实现 ·UI 」阶段强制参考
L1 ：项⽬总览 ——AI ⼊场的 " ⼤堂导览 "
overview.md  只做⼀件事：⽤⼀张表告诉  AI " 这个项⽬有哪些模块、各⾃负责什么 " 。例如：
模块 职责 详细⽂档
MList/ 邮件列表展⽰、同步、过滤、多选编辑mlist.md
RMail/ 邮件正⽂渲染、附件预览、 AI 总结 / 翻译 rmail.md
CMail/ 邮件撰写、富⽂本编辑、附件上传、 AI 润⾊ cmail.md
Model/ 领域模型  + DB 持久化  + 业务管理器 model.md
... （共  N 个⼀级模块）
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
规模⽰例： Model 模块统计（ 686 个   .h、 456 个   .mm、 Top 5 ⼤⽂件）。整份⽂件控制在
5KB 以内，可以毫⽆负担地塞进每次定位上下⽂。
L2 ：模块级 —— ⽂件粒度的 " 街道地图 "
每份   <module>.md 顶部有⼀段机器可读的元数据：
<!-- module_id: mlist -->
<!-- root_dirs:
  - App/Mailbox/MList/
-->
<!-- desc: 邮件列表展示、同步、过滤、多选编辑  -->
接下来是按   Controller/ ViewModel/ View/ Helper/ Lab/  分组的⽂件登记表，每个⽂件⼀⾏职
责：
⽂件 功能说明
XYZMListController.h/.mm邮件列表主控制器
，管理列表展⽰、同步、过滤、长按、多选编辑
XYZMListViewModel.h/.mm邮件列表  ViewModel
，管理数据加载、分页、过滤、排序、未读数
XYZTipsView.h/.mm 邮件列表顶部提⽰条（同步状态、代收失败、运营活动等）
...
L3 ：领域语义桥 —— 抹平 " 设计  / 协议 " 和 " 代码 " 的鸿沟
这⼀层是最容易被低估、却最能体现⼯程价值的部分。
举个例⼦：设计稿上写着   Mobile/callout， AI 该怎么写代码？⽬测字号？硬编码   [UIFont syst
emFontOfSize:15]？ —— 都不对。 Skill 把这种翻译规则全部沉淀到   figma_token_mapping.m
d：
// ❌  错误：⽬测字号  + 硬编码颜⾊
self.titleLabel.font = [UIFont systemFontOfSize:15];
self.titleLabel.textColor = [UIColor colorWithRed:0.1 green:0.1 blue:0.1 alpha:1.0];
// ✅  正确：按映射规则翻译  Figma Token
self.titleLabel = [UILabel xyz_styledLabel:@"callout"];       // Mobile/callout
self.titleLabel.textColor = XYZColor(base_gray_100);          // Base/base_gray_100
self.titleLabel.text = R_NSSTRING(XYZ::XXX::TITLE_KEY);       // i18n
这相当于把 " ⽼司机脑⼦⾥的项⽬地图 " 显式打印出来：哪个⽂件是⼲嘛的、它和兄弟⽂件
什么关系 —— ⼀次读  70 ⾏就能在脑⼦⾥建⽴整个模块的拓扑。
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
整张映射表覆盖了：
⽂字样式Mobile/title_1 ~ caption_2  ↔   xyz_styledLabel:
颜⾊Base/base_gray_100  ↔   XYZColor(base_gray_100)（⾃动响应  Dark Mode ）
按钮组件button_blue_large  ↔   [UIButton xyz_styledButton:...]
阴影  / 渐变  / 字体兜底 等约  20+ 类规范
⛔  RL-29 ： UI 改动必须⽐对   figma_token_mapping.md，禁⽌硬编码字号 / 颜⾊—— 这是从
⽆数 " 设计稿⾛样 " 事故中淬出来的红线。
5.2 ⾃维护：让知识库永不过时
构建知识库不难，难的是让它不随代码漂移。该项⽬半年内净增  200+ ⽂件、改动  1000+
处，靠⼈⼯维护早就崩了。
Skill 的解法是⼀个核⼼脚本： **check_project_wiki_stale.py** 。
关键设计：
机制 作⽤
SHA 基线缓存
（.review_cache.json） 记录每个⽂件上次审阅时的  SHA 。再次变化时⾃动  ﬂag " 待复核 "
三⾊分诊清单 新增  / 删除  / ⼤改三类信号分开列， 30 秒就能扫完
pre-commit hook 阻断 退出码  1 = 有  stale 信号  →  阻⽌提交，强制开发者顺⼿维护
元数据驱动  overview <module>.md
 顶部改  desc，overview.md  索引⾃动跟随
5.3 知识库  + 定位法： 1 + 1 > 2
回到第四章的五步定位法，把它和知识库结合，就能看清整个精准定位的完整闭环：
第  1 步：从  L1 总览⾥  1 秒选出 "MList" 模块（不⽤  grep ）
效果：本项⽬的全部模块  wiki 在过去  6 个⽉⾥没有出现过 " 地图和代码脱节 " 的情况 ——
因为每次有⼈改了代码、想  commit 上去， hook 都会提醒他顺⼿把  wiki 同步了。
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
第  2 步：从  L2 模块  wiki ⾥  5 秒锁定   XYZTipsView.h/.mm（不⽤读源码）
第  3 步：进⼊⽂件后   rg  精准搜索（脚本⽽⾮  LLM ）
第  4 步：只读相关⽚段（ ~10K token ）
第  5 步：写代码前先查  L3 映射表（杜绝硬编码）
总  token 消耗从 " 全项⽬灌⼊ " 的  ~10M+ 降到  ~30K——300× 的压缩⽐。这就是知识库带来
的本质提效。
但这只解决了问题的⼀半。
知识库让  AI 拥有了 " 代码侧的地图 "—— 可它还要看懂 " 需求侧的描述 " 。产品同学说的 " 加个红
点 " 和⼯程师写的   setMailboxBadgeValue:，中间隔着⼀道语义鸿沟：⾃然语⾔模糊、⼝语化、
以业务视⾓描述；代码精确、形式化、以技术视⾓组织。
要让  AI 独⽴跑完，必须把这道鸿沟也补平。这就是下⼀节要讲的。
六、需求语义翻译：把 " 产品语⾔ " 变成 " 代码指令 "
6.1 鸿沟在哪？
下图是⼀条典型的 " 产品  →  代码 " 翻译链。每⼀层都可能翻车：
✨  ⼀个有意思的副作⽤：这套知识库对⼈类新⼈同样有⽤。我们组新同学⼊职后，不再
需要 " 找⽼⼈聊⼀上午 " 才知道项⽬结构 —— 直接读   overview.md  加⼏份模块  wiki ，半天
就能上⼿改  bug 。"AI 友好 " 和  " 新⼈友好 " 在这⾥完全统⼀了。
直觉上  AI 在提效，过程却强依赖于⼈ —— 很⼤⼀部分 " ⼈⼯成本 " 花在了这道翻译上：开
发者读完  PRD/Figma/CGI 后在脑⼦⾥完成 " 产品语⾔  →  代码语⾔ " 的转换，再把翻译结
果喂给  AI 。这⼀步如果不做， AI 经常会越界、漏改、改错位。Skill 在「拆解」阶段把这
道翻译规则化、可执⾏化，做到  AI 也能独⽴完成。
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
每⼀步翻车都很真实：
翻车点 真实场景 代价
①  范围错判PRD 段落整体在讲 " 后台配置 " ，中间⼀句 " ⼿机上看到的效果 " 被
当⼝语忽略 漏实现移动端  UI
②  归宿不明 设计稿  9 张移动端候选稿， AI 只挑  2 张做需求点，其余笼统
当 " 参考图 " 漏  7 个独⽴页⾯
③  联想扩⼤⽤户说 " 点  A 拦截 " ， AI 联想 " 按⼀致性  B 也应该拦 " ，⾃作主张
越界
改了不该改的逻
辑
④  关键词找不
到
直接  grep " ⼩红条 "  →  0 命中；只  grep "tips"  →  800+ 处
淹没
定位失败或误命
中
⑤  找错⽂件" 邮件红点 " 翻译错位置，改了  RMail ⽽不是  MList 功能完全⾛错地
⽅
Skill ⽤五个确定性规则逐层堵住每个翻车点。
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
6.2 ①  范围识别：⽤ " 硬关键词表 " 代替  LLM 直觉
PRD 是产品视⾓写的，常常  Web 后台和移动端混在⼀段⾥。让  LLM " 凭语义判断 " 是个灾难
—— 同⼀段描述⾥出现 " 配置后台 "+" 客户端展⽰ " ， LLM 经常因为段落主语是后台就把整段判
为⾮移动端。
Skill 的解法是⼀张强信号关键词表，硬触发，不依赖  LLM 语义理解：
类别 关键词（命中即强制打 " 移动端 " 标签）
平台  / 端 ⼿机上
、⼿机端、移动端、iOS、Android、安卓、苹果、客户端、App
原⽣控件  / 交互 Toast
、弹窗、浮层、⼩红条、红点、Tab ⻆标、⻆标、下拉刷新、侧滑、⻓按
iOS 系统组件 状态栏
、导航栏、Home Indicator、底部安全区、刘海
移动端页⾯术语输⼊法
、键盘展开、全屏弹窗、actionsheet
硬规则：
这条规则⾮常朴素，但威⼒巨⼤：把 "AI 范围错判 " 这种最典型的翻车，从概率事件压成  0 。
6.3 ②  设计稿归宿：每张图必须归到三类之⼀
关键铁律：如果某张图归不到任何需求点 ——
要么是筛选误纳（回去把它从候选清单⾥去掉）
即使段落主旨在讲后端  / 配置  / 推送规则，只要任⼀关键词命中，那⼀段所描述的功能点
就必须单独拆成移动端项。  范围判断不是 "AI 觉得 " ，是 " 关键词命中 "—— 客观、可机器
复现、不允许降级。
⛔  RL-12：候选清单⾥每张设计稿都必须归宿明确，不允许出现 " 未归类 " 。
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
要么是需求点遗漏（新增⼀项）
不允许⽤ " 参考图 " 当万能垃圾桶。这条规则把 " 漏需求 " 这种最隐蔽的事故彻底显式化。
6.4 ③  拦截点清单：禁⽌ " 语义联想 "
需求⾥最容易出错的是 " 交互拦截 " 。产品⽂档常常⼀句话带过， AI 最容易 " ⾃由发挥 " 。
Skill 强制要求输出⼀张可验证的清单：
# 触发元素  X 触发事件响应  Y 依据来源
1 邮件列表 " 全选 "
按钮 点击 Toast 提⽰ " 超过  100
封不可全选 "
figma_overview_p3.png
  上从全选按钮指向  toast 的绿
⾊箭头
2 顶部⼩红条点击 跳转管理页 TAPD 原⽂： " ⼩红条点击跳
转  https://..."
「依据来源」只接受三种：
1. 设计稿标注： PNG 上的连接线  / 箭头从  X 指向  Y （必须有  nodeId ）
2. ⽂档原⽂： TAPD / 企微⽂档的直接引⽤原句
3. ⽤户消息：⽤户原话引⽤
禁⽌⽤业务语义作依据：
填不出具体引⽤的⾏直接删掉，不实施。这是⼀条⾮常硬的红线，把 "AI ⾃作主张越界 " 这个公
认顽疾彻底锁住。
6.5 ④  领域联想：把 " 产品语⾔ " 扩展成 " 代码搜索词 "
到这⼀步，我们已经把需求拆出了 "M1 邮件列表顶部⼩红条 " 这样精确的需求项。但它在代码
⾥叫什么？
产品同学说 " ⼩红条 " ，⼯程师在代码⾥可能找到的是：
XYZMListTipsView         // "Tips"  才是这个组件的⼯程命名
XYZMListTipsType_xxx     // 枚举值
showWarningTips:               // 显示⽅法
⛔  RL-21：任何 " 点击  X →  触发  Y" 类拦截， X 必须有具体引⽤依据，禁⽌凭语义联想扩
⼤范围。
❌  "Z 看起来也属于这类功能 " →  删除  ❌  " 为了⼀致性应该也拦⼀下 " →  删除  ❌  " 属于
同类功能⾏为 " →  删除
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
is_show_warning_icon_in_mailtab // CGI 字段
XYZLOG_WARN(@"show tips")       // ⽇志关键字
" ⼩红条 " 和   Tips /  Warning /  Icon  之间，隔着⼀道领域知识鸿沟—— 它不是  AI 不够聪明，
⽽是产品语⾔和代码命名本来就属于两套词汇体系。
如果直接   grep " ⼩红条 "，结果⼀定是  0 。如果只   grep "tips"，⼜会被⼏百处历史⽤法淹没。
Skill 的解法是：⽤  5 个搜索维度做交叉扩展，把⼀个需求项展开成⼀组⾼命中率的候选搜索
词。
5 维搜索矩阵
5 个维度的设计哲学：
维度 出发点 命中什么
①  iOS 事件⽅
法 平台标准  API didSelectRowAtIndexPath:
 / handleTapGesture: / touchUpInside:
②  功能语义 产品意图的英⽂同义
词
" ⼩红条 " →  tips / banner / warning / notice / aler
t
③  OC 命名习惯项⽬⾥的命名前缀show*
 / handle* / on* / goto* / setup*
④  协议  / 代理谁通知谁 tableViewDelegate
 / <XxxDelegate> / didSelectXxx:
⑤  通知  / 回调跨模块通信 XxxNotification
 / XxxCallback / XxxHandler / RACSignal
联想的依据：知识库  + Glossary
5 维矩阵不是凭空联想，背后有两份领域知识作为依据：
💡  关键洞察：这五个维度不是按 " 和需求最相关 " 排，是按 " 代码⾥实际可能出现的位
置 " 排。①  是平台层、②  是业务层、③  是项⽬命名风格层、④⑤  是跨模块通信层 ——任
何⼀个  UI ⾏为，必然落在这  5 层之⼀。把它当成⼀张 " 代码命名空间的全景图 " ，⽽不是
凭运⽓联想关键词。
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
L2 模块  wiki（第五章）告诉  AI ： " 邮件列表模块下已经有   XYZTipsView.h/.mm，描述
是 ' 邮件列表顶部提⽰条 '"—— 这⼀条直接把 " ⼩红条 " 翻译成了   Tips
项⽬  Glossary（命名约定的总结）告诉  AI ： " 本项⽬⽤   show* 表⽰显⽰、goto* 表⽰跳
转、XYZ  是邮件插件类前缀 "—— 这能从动词层⾯匹配代码命名
实战：从⼀句产品话到⼀组  grep 命令
⽤⼀个真实例⼦完整⾛⼀遍：
📝  产品原⽂：
   " 邮件列表顶部出现红⾊⼩条，提示⽤户域名即将过期，
    点击跳转域名管理⻚ "
⬇  第 ① 层联想（功能语义）：
    红⾊⼩条  → tips / banner / warning / alert
    即将过期  → expire / expiry / due / warning
    跳转管理  → goto / route / push / open
⬇  第 ② 层联想（项⽬命名⻛格）：
    邮件列表前缀  → XYZMList*
    提示组件类   → *TipsView / *Banner / *Notice
    跳转⽅法     → goto* / open* / push*
⬇  第 ③ 层（结合  mlist.md L2 wiki ）：
    命中⽂件： XYZTipsView.h/.mm
   " 邮件列表顶部提示条 "—— 直接对应
⬇  候选搜索词集合（按命中概率从⾼到低）：
   1. XYZTipsView                  ( 强命中：组件类 )
   2. showWarningTips:                ( 强命中：显示⽅法 )
   3. XYZMListTipsType_         ( 中：枚举类型前缀 )
   4. didTapTipsView:                 ( 中：点击响应 )
   5. domainExpire / domainWarning   ( 中：业务关键词 )
   6. gotoDomainManagement            ( 弱：跳转⽅法名猜测 )
⬇  最终  grep 命令（漏⽃式收敛）：
没有这两份知识， AI 联想出来的关键词是 " 瞎猜 " ；有了这两份知识，联想出来的关键词
命中率  > 80% 。
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
   $ rg "XYZTipsView|showWarningTips" App/Mailbox/MList/ -l
   App/Mailbox/MList/View/XYZTipsView.mm     ←  命中！
   App/Mailbox/MList/Controller/XYZMListController.mm ←  调⽤⽅
反例：不联想会怎么翻车？
反例 后果
直接  grep " ⼩红条 " 0 命中（中⽂  →  英⽂鸿沟）
只  grep "tips" 命中  800+ 处（项⽬⾥历史⽤法太多， AI 看不过来）
只  grep "warning" 命中错位置（项⽬⾥  "WeComKit" 也有  warning ）
grep "domain expire"0 命中（产品想到的业务词不在代码⾥出现）
5 维交叉才是唯⼀稳定路径 —— 单维都会要么  0 命中、要么海量误命中。
与红线  RL-21 的边界
6.6 ⑤  翻译产物：五列表格  + subtasks.json
经过①②③  三道关之后，需求侧的语义已经被收敛成结构化清单。它就是「拆解」阶段的产
出：
⼈类可读的五列表格：
序号 需求项 类型 数据来源 关联设计稿  no
deId
M1 邮件列表顶部⼩
红条 新增  UI CGI 字段  is_show_warning_i
con_in_mailtab 153:74513
M2 Tab ⾓标显⽰感
叹号 修改逻辑已存字段  + 优先级判定 153:74600
M3 点击⼩红条跳转
管理页 新增交互TAPD 原⽂（已引⽤）153:74521
** 机器可读的   subtasks.json**（结构化字段）：
✨  整个过程不需要 " 读源码猜⽅法名 "—— 只⽤  wiki + 命名约定就把关键词扩展出来了。
从产品原⽂到  grep 命令，全程机器可执⾏。
⚠  6.5 联想关键词和6.4 拦截点禁⽌语义联想是两件事，不要混淆：
6.5 允许联想：在 " 找代码该改哪⾥ " 这件事上，必须⽤领域知识扩展候选搜索词，否
则根本搜不到（这⼀步只是缩⼩搜索范围，不直接影响实现）
6.4 禁⽌联想：在 "X 触发  Y 是哪条交互 " 这件事上，必须有具体引⽤依据，不能因
为 " 看起来像 " 就加进拦截清单（这⼀步直接决定实现内容，关系到 "AI 越界 " 红线）
⼀句话：联想⽤于搜索，引⽤⽤于决策。
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
[
  {"id":"M1","title":" 邮件列表顶部⼩红条 ","type":" 新增 UI",
   "data_source":"CGI 字段 is_show_warning_icon_in_mailtab",
   "figma_node":"153:74513","depends_on":[]},
  {"id":"M2","title":"Tab ⻆标显示感叹号 ","type":" 修改逻辑 ",
   "data_source":"已存字段 ","figma_node":"153:74600","depends_on":["M1"]}
]
这份  JSON 是  Skill 的关键中枢—— 它同时承担三个⾓⾊：
到这⾥， " 产品语⾔  →  代码指令 " 的语义鸿沟就被彻底抹平了：
输⼊ 经过  Skill
拆解后 给  AI 的指令变成
PRD ⼀段话： " 邮件列
表顶部加红⾊提⽰条，
点击跳转管理页 "
M1 + M3 两
个需求项
" 在  XYZTipsView.h/.mm（来⾃  mlist.md L2 wiki ）新增
类型  XYZMListTipsType_xxx（参考已有枚举），点击响
应跳转  XYZWeeklyReportViewController（来⾃  man
ager.md L2 wiki ） "
6.7 完整翻译链：知识库  + 拆解规则  = 闭环
把第五章的代码侧地图、和本章的需求侧翻译合在⼀起看，就能看清  Skill 是怎么把 "AI 独⽴开
发需求 " 这件事⼯程化的：
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
两条链⼀对接， AI 就拥有了 " 独⽴开发完整需求 " 所需的全部确定性输⼊：
需求侧：每个需求点是什么、范围在哪、关联设计稿哪个  nodeId 、依据是什么
代码侧：项⽬⾥有哪些模块、每个模块有哪些⽂件、每个⽂件做什么、 UI Token 怎么翻译
💡  ** 真正的提效不在 "AI 写代码 " ，⽽在 "AI 不再需要⼈来当翻译 "** 。当语义翻译这件事
被规则化、可执⾏化、有产物可校验后，开发者从 "PRD 翻译机 " 的⾓⾊⾥解放出来，转
⽽成为 "AI 的产品经理 "—— 只在硬关卡处做决策。这就是  94% 代码⽣成率背后的真正机
制。
````

## PDF 第 16 页

[原页](RAW.pdf#page=16)

````text
七、公理  Ⅱ ：把 " 判断 " 留给  LLM ，把 " 数据 " 交给脚本
LLM 最不擅长两件事：精确数值和幂等执⾏。 Skill 把这两类⼯作全部下沉到脚本， LLM 只负
责 " 读结果  + 下决策 " 。
7.1 多源物料收集：每种来源⼀个专⽤脚本
整个  Skill ⽀持六类输⼊，每类都有⾃⼰的 " 专⽤通道 " ， ** 严禁通⽤   web_fetch**：
为什么不能⽤   web_fetch？  这正是  Skill 写死的  Critical 红线：
7.2 设计稿筛选：脚本直⽅图  vs LLM " ⼿感 "
Figma ⼀个  ﬁleKey 下⾯常有⼏⼗上百个画板：海报、 PC 端、平板、移动端、变体、注释
稿 …… 让  LLM 凭 " 看起来像移动端 " 挑出移动端是灾难。
Skill 的做法是：
⛔  RL-17 ：严禁  LLM ⼿⼯分桶—— 必须先跑   scan_figma_frames.py 出直⽅图（数据来⾃   to
ols/iphone_sizes.json  这份  iPhone 尺⼨⽩名单）， LLM 只能在已分桶基础上补判UNCERTAI
N  项，不能凭印象决定。
⛔  RL-02doc.weixin.qq.com 必须⾛   wecom-cli，web_fetch  鉴权后只拿到  HTML 外
壳⛔  RL-03 TAPD URL 必须⾛   tapd_mcp_http MCP ，web_fetch  拿不到  markdown 描
述
````

## PDF 第 17 页

[原页](RAW.pdf#page=17)

````text
这条红线把 "AI 看图选稿 " 的随机性从根上扫掉了。
7.3 " 落盘判定成功 " — RL-32 的⼯程美感
git commit 长消息会被  terminal 当后台任务、 stdout 会被截断、管道命令会变成异步 …… 这
些都是脚本和  LLM 之间常见的 " 信号丢失 " 陷阱。
Skill 引⼊了⼀个朴素但极漂亮的设计：sentinel ⽂件  = 成功的唯⼀判据。
同样的思路也⽤在   git commit（ RL-31 ：以   git log -1 hash  更新为唯⼀判据）。任何 " 长跑命
令 " 都不靠  stdout 报告成功，全靠落盘⽂件—— 这是从⽆数翻车⾥淬出来的⼯程经验。
⼋、公理  Ⅲ ：红线机制 —— 把 " 翻车 " 前置成 " 硬关卡 "
LLM 在⼯程上最⼤的风险，是它 " 什么都敢说，什么都敢做 " 。 Skill ⽤⼀套红线系统给它戴上
紧箍。
8.1 红线架构： YAML 单⼀真源  + 分层加载
红线分两级：
🔴  Critical（ 6 条）：全流程必守，启动即加载，违反会直接造成线上事故或严重返⼯
🟡  Standard（ 30+ 条）：按阶段加载，违反会污染⼯程规范
8.2 触发即停  + 模板化报告
````

## PDF 第 18 页

[原页](RAW.pdf#page=18)

````text
任何红线被触发， AI 必须停下并按固定模板汇报：
⛔  触发红线  RL-XX ： < 标题 >
当前情形： < 具体说明 >
建议处理： < 回退到哪个步骤  / 需要⽤户确认什么 >
这把 "AI 偷偷做了它不该做的事 " 变成 "AI 主动告诉你它撞上红线了 "——可观测性远⽐聪明更
重要。
8.3 ⼏条 " ⾎泪换来 " 的  Critical 红线
红线 来源 设计思想
RL-15
  编译必须通过"AI 说做完了但其实编译都没过 " 退出码  0 = 唯⼀判据；⾃修复硬
上限  3 轮
RL-16
  未按阶段执⾏
" ⽤户⼀句话指令  →  AI 跳过拆解直接改代码
→  越界 " 后⼀阶段输⼊  = 前⼀阶段产出
RL-13/14
  先看后写、模仿
已有
"AI 发明新模式  →  项⽬⾥独此⼀家 " 先通读完整⽅法  + 搜索同类分⽀
RL-31
 commit 同步执⾏
" 长  commit 消息被  terminal 置后台  →  AI 误
判失败重提 "
git log -1
 hash 更新是唯⼀成功证据
九、运⾏时验证：让  AI ⾃⼰跑通
9.1 闸门⼀：编译验证 —— 退出码  0 是唯⼀判据
代码改完后， AI 不允许说 " 实现完成 "—— 必须先跑通   bazel build。
红线只是把 " 翻车点 " 拉到了硬关卡，但还有⼀个更根本的问题：AI 怎么证明⾃⼰写的代
码真的 " 做对了 " ？编译过  ≠ 跑得对，跑得起  ≠ 长得对。下⼀节我们讲  Skill 怎么把 " 代码
质量验证 " 也⼯程化、⾃动化。
AI 最⼤的诚信问题是 " ⾃报完成 "—— 说 " 已经做完了 " ，结果编译都没过；说 " 功能正常 " ，
截图打开⼀看  UI 错位。Skill 把 " 验证 " 拆成两道闸门：编译验证（代码层） + 模拟器验证
（运⾏时  + 视觉），两道都通过才允许进⼊沉淀阶段。
````

## PDF 第 19 页

[原页](RAW.pdf#page=19)

````text
A/B 分类的设计精髓：
类别 典型场景 AI 能否⾃处理
A 可⾃修复缺分号  / 标识符未声明  / 类型不匹配  / 枚举漏  case
/ #import  找不到
✅  直接  replace_in_fil
e  修，重跑编译
B 需⽤户介
⼊
BUILD.bazel
  配置错  / 链接错误  / 错误位于三⽅  framework / 错
误⽂件不在本次改动集合
⛔  ⽴即停下，绝不硬试
报告⾥直接带上下⽂代码⾏—— 让  AI 不⽤回头读源码就能修。这是脚本设计的⼀个⼩巧思：
App/Mailbox/mailcore/mailbox_protocol.cpp:1822:25:
  error: use of undeclared identifier 'undefined_xxx'
 1822 | void __test_error__() { undefined_xxx(); }
      |                         ^^^^^^^^^^^^^
9.2 闸门⼆：模拟器验证 —— 真跑⼀遍  + 截图核对
编译通过  ≠ 功能正确。 Skill ⽤⼀套⾃动化  UI 验证流程让  AI ⾃⼰装机、⾃⼰点击、⾃⼰截
图、⾃⼰核对预期。
⛔  RL-15 + ⾃修复硬上限  3 轮：超过  3 轮仍编译不过  →  强制停下报告⽤户，不允许继
续。这条规则把 "AI 越改越乱 " 的死循环锁死。
````

## PDF 第 20 页

[原页](RAW.pdf#page=20)

````text
第①步：路径推导 —— 从  git diﬀ 反推⼀条  UI 路径
AI 不是 " 想点哪点哪 " ，⽽是按   git diff  改动  + TECH_SPEC §3 「相关代码位置」 + 设计稿终
态图，反推出⼀条具体的  UI 验证路径：
改动类型 验证终点
改  UI （ View / Controller ） 该  UI 的真实可见状态（截图能看到）
改数据  / 解析 UI 上能体现该数据的页⾯  + 抓⽇志确认数据流
改纯逻辑（⽆  UI 直接体现） XYZLOG_WARN
  ⽇志关键字命中
verify_plan.md 的标准⾻架：
# 模拟器验证计划： <feature-name>
## 操作步骤
1. launch App                                  → 01_launched.png
2. tap 邮件  Tab                                 → 02_mail_tab.png
3. tap 第⼀封邮件                                → 03_detail.png
4. 观察顶部  Tips ⽂字是否含  "xxx"               → 04_tips.png
5. tap nav_back_arrow                          → 05_back.png
## 预期
- 步骤  4 截图中  Tips ⽂字  == "<期望⽂案>"
- runtime.log 中  `XYZLOG_WARN(@"mailbox xxx")`  命中  ≥ 1
UI 路径预扫描： 6 步反向溯源（附录  A 的精华）
如果改动涉及 " 按钮  enable 条件  / 拦截弹窗  / 新增点击响应 " ， AI 必须先做⼀次预扫描，把 " 代
码层⽅法名 " 反推到 "UI 层可点击控件 " ，避免点错或点了没反应：
````

## PDF 第 21 页

[原页](RAW.pdf#page=21)

````text
第③④步：执⾏  + A/B/C 三类诊断
每步固定  5 个动作，实时汇报，不静默连跑：
🎬  步骤  N/M ： < 动作 >
- 命令： idb ui tap --udid $UDID 200 420
- 截图： 03_detail.png
- 观察：导航栏标题  " 邮件详情 "， Tips 区域可⻅
预期点核对失败时，按  A/B/C 分类分流：
类 现象 处理
A 真问题
（代码  bug ）
期望  UI 没出现  / 字段值错  / assert|crash|Er
ror  命中
⛔  本阶段不修代码，回「实现」
阶段
B 路径不通
（验证设计错）
被登录页  / 引导页拦截  / 当前帐号没数据  / 真机
才能复现 ⛔  修订  verify_plan 或跳过
C 脚本 / 时序
（可⾃修复）元素未渲染就  tap / 坐标算错  / 输⼊法没切到位✅  阶段内重试  ≤ 2 轮
第⑤步：视觉对齐核对 ——RL-30 的硬关卡
光 " 截图能看到 " 还不够， UI 改动还要逐项核对数值：
## 视觉对⻬核对（依据  ui_alignment_spec.md ， RL-30 ）
- [x] XYZTopicEmptyFooter container.height = 280 ✅ （截图实测  280 ）
- [x] icon 居中且  size 96×96 ✅
- [x] title 字号  16 / Medium ✅
- [ ⚠ ] desc lineHeight 偏⼩  1pt （已知偏差， spec 已记录）
📌  桥梁法—— 当依赖变量跨⽂件赋值时，按  3 类桥梁定位源头：通知（postNotification
Name:） / KVO （RACObserve(） / Delegate （<DelegateProtocol> =）。这是把 "AI 找不
到控件来源 " 这种顽疾规则化的关键。
🎯  设计精髓： A/B/C 分类把 " 该不该重试 " 这个糊涂账变成清晰决策。 AI 不允许在  A/B 类
问题上反复硬试，最多  2 轮  C 类重试不过  →  升级为实质性问题报告⽤户。
⛔  RL-30：触发了  RL-29 （ UI 改动）但   ui_alignment_spec.md 不存在  / 未对齐项  ≥1 →
视觉对齐直接判  FAIL，不允许跳过。
````

## PDF 第 22 页

[原页](RAW.pdf#page=22)

````text
- [x] cta 主蓝⾊  ✅
## 视觉对⻬结论
- 关键差异  0 / 接受偏差  1 / ** 未对⻬  0**
- 未对⻬  ≥1 → 状态⾃动降级为  ❌  FAIL
这把 " 设计稿⾛样 " 这个  UI ⼯程顽疾彻底显式化 ——不再依赖测试同学⼿⾁眼⽐对，⽽是  AI ⾃
⼰拿着数值清单逐项核对。
9.3 那些 " ⾎泪换来 " 的运⾏时⼩坑
模拟器验证过程踩过不少坑， Skill 把它们沉淀成   simulator_toolbox.md  ⾥的死⾓清单—— 这
些是  AI 必须知道的 " 不能做什么 " ：
死⾓ 为什么不⾏ 替代⽅案
边缘左滑返回
UIScreenEdgePanGestureRecognizer
  要求真实  touchDown→hold→move  时序，i
db ui swipe  是合成事件，模拟器永远识别
不出
找  nav_back_arrow 的  AX
标识  + tap
3D Touch / ⼒度长按模拟器不⽀持⼒度感应 ⽤菜单按钮  / 开  debug 后门
物理像素  ↔  逻辑像
素
截图是物理像素，idb ui tap  吃逻辑像
素，硬编码坐标必错
scale = logical_w / p
hysical_w
 动态换算
登录态丢失simctl uninstall
  清沙盒会丢登录
同  bundle id simctl inst
all  不动沙盒，登录态保留
shell heredoc ⾥  Pyt
hon f-string !r zsh 把  !r 当  history expansion →  命令变乱改⽤  repr(x)  或独⽴  .p
y  ⽂件
9.4 验证闭环：从代码改动到 " 敢说做完了 "
把两道闸门串起来看， AI 从 " 改完代码 " 到 " 敢说做完了 " 经历了  5 道把关：
每⼀道关都有机器可校验的产物：build_report.txt  退出码、<NN>_xxx.png  截图、runtime.l
og  ⽇志命中、result.md  状态字段。全部由⽂件证明，不靠  AI ⾃报。
这些坑没有⼀条是 " 模型不够聪明 " 导致的 —— 全是⼯程层⾯的真实陷阱。沉淀成⼿册之
后，每个新会话的  AI 都能直接绕开。
💡  本质思想：把 " 质量保障 " 这件事从 " 靠测试同学发现  bug" 变成 "AI ⾃⼰写代码⾃⼰验证
⾃⼰交差 " 。这才是  AI 能从 " 辅助 " 升级为 " 主导 " 的关键 ——当  AI 拿出来的不仅是代码，
````

## PDF 第 23 页

[原页](RAW.pdf#page=23)

````text
⼗、公理  Ⅳ ：跨会话知识传承 ——TECH_SPEC.md 是灵魂
如果说前三公理解决的是 " ⼀次会话内的提效 " ，那这条公理解决的是真正让  AI 像团队成员⼀
样⼯作—— 会做、能记、可接⼒。
10.1 三件套：分别承担不同尺度的 " 记忆 "
⽂件 时间尺度内容
TECH_SPEC.md永久 功能边界、模块地图、不变式、 Bug/ 迭代演进历史
subtasks.json跨会话 每个⼦需求的状态、当前阶段、关联  commit
timeline.txt会话内 start
 / human-correction / commit  三类事件流⽔
10.2 TECH_SPEC.md 的章节结构（精华）
§0  AI ⾃检清单          ←  给下次会话的  AI 当"⼊场扫描 "
§1   功能边界            ←  哪些做、哪些不做（防越界）
§3   模块地图            ←  ⽂件  + 关键⽅法  + 调⽤链
§5   不变式              ←  不能动的命名、⽂件清单、拦截边界
§7   演进事件            ←  按时间线排列的  BUG-N / ITER-N / REV-N
§8   产物清单            ←  每次  commit 改了什么
§9   版本号              ←  v1.0 → v1.1 → ... → v2.0 (baseline 合并 )
新会话的  AI 只要按  §0 →  §1 →  §3 →  §5 →  §7 顺序读完，就能 " ⽆缝接⼒ " 。
10.3 四类⼊⼝：根据现场状况⾃动分流
这套接⼒机制配合  4 种⼊⼝，把 " 需求开发 " 覆盖到了完整⽣命周期：
还有截图、⽇志、视觉对齐报告时，开发者只需要做最后⼀道  review ，⽽不是⼿动跑⼀
遍验证。
````

## PDF 第 24 页

[原页](RAW.pdf#page=24)

````text
10.4 硬关卡  HK ：信任但不放任
每个⼯作流⾥都嵌着若⼲⼈机硬关卡（ Hard Checkpoint ），强制要求⽤户确认：
硬关卡 触发时机 ⽤户回什么
HK-0
  现场快报 接⼒⼊⼝进⼊后第⼀时间 确认进度  / 改  N
HK-1
 PENDING 条⽬ §7 翻译完成后 " 确认  / 改  xxx"
HK-2
  沉淀  ok TECH_SPEC 落盘前 " 沉淀  ok / 通过 "
HK-3
 commit ⽂案 git commit 前 " 提交  / go"
这套 " 硬关卡 " 是  Skill ⼯程的精髓之⼀ ——⾃动化和可控性的平衡点： AI 跑得飞快，但任何⼀
个不可逆动作都先让⼈点头。
⼗⼀、提效效果：到底快了多少？
同⼀个  TAPD 需求的整个⽣命周期 —— 从⾸次实现到  N 轮迭代、 M 个  bug 修复、偶尔的
推倒重来 —— 全部由这⼀份   TECH_SPEC.md 串联起来。
数据来源于本项⽬近半年实际跑下来的体感（⾮严格  benchmark ），仅供参考。
````

## PDF 第 25 页

[原页](RAW.pdf#page=25)

````text
环节 传统⽅式 Skill ⽅式 提效来源
需求拆解 1~2 ⼩时（看  TAPD / Figma
+ 整理） 5~10 分钟 多源脚本⼀站式拉取  + ⾃动
归宿校验
代码定位30 分钟 ~2 ⼩时（ grep 试错）5~15 分钟 五步定位法  + project_wiki
索引
实现 视复杂度 -30%~50% " 先看后写  + 模仿已有 " 减少
返⼯
编译⾃查 ⼿动来回 ⾃动  3 轮 build_verify.sh
 + ⾃修复
UI 验证 ⼿动装机点击  + ⾁眼⽐对 ⾃动装机  + 截图  + 视
觉对齐
install_to_simulato
r.sh
 + A/B/C 诊断  + RL-30 数值
核对
Bug 修复接
⼒ 重新读代码  1+ ⼩时 5 分钟恢复现场 TECH_SPEC.md + subtask
s.json
提交规范 ⼿写  commit 三段 ⾃动渲染  + ⼈⼯确认时间线  + 模板
最⼤的隐性收益：新⼈  / AI 都能直接接⼿已有需求的迭代，不再依赖 " 问原作者 " 。这是   TEC
H_SPEC.md 带来的复利效应。
⼗⼆、关键启⽰：如果你也想做这种  Skill
我们踩过的坑收敛成  5 条原则，普适性强，建议复⽤到你⾃⼰的项⽬：
原则 ⼀句话总结
流⽔线化 把 " 需求开发 " 拆成  8 个语义化阶段，每个阶段输⼊ / 输出 / 退出标准都可机器校验
脚本兜底LLM 负责 " 读判断 " ，精确数值 / 幂等执⾏ / 批量操作全部下沉到  Python/Shell 脚本
红线前置 把 " 哪些事  AI 绝对不能做 " 写成  YAML + 分层加载，触发即停、模板化报告
落盘判定任何长跑命令的成功证据都是 " ⽂件存在 " ，不依赖  stdout （ terminal 会截断 / 置后台）
沉淀闭环每次需求产出⼀份  git-tracked 的  TECH_SPEC.md，让 " 知识 " 和 " 代码 " 等量齐观
⼗三、附录： Skill ⽬录速览
整套  Skill 由  6 ⼤组件构成，按 "AI 进⼊流⽔线 " 的视⾓分层组织：
skills/mailplugin-feature-dev/
│
├── ①  对外⼊⼝（ LLM 启动时加载）
````

## PDF 第 26 页

[原页](RAW.pdf#page=26)

````text
│   ├── SKILL.md                          # 流程总图  + 4 类⼊⼝分流  + 强约束
│   ├── README.md                         # 给⼈看的使⽤指南
│   └── CHANGELOG.md                      # 版本变更⽇志
│
├── ②  安装与配置
│   └── setup/
│       ├── install.sh                    # ⼀键安装（含  MCP 注册、依赖检测）
│       ├── uninstall.sh                  # ⼀键卸载
│       └── mcp.tapd.json                 # TAPD MCP Server 配置
│
├── ③  ⾃动化脚本（" 判断交给  LLM ，数据交给脚本 "）
│   └── tools/
│       │  —— 收料（公理  Ⅱ ：绕过上下⽂截断） ——
│       ├── fetch_tapd_story.py           # TAPD ⼀站式收料：单据 + 附件 + 评论
│       ├── fetch_tapd_images.py          # TAPD 图⽚批量下载
│       ├── fetch_figma_mcp.py            # Figma MCP 数据落盘
│       ├── scan_figma_frames.py          # 设计稿直⽅图筛选（ RL-17 ）
│       │
│       │  —— ⽂档⽣成与维护  ——
│       ├── locate_feature_doc.py         # 定位  TECH_SPEC.md 路径
│       ├── render_tech_spec.py           # TECH_SPEC.md ⾸次渲染
│       ├── append_evolution_log.py       # §7/§8/§9 增量维护  + sentinel
│       ├── append_bug_fix.py             # bug 修复记录追加
│       ├── breakdown_subtasks.py         # ⼦任务台账（跨会话接⼒）
│       ├── gen_red_lines_docs.py         # 红线  yaml → 派⽣  md
│       │
│       │  —— 编译与验证（公理  Ⅰ ：落盘判定） ——
│       ├── build_verify.sh               # bazel 编译  + 报告
│       ├── check_implement_done.sh       # 实现完成度⾃检
│       ├── check_intermediate_artifacts.py # 阶段产物完整性检查
│       ├── check_project_wiki_stale.py   # 知识库时效性扫描
│       ├── check_ui_token_usage.sh       # UI Token 合规检查
│       │
│       │  —— 模拟器与提交  ——
│       ├── install_to_simulator.sh       # 安装包到模拟器
│       ├── iphone_sizes.json             # 设备尺⼨数据库
│       ├── finalize_commit.sh            # 提交收尾
│       ├── render_commit_msg.py          # commit message 模板渲染
│       ├── timeline_to_commit_lines.py   # 时间线  → commit ⾏
│       └── md_to_pdf.py                  # ⽂档导出
│
├── ④  知识库与映射（" 代码侧地图  + 语义桥 "）
│   └── references/
│       ├── project_wiki/                 # 分模块知识库（按业务域  + 基础设施分册）
│       │   ├── overview.md               # 总览索引（ < 5KB ，作为  L1 ⼊⼝）
│       │   └── *.md                      # 各模块  L2 详情（按需加载）
│       │
````

## PDF 第 27 页

[原页](RAW.pdf#page=27)

````text
│       ├── figma_token_mapping.md        # L3 语义桥： Figma → ⼯程代码
│       ├── figma_device_sizes.md         # 设计稿设备尺⼨映射
│       └── ui_components_wiki.md         # 统⼀  UI 组件⽂档
│
├── ⑤  流程细则（按需加载，不污染上下⽂）
│   └── references/
│       │  —— 8 个阶段完整执⾏细则  ——
│       ├── stage_locate.md               # 阶段  1 ：意图消歧  + 定位
│       ├── stage_design.md               # 阶段  2 ：设计⽂档收料
│       ├── stage_breakdown.md            # 阶段  3 ：需求拆解  + ⼦任务台账
│       ├── stage_implement.md            # 阶段  4 ：编码实现
│       ├── stage_verify.md               # 阶段  5 ：编译验证
│       ├── stage_simulator_verify.md     # 阶段  6 ：模拟器验证
│       ├── stage_commit.md               # 阶段  7 ：提交收尾
│       ├── stage_archive.md              # 阶段  8 ：归档与沉淀
│       │
│       │  —— 4 类⼊⼝⼦流程  ——
│       ├── bug_fix_workflow.md           # ⼊⼝  ② ： bug 修复
│       ├── incremental_workflow.md       # ⼊⼝  ③ ：增量迭代
│       ├── redo_workflow.md              # ⼊⼝  ④ ：推倒重来
│       │
│       │  —— ⼯具箱  ——
│       ├── simulator_toolbox.md          # 模拟器调试⼯具箱
│       └── tech_spec_template.md         # TECH_SPEC.md 模板
│
└── ⑥  红线机制（公理  Ⅲ ：硬关卡）
    └── references/
        ├── red_lines.yaml                # 红线单⼀真源（ DSL ）
        ├── red_lines_critical.md         # 全局强制加载（启动即⽣效）
        └── red_lines_by_stage/           # 分阶段按需加载
            ├── global.md                 # 跨阶段通⽤红线
            ├── locate.md                 # 阶段  1 红线
            ├── design.md                 # 阶段  2 红线
            ├── breakdown.md              # 阶段  3 红线
            ├── implement.md              # 阶段  4 红线（最厚⼀份）
            ├── verify.md                 # 阶段  5 红线
            ├── simulator_verify.md       # 阶段  6 红线
            ├── commit.md                 # 阶段  7 红线
            └── archive.md                # 阶段  8 红线
写在最后
⼀个直观感受： **references/ ⽐   tools/  体量更⼤ **—— 这是 "AI 提效在⼯程⽽不在模
型 " 最朴素的证据，绝⼤部分能⼒都来⾃被显式编写的规则、知识、模板，⽽不是 " 指望模
型聪明 " 。
````

## PDF 第 28 页

[原页](RAW.pdf#page=28)

````text
阅读 5 . 0 万
我们⼀开始想做的是 " 让  AI 帮我写代码 " ；做完才意识到 ——真正有价值的，是让 " 需求开
发 " 这件事本⾝被显式建模、可观测、可接⼒。
Skill 只是把这些⼯程规范 " 具象成了  LLM 能消化的格式 " 。⽽沉淀下来的   TECH_SPEC.m
d  和   project_wiki，即使有⼀天换掉  AI ，对⼈也是同样有⽤的资产。
AI 提效的天花板，既在模型，也在⼯程。
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
留⾔ 1
写留⾔
````

## PDF 第 29 页

[原页](RAW.pdf#page=29)

````text
asc⼴东7 ⽉ 23 ⽇
 31
⼀个 xxx 跑通 xxx 的，⼀律当忽悠
````


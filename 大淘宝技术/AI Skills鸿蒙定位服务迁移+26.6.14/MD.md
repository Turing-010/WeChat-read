# 用 AI Skills 打通中间件迁移：定位服务从 Android 到鸿蒙的完整实践：PDF文本转写

> 这是原始PDF文本层转写，不是学习摘要。页码为PDF物理页序；图表、代码版面和图片文字不能完整表达在此文本层。已查看图像的内容和质量问题见AI学习笔记及META.json。

[原文PDF](RAW.pdf) · [AI学习笔记](AI_AI Skills鸿蒙定位服务迁移.md) · [处理与质量记录](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
用 AI Skills 打通中间件迁移：定位服务从 Android 到鸿蒙的完整实
践
原创
用户&内容技术 2026年6月14日 23:06 浙江
大淘宝技术 8人
本文以Andro
领域知
id到鸿蒙的定位服务迁移为实战案例，深
入剖析了AI辅助开
发
中通用智能与
识断层的根本矛盾，提出并验证了“AI
+ Skills”解决
方
案。该方
案通过将API映
射
、枚举细节、回调差异及常见陷阱等隐性知
识转化为结构化、AI可读的Skills文档，明
确了AI负责通用逻辑生成、Skills提供精准领域知
识的分工模型，实现了从“面向人”到
“面向AI”的知
识传递转变。实
践表明，相比纯AI翻译的低
准确率和人工查源码的低效率，
AI
+ Skills模式
不仅将单服务迁移时间缩短至30分钟且零编译错误，更在154个服务的规
模化迁移中节省25小时，实现了知
识的资
产化、可复用与持续演进，最终展望了从静态文
档向知
识图谱、主动建议
及
组织级知
识中台发
展的未来路径。
引言：AI 辅助开
发
的根本矛盾
又双叒叕经历从0到1翻译一个安卓应用到鸿蒙的需求，并且近期Skill的概念很火，想着能通过
Skill真正的解决一些实际业务遇到的一些问题，所以开始着手维护一个鸿蒙依
赖
分析的Skill，为
了协助Curosr更好的理解端侧的二方包，最后我得出了两个暴论：
1、
目前很多知
识库是冗余的，随着模型能力越来越强，需要提供的业务知
识库是需要减负的
2、未来我们各种二方包的接入方式都会以Skill的形式提供，从面向人转到面向AI
▐ 现状：AI 很强大，但不够"准确"
场景还原：
1
2
3
4
5
// 你向 AI 提问："帮我将 Android 定位服务迁移到鸿蒙"
// AI 生成的代码（看起来很专业）
LocationExpires.ONE
_
MINUTE // ❌ 这个枚举值不存在
params.onSuccess = (result) => { ... } // ❌ 回调位置错误
// 编译
器提示：13 个错误
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
6 Property 'ONE
_
MINUTE' does not exist on type 'LocationExpires'
开
发
者的困惑：
AI 不是能理解代码吗？为什么会犯这种低
级错误？
文档明明存在，为什么 AI 不
看文档？
第一次踩
坑修好了
,第二次还会踩
,知
识怎
么沉淀？
▐ 本质：AI 的能力边界
根本矛盾：
重新定义问题
▐ 这不只是"代码翻译"问题
表面问题：Android 代码如何迁移到鸿蒙？
深层问题：
1.
知
识获取：开
发
者如何快速掌握新平台的 API？
2.
知
识传递：团队如何避免重复踩
坑？
3.
知
识演进：API 更新后如何快速同步？
4. AI 协同：如何让 AI 使用最新的领域知
识？
对比传统方式：
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 这是一个"知
识工程"问题
软件工程的两
大知
识库：
知
识的三个状态：
1. 隐性知
2. 显性知
3. 可执
知
行
识：在老员工脑子里（"这里要用 ONE
MIN，别用 ONE
_
识：在文档里（但分散、
滞
后
、难搜
索）
识：在 Skills 里（结构化、可索引、AI 可读）
MINUTE"）
_
AI + Skills 的价值：
AI
+ Skills 方法论
▐ 核心概念
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
定义：
AI + Skills = AI 的通用能力 + 可执
类比理解：
行
的领域知
识包
▐ 分工模型
▐ 工作流程
完整闭环：
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
关键环节：
1. 输
入阶段：AI 加载 Skills 获取领域知
识
2. 生成阶段：AI 使用 Skills 中的映射表
3. 验证阶段：编译/测试验证准确性
4.
反馈阶段：问题 → 提炼 → 更新 Skills
5. 沉淀
阶段：成功经验 → 记录到 Skills
实战案例 安卓定位服务 - 鸿蒙代码迁移
▐ 问题背景
业务场景：穿搭业务需要从0到1迁移到鸿蒙
技术挑战：
154 个 Android 服务需要迁移
每个服务涉及不同的 API 映射
团队中
大部分人不熟悉鸿蒙 API
传统方式的成本：
▐ 三种方式对比
方式 1：纯 AI 翻译（❌ 快但不
准）
操作：
提问："帮我将 Android 的 LBSService 翻译到鸿蒙"
AI 生成的代码：
1
2
3
// AI 基于"常识"猜
测的枚举值
LocationExpires.ONE
_
MINUTE // ❌ 实际是 ONE
_
MIN
LocationExpires.FIVE
_
MINUTE // ❌ 实际是 FIR
_
MIN
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
4
5
6
7
LocationAccuracy.MID
_
MODE // ❌ 这个枚举不存在
// AI 推测的回调
方式
const params = new LocationRequestLocationParams();
params.onSuccess = (result) => { ... }; // ❌ 回调不在这里
结果：
编译错误：13 个
调试时间：无法估计
根本原因：AI 没有准确的 API 文档
方式 2：查源码 +
人工修正（✅ 准但慢）
操作流程：
1. 打开 Mega Location 源码
2. 查看
实际的枚举定义
3. 逐个修正 AI 生成的错误
4. 测试验证
发现的真相：
1
2
3
4
5
6
7
8
9
10
11
12
// ✅ 实际的枚举定义（非常反直觉）
export enum LocationExpires {
ONE
MIN = "ONE
MIN"
_
_
, // 不是 ONE
_
MINUTE
SEC
MIN = "SEC
MIN"
_
_
, // 不是 TWO
MINUTE (SEC = SECOND)
_
THR
MIN = "THR
MIN"
_
_
, // 不是 THREE
MINUTE (THR = THREE)
_
FOR
MIN = "FOR
MIN"
_
_
, // 不是 FOUR
MINUTE (FOR = FOUR)
_
FIR
MIN = "FIR
_
_
MIN" // 不是 FIVE
MINUTE (FIR = FIVE)
_
}
// ✅ 实际的回调
方式
const options: Location.LocationRequestOptions = {
onSuccess: (result: LocationData) => { ... } // 回调在 options 内
};
结果：
编译错误：0 个
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
耗时：40 分钟
问题：知
识留在开
发
者脑子里，下次还要重新查
方式 3：AI
+ Skills（✅ 又快又准）
Step 1：构建 Skills
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
## 4. API 对比
### 4.1 LocationExpires 枚举值映射
| Android 常量 | 鸿蒙枚举 | 说明 |
|-------------|---------|------|
| "1m" | LocationExpires.ONE
_
MIN | ⚠ 不是 ONE
_
MINUTE |
| "2m" | LocationExpires.SEC
_
MIN | SEC = SECOND，不是 TWO
_
MIN |
| "3m" | LocationExpires.THR
_
MIN | THR = THREE，不是 THREE
_
MIN |
| "4m" | LocationExpires.FOR
_
MIN | FOR = FOUR，不是 FOUR
_
MIN |
| "5m" | LocationExpires.FIR
_
MIN | FIR = FIVE，不是 FIVE
_
⚠ **不存在的枚举值**（AI 经常错误生成）：
MIN |
- ❌ `ONE
MINUTE`
,
`TWO
MINUTE`
,
`FIVE
MINUTE`
_
_
_
- ❌ `TEN
MINUTE`
_
,
`MID
MODE`
_
### 4.2 定位请求
方法对比
| Android | 鸿蒙 | 差异说明 |
|---------|------|---------|
| `LocationServiceBridge.requestLocation()` | `Location.requestLocatio
#### 关键差异：回调设置方式
**Android**（回调
作为独立参数）：
```kotlin
LocationServiceBridge.requestLocation(
params,
{ result -> ... }, // 成功回调
{ error -> ... } // 失败回调
)
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
鸿蒙（回调在 options 对象内）：
1
2
3
4
5
6
const options: Location.LocationRequestOptions = {
bizName: 'TB
SHOPPING
PROCESS'
_
_
,
onSuccess: (result: LocationData) => { ... }, // ✅ 在 options 内
onFail: (error: string) => { ... }
};
Location.requestLocation(params, options);
▐ 三种方式的本质差异
关键洞察：
▐ 规模化效果
单个服务的迁移效率：
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
154 个服务的总成本：
节省时间：102 - 77 = 25 小时
关键价值：
⏰ 效率提升：节省 25 小时
📚 知
识资
产：154 个服务的迁移经验永久沉淀
🚀 团队加速：新人 0 学习成本
🔄 持续演进：API 更新后，只需更新 Skills
方法论推广
▐ 适用场景
AI + Skills 模式
不只适用于代码迁移，而是适用于所有需要领域知
识的 AI 辅助开
发场景：
通用模式：
有明确知
识的场景 → 知
识结构化为 Skills → AI 索引使用 → 提升质量和效率
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 构建 Skills 的原则
原则 1：AI 友好的结构化
❌ 不友好的文档（人类可读，AI 难索引）：
✅ AI 友好的文档（表格化、结构化）：
原则 2：持续演进
Skills 更新流程：
遇到问题 → 查看源码 → 提炼规律 → 更新 Skills → 发布版本 → 团队同步
原则 3：分层组织
Skill 文档结构：
```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
未来展望
▐ 从 Skills 到知
识图谱
当前：文档化的 Skills
未来：知
识图谱
价值：
AI 可以理解模块间的依
关系
赖
自动推荐相关
的 Skills
提供跨模块的最佳实
践
▐ 从被动查询到主动建议
```

## PDF 第12页

[查看原页](RAW.pdf#page=12)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
当前：开
者主动询问 AI
发
未来：AI 主动发现问题
技术方
案：
IDE 插件
实时分析代码
匹配 Skills 中的常见陷阱
编译前预警
▐ 从静态文档到动态生成
当前：人工编写 Skills
工程师踩
坑 → 查源码 → 编写文档 → 更新 Skills
未来：AI 自动生成 Skills
价值：
Skills 永远是最新的
0 人工维护成本
覆盖所有场景
```

## PDF 第13页

[查看原页](RAW.pdf#page=13)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 从个人工具到组织能力
当前：个人/团队使用
开
发
者 → AI + Skills → 提升个人效率
未来：组织级知
识平台
终极愿景：
新人入职第一天就能高效工作（AI 教学）
老人离职后知
识不流失（Skills 沉淀）
组织智慧持续积累（每次踩
坑都是资
产）
结语：重新定义软件工程的知
▐ 传统模式的困境
▐ AI + Skills 的突破
识传递
```

## PDF 第14页

[查看原页](RAW.pdf#page=14)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 核心价值主张
1. 效率提升：AI 的速度 + 领域专家的准确度
2.
知
识沉淀：从"人脑记忆"到"
组织资
产"
3. 持续演进：每次踩
坑都让 Skills 更完善
4. 团队赋能：新人 0 学习成本，老人不再重复劳动
团队介绍
本文作者开益，来自淘天集团-用户终端技术团队。我们服务于淘宝基础用户产品，是淘宝最
重要的业务线之一。首页、信息流推荐、消息聊天、
搜
索、我淘、用增、互动、内容等亿级用
户规模产品，为我们带来大量业务/技术挑战及机会。
团队在保证业务的同时，以先进的跨端框架和研发模式
不
程技术，保障多端设备的适配和稳定运
行
，并探索端智能等创
断完善自己，打造最极致的体验和工
的良性发
展。持续探索以AI为底座构建从需求到上线
新机会，通过技术高效驱动业务
的端到端自动化与产品化能力，使亿级规
模的交付更快、更稳
、更可控。
¤ 拓展阅读 ¤
3DXR技术 | 终端技术 | 音视频技术
服务端技术 | 技术质量 | 数据算法
大淘宝技术
大淘宝技术官方账号
967篇原创内容
公众号
阅读 2554
留言
```

## PDF 第15页

[查看原页](RAW.pdf#page=15)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
写留言
还没有
留言，来写首评
```

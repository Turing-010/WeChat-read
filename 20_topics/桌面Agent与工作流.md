# 桌面Agent与工作流

> AI跨文学习整理，2026-10-23更新。以下正文以本轮全文证据为依据；全库全文证据已汇总，本专题已按实质机制补查；全库结构验收另行记录。示例为教学推导，文章效果未在本地复现，官方核查仅限文档。个人记录区保持原文。

> 修订原因：把按文章追加的重复摘要合并为机制、条件、例子与跨篇对照；分开事件时间和发布日期，并修正效果口径、计划状态与过时接口。

## 我对这个主题的理解

（待本人填写；AI默认不修改）

## 桌面Agent的重点是把工作连接成可验收过程

用户入口、模型决策、工具执行、业务系统和产物展示可以在不同位置。一个手机入口不等于任务跑在手机；一个工作目录不等于沙箱；一个漂亮页面也不证明后台操作完成。学习时先画清“哪里接受请求、哪里运行、用谁的权限、结果在哪里验收”。[art-0130／capture-001，p.13–22、44–60、187–193](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/WorkBuddy%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E7%B2%BE%E9%80%9A%2B26.8.12/RAW.pdf#page=13) [art-0167／capture-001，p.5–9](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Kuikly%E8%BF%9C%E7%A8%8B%E6%8E%A7%E5%88%B6DSH%2B26.9.8/RAW.pdf#page=5)

## 用一条工作流理解各组件分工

以“从业务数据生成可分享周报”为教学例：

1. 确认数据来源、授权范围、时间口径、输出位置和验收标准。
2. 有API就用受控接口；有SDK/脚本可包装结构化CLI；只有界面才用浏览器/RPA。MCP暴露能力，后端仍可以调用API或CLI，三者并非互相排斥。
3. Skill组织步骤、失败分支和质量检查；工具执行层落实参数、权限、超时和真实结果。
4. 生成产物后校对数值、来源和可运行性；保存版本，把反馈绑定到具体页面/位置。
5. 单次跑通后再考虑定时，记录运行、失败、成本和停止条件；本地执行依赖机器可用。

这是多篇机制合并出的练习路径，没有替用户安装或定时执行任何系统。[art-0139／capture-001，p.1–6](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E8%80%81%E7%B3%BB%E7%BB%9F%E6%8E%A5AI%E6%8E%A5%E5%85%A5%E5%9B%BE%2B26.10.12/RAW.pdf#page=1) [art-0173／capture-001，p.3–10、19–30](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E8%85%BE%E8%AE%AFWorkBuddy%20Agent%E4%BA%A7%E5%93%81%E5%AE%9E%E8%B7%B5%2B26.7.24/RAW.pdf#page=3) [art-0130／capture-001，p.130–135、160–171](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/WorkBuddy%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E7%B2%BE%E9%80%9A%2B26.8.12/RAW.pdf#page=130) [art-0152／capture-001，p.1–5](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/WorkBuddy%20%E5%A4%9A%E4%BA%BA%E5%8D%8F%E4%BD%9C%2B26.9.17/RAW.pdf#page=1)

## 接入层、工作流层与展示层不要混淆

| 层 | 解决的问题 | 材料中的机制 | 边界 |
|---|---|---|---|
| 接入 | 如何调用已有系统 | API薄封装、结构化CLI、浏览器/RPA、MCP | 接通不证明权限、语义或错误恢复正确 |
| 流程 | 什么时候做哪一步 | Skill、Loop、Graph、Hook和人为确认 | 名称不保证质量；确定步骤和自主循环可组合 |
| 执行 | 如何控制副作用 | 工具前校验、限时、取消、隔离和回执 | 桌面本地执行仍可能把资料发到远程模型 |
| 展示 | 怎样呈现真实业务数据 | QueryRegistry或工具产出数据/UI描述 | 模型直写实时数字可能过期或虚构 |
| 协作 | 怎样让反馈指向当前产物 | 同URL、位置评论、版本历史 | 同链接不等于无并发写冲突 |
| 远程入口 | 手机继续查看控制任务 | Host RPC、事件补齐、连接世代号 | 电脑离线时不能仅凭入口在线推断仍执行 |

[art-0139／capture-001，p.1–6](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E8%80%81%E7%B3%BB%E7%BB%9F%E6%8E%A5AI%E6%8E%A5%E5%85%A5%E5%9B%BE%2B26.10.12/RAW.pdf#page=1) [art-0173／capture-001，p.19–30](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E8%85%BE%E8%AE%AFWorkBuddy%20Agent%E4%BA%A7%E5%93%81%E5%AE%9E%E8%B7%B5%2B26.7.24/RAW.pdf#page=19) [art-0170／capture-001，p.3–11](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E8%85%BE%E8%AE%AFOmega%20AI%20BI%E6%9E%B6%E6%9E%84%2B26.8.3/RAW.pdf#page=3) [art-0237／capture-001，p.7–16](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/%E5%8D%A1%E7%89%87%E5%BC%8F%E5%AF%B9%E8%AF%9D%E5%8D%8F%E8%AE%AE%E6%96%B9%E6%A1%88%E6%8E%A2%E7%B4%A2%2B26.4.17/RAW.pdf#page=7) [art-0152／capture-001，p.1–5](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/WorkBuddy%20%E5%A4%9A%E4%BA%BA%E5%8D%8F%E4%BD%9C%2B26.9.17/RAW.pdf#page=1) [art-0167／capture-001，p.4–9](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Kuikly%E8%BF%9C%E7%A8%8B%E6%8E%A7%E5%88%B6DSH%2B26.9.8/RAW.pdf#page=4) [art-0040／capture-001，p.22–24](../%E9%98%BF%E9%87%8C%E6%8A%80%E6%9C%AF/%E5%9E%82%E7%B1%BB%E7%94%9F%E4%BA%A7%E7%BA%A7Agent%E8%90%BD%E5%9C%B0%2B26.9.16/RAW.pdf#page=22)

## 界面反馈与接口复用怎样配合

GUI Agent入门案例把循环具体化为“截图—模型决策—鼠标键盘执行—新截图”。历史记录只说明之前决定做什么，新截图才提供界面发生了什么的证据。例如上轮决定输入“你好”，本轮应核对文本是否已出现，不能因历史里有输入动作就结束。模型给出的0—1000坐标还需按屏幕宽高变换；1920×1080屏幕中的(500,500)对应(960,540)，缩放和多屏环境仍须验证。这补充了桌面工作流中观察、动作协议和效果验收的连接。[art-0119／capture-001，p.3—9、11—13、17](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/GUI%20Agent%20%E5%85%A5%E9%97%A8%2B26.1.19/RAW.pdf#page=3)

该教程把空动作和模型的finished声明视为停止，关闭了pyautogui的fail-safe，且若干代码行截断；这些不是可靠交付的保证。解析失败应成为明确错误，终止时核对目标状态，并保留独立停止保护和必要的操作确认。本轮仅学习其流程，没有执行这些代码。[art-0119／capture-001，p.7、11—16](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/GUI%20Agent%20%E5%85%A5%E9%97%A8%2B26.1.19/RAW.pdf#page=7)

OpenCLI文章则补充另一种组合：先用GUI触发懒加载操作、观察前后网络请求，验证接口语义，再把可重复操作封为参数明确、返回值结构化的CLI适配器；GUI仍可用于发现与兜底。这样可以减少反复识别界面的成本，但接口、签名和会话也会变化，并非所有页面都能还原为稳定JSON接口。凭据不应固化到共享适配器，实际授权与写入结果仍要由执行层核对。[art-0225／capture-001，p.1—6](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/%E6%B5%8F%E8%A7%88%E5%99%A8%E8%87%AA%E5%8A%A8%E5%8C%96GUI%E5%88%B0OpenCLI%2B26.5.22/RAW.pdf#page=1)

**时间关系：** GUI教程发表于2026-01-19，OpenCLI实践发表于2026-05-22；二者是并行方案的互补，未证后者直接继承前者，更不能理解为GUI已经被淘汰。OpenCLI原文当时的录制器未完整捕获POST/PUT请求体，因此自动生成受限于只读接口；这是未锁版本的历史观察，不是当前项目能力结论。文中招聘沟通截图也未提供文字层的发送回执，不能据此认定写操作闭环已验证。[art-0225／capture-001，p.7—10](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/%E6%B5%8F%E8%A7%88%E5%99%A8%E8%87%AA%E5%8A%A8%E5%8C%96GUI%E5%88%B0OpenCLI%2B26.5.22/RAW.pdf#page=7)

## 为什么“800行实现”与成熟产品仍有距离

教学OpenClaw把工具声明/执行注册、消息总线、AgentLoop拆开，适合看懂核心循环；但单线程也会在`await`间交错，共享文件和处理标志仍可能竞争。去掉`edit_file`而保留`write_file/exec`不构成文件修改限制；字符串规则检查命令不等于沙箱。学架构时保留这些边界，别把演示的简洁当生产完整性。[art-0234／capture-001，p.1–12](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/OpenClaw%E6%A0%B8%E5%BF%83%E6%9E%B6%E6%9E%84800%E8%A1%8C%E5%AE%9E%E7%8E%B0%2B26.4.24/RAW.pdf#page=1)

DSH/Cordis则展示依赖激活、资源登记和逆序卸载，这解决插件生命周期；Worker限制堆和运行时间也有帮助，但与OS权限隔离是不同问题。插件共享实例还要处理会话状态是否串用。[art-0144／capture-001，p.2–14](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/DeepSeek%20Harness%E6%9E%B6%E6%9E%84%2B26.8.14/RAW.pdf#page=2) [art-0145／capture-001，p.4–23](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Cordis%E4%B8%8EDSH%E8%BF%90%E8%A1%8C%E6%97%B6%2B26.9.4/RAW.pdf#page=4)

## 交互卡片的进步发生在哪里

art0237从模型直接生成业务数据，推进到带ID占位、异步补数据，再到工具返回真实数据和UI描述。核心变化是把**数据真值和执行逻辑交给受控系统**，模型负责意图和编排。流式JSON未完整时不能直接解析；卡片需完整性状态、schema验证、错误显示和受限事件处理。固定模板到动态组合扩大表达范围，但不取消客户端支持组件的边界。[art-0237／capture-001，p.1–16](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/%E5%8D%A1%E7%89%87%E5%BC%8F%E5%AF%B9%E8%AF%9D%E5%8D%8F%E8%AE%AE%E6%96%B9%E6%A1%88%E6%8E%A2%E7%B4%A2%2B26.4.17/RAW.pdf#page=1)

因此一个“刷新”按钮至少带明确动作与参数，宿主校验权限后查询，回传状态和错误；不能因为UI不含任意JavaScript，就假定它没有危险业务副作用。[art-0237／capture-001，p.11–16](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/%E5%8D%A1%E7%89%87%E5%BC%8F%E5%AF%B9%E8%AF%9D%E5%8D%8F%E8%AE%AE%E6%96%B9%E6%A1%88%E6%8E%A2%E7%B4%A2%2B26.4.17/RAW.pdf#page=11) [art-0170／capture-001，p.6–11](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E8%85%BE%E8%AE%AFOmega%20AI%20BI%E6%9E%B6%E6%9E%84%2B26.8.3/RAW.pdf#page=6)

| 补充案例（发布日期） | 独特贡献 | 不能越过的边界 |
|---|---|---|
| art0320 Gemini CLI（2025-11-24） | core做工具调度/确认、cli做UI；工具结果经回调重入模型；显示历史、API历史、固定知识和快照有不同生命周期 | 未锁源码SHA；本地save/resume不等于恢复外部副作用，架构图存在加载缺口 |
| art0322 PPT工作流（2025-12-29） | 从零HTML转换、OOXML精修、模板复用分三路；中间表示和最终渲染分别验收 | 全清文字后回填要求完整清单；shape ID依模板版本，结构通过不等于布局/事实正确；并发异常被捕获不等于每页成功 |

[art-0320／capture-001，p.4–13](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/GeminiCLI%E5%86%85%E6%A0%B8%E6%BA%90%E7%A0%81%E8%A7%A3%E6%9E%84%2B25.11.24/RAW.pdf#page=4) [art-0322／capture-001，p.25、32–49](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/PPTSkill%E4%B8%89%E7%A7%8D%E6%96%87%E6%A1%A3%E5%B7%A5%E4%BD%9C%E6%B5%81%2B25.12.29/RAW.pdf#page=25) 这两篇分别补内核运行链和非代码文档验收，并非由桌面产品名称串成的版本递进。PPT教程是2025特定Skill分析，不能当当前工具能力保证。

## 同产品材料如何互补

| 来源（发布日期） | 可学机制或核验方法 | 时间与效果边界 |
|---|---|---|
| art0122 Clawdbot/Moltbot（2026-01-27） | IM入口→本地Agent→模型API→文件/终端；入口用户白名单与执行权限分开 | 文章说刚改名但未给确切日，旧配置不当安装指南；本地存储不等于离线推理 |
| art0098 Marvis（2026-05-27） | 同会话继承尝试状态，跨会话只传关键memory；按每个子目标验收，案例承认重命名未完成 | 30→40→10→6→3→2分钟是同会话样例，非权重训练或独立性能曲线 |
| art0053 Marvis（2026-06-24） | 限测试目录，分析附行列计算，网页附来源，系统操作先诊断再授权 | 六任务体验无正式基准；本地模式不能据此证明所有网络链路不外传 |
| art0157 Marvis访谈（2026-07-15） | 按端云职责分工，目录白名单、恢复开关卡片和远程连接可见性 | 设计理由不证明底层不可绕过；垂直小模型仍计划，访谈时间未知 |

[art-0122／capture-001，p.1–6](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Clawdbot%E4%BA%A7%E5%93%81%E5%85%A5%E5%8F%A3%2B26.1.27/RAW.pdf#page=1) [art-0098／capture-001，p.3–10、14–16](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Marvis%E6%A1%8C%E9%9D%A2Agent%E5%AE%9E%E6%B5%8B%2B26.5.27/RAW.pdf#page=3) [art-0053／capture-001，p.7–9、15–19](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Marvis%E9%A9%AC%E7%BB%B4%E6%96%AF%E5%85%A5%E9%97%A8%2B26.6.24/RAW.pdf#page=7) [art-0157／capture-001，p.3–5](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Marvis%E5%85%AD%E5%8F%AA%E5%B0%8F%E9%A9%AC%2B26.7.15/RAW.pdf#page=3) 后三篇是同产品的内部体验、用户核验和设计访谈，不是三个架构版本；2026-05-20上线是作者所述事件，不能用各篇发文日替代。

## 时间线：明确的继承与并行发展

| 事件时间 | 文章发布日期 | 关系与变化 |
|---|---|---|
| 2020 Koishi→2022 Cordis包→2023末3.x→2024-11 4预发布 | 2026-09-04，art0145 | 插件系统直接演化，2026被复用于Harness |
| 2024 DataTalk→2026-01 Omega开工 | 2026-08-03，art0170 | 同团队从问答推进到可持续运行分析产物 |
| 卡片方案探索的实施日未给 | 2026-04-17，art0237 | 直接生成→占位→工具数据为文内设计路径；不是各协议替代史 |
| 教学实现未给逐阶段日期 | 2026-04-24，art0234 | 用短实现解释循环和工具，不能看作完整产品发布 |
| 产品实践状态 | 2026-07-24／08-12，art0173／0130 | 从架构分层到用户任务操作；长手册混有旧FAQ和新功能，非统一版本快照 |
| DSH v0.1.1-rc.2移动实践 | 2026-09-08，art0167 | 增加远程观察/控制，执行仍在Host |
| PPT协同仍内测待上线 | 2026-09-17，art0152 | 共享产物和位置反馈已作为场景描述；不补写未上线能力 |

[art-0145／capture-001，p.1–6](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Cordis%E4%B8%8EDSH%E8%BF%90%E8%A1%8C%E6%97%B6%2B26.9.4/RAW.pdf#page=1) [art-0170／capture-001，p.1–2](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E8%85%BE%E8%AE%AFOmega%20AI%20BI%E6%9E%B6%E6%9E%84%2B26.8.3/RAW.pdf#page=1) [art-0237／capture-001，p.7–16](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/%E5%8D%A1%E7%89%87%E5%BC%8F%E5%AF%B9%E8%AF%9D%E5%8D%8F%E8%AE%AE%E6%96%B9%E6%A1%88%E6%8E%A2%E7%B4%A2%2B26.4.17/RAW.pdf#page=7) [art-0234／capture-001，p.1–12](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/OpenClaw%E6%A0%B8%E5%BF%83%E6%9E%B6%E6%9E%84800%E8%A1%8C%E5%AE%9E%E7%8E%B0%2B26.4.24/RAW.pdf#page=1) [art-0173／capture-001，p.3–30](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E8%85%BE%E8%AE%AFWorkBuddy%20Agent%E4%BA%A7%E5%93%81%E5%AE%9E%E8%B7%B5%2B26.7.24/RAW.pdf#page=3) [art-0130／capture-001，p.187–193](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/WorkBuddy%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E7%B2%BE%E9%80%9A%2B26.8.12/RAW.pdf#page=187) [art-0167／capture-001，p.4–9](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Kuikly%E8%BF%9C%E7%A8%8B%E6%8E%A7%E5%88%B6DSH%2B26.9.8/RAW.pdf#page=4) [art-0152／capture-001，p.3–4](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/WorkBuddy%20%E5%A4%9A%E4%BA%BA%E5%8D%8F%E4%BD%9C%2B26.9.17/RAW.pdf#page=3)

## 当前协议核查：新名称不能套旧语义

截至2026-10-23，MCP Apps可由工具关联互动HTML，在宿主iframe中展示，并支持双向交互及同服务工具调用，不能简化成“一工具固定一张静态卡片”。[MCP Apps官方说明](https://modelcontextprotocol.io/extensions/apps/overview)

当前WebMCP为2026-10-20社区草案，接口是`Document.modelContext`；旧示例中的`navigator.modelContext`需按版本核对。它是页面向Agent提供结构化能力的Web API，不等同把网页变成远程MCP Server，也不是W3C正式标准。[WebMCP草案](https://webmachinelearning.github.io/webmcp/)

MCP Streamable HTTP的2026-07-28规范移除GET流和协议session；POST可返回JSON或请求范围SSE，旧版会话恢复不能直接照搬。这里的SSE技术仍存在，被替代的是旧HTTP+SSE传输安排。[当前传输规范](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http) [art-0139／capture-001，p.4–5](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E8%80%81%E7%B3%BB%E7%BB%9F%E6%8E%A5AI%E6%8E%A5%E5%85%A5%E5%9B%BE%2B26.10.12/RAW.pdf#page=4)

这些核查只确认规范和文档，未测试任意桌面宿主支持情况。产品按钮、收费、模式和兼容性以实际版本为准；本文不把手册里的截图当当前功能保证。

## 自测：先回答，再展开

**1. 手机可以发任务，为什么还可能依赖电脑不能休眠？**
<details><summary>答案</summary>
手机可能只是入口和渲染客户端，Agent与工具仍在电脑Host运行。必须区分通道在线和执行环境在线。
</details>

**2. CLI、MCP和Skill应该选哪一个？**
<details><summary>答案</summary>
它们常处于不同层：CLI可实现能力，MCP可暴露能力，Skill组织使用流程。按已有接口、权限和任务契约组合，再做同功能比较。
</details>

**3. 分享的是同一个页面URL，为什么仍需要版本和冲突处理？**
<details><summary>答案</summary>
同入口只帮助大家定位产物，不保证同时写入有序、引用版本一致或反馈不会覆盖。需版本、修改范围与验收机制。
</details>

**4. 卡片数据由工具返回，就一定可以放心显示和执行吗？**
<details><summary>答案</summary>
仍需验证时效、权限、schema、错误状态及事件参数；按钮引发的真实操作要单独授权，工具结果也不天然正确。
</details>


## 来源索引

以下采用META指定默认采集版本。正文引用使用PDF物理页；发布日期不是机制首次出现时间。

| 来源 | 发布日期 | 本专题使用页 | 证据报告 |
|---|---|---|---|
| [art-0320 深入AI Agent内核: Google gemini-cli 源码深度解构](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/GeminiCLI%E5%86%85%E6%A0%B8%E6%BA%90%E7%A0%81%E8%A7%A3%E6%9E%84%2B25.11.24/RAW.pdf)（capture-001） | 2025-11-24 | 4–13 | inbox-05.json |
| [art-0322 用AI写PPT，没想到效果这么好啊](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/PPTSkill%E4%B8%89%E7%A7%8D%E6%96%87%E6%A1%A3%E5%B7%A5%E4%BD%9C%E6%B5%81%2B25.12.29/RAW.pdf)（capture-001） | 2025-12-29 | 25、32–49 | inbox-07.json |
| [art-0122 一夜爆火，Clawdbot 是否才是真正的 AI 入口产品?](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Clawdbot%E4%BA%A7%E5%93%81%E5%85%A5%E5%8F%A3%2B26.1.27/RAW.pdf)（capture-001） | 2026-01-27 | 1–6 | tencent-01.json |
| [art-0237 卡片式对话的协议方案探索和思考](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/%E5%8D%A1%E7%89%87%E5%BC%8F%E5%AF%B9%E8%AF%9D%E5%8D%8F%E8%AE%AE%E6%96%B9%E6%A1%88%E6%8E%A2%E7%B4%A2%2B26.4.17/RAW.pdf)（capture-001） | 2026-04-17 | 1–16；7–16；11–16 | taobao-06.json |
| [art-0234 800行代码实现 Open Claw 的 Tool、消息总线、子Agent管理架构](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/OpenClaw%E6%A0%B8%E5%BF%83%E6%9E%B6%E6%9E%84800%E8%A1%8C%E5%AE%9E%E7%8E%B0%2B26.4.24/RAW.pdf)（capture-001） | 2026-04-24 | 1–12 | taobao-06.json |
| [art-0098 Marvis 实测：6 个 AI “牛马”扎根桌面之后](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Marvis%E6%A1%8C%E9%9D%A2Agent%E5%AE%9E%E6%B5%8B%2B26.5.27/RAW.pdf)（capture-001） | 2026-05-27 | 3–10、14–16 | tencent-05.json |
| [art-0053 从0到1带你速通Marvis马维斯](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Marvis%E9%A9%AC%E7%BB%B4%E6%96%AF%E5%85%A5%E9%97%A8%2B26.6.24/RAW.pdf)（capture-001） | 2026-06-24 | 7–9、15–19 | tencent-07.json |
| [art-0157 上线后差点‘挤爆’服务器，Marvis凭什么让用户追着6只小马‘上班’？](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Marvis%E5%85%AD%E5%8F%AA%E5%B0%8F%E9%A9%AC%2B26.7.15/RAW.pdf)（capture-001） | 2026-07-15 | 3–5 | tencent-08.json |
| [art-0173 腾讯 WorkBuddy 实践：如何把 Agent 做成可用产品](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E8%85%BE%E8%AE%AFWorkBuddy%20Agent%E4%BA%A7%E5%93%81%E5%AE%9E%E8%B7%B5%2B26.7.24/RAW.pdf)（capture-001） | 2026-07-24 | 3–10、19–30；3–30；19–30 | tencent-late-01.json |
| [art-0170 腾讯 Omega：下一代“AI BI”的答案?](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E8%85%BE%E8%AE%AFOmega%20AI%20BI%E6%9E%B6%E6%9E%84%2B26.8.3/RAW.pdf)（capture-001） | 2026-08-03 | 1–2；3–11；6–11 | tencent-late-01.json |
| [art-0130 3万字长文带你 WorkBuddy 从入门到精通](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/WorkBuddy%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E7%B2%BE%E9%80%9A%2B26.8.12/RAW.pdf)（capture-001） | 2026-08-12 | 13–22、44–60、187–193；130–135、160–171；187–193 | tencent-late-03.json |
| [art-0144 DeepSeek Harness 拆解：一套能拼装的 Agent 架构](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/DeepSeek%20Harness%E6%9E%B6%E6%9E%84%2B26.8.14/RAW.pdf)（capture-001） | 2026-08-14 | 2–14 | tencent-late-03.json |
| [art-0145 DeepSeek Harness 背后的“心脏”：Cordis 到底是什么](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Cordis%E4%B8%8EDSH%E8%BF%90%E8%A1%8C%E6%97%B6%2B26.9.4/RAW.pdf)（capture-001） | 2026-09-04 | 1–6；4–23 | tencent-late-06.json |
| [art-0167 我用腾讯 Kuikly，把 DeepSeek Harness 装进了口袋](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Kuikly%E8%BF%9C%E7%A8%8B%E6%8E%A7%E5%88%B6DSH%2B26.9.8/RAW.pdf)（capture-001） | 2026-09-08 | 4–9；5–9 | tencent-late-07.json |
| [art-0040 垂类业务如何落地生产级 Agent](../%E9%98%BF%E9%87%8C%E6%8A%80%E6%9C%AF/%E5%9E%82%E7%B1%BB%E7%94%9F%E4%BA%A7%E7%BA%A7Agent%E8%90%BD%E5%9C%B0%2B26.9.16/RAW.pdf)（capture-001） | 2026-09-16 | 22–24 | ali-07.json |
| [art-0152 WorkBuddy资料库：从三大场景开始，让多人多Agent轻松协作](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/WorkBuddy%20%E5%A4%9A%E4%BA%BA%E5%8D%8F%E4%BD%9C%2B26.9.17/RAW.pdf)（capture-001） | 2026-09-17 | 1–5；3–4 | tencent-late-08.json |
| [art-0139 Agent、MCP、Skill、Cli、Model 一次讲透：老系统接入 AI 的概念地图与三条路径](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E8%80%81%E7%B3%BB%E7%BB%9F%E6%8E%A5AI%E6%8E%A5%E5%85%A5%E5%9B%BE%2B26.10.12/RAW.pdf)（capture-001） | 2026-10-12 | 1–6；4–5 | tencent-late-10.json |

## 我的实践与修正

（待本人填写；AI默认不修改）

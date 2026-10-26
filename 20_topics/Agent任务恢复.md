# Agent任务恢复

> AI跨文学习整理，2026-10-23更新。以下正文以本轮全文证据为依据；全库全文证据已汇总，本专题已按实质机制补查；全库结构验收另行记录。示例为教学推导，文章效果未在本地复现，官方核查仅限文档。个人记录区保持原文。

> 修订原因：把按文章追加的重复摘要合并为机制、条件、例子与跨篇对照；分开事件时间和发布日期，并修正效果口径、计划状态与过时接口。

## 我对这个主题的理解

（待本人填写）

## 恢复的对象至少有四层

长任务中断后，先判断究竟丢了什么：模型的推理上下文、工作文件/产物、运行状态、外部系统的真实结果。保存一份总结只能帮助重建上下文；保存工作目录也不自动保存图节点、待审批动作、工具回执或外部事务。恢复是重新建立这些层之间的一致关系。[art-0003／capture-002，p.6–11](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/LLM%E5%88%B0Harness%2B26.9.7/RAW_%E8%A1%A5%E9%87%87001.pdf#page=6) [art-0040／capture-001，p.18–25](../%E9%98%BF%E9%87%8C%E6%8A%80%E6%9C%AF/%E5%9E%82%E7%B1%BB%E7%94%9F%E4%BA%A7%E7%BA%A7Agent%E8%90%BD%E5%9C%B0%2B26.9.16/RAW.pdf#page=18)

## 可恢复任务需要留下什么

| 层次 | 最小应记录内容 | 不能据此声称 |
|---|---|---|
| 目标与验收 | 当前目标、约束、完成/失败/未验证项 | 文字写“完成”就等于验收通过 |
| 产物 | 路径、版本/hash、关联任务、已确认修改 | 文件存在就是当前有效版本 |
| 执行状态 | 线程/运行身份、阶段、节点、待办、检查点版本 | 只有sessionId就保存了完整状态或得到访问权 |
| 外部动作 | 请求身份、幂等键、参数、回执和权威查询方式 | 本地没收到成功就意味着外部没执行 |
| 批准 | 批准者、范围、参数版本、有效期 | 旧批准适用于后来改变的动作 |

这是把框架恢复、业务SOP和文件交接合并后的设计清单，实际字段随业务而定。[art-0324／capture-001，p.7–13、21](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/LangGraph%E4%BA%BA%E5%B7%A5%E5%B9%B2%E9%A2%84%E4%B8%8E%E6%81%A2%E5%A4%8D%2B25.12.15/RAW.pdf#page=7) [art-0040／capture-001，p.19–25](../%E9%98%BF%E9%87%8C%E6%8A%80%E6%9C%AF/%E5%9E%82%E7%B1%BB%E7%94%9F%E4%BA%A7%E7%BA%A7Agent%E8%90%BD%E5%9C%B0%2B26.9.16/RAW.pdf#page=19) [art-0203／capture-001，p.5–6、10–16](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/%E6%95%B0%E6%8D%AE%E9%9C%80%E6%B1%8224h%E4%BA%A4%E4%BB%98Skill%2B26.7.19/RAW.pdf#page=5) [art-0184／capture-001，p.19–20、25–26](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/%E4%BC%9A%E5%9C%BAAgent%20Harness%2B26.10.19/RAW.pdf#page=19)

## 检查点与人工中断怎样合作

LangGraph示例先配置checkpointer，以`thread_id`定位线程，在节点调用`interrupt`发出审查载荷，再以相同线程传`Command(resume=...)`。关键是恢复会从**节点开头重跑**，不是从程序某一行往后无缝继续。中断前尽量保留纯计算；写外部系统放在批准分支或独立步骤，同时用幂等和权威状态检查控制重试窗口。子图的父节点前段也可能重跑。[art-0324／capture-001，p.3、7–13、21](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/LangGraph%E4%BA%BA%E5%B7%A5%E5%B9%B2%E9%A2%84%E4%B8%8E%E6%81%A2%E5%A4%8D%2B25.12.15/RAW.pdf#page=3)

Checkpointer保存图状态；Store管理跨线程应用数据；两者都可用内存或持久后端。`InMemorySaver`不支持进程重启后的恢复。线程、检查点和用户是不同身份：同一线程有多个检查点，知道线程ID不等于有权限读它。[art-0330／capture-001，p.3–18](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/LangGraph%E9%95%BF%E7%9F%AD%E6%9C%9F%E8%AE%B0%E5%BF%86%E5%AE%9E%E8%B7%B5%2B25.12.8/RAW.pdf#page=3)

SAA1.1.2.0案例把框架检查点与跨进程**恢复调度**分开：任务表记录业务请求和Agent类型，MQ触发恢复，关机先摘流再停。多工具同节点的协作中断会把未执行工具标成error/mock，待节点正常结束后保存；这个办法不覆盖任意强杀，保存前已发生的外部动作仍要幂等。`WORKING`也不会自动让MQ重投，需要ack、扫描、租约/心跳及并发抢占协议。[art-0009／capture-001，p.2–13](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/%E9%95%BF%E7%A8%8B%E4%BB%BB%E5%8A%A1%E6%96%AD%E7%82%B9%E7%BB%AD%E4%BC%A0%2B26.9.9/RAW.pdf#page=2)

Loop engineering把下一轮入口写进外部状态：目标、已试方法、失败证据、验证结果和继续/重试/换策略/人工/结束决策；定时唤醒只是触发器。状态文件只有下次真的读取才有作用，worktree也只隔离一部分文件改动，不隔离共享服务或语义冲突。[art-0013／capture-001，p.1–12](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/Loop%E5%B7%A5%E7%A8%8B%E5%BE%AA%E7%8E%AF%2B26.9.20/RAW.pdf#page=1)

art0306（2025-10-20）是这条主线的早期概念补充：状态、节点、条件边与循环把人工介入和恢复点显式化；Planner、业务取证、Policy/Critic和执行角色按证据责任划分。材料没有完整恢复实验，且图可以同时承载确定流程和自主决策，不应按框架品牌划为互斥阵营。[art-0306／capture-001，p.2–8、10–13](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Agent%E6%A1%86%E6%9E%B6%E4%B8%8EWorkflow%E9%80%89%E5%9E%8B%2B25.10.20/RAW.pdf#page=2)

## 最小例子：提交成功但回执丢了

教学任务：生成报告后提交到业务系统。执行顺序是准备产物→记录提交参数和幂等键K→提交→保存回执→验收。若恰好在提交成功后、保存回执前崩溃，恢复时记录看起来仍是“提交中”。

此时先向权威系统按K查询。若已成功，补记回执再验收；若确定未执行，才以同一K重试；若结果未知，保留不确定状态并按业务策略处理。单纯把本地状态改成“完成”会丢验收，换新K直接重试可能产生重复。图检查点不能自动把远程业务提交和本地保存变成一个原子事务。[art-0040／capture-001，p.19–25](../%E9%98%BF%E9%87%8C%E6%8A%80%E6%9C%AF/%E5%9E%82%E7%B1%BB%E7%94%9F%E4%BA%A7%E7%BA%A7Agent%E8%90%BD%E5%9C%B0%2B26.9.16/RAW.pdf#page=19) [art-0324／capture-001，p.8、21](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/LangGraph%E4%BA%BA%E5%B7%A5%E5%B9%B2%E9%A2%84%E4%B8%8E%E6%81%A2%E5%A4%8D%2B25.12.15/RAW.pdf#page=8)

## 跨篇对照：恢复文件、沙箱和连接并非同一能力

| 材料 | 能恢复什么 | 特别容易误解的地方 |
|---|---|---|
| art0114工作检查点、art0051交接摘要 | 目标、有效决策、待办、文件线索 | 手写摘要有损；历史过程应与当前有效状态分开 |
| art0184 OSS备份 | SID目录与manifest关联的工作文件 | 两步写不是原子发布，不等于完整运行检查点；SID不是授权 |
| art0203 Spec文件 | 需求、建模证据和阶段产物 | 文件出现不证明人已确认，需阶段状态和版本 |
| art0142 Cube快照 | 兼容节点间暂停后恢复内存/文件系统 | v0.7预览不是无停顿迁移，节点故障自动恢复仍计划 |
| art0167移动客户端 | 重新订阅Host状态，补事件和完整队列快照 | 手机重连不应重发任务；queue/jobs不全在事件日志里 |
| art0170查询产物 | 已验证查询/图表契约、局部刷新及失败状态 | timeout与长时间没有输出不同；旧请求应取消并防迟到覆盖 |

[art-0114／capture-001，p.5–7](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/WorkBuddy%E4%BD%BF%E7%94%A8%E6%8A%80%E5%B7%A7%2B26.9.9/RAW.pdf#page=5) [art-0051／capture-001，p.7–8、19–21](../%E9%98%BF%E9%87%8C%E6%8A%80%E6%9C%AF/%E6%9C%AC%E5%9C%B0%E7%94%9F%E6%B4%BB%E5%88%86%E6%9E%90Agent%E5%AE%9E%E8%B7%B5%2B26.9.30/RAW.pdf#page=7) [art-0184／capture-001，p.19–20、25–26](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/%E4%BC%9A%E5%9C%BAAgent%20Harness%2B26.10.19/RAW.pdf#page=19) [art-0203／capture-001，p.5–6、10–16](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/%E6%95%B0%E6%8D%AE%E9%9C%80%E6%B1%8224h%E4%BA%A4%E4%BB%98Skill%2B26.7.19/RAW.pdf#page=5) [art-0142／capture-001，p.1–3](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/CubeSandbox%200.7.0%2B26.8.31/RAW.pdf#page=1) [art-0167／capture-001，p.4–9](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Kuikly%E8%BF%9C%E7%A8%8B%E6%8E%A7%E5%88%B6DSH%2B26.9.8/RAW.pdf#page=4) [art-0170／capture-001，p.8–11](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E8%85%BE%E8%AE%AFOmega%20AI%20BI%E6%9E%B6%E6%9E%84%2B26.8.3/RAW.pdf#page=8)

客户端恢复特别值得单独学：先恢复通道→按序号补session/event→对齐history→用queue/jobs完整快照覆盖；连接世代号丢弃上一次连接迟到的RPC。这里“补观察”与“重执行”分开，适用于很多远程任务界面。[art-0167／capture-001，p.4–5](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Kuikly%E8%BF%9C%E7%A8%8B%E6%8E%A7%E5%88%B6DSH%2B26.9.8/RAW.pdf#page=4)

## 时间线与递进边界

| 事件时间 | 发布日期 | 机制变化与关系 |
|---|---|---|
| 示例开发日未给 | 2025-12-08，art0330 | 框架层区分线程检查点与跨线程Store |
| 示例开发日未给 | 2025-12-15，art0324 | 在持久状态上增加中断载荷、批准和恢复值；同框架互补机制 |
| Spec实践日未给 | 2026-07-19，art0203 | 业务交接状态外显，补上人工阶段确认问题 |
| v0.6已引入Kubernetes；v0.7发布跨机预览 | 2026-08-31，art0142 | 同项目沙箱能力直接演化；自动故障迁移尚非已完成状态 |
| DSH v0.1.1-rc.2客户端实践 | 2026-09-08，art0167 | 连接恢复补状态和观察，不重发任务 |
| 实施日期未给 | 2026-10-19，art0184 | 工作文件备份可支撑任务延续，但不能借“备份”推完整执行恢复 |

这些方案位于不同层，可组合，不应写成“云备份取代图检查点”或“手机重连解决所有故障”。[art-0330／capture-001，p.3–18](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/LangGraph%E9%95%BF%E7%9F%AD%E6%9C%9F%E8%AE%B0%E5%BF%86%E5%AE%9E%E8%B7%B5%2B25.12.8/RAW.pdf#page=3) [art-0324／capture-001，p.7–13](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/LangGraph%E4%BA%BA%E5%B7%A5%E5%B9%B2%E9%A2%84%E4%B8%8E%E6%81%A2%E5%A4%8D%2B25.12.15/RAW.pdf#page=7) [art-0203／capture-001，p.5–6、14–16](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/%E6%95%B0%E6%8D%AE%E9%9C%80%E6%B1%8224h%E4%BA%A4%E4%BB%98Skill%2B26.7.19/RAW.pdf#page=5) [art-0142／capture-001，p.1–3](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/CubeSandbox%200.7.0%2B26.8.31/RAW.pdf#page=1) [art-0167／capture-001，p.4–9](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Kuikly%E8%BF%9C%E7%A8%8B%E6%8E%A7%E5%88%B6DSH%2B26.9.8/RAW.pdf#page=4) [art-0184／capture-001，p.19–20、25–26](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/%E4%BC%9A%E5%9C%BAAgent%20Harness%2B26.10.19/RAW.pdf#page=19)

## 当前核查与验证练习

截至2026-10-23，LangGraph官方仍明确要求恢复时保持线程身份、配置持久checkpointer，并说明中断节点会从头重跑。不能把2025示例里“保存在哪一行”的比喻当实际语义。[Interrupts官方文档](https://docs.langchain.com/oss/python/langgraph/interrupts) [Persistence官方文档](https://docs.langchain.com/oss/python/langgraph/persistence)

art0009发表于2026-09-09；它引用的恢复消息顺序问题实际在2026-05-28提出，修复PR4685于6月4日合入main，先保留历史再追加恢复输入。这里确认的是上游合并，未确认哪个发布版本首次包含修复，也未运行回归测试。[SAA issue4662](https://github.com/alibaba/spring-ai-alibaba/issues/4662) [修复PR4685](https://github.com/alibaba/spring-ai-alibaba/pull/4685) [art-0009／capture-001，p.5、13](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/%E9%95%BF%E7%A8%8B%E4%BB%BB%E5%8A%A1%E6%96%AD%E7%82%B9%E7%BB%AD%E4%BC%A0%2B26.9.9/RAW.pdf#page=5)

art0013发表于2026-09-20，为方法与引用案例综述；它没有提供可据此认定当前产品自动化行为相同的版本证据。本专题仅学习状态、反馈和终止机制，不照搬其产品操作。

可以用无外部副作用的演练任务做四个故障点：节点执行前、生成产物后、模拟提交后、保存回执后。每次重启后核目标、版本、待办和终态，检查是否重复执行；涉及真实业务动作时还需要其幂等/查询契约。此处提供练习设计，未运行这些故障注入，不能据此宣称任一框架已经提供exactly-once。

## 自测：先回答，再展开

**1. 备份工作目录为什么不等于完整任务检查点？**
<details><summary>答案</summary>
工作目录可能不含调度状态、线程检查点、待批准动作、外部回执和权威系统状态；多文件写入也可能不原子。
</details>

**2. interrupt之前打印或发送了邮件，恢复时会怎样？**
<details><summary>答案</summary>
节点从头重跑，之前代码可能再次执行。日志可重复、邮件也可能重复；把副作用移到批准后仍需要幂等和崩溃窗口处理。
</details>

**3. 断网回来后手机看到任务没结束，应重新提交吗？**
<details><summary>答案</summary>
先恢复观察、补事件与完整队列状态并重新订阅。Host可能仍在执行，重新提交会创建重复任务。
</details>

**4. 已有sessionId为何既不是长期记忆，也不是授权凭证？**
<details><summary>答案</summary>
它只是定位身份之一；保存了哪些状态、保留多久、是否持久、谁可读写分别由存储与权限策略决定。
</details>


## 来源索引

以下采用META指定默认采集版本。正文引用使用PDF物理页；发布日期不是机制首次出现时间。

| 来源 | 发布日期 | 本专题使用页 | 证据报告 |
|---|---|---|---|
| [art-0306 一文讲懂Agent及其主流框架：自己想、自己干、自己复盘的才是好Agent!](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Agent%E6%A1%86%E6%9E%B6%E4%B8%8EWorkflow%E9%80%89%E5%9E%8B%2B25.10.20/RAW.pdf)（capture-001） | 2025-10-20 | 2–8、10–13 | inbox-03.json |
| [art-0330 让AI智能体拥有像人类的持久记忆：基于LangGraph的长短期记忆管理实践指南](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/LangGraph%E9%95%BF%E7%9F%AD%E6%9C%9F%E8%AE%B0%E5%BF%86%E5%AE%9E%E8%B7%B5%2B25.12.8/RAW.pdf)（capture-001） | 2025-12-08 | 3–18 | inbox-07.json |
| [art-0324 破除AI Agent自主操控风险：万字解读LangGraph“人工干预”机制，附零基础实战](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/LangGraph%E4%BA%BA%E5%B7%A5%E5%B9%B2%E9%A2%84%E4%B8%8E%E6%81%A2%E5%A4%8D%2B25.12.15/RAW.pdf)（capture-001） | 2025-12-15 | 3、7–13、21；7–13、21；7–13；8、21 | inbox-07.json |
| [art-0203 Copilot 需求交付 Skill 如何实现数据需求24h交付](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/%E6%95%B0%E6%8D%AE%E9%9C%80%E6%B1%8224h%E4%BA%A4%E4%BB%98Skill%2B26.7.19/RAW.pdf)（capture-001） | 2026-07-19 | 5–6、14–16；5–6、10–16 | root-taobao-01.json |
| [art-0170 腾讯 Omega：下一代“AI BI”的答案?](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E8%85%BE%E8%AE%AFOmega%20AI%20BI%E6%9E%B6%E6%9E%84%2B26.8.3/RAW.pdf)（capture-001） | 2026-08-03 | 8–11 | tencent-late-01.json |
| [art-0142 CubeSandbox v0.7.0 发布：沙箱跨机流动，集群平滑演进](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/CubeSandbox%200.7.0%2B26.8.31/RAW.pdf)（capture-001） | 2026-08-31 | 1–3 | tencent-late-06.json |
| [art-0003 从一次 LLM 调用到完整 Harness，Agent 到底经历了什么？](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/LLM%E5%88%B0Harness%2B26.9.7/RAW_%E8%A1%A5%E9%87%87001.pdf)（capture-002） | 2026-09-07 | 6–11 | tencent-late-07.json |
| [art-0167 我用腾讯 Kuikly，把 DeepSeek Harness 装进了口袋](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Kuikly%E8%BF%9C%E7%A8%8B%E6%8E%A7%E5%88%B6DSH%2B26.9.8/RAW.pdf)（capture-001） | 2026-09-08 | 4–5；4–9 | tencent-late-07.json |
| [art-0009 Agent 长程任务断点续传：从框架 Checkpoint 到跨进程恢复的完整实践](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/%E9%95%BF%E7%A8%8B%E4%BB%BB%E5%8A%A1%E6%96%AD%E7%82%B9%E7%BB%AD%E4%BC%A0%2B26.9.9/RAW.pdf)（capture-001） | 2026-09-09 | 2–13；5、13 | taobao-11.json |
| [art-0114 10 个技巧，让你的 WorkBuddy 比别人好用！](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/WorkBuddy%E4%BD%BF%E7%94%A8%E6%8A%80%E5%B7%A7%2B26.9.9/RAW.pdf)（capture-001） | 2026-09-09 | 5–7 | tencent-late-07.json |
| [art-0040 垂类业务如何落地生产级 Agent](../%E9%98%BF%E9%87%8C%E6%8A%80%E6%9C%AF/%E5%9E%82%E7%B1%BB%E7%94%9F%E4%BA%A7%E7%BA%A7Agent%E8%90%BD%E5%9C%B0%2B26.9.16/RAW.pdf)（capture-001） | 2026-09-16 | 18–25；19–25 | ali-07.json |
| [art-0013 Loop engineering：把 agent 放进工程循环](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/Loop%E5%B7%A5%E7%A8%8B%E5%BE%AA%E7%8E%AF%2B26.9.20/RAW.pdf)（capture-001） | 2026-09-20 | 1–12 | taobao-12.json |
| [art-0051 高德本地生活分析 Agent 的 AI Native 实践全景（万字长文回顾）](../%E9%98%BF%E9%87%8C%E6%8A%80%E6%9C%AF/%E6%9C%AC%E5%9C%B0%E7%94%9F%E6%B4%BB%E5%88%86%E6%9E%90Agent%E5%AE%9E%E8%B7%B5%2B26.9.30/RAW.pdf)（capture-001） | 2026-09-30 | 7–8、19–21 | ali-inbox-extra.json |
| [art-0184 告别 AI Demo 页面：构建支持淘内货品运营、可C端投放的会场 Agent Harness](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/%E4%BC%9A%E5%9C%BAAgent%20Harness%2B26.10.19/RAW.pdf)（capture-001） | 2026-10-19 | 19–20、25–26 | root-taobao-01.json |

## 我的实践与修正

（待本人填写；AI默认不修改）

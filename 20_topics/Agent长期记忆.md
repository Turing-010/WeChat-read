# Agent长期记忆

> AI跨文学习整理，2026-10-23更新。以下正文以本轮全文证据为依据；全库全文证据已汇总，本专题已按实质机制补查；全库结构验收另行记录。示例为教学推导，文章效果未在本地复现，官方核查仅限文档。个人记录区保持原文。

> 修订原因：把按文章追加的重复摘要合并为机制、条件、例子与跨篇对照；分开事件时间和发布日期，并修正效果口径、计划状态与过时接口。

## 我对这个主题的理解

（待本人填写）

## 长期记忆的价值要到下次任务里验证

把内容写进文件或向量库，只完成了保存。可用的记忆还需要：知道来源与适用范围，能在新任务中找回，能处理更新冲突，能纠正或删除，最后能改变正确行为。记忆条数、注入次数、引用次数、采纳次数和任务收益是不同指标。[art-0132／capture-001，p.1–11](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/AI%20Coding%E5%9B%A2%E9%98%9F%E7%BB%8F%E9%AA%8C%E7%B3%BB%E7%BB%9F%2B26.7.30/RAW.pdf#page=1) [art-0141／capture-001，p.5–10](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Agent%E5%9B%A2%E9%98%9F%E7%9F%A5%E8%AF%86%E5%BA%95%E5%BA%A7%2B26.8.17/RAW.pdf#page=5)

先分三个用途：**会话/任务状态**让当前工作继续；**跨任务记忆**保存偏好、事实和经验；**外部知识库**提供业务资料。tRPC把Session、Memory、Knowledge分开；LangGraph把线程Checkpointer与跨线程Store分开。这些是作用域和用途，不能简化成“RAM=短期、磁盘=长期”。[art-0305／capture-001，p.28–34](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/tRPCAgentGo%E6%A1%86%E6%9E%B6%E6%9E%B6%E6%9E%84%2B25.10.13/RAW.pdf#page=28) [art-0330／capture-001，p.3–20](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/LangGraph%E9%95%BF%E7%9F%AD%E6%9C%9F%E8%AE%B0%E5%BF%86%E5%AE%9E%E8%B7%B5%2B25.12.8/RAW.pdf#page=3)

## 一条可维护的记忆生命周期

1. **收集原证据。** 保留会话、代码版本、任务、时间和权限；不要只留模型结论。L0原对话→L1事实→L2场景→L3认知是访问层次，高层仍应能回到原Turn。[art-0163／capture-001，p.6–9](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E5%9B%A2%E9%98%9F%E8%AE%B0%E5%BF%86%E5%AE%9E%E8%B7%B5%2B26.8.18/RAW.pdf#page=6)
2. **候选准入。** 把“用户明确说的事实/偏好”“观察到的行为”“模型推断”“一次失败后提出的规则”分开。广泛生效的规则门槛更高，负例不能误写成推荐做法。[art-0173／capture-001，p.15–18](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E8%85%BE%E8%AE%AFWorkBuddy%20Agent%E4%BA%A7%E5%93%81%E5%AE%9E%E8%B7%B5%2B26.7.24/RAW.pdf#page=15) [art-0155／capture-001，p.13–16](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Agent%E8%87%AA%E8%BF%9B%E5%8C%96%E9%A3%9E%E8%BD%AE%2B26.8.26/RAW.pdf#page=13)
3. **审查、去重、合并。** Review检验事实和粒度，Dedup比较场景、结论类型和用途；A像B、B像C不推出A应与C合并。更新要保留When/What/Why；矛盾应进入裁决。[art-0132／capture-001，p.6–8、11](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/AI%20Coding%E5%9B%A2%E9%98%9F%E7%BB%8F%E9%AA%8C%E7%B3%BB%E7%BB%9F%2B26.7.30/RAW.pdf#page=6)
4. **检索与装配。** 权限先过滤，再按任务召回和排序；必要规则可固定绑定，不应被相关性评分冲掉。先看概要，按证据需求展开，不等于每次塞入全部历史。[art-0163／capture-001，p.3、7–9、19](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E5%9B%A2%E9%98%9F%E8%AE%B0%E5%BF%86%E5%AE%9E%E8%B7%B5%2B26.8.18/RAW.pdf#page=3)
5. **验证使用和退出。** 记录命中、是否采纳、效果、负迁移、版本、TTL和纠正。引用或点赞可以触发重审，不能证明旧规则仍正确。[art-0141／capture-001，p.5–10](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Agent%E5%9B%A2%E9%98%9F%E7%9F%A5%E8%AF%86%E5%BA%95%E5%BA%A7%2B26.8.17/RAW.pdf#page=5) [art-0155／capture-001，p.13–24](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Agent%E8%87%AA%E8%BF%9B%E5%8C%96%E9%A3%9E%E8%BD%AE%2B26.8.26/RAW.pdf#page=13)

## 最小例子：一条经验应该怎样存

教学例：“这个仓库的支付重试会导致重复通知”不是完整记忆。至少保存：适用于仓库R、分支/版本V、某服务调用路径；发生在哪个任务、原日志/提交在哪里；当时原因是什么；已验证的修复是什么；哪些条件尚未验证。

新任务来自另一分支时先核对版本和当前代码；用户没有该仓库权限时不应先召回再删敏感句。若后来修复改变了重试机制，旧经验应标失效或缩小适用区间，而非因曾被多次引用继续排在前列。这是结合When/What/Why与ACL/版本检索的教学设计。[art-0132／capture-001，p.6–11](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/AI%20Coding%E5%9B%A2%E9%98%9F%E7%BB%8F%E9%AA%8C%E7%B3%BB%E7%BB%9F%2B26.7.30/RAW.pdf#page=6) [art-0163／capture-001，p.7–19](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E5%9B%A2%E9%98%9F%E8%AE%B0%E5%BF%86%E5%AE%9E%E8%B7%B5%2B26.8.18/RAW.pdf#page=7)

HL-Mem补充**双时间**：valid time是现实何时有效，recorded time是系统何时得知。若3月记录住杭州，8月得知5月已搬北京，那么“6月实际住哪里”与“6月系统当时知道住哪里”分别是北京和杭州；4月实际仍杭州，不能沿用原文错例写成北京。Event原记录、Claim认知和EvidenceLink分离，supersede令旧认知退出当前召回但保留历史；用户删除则要覆盖派生依赖与恢复流程，防旧备份复活。[art-0010／capture-001，p.3–10](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/HL-Mem%E9%95%BF%E6%9C%9F%E8%AE%B0%E5%BF%86%2B26.9.11/RAW.pdf#page=3)

小游戏实践把经验挂到可证伪业务提案：记录预测区间、验证条件、引用知识来源，再回收A/B结果；专家共识仍不是事实。事件线是2026-01单点协作→7月两周6款→8月底自运营首周迭代，2026-09-22才发表。它补“经验如何被业务反馈检验”，未证明所有迭代增益均由记忆造成。[art-0014／capture-001，p.1–7、21–27](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/%E5%B0%8F%E6%B8%B8%E6%88%8F%E8%87%AA%E8%BF%AD%E4%BB%A3Agent%2B26.9.22/RAW.pdf#page=1)

Ontology实践补上长期写入的明确门槛：先读已有知识、工具取证、执行已有决策，发现缺口后生成learning proposal，再经结构验证、案例回归和review进入长期库。共享decision/reject路线会影响多个组合，必须记录版本与失效范围；临时日志或猜测不能直接晋升正式规则。2026-09-27是发表日，“近三个月120+工作项”只有相对时间和内部规模，不能推导已验证长期收益；结构字段本身也不强制执行这套协议。[art-0015／capture-001，p.2–5、11–14](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/Ontology%E5%86%B3%E7%AD%96%E7%BB%93%E6%9E%84%E5%8C%96%2B26.9.27/RAW.pdf#page=2)

## 这些文章讲的是不同层，而非互相替代

| 路线 | 有效补充 | 主要边界 |
|---|---|---|
| LangGraph Store | 命名空间和跨线程读写/检索 | namespace不等于授权；InMemoryStore不支持进程重启持久性 |
| OpenClaw日记/会话 | 持久会话、摘要、临时修剪分工 | 快照刷新与配置需版本核查；删会话不是通用无损修复 |
| Memory offload | 原结果、摘要、任务图、索引分层 | 主要服务长任务上下文，不自动变成跨任务经验 |
| Review→Dedup→Merge | 从轨迹提炼可复用团队经验 | 入库“有效”不等于已采纳；原文承认过期治理缺口 |
| TTL与业务流程准入 | 把知识沉淀挂到真实流程 | 90天是团队策略，点赞不是事实正确性证明 |
| L0—L3团队记忆 | 保留原Turn、权限、版本和强弱关系 | 22361关系只有231强关系，Shadow只助发现不能自动执行 |

[art-0330／capture-001，p.14–23、32–40](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/LangGraph%E9%95%BF%E7%9F%AD%E6%9C%9F%E8%AE%B0%E5%BF%86%E5%AE%9E%E8%B7%B5%2B25.12.8/RAW.pdf#page=14) [art-0060／capture-001，p.8–12、18–23](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/OpenClaw%E6%9E%B6%E6%9E%84%E4%B8%8E%E5%A4%9AAgent%2B26.3.9/RAW.pdf#page=8) [art-0094／capture-001，p.14–29](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E5%8F%AF%E6%81%A2%E5%A4%8D%E7%9A%84%E5%88%86%E5%B1%82%E4%BB%BB%E5%8A%A1%E8%AE%B0%E5%BF%86%2B26.5.22/RAW.pdf#page=14) [art-0132／capture-001，p.6–11](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/AI%20Coding%E5%9B%A2%E9%98%9F%E7%BB%8F%E9%AA%8C%E7%B3%BB%E7%BB%9F%2B26.7.30/RAW.pdf#page=6) [art-0141／capture-001，p.5–10](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Agent%E5%9B%A2%E9%98%9F%E7%9F%A5%E8%AF%86%E5%BA%95%E5%BA%A7%2B26.8.17/RAW.pdf#page=5) [art-0163／capture-001，p.12–18](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E5%9B%A2%E9%98%9F%E8%AE%B0%E5%BF%86%E5%AE%9E%E8%B7%B5%2B26.8.18/RAW.pdf#page=12)

## 记忆如何评测

至少拆为提取、检索、更新、时间推理、冲突处理/拒答和最终任务收益。只测“姓名还能答出来”远远不够；重启试验不能把姓名又作为新输入给系统。跨时间评测时，只允许目标任务发生前可用的经验，不能把未来修复注入历史任务。[art-0330／capture-001，p.7–9、23–32](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/LangGraph%E9%95%BF%E7%9F%AD%E6%9C%9F%E8%AE%B0%E5%BF%86%E5%AE%9E%E8%B7%B5%2B25.12.8/RAW.pdf#page=7) [art-0220／capture-001，p.13–23、25–33](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/Agent-Memory%E8%AF%84%E6%B5%8B%E5%85%A8%E6%99%AF%2B26.6.3/RAW.pdf#page=13) [art-0163／capture-001，p.15–18](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E5%9B%A2%E9%98%9F%E8%AE%B0%E5%BF%86%E5%AE%9E%E8%B7%B5%2B26.8.18/RAW.pdf#page=15)

art0163报告60%→80%缺固定子集、重复次数和区间；same_problem抽检69%没有达到文中70%目标。标题“任何错误只犯一次”应理解为目标。art0132的95%有效主要评价入库治理，不能与任务成功率混成同一个指标。[art-0163／capture-001，p.12–18](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E5%9B%A2%E9%98%9F%E8%AE%B0%E5%BF%86%E5%AE%9E%E8%B7%B5%2B26.8.18/RAW.pdf#page=12) [art-0132／capture-001，p.6–11](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/AI%20Coding%E5%9B%A2%E9%98%9F%E7%BB%8F%E9%AA%8C%E7%B3%BB%E7%BB%9F%2B26.7.30/RAW.pdf#page=6)

## 时间线：保存→治理→任务收益，哪些已做哪些未做

| 事件时间 | 发布日期 | 递进关系 |
|---|---|---|
| 2025框架状态，未锁commit | 2025-10-13，art0305 | Session/Memory/Knowledge分工提供基础服务 |
| 示例开发日未给 | 2025-12-08，art0330 | 补线程检查点与长期Store；可靠自主更新/遗忘仍未实现 |
| 综述统计截止2026-02 | 2026-06-03，art0220 | 整理多类记忆评测；发表晚不代表覆盖到6月所有进展 |
| 2026-05-27一次入库运行 | 2026-07-30，art0132 | 同团队从大量垃圾候选发展到Review/Dedup/Merge；采纳观测尚缺 |
| 2026-05至07-09运营观察 | 2026-08-17，art0141 | 另一团队补准入、TTL与注入运营；不是art0132后继版本 |
| 实验日期未给 | 2026-08-18，art0163 | 更明确区分强关系/Shadow，并用按时间约束的后续任务检验迁移 |

[art-0305／capture-001，p.28–34](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/tRPCAgentGo%E6%A1%86%E6%9E%B6%E6%9E%B6%E6%9E%84%2B25.10.13/RAW.pdf#page=28) [art-0330／capture-001，p.3–20、40](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/LangGraph%E9%95%BF%E7%9F%AD%E6%9C%9F%E8%AE%B0%E5%BF%86%E5%AE%9E%E8%B7%B5%2B25.12.8/RAW.pdf#page=3) [art-0220／capture-001，p.2、13–23](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/Agent-Memory%E8%AF%84%E6%B5%8B%E5%85%A8%E6%99%AF%2B26.6.3/RAW.pdf#page=2) [art-0132／capture-001，p.8–11](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/AI%20Coding%E5%9B%A2%E9%98%9F%E7%BB%8F%E9%AA%8C%E7%B3%BB%E7%BB%9F%2B26.7.30/RAW.pdf#page=8) [art-0141／capture-001，p.5–10](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Agent%E5%9B%A2%E9%98%9F%E7%9F%A5%E8%AF%86%E5%BA%95%E5%BA%A7%2B26.8.17/RAW.pdf#page=5) [art-0163／capture-001，p.12–18](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E5%9B%A2%E9%98%9F%E8%AE%B0%E5%BF%86%E5%AE%9E%E8%B7%B5%2B26.8.18/RAW.pdf#page=12)

## 当前官方核查

截至2026-10-23，LangGraph文档仍将Checkpointer与Store分工。删除当前消息状态不意味着清除了历史检查点或备份，需分别设计保留与删除流程。[LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence) [art-0330／capture-001，p.23–32](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/LangGraph%E9%95%BF%E7%9F%AD%E6%9C%9F%E8%AE%B0%E5%BF%86%E5%AE%9E%E8%B7%B5%2B25.12.8/RAW.pdf#page=23)

HL-Mem当前官方README仍保留Event→Claim、双时间和独立Experience通道，同时明确是SQLite单机系统，没有分布式worker、高可用或多租户隔离，Provider是受信进程内代码。文章v1.1的50题86%观察不能当完整LongMemEval基准或今天的性能保证。[HL-Mem官方仓库](https://github.com/lohr13/hl_mem) [art-0010／capture-001，p.9–13](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/HL-Mem%E9%95%BF%E6%9C%9F%E8%AE%B0%E5%BF%86%2B26.9.11/RAW.pdf#page=9)

LongMemEval V1含500个问题，考查抽取、跨会话、更新、时间推理和拒答；当前V2改用网页/企业多模态轨迹，451个人工问题，关注状态、工作流、环境陷阱和前提，并同时评准确性与延迟。因此不能把V1与V2分数连成提升曲线。[V1官方仓库](https://github.com/xiaowu0162/LongMemEval) [V2官方仓库](https://github.com/xiaowu0162/LongMemEval-V2) 本次仅核文档，没有跑基准或证明某系统已满足这些能力。

## 自测：先回答，再展开

**1. 已经把全部对话放进向量库，长期记忆还缺什么？**
<details><summary>答案</summary>
来源和适用范围、准入、权限、时间/版本、更新冲突、删除、检索装配、采纳观测及任务效果。相关文本不自动成为有效经验。
</details>

**2. A与B相似、B与C相似，为什么不应自动合并A与C？**
<details><summary>答案</summary>
相似关系一般不具传递性；三者适用场景、结论类型或粒度可能不同。合并需直接验证目标边界和来源。
</details>

**3. 某经验注入了100次，能证明带来100次帮助吗？**
<details><summary>答案</summary>
不能。还要区分实际读取、采纳、行为改变和净收益，并记录无效或负迁移；使用次数不是正确性证据。
</details>

**4. 用今年修复后的知识回测去年任务会有什么问题？**
<details><summary>答案</summary>
可能泄漏未来信息，高估当时可取得的效果。应按事件/可获得时间截断记忆，并保留版本与原始证据。
</details>


## 来源索引

以下采用META指定默认采集版本。正文引用使用PDF物理页；发布日期不是机制首次出现时间。

| 来源 | 发布日期 | 本专题使用页 | 证据报告 |
|---|---|---|---|
| [art-0305 tRPC-Agent-Go：构建智能AI应用的Go语言Agent框架](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/tRPCAgentGo%E6%A1%86%E6%9E%B6%E6%9E%B6%E6%9E%84%2B25.10.13/RAW.pdf)（capture-001） | 2025-10-13 | 28–34 | inbox-06.json |
| [art-0330 让AI智能体拥有像人类的持久记忆：基于LangGraph的长短期记忆管理实践指南](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/LangGraph%E9%95%BF%E7%9F%AD%E6%9C%9F%E8%AE%B0%E5%BF%86%E5%AE%9E%E8%B7%B5%2B25.12.8/RAW.pdf)（capture-001） | 2025-12-08 | 3–20、40；3–20；7–9、23–32；14–23、32–40；23–32 | inbox-07.json |
| [art-0060 玩转OpenClaw，你需要了解的：核心架构、运作原理、Agent部署步骤](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/OpenClaw%E6%9E%B6%E6%9E%84%E4%B8%8E%E5%A4%9AAgent%2B26.3.9/RAW.pdf)（capture-001） | 2026-03-09 | 8–12、18–23 | tencent-02.json |
| [art-0094 腾讯云 Agent Memory 节省 61% Token 提升 52% 成功率的诀窍：Mermaid 无限画布 × 上下文卸载](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E5%8F%AF%E6%81%A2%E5%A4%8D%E7%9A%84%E5%88%86%E5%B1%82%E4%BB%BB%E5%8A%A1%E8%AE%B0%E5%BF%86%2B26.5.22/RAW.pdf)（capture-001） | 2026-05-22 | 14–29 | tencent-05.json |
| [art-0220 Agent-Memory 评测全景：基准、评估与记忆系统（理论篇）](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/Agent-Memory%E8%AF%84%E6%B5%8B%E5%85%A8%E6%99%AF%2B26.6.3/RAW.pdf)（capture-001） | 2026-06-03 | 2、13–23；13–23、25–33 | taobao-08.json |
| [art-0173 腾讯 WorkBuddy 实践：如何把 Agent 做成可用产品](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E8%85%BE%E8%AE%AFWorkBuddy%20Agent%E4%BA%A7%E5%93%81%E5%AE%9E%E8%B7%B5%2B26.7.24/RAW.pdf)（capture-001） | 2026-07-24 | 15–18 | tencent-late-01.json |
| [art-0132 AI Coding 的下一站，不是更会写代码，而是更懂团队](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/AI%20Coding%E5%9B%A2%E9%98%9F%E7%BB%8F%E9%AA%8C%E7%B3%BB%E7%BB%9F%2B26.7.30/RAW.pdf)（capture-001） | 2026-07-30 | 1–11；6–11；6–8、11；8–11 | tencent-late-01.json |
| [art-0141 Agent 的上限，可能不在模型，而在团队知识](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Agent%E5%9B%A2%E9%98%9F%E7%9F%A5%E8%AF%86%E5%BA%95%E5%BA%A7%2B26.8.17/RAW.pdf)（capture-001） | 2026-08-17 | 5–10 | tencent-late-04.json |
| [art-0163 任何错误只犯一次：TencentDB Agent Memory 的团队记忆实践](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/%E5%9B%A2%E9%98%9F%E8%AE%B0%E5%BF%86%E5%AE%9E%E8%B7%B5%2B26.8.18/RAW.pdf)（capture-001） | 2026-08-18 | 3、7–9、19；6–9；7–19；12–18；15–18 | tencent-late-04.json |
| [art-0155 一篇讲透 Agent 自进化飞轮怎么搭：评测 → 记忆 → 落地 → 控制](../%E8%85%BE%E8%AE%AF%E6%8A%80%E6%9C%AF%E5%B7%A5%E7%A8%8B/Agent%E8%87%AA%E8%BF%9B%E5%8C%96%E9%A3%9E%E8%BD%AE%2B26.8.26/RAW.pdf)（capture-001） | 2026-08-26 | 13–24；13–16 | tencent-late-05.json |
| [art-0010 让 Agent 像人一样记忆：本地长期记忆系统 HL-Mem 的设计与取舍](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/HL-Mem%E9%95%BF%E6%9C%9F%E8%AE%B0%E5%BF%86%2B26.9.11/RAW.pdf)（capture-001） | 2026-09-11 | 3–10；9–13 | taobao-11.json |
| [art-0014 AI 自迭代的小游戏 Agent：2周上线6款小游戏，3天迭代12款小游戏](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/%E5%B0%8F%E6%B8%B8%E6%88%8F%E8%87%AA%E8%BF%AD%E4%BB%A3Agent%2B26.9.22/RAW.pdf)（capture-001） | 2026-09-22 | 1–7、21–27 | taobao-12.json |
| [art-0015 改变世界前先认识世界-Ontology 决策结构化实践](../%E5%A4%A7%E6%B7%98%E5%AE%9D%E6%8A%80%E6%9C%AF/Ontology%E5%86%B3%E7%AD%96%E7%BB%93%E6%9E%84%E5%8C%96%2B26.9.27/RAW.pdf)（capture-001） | 2026-09-27 | 2–5、11–14 | taobao-12.json |

## 我的实践与修正

（待本人填写；AI默认不修改）

# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
从 0 开发⼤模型的 17 种 Agent 架构演进详细拆解
2026 年 5 ⽉ 18 ⽇ 02 : 39⼴东腾讯技术⼯程 75 ⼈
作者： linkxzhou ，公众号《周末程序猿》
在  github 看到⼀个项⽬  all-agentic-architectures，实现的是关于  17 种  Agent 模
式⼤全，我把  all-agentic-architectures  这个项⽬完整过了⼀遍。  它最有价值的地
⽅，不是列了  17 中  Agent 代码，⽽是把  17 次系统升级拆解：上⼀个架构为什么不够、下⼀
个架构到底多了什么控制能⼒、复杂度⼜是从哪⾥开始失控的。  这些信息真正决定⼀个
agent 系统能不能落地的，通常不是模型回答是不是够好，⽽是：
状态有没有被正确建模
控制流有没有被显式表达
错误能不能被局部截断
副作⽤能不能被关进闸门
系统知不知道⾃⼰什么时候该停
不过  all-agentic-architectures  是⽤  langchain 和  langgraph  实现的，但是  agn
o  框架更加简洁，于是  ⽤  agno  把这  17 种控制流从头写⼀遍。  为了说明⼀件事：
Agent architecture 的本质不是  prompt engineering ，也不是某个框架的  DSL ，⽽是控制流
设计。  它应该能在任何体⾯的  agent 框架⾥复现，以下是  Agent 演化路径：
从单次⽣成到反思闭环
从反思闭环到⼯具交互
从⼯具交互到观察 - ⾏动循环
从局部决策到显式规划
从⽆验证执⾏到验证驱动重规划
从单  agent到多  agent 编排
从短期上下⽂到长期记忆系统
从线性推理到搜索、模拟与涌现计算
从能做事到可信任
总演化图：
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
1. 统⼀分析框架
后⾯每⼀种架构，我都会⽤同⼀套问题来拆。
六个固定问题
1. 它要解决什么问题？  上⼀代架构哪⾥不够。
2. 它的  State 是什么？  新增了哪些字段，为什么必须存在。
3. 它的拓扑是什么？  线性链、循环、分叉汇聚、共享⿊板、树搜索还是⽹格涌现。
4. 它的  Router 怎么⼯作？ 固定边、条件边、动态调度、验证回路、⼈⼯审批。
5. 它的失败模式是什么？  架构最容易在哪个环节坏掉。
6. 什么时候该升级到下⼀种？ 当前模式的能⼒边界在哪⾥。
2. ⽤  agno 看  Agent
这个项⽬⼏乎所有架构都能被  agno 的⼏个抽象表达清楚：
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.workflow.v2 import Workflow, Step, Router, Loop
# ⼀个最简  Agent = ⼀次状态变换
agent = Agent(
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[...],
    instructions="...",
    response_model=SomePydanticModel,  # 结构化输出
)
# ⼀个  Workflow = 显式控制流
wf = Workflow(
    name="my_flow",
    steps=[
        Step(name="plan", agent=planner_agent),
        Loop(
            name="execute_and_verify",
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
            steps=[executor_step, verifier_step],
            end_condition=lambda outputs: outputs[-1].content.is_done,
        ),
        Step(name="synthesize", agent=synthesizer_agent),
    ],
)
wf.run(message="...")
这段代码背后已经包含了⼀个  agent 系统的最⼩数学结构：
response_model 定义状态空间
Agent / tools / Step 函数定义状态变换
steps  列表定义确定性转移
Router / Condition 定义条件转移
Loop.end_condition 定义终⽌条件
wf.run() 定义可执⾏系统
后⾯我⼏乎不把问题描述成 " 这个架构更聪明 " ，⽽描述成：它新增了什么状态字段、什么
agent 或⼯具、什么路由逻辑、什么验证机制。
3. 总览：逐步添加控制能⼒
阶段 新增能⼒ ⼀句话解释 代表架构
单次⽣成优化critique pass 让模型先出⼀版，再⾃⼰挑⽑病改掉，把 " ⽣
成 " 拆成  generator + critic + reﬁner 三步。 Reﬂection
与世界交互tool interface 把外部  API / 函数挂成结构化⼯具接⼝，打破
参数知识边界和上下⽂封闭性。Tool Use
基于观察持续
⾏动
observation lo
op
Thought →  Action →  Observation 滚动循
环，上⼀步的观察决定下⼀步的动作。ReAct
先⽣成控制流
再执⾏
explicit plannin
g
先让模型产出⼀份可检视的步骤清单（ pla
n ），再按清单逐步执⾏，把控制流本⾝做成可
审计对象。
Planning
把验证接⼊主
回路
veriﬁcation loo
p
每⼀步执⾏完都强制过⼀次  veriﬁer ，失败就
回到重规划，⽽不是把验证当成事后检查。PEV
把认知任务拆
成⾓⾊
role decompos
ition
不再让⼀个  agent 什么都⼲，把研究员  写作
审阅等⾓⾊拆开，⽤流⽔线或图把它们串起
来。
Multi-Agent
把中间状态显
式共享
shared worksp
ace
把中间产物写到⼀块共享 " ⿊板 " 上，⼀个  con
troller 根据⿊板当前状态动态决定下⼀个该谁
上场。
Blackboard
把⼊⼝做成路
由系统 entry routing
在请求⼊⼝先分类⼀次，把任务路由到最合适
的专家⼦  agent ，避免⼀个  agent 背所有能
⼒。
Meta-Controller
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
阶段 新增能⼒ ⼀句话解释 代表架构
⽤冗余换可靠
性
parallel redund
ancy
同⼀个问题同时交给多个独⽴  agent 处理，
再由  aggregator 融合 / 投票，⽤冗余换稳定性
和去偏。
Ensemble
把历史状态纳
⼊系统
long-term me
mory
把对话⽚段放进向量库（ episodic ），把结构
化事实放进图 /KV （ semantic ），让系统记得
住、查得到。
Episodic + Sem
antic / Graph
把推理变成搜
索 search tree
不再是⼀条思路⾛到底，⽽是展开多条思路形
成树，边展开边打分、剪枝，把 " 推理 " 变
成 " 搜索 " 。
ToT
把⾏动前评估
做成模拟
counterfactual
execution
真正动⼿之前，先在内部世界模型⾥预演⼀
遍，评估风险和收益，再决定是否真执⾏。Mental Loop
把副作⽤关进
闸门
side-eﬀect gati
ng
任何有副作⽤的动作必须先  dry-run + 审核
（⼈或⾃动检查）通过后，才允许落到真实环
境。
Dry-Run
把⾃我边界建
模
self-boundary r
easoning
系统维护⼀份⾃我模型，知道⾃⼰ " 擅长什
么、不擅长什么 " ，据此选择亲⾃做、调⼯
具，还是交给⼈。
Metacognitive
把质量改进做
成循环
iterative reﬁne
ment loop
editor agent 对输出打分并给出修改意见， wri
ter 按意见改稿，⾼分样本沉淀下来⽤于持续
改进。
Self-Improve
去中⼼化计算emergence
没有中⼼  LLM 在推理，每个格⼦ / 单元只跑简
单局部规则，全局⾏为（寻路、扩散等）从局
部交互中涌现出来。
Cellular Automat
a
所谓 "agent 架构演化 " ，不是追求  AGI ，⽽是解决⼀个⽼问题：怎样让系统在更复杂的环境
⾥，依然保持可控、可解释、可恢复。
下⾯正式开始。为了篇幅，代码⾥我统⼀省略  from agno... import 的重复部分。
4. Reﬂection ：最⼩质量闭环
Reflection 的价值不在于 " 模型会反思 " ，⽽在于它第⼀次把⽣成过程拆成了两个不同职能
的  pass ：⽣成和评估，它是最⼩质量闭环，但还不是完整控制闭环。
它要解决什么问题？
单次  LLM ⽣成质量不稳定， Reﬂection 就是最⼩修复：先⽣成  →  再评估  →  再根据评估修
改。这不是 " 增加智能 " ，⽽是把单步⽣成改成三阶段控制流。
它的  State 是什么？
核⼼三个字段是  draft / critique / refined_code，在  agno ⾥直接⽤  Pydantic 把
它们定义成结构化输出：
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
from pydantic import BaseModel, Field
from typing import List
class DraftCode(BaseModel):
    code: str = Field(description="Python code to solve the user's request.")
    explanation: str = Field(description="A brief explanation of how the code works.")
class Critique(BaseModel):
    has_errors: bool
    is_efficient: bool
    suggested_improvements: List[str]
    critique_summary: str
class RefinedCode(BaseModel):
    refined_code: str
    refinement_summary: str
系统第⼀次把 " 中间思考结果 " 显式写进  state ，⽽不是埋在上下⽂⾥，response_model
=...  让这件事⼏乎零成本。
它的拓扑是什么？
纯线性：
⽤  agno 写出来：
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.workflow.v2 import Workflow, Step
model = OpenAIChat(id="gpt-5-mini")
generator = Agent(name="generator", model=model, response_model=DraftCode,
    instructions="You are an expert Python programmer. Write code and a brief explanation
critic = Agent(name="critic", model=model, response_model=Critique,
    instructions="You are a senior code reviewer. Analyze for bugs, inefficiencies and PE
refiner = Agent(name="refiner", model=model, response_model=RefinedCode,
    instructions="Rewrite the code, incorporating every suggestion from the critique.")
def generator_step(step_input):
    draft = generator.run(step_input.message).content
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
    step_input.workflow_session_state["draft"] = draft
    return draft
def critic_step(step_input):
    draft: DraftCode = step_input.workflow_session_state["draft"]
    return critic.run(f"Review this code:\n```python\n{draft.code}\n```").content
def refiner_step(step_input):
    draft: DraftCode = step_input.workflow_session_state["draft"]
    critique: Critique = step_input.previous_step_output.content
    prompt = (f"Original code:\n```python\n{draft.code}\n```\n"
              f"Critique: {critique.model_dump_json(indent=2)}\nProduce the refined code.
    return refiner.run(prompt).content
reflection_wf = Workflow(
    name="reflection",
    session_state={"draft": None},
    steps=[
        Step(name="generator_step", executor=generator_step),
        Step(name="critic_step", executor=critic_step),
        Step(name="refiner_step", executor=refiner_step),
    ],
)
reflection_wf.run(message="Write a Python function to find the nth Fibonacci number.")
Workflow.steps  列表⾥的顺序就是确定性边：上⼀步的输出⾃动作为下⼀步的  previo
us_step_output，每⼀步的  state 流动由  agno 托管 ——previous_step_output  是
⼀个  StepOutput，它的  .content 才是上⼀步  response_model 的实例；跨⾮相邻
步骤的数据⽤  workflow_session_state  显式传递。
Router 怎么⼯作？
没有  router 。  这是  Reﬂection 很关键的技术边界：没有条件分⽀，没有失败恢复，系统默认
三步⾛完直接结束。
它为什么⽐单次⽣成强？
因为它把⼀个模糊任务拆成了三个更明确的⼦任务：先尽量⽣成  →  再专门找问题  →  最后只
解决问题。这⾥的核⼼经验判断是：LLM 作为  critic 往往⽐作为  generator 更稳定。
它的失败模式
最⼤的问题是：它不能验证  reﬁner 是否真的修好了  critic 提到的问题。  它有  critique ，但没
有闭环。
什么时候升级？
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
当你需要系统根据中间结果继续⾏动，就必须进⼊下⼀代：要么让它接触世界（ Tool Use ），
要么形成持续观察 - ⾏动回路（ ReAct ）。
5. Tool Use ：⽂本世界到结构化世界的跨越
它要解决什么问题？
Reﬂection 解决 " 质量 " ，但没解决 " 知识边界 " ，⼀个不带⼯具的  LLM 再会反思也被困在参数
⾥， Tool Use 要让系统突破上下⽂与知识截⽌⽇期的封闭性。
它的  State 是什么？
Tool Use 的  state 本质上是⼀条 " 事件⽇志 " ：⽤户输⼊  →  模型输出  →  ⼯具调⽤  →  ⼯具返回
→  下⼀轮推理。  在  agno ⾥，这条⽇志是  Agent  内部⾃动维护的 —— ⼀次  agent.run
()  内部就完整地跑完这整个链路。
state 从 " 你需要⾃⼰维护的数据结构 " 变成了 " 框架托管的会话上下⽂ " ，这也是  Tool Use 和
Reﬂection 在⼯程侧最显眼的差别。
它的关键代码
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
def get_stock_price(symbol: str) -> str:
    """Return the latest stock price for a given symbol."""
    return f"The current price of {symbol.upper()} is $172.35."
tool_agent = Agent(
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[get_stock_price, DuckDuckGoTools()],
    instructions="Use tools to answer questions that need real-time data.",
    show_tool_calls=True,
)
tool_agent.run("What is Apple's current stock price?")
底层等价于：
# 概念上  agno 内部循环
while True:
    response = llm_with_tools.invoke(messages)
    messages.append(response)
📎  参考实现：01_reflection.ipynb
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
    if not response.tool_calls:
        break
    for call in response.tool_calls:
        observation = tool_registry[call.name](**call.args)
        messages.append(ToolMessage(observation, tool_call_id=call.id))
这个  while 循环是  agno Agent  帮你内置的。
它真正新增了什么能⼒？
不是 " 会调⽤函数 " ，⽽是：⽂本控制流可以跨越到结构化世界，再返回⽂本世界。  这个跨越
点是整个  agent engineering 的第⼀道硬边界。
失败模式
失败通常不来⾃  LLM 本⾝，⽽来⾃ " 边界层 " ：⼯具名幻觉、参数类型错误、⼯具返回格式不
对、⼯具结果被模型错误综合。 Tool Use 的关键难点不是  prompt ，⽽是序列化与反序列化。
它为什么还不够？
因为  Tool Use 没有显式规定 " ⼀定要循环 " ，在最原始的实现⾥，模型可能只调⼀次⼯具就收
尾，你需要真正的观察 - ⾏动闭环 —— 这就是  ReAct 。
6. ReAct ： Agent 真正成形的地⽅
它要解决什么问题？
Tool Use 的控制流还太浅， ReAct 要让⼯具结果不只是被消费⼀次，⽽是进⼊下⼀轮决策。
从这⾥开始， agent 不再只是 " 会⽤⼯具 " ，⽽是 " 会根据新观察更新计划 " 。
State 还是消息序列，为什么语义却变了？
在  ReAct ⾥  agent 的消息序列不再只是对话历史，⽽是⾏动轨迹（ trace ）：当前问题  →  上⼀
步推理  →  ⼯具调⽤  →  ⼯具观测  →  新⼀轮判断。  你可以把它看成隐式的⼯作记忆带，在
agno ⾥，这条  trace 是  Agent  内部⾃动维护的 —— ⼀次  agent.run()  内部就包含⽤户
输⼊、模型输出、⼯具调⽤、⼯具返回、⼆次推理，你不需要⼿写任何状态容器。
它的关键代码
agno 内置的  reasoning=True 会把  ReAct 的 "Thought Action Observation" 显式写进
trace ：
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
📎  参考实现：02_tool_use.ipynb
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
from agno.tools.yfinance import YFinanceTools
react_agent = Agent(
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[DuckDuckGoTools(), YFinanceTools(stock_price=True, company_news=True)],
    instructions=[
        "You are a research assistant.",
        "Think step by step. For each step decide whether to use a tool or answer.",
        "After each tool observation, re-evaluate what you still need before answering.",
    ],
    reasoning=True,
    markdown=True,
    show_tool_calls=True,
)
react_agent.print_response(
    "Based on the latest news, should I be worried about AAPL next quarter?",
    stream=True,
)
关键不是某⼀⾏代码，⽽是  agno 内部那条 " 回边 " ：只要  model 回复⾥还有  tool_calls ，就回
到  model 再跑⼀次。  这条  tool → model 的循环边，是整个  agent architecture ⾥最重要
的回边之⼀ —— 它把 " 单次调⽤ " 变成了 " 持续交互 " 。
拓扑本质
最⼩闭环：
系统终于从 " 线性流程 " 进⼊ " 持续交互系统 " 。
它为什么是  80% 任务的起点？
因为⼤多数任务并不需要复杂规划，它们只需要：先看⼀眼  →  做个动作  →  根据反馈再决定
下⼀步，已⾜够覆盖多轮搜索、多跳问答、⽹页研究、⼯具驱动的数据收集。
失败模式
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
局部贪⼼。  它每次只基于当前  observation 决策，容易⾛弯路、重复搜索、陷⼊局部最优、
⽆法提前安排多步任务。
什么时候升级？
当任务需要显式的步骤顺序控制，就该上  Planning 。
7. Planning ：把控制流本⾝变成模型输出
它要解决什么问题？
ReAct 本质是在线贪⼼策略，对需要顺序约束、步骤依赖和过程可追踪的任务，它开始不够
⽤。 Planning 要把原本隐式存在模型脑⼦⾥的执⾏顺序，显式拿出来，写进  state。
系统第⼀次把 " 控制流 " 对象化了。
State 新增了什么？
class Plan(BaseModel):
    steps: List[str] = Field(description="Ordered list of tool/sub-questions.")
workﬂow 的  session_state  ⾥还要带上中间结果：
session_state = {"plan": [], "intermediate": []}
在  ReAct ⾥下⼀步做什么是临时决定的，在  Planning ⾥下⼀步做什么先被⽣成出来，然后才
执⾏。
关键代码
agno 的  Workflow  提供  Loop step ，天然表达 " 循环执⾏直到  plan 空 " ：
from agno.workflow.v2 import Workflow, Step, Loop
from agno.tools.duckduckgo import DuckDuckGoTools
planner = Agent(name="planner", model=OpenAIChat(id="gpt-5-mini"), response_model=Plan,
    instructions="Decompose the user request into a list of atomic tool-queryable steps."
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
📎  参考实现：03_ReAct.ipynb
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
executor = Agent(name="executor", model=OpenAIChat(id="gpt-5-mini"),
    tools=[DuckDuckGoTools()],
    instructions="Answer exactly one sub-question using tools.")
synthesizer = Agent(name="synthesizer", model=OpenAIChat(id="gpt-5-mini"),
    instructions="Combine intermediate findings into a final answer.")
def plan_step(step_input):
    plan: Plan = planner.run(step_input.message).content
    step_input.workflow_session_state["plan"] = list(plan.steps)
    step_input.workflow_session_state["intermediate"] = []
    return plan
def execute_step(step_input):
    state = step_input.workflow_session_state
    next_q = state["plan"].pop(0)
    obs = executor.run(next_q).content
    state["intermediate"].append(f"Q: {next_q}\nA: {obs}")
    return obs
def synth_step(step_input):
    state = step_input.workflow_session_state
    notes = "\n\n".join(state["intermediate"])
    return synthesizer.run(
        f"Question: {step_input.message}\nNotes:\n{notes}\nFinal answer:"
    ).content
def plan_is_empty(_outputs) -> bool:
    """Loop 终⽌条件： agno 的  end_condition 只接收⼀个参数（ StepOutput 列表）。 """
    return len(planning_wf.session_state["plan"]) == 0
planning_wf = Workflow(
    name="planning",
    session_state={"plan": [], "intermediate": []},
    steps=[
        Step(name="plan", executor=plan_step),
        Loop(
            name="execute_all",
            steps=[Step(name="execute_one", executor=execute_step)],
            end_condition=plan_is_empty,
        ),
        Step(name="synthesize", executor=synth_step),
    ],
)
planning_wf.run(message="Compare the latest revenue of AAPL and MSFT and explain the gap.
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
路由逻辑从 "LLM 在  prompt ⾥决定下⼀步 " 变成了 " ⼀个数据结构是否还有剩余项 "—— 这才是
Planning 真正的结构变化。
新增的核⼼能⼒
Planning 新增的不是 " 更聪明的思考 " ，⽽是：把未来控制流提前  materialize 成⼀个数据结
构。  你现在可以可视化计划、检查计划、修改计划、追踪执⾏进度。
失败模式
它过于乐观，⼀旦  plan 错了，后⾯每⼀步都可能是错的。可预测性增强了，适应性下降了。
什么时候升级？
当你不再相信⼯具会稳定成功，就必须上  PEV 。
8. PEV ：把 " 验证 " 提升为控制流的⼀等公民
它要解决什么问题？
Planning 默认世界是稳定的，但真实世界不是： API 会失败、搜索会返回噪⾳、数据会缺失、
⼯具会超时。
PEV （ Plan →  Execute →  Verify ）解决的是：不要把执⾏结果默认为真，⽽要显式验证。  系
统现在不再把执⾏视为 " 完成了⼀步 " ，⽽是把执⾏视为 " ⽣成了⼀个待验证结果 " 。
State 新增了什么？
class VerificationResult(BaseModel):
    is_successful: bool = Field(description="True if the tool execution was successful an
    reasoning: str = Field(description="Reasoning for the verification decision.")
veriﬁer 不是随便说⼀句 " 好像不对 " ，⽽是输出⼀个结构化  verdict 。verification_resul
t  字段⼀出现，图结构就不再是  plan -> execute -> next step，⽽是  plan ->
execute -> verify -> (continue | replan | finish)。
关键代码
为了演⽰为什么需要验证，故意放了⼀个会失败的⼯具：
📎  参考实现：04_planning.ipynb
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
def flaky_web_search(query: str) -> str:
    """Search the web. This tool is intentionally unreliable."""
    if"employee count"in query.lower():
        return"Error: Could not retrieve data. The API endpoint is currently unavailable.
    return f"Mock search result for: {query}"
verifier = Agent(
    name="verifier",
    model=OpenAIChat(id="gpt-5-mini"),
    response_model=VerificationResult,
    instructions=(
        "Given a sub-question and the raw tool observation, decide if the "
        "observation actually answers the sub-question. Treat 'Error', "
        "'unavailable', empty strings and obviously irrelevant text as failures."
    ),
)
pev_executor = Agent(
    name="pev_executor",
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[flaky_web_search],
    instructions="Answer exactly one sub-question using tools.",
)
def pev_execute(step_input):
    state = step_input.workflow_session_state
    next_q = state["plan"][0]
    obs = pev_executor.run(next_q).content
    state["last_obs"] = obs
    state["last_q"] = next_q
    return obs
def pev_verify(step_input):
    state = step_input.workflow_session_state
    verdict: VerificationResult = verifier.run(
        f"Sub-question: {state['last_q']}\nObservation:\n{state['last_obs']}"
    ).content
    if verdict.is_successful:
        state["plan"].pop(0)
        state["intermediate"].append(f"Q: {state['last_q']}\nA: {state['last_obs']}")
        state["retries"] = 0
    else:
        state["retries"] = state.get("retries", 0) + 1
    state["last_verdict"] = verdict
    return verdict
from agno.workflow.v2 import Router
````

## PDF 第 16 页

[原页](RAW.pdf#page=16)

````text
# 先把所有可能⽤到的  Step 物化⼀次 ——Router selector 只能返回  workflow 已知的  Step
replan_step = Step(name="replan", executor=plan_step)
noop_step = Step(name="noop", executor=lambda si: "continue")
def pev_router(step_input):
    """ 根据本轮  verdict 决定下⼀轮是否需要重规划；不需要就放  noop ，交给  Loop 判断是否再来⼀轮。 """
    state = step_input.workflow_session_state
    if not state["plan"]:
        return [noop_step]  # 外层  Loop 的  end_condition 会看到  plan 空，直接终⽌
    if not state["last_verdict"].is_successful and state["retries"] >= 2:
        state["retries"] = 0
        return [replan_step]
    return [noop_step]
def pev_loop_done(_outputs) -> bool:
    """ 所有⼦任务都通过验证后，退出  Loop 。 """
    return len(pev_wf.session_state["plan"]) == 0
pev_wf = Workflow(
    name="pev",
    session_state={"plan": [], "intermediate": [], "retries": 0,
                   "last_q": "", "last_obs": "", "last_verdict": None},
    steps=[
        Step(name="plan", executor=plan_step),
        Loop(
            name="pev_loop",
            steps=[
                Step(name="pev_execute", executor=pev_execute),
                Step(name="pev_verify", executor=pev_verify),
                Router(name="decide_next", selector=pev_router),
            ],
            end_condition=pev_loop_done,
        ),
        Step(name="synthesize", executor=synth_step),
    ],
)
拓扑变成：
它真正带来的系统收益
PEV 的本质是：让错误不再静默传播。  在普通  Planning ⾥，⼀次失败可能污染整个剩余流
````

## PDF 第 17 页

[原页](RAW.pdf#page=17)

````text
程；在  PEV ⾥，失败在局部被识别，并被重定向回  re-plan 路径。
失败模式
额外成本⾼
veriﬁer 本⾝可能误判
过度验证会拖慢系统
某些任务⾥ " 验证 " 本⾝⽐ " 执⾏ " 更难
什么时候升级？
如果你接下来的问题不是 " 执⾏步骤会不会失败 " ，⽽是 " ⼀个  agent 根本不该包揽所有认知⾓
⾊ " ，那就该进⼊多  agent 时代。
9. Multi-Agent Collaboration ：把认知分⼯写进图⾥
多  agent 的核⼼不是 " 多个模型⼀起跑 " ，⽽是把认知分⼯、调度策略和冗余机制显式写进图结
构，真正要分清三件事：固定分⼯、动态调度、并⾏冗余。
它要解决什么问题？
当单个  agent 的  prompt 同时容纳太多⾓⾊时，系统就会变形，最典型的问题不是  token 不
够，⽽是⾓⾊冲突， Multi-Agent 的核⼼价值是：把认知分⼯编码到架构⾥。
State 是什么？
在  agno ⾥它就是  workflow_session_state  ⾥按⾓⾊划分的⼏块区域：
wf = Workflow(
    name="multi_agent",
    session_state={
        "user_request": None,
        "news": None,        # 由  news_analyst 写⼊
        "tech": None,        # 由  technical_analyst 写⼊
        "fin": None,         # 由  financial_analyst 写⼊
        "final_report": None, # 由  report_writer 写⼊
    },
📎  参考实现：06_PEV.ipynb
````

## PDF 第 18 页

[原页](RAW.pdf#page=18)

````text
    steps=[...],
)
不同⾓⾊写⼊不同字段 ——state 不再只是 " 共享上下⽂ " ，⽽开始体现⾓⾊边界。
关键代码
agno 表达这种固定流⽔线，有两条路：⽤  Workflow  拼，或者⽤  Team(mode="coordi
nate")  让⼀个  leader 固定地调度，这⾥选最直接的做法 ——Workflow + 多个  Agen
t：
news_analyst = Agent(
    name="news_analyst",
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[DuckDuckGoTools()],
    instructions="You are a financial news analyst. Produce a concise markdown section on 
)
technical_analyst = Agent(
    name="technical_analyst",
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[YFinanceTools()],
    instructions="You are a technical analyst. Produce a concise markdown section on pric
)
financial_analyst = Agent(
    name="financial_analyst",
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[YFinanceTools(income_statements=True, key_financial_ratios=True)],
    instructions="You are a financial analyst. Produce a concise markdown section on fund
)
report_writer = Agent(
    name="report_writer",
    model=OpenAIChat(id="gpt-5-mini"),
    instructions="Compose a final investment memo from the three sub-reports.",
)
def news_step(si):
    out = news_analyst.run(si.message).content
    si.workflow_session_state["news"] = out
    return out
def tech_step(si):
    out = technical_analyst.run(si.message).content
    si.workflow_session_state["tech"] = out
    return out
````

## PDF 第 19 页

[原页](RAW.pdf#page=19)

````text
def fin_step(si):
    out = financial_analyst.run(si.message).content
    si.workflow_session_state["fin"] = out
    return out
def write_step(si):
    s = si.workflow_session_state
    return report_writer.run(
        f"News:\n{s['news']}\n\nTechnical:\n{s['tech']}\n\nFinancial:\n{s['fin']}"
    ).content
multi_wf = Workflow(
    name="multi_agent",
    session_state={},
    steps=[
        Step(name="news", executor=news_step),
        Step(name="tech", executor=tech_step),
        Step(name="fin", executor=fin_step),
        Step(name="write", executor=write_step),
    ],
)
或者，如果你想让 " 编排也能省掉 " ，直接⽤  Team 的  coordinate 模式：
from agno.team import Team
analysts_team = Team(
    name="analysts",
    mode="coordinate",
    model=OpenAIChat(id="gpt-5-mini"),
    members=[news_analyst, technical_analyst, financial_analyst],
    instructions=[
        "Route each relevant sub-question to the right analyst.",
        "Collect their outputs and synthesize a final investment memo.",
    ],
    markdown=True,
)
analysts_team.print_response("Write an investment memo about AAPL.", stream=True)
新增的能⼒
````

## PDF 第 20 页

[原页](RAW.pdf#page=20)

````text
把⼀个⼤  prompt 内部的隐式⾓⾊切换，变成多个显式节点。  这带来⾮常⼤的⼯程收益：你
可以单独调试某个⾓⾊、替换某个⾓⾊的  prompt 、单独评估某个⾓⾊输出、给不同⾓⾊不同
⼯具。
失败模式
最⼤问题是：流程固定。  如果执⾏到⼀半发现还需要更多新闻背景，固定流⽔线不会⾃动返
回新闻分析师；如果发现技术分析其实不必要，也不会跳过，解决了 " 认知拆分 " ，但没有解
决 " 动态调度 " 。
什么时候升级？
当多个⾓⾊之间的先后顺序本⾝也需要动态决定时，你需要  Blackboard 。
10. Blackboard ：共享状态成为系统中⼼
它要解决什么问题？
Multi-Agent ⾥⾓⾊有了，但顺序还是硬编码的。 Blackboard 解决的是：不要预先写死专家的
调⽤顺序，⽽是让共享⼯作区的当前状态来决定下⼀步应该激活谁。
State 是什么？
class BlackboardState(BaseModel):
    user_request: str
    blackboard: dict
    next_agent: Optional[str] = None
    is_complete: bool = False
之前的  state 更像 " 按字段分区的结果容器 " ；现在的  state 变成了⼀个共享⼯作台。所有专家
都围绕这块⿊板读写。
关键代码
import json
class ControllerDecision(BaseModel):
    next_agent: str = Field(description="One of ['news', 'technical', 'financial', 'write
    reasoning: str = Field(description="A brief reason for choosing the next agent.")
controller = Agent(
    name="controller",
    model=OpenAIChat(id="gpt-5-mini"),
    response_model=ControllerDecision,
📎  参考实现：05_multi_agent.ipynb
````

## PDF 第 21 页

[原页](RAW.pdf#page=21)

````text
    instructions=(
        "You are the controller of a blackboard system. "
        "Inspect what is currently on the blackboard and decide which specialist "
        "should be called next, or FINISH if the report is ready."
    ),
)
SPECIALISTS = {
    "news": news_analyst,
    "technical": technical_analyst,
    "financial": financial_analyst,
    "writer": report_writer,
}
def controller_step(si):
    s = si.workflow_session_state
    bb_snapshot = json.dumps(s["blackboard"], indent=2, ensure_ascii=False)
    decision = controller.run(
        f"Original request: {s['user_request']}\n\nBlackboard so far:\n{bb_snapshot}"
    ).content
    s["next_agent"] = decision.next_agent
    return decision
def specialist_step(si):
    s = si.workflow_session_state
    if s["next_agent"] == "FINISH":
        return"finished"
    agent = SPECIALISTS[s["next_agent"]]
    piece = agent.run(
        f"Request: {s['user_request']}\nBlackboard:\n{json.dumps(s['blackboard'])}"
    ).content
    s["blackboard"][s["next_agent"]] = piece
    return piece
def bb_loop_done(_outputs) -> bool:
    """controller 选出  FINISH 就终⽌循环。 """
    return blackboard_wf.session_state["next_agent"] == "FINISH"
blackboard_wf = Workflow(
    name="blackboard",
    session_state={"user_request": "", "blackboard": {}, "next_agent": None},
    steps=[
        Loop(
            name="bb_loop",
            steps=[
                Step(name="controller", executor=controller_step),
                Step(name="specialist", executor=specialist_step),
            ],
````

## PDF 第 22 页

[原页](RAW.pdf#page=22)

````text
            end_condition=bb_loop_done,
        ),
    ],
)
拓扑不是固定链，⽽是⼀个持续调度回路：
系统控制中⼼从  " 预定义⼯作流 " 转向  " 共享状态  + 调度器 " 。
新增的能⼒
持续的、基于中间状态的动态编排。
失败模式
controller 决策不稳定
blackboard 结构变脏，信息冲突
专家之间重复劳动
系统容易过度循环
Blackboard ⽤灵活性换来了调度复杂度。
什么时候升级 / 降级？
如果问题的顺序本来就很固定，⽤  Blackboard 反⽽是过度设计，但如果你真正需要的不是持
续调度，⽽只是 " 请求进来时先分诊⼀次 " ，那就该看  Meta-Controller 。
11. Meta-Controller ：⼀次性路由，⽽不是持续编排
📎  参考实现：07_blackboard.ipynb
````

## PDF 第 23 页

[原页](RAW.pdf#page=23)

````text
它要解决什么问题？
很多系统并不需要  Blackboard 那种持续调度，它们的问题更像是：这条请求是研究类，还是
编码类，还是通⽤问答？
Meta-Controller 解决的是：⼊⼝分诊。
State 是什么？
class MetaAgentState(BaseModel):
    user_request: str
    selected_agent: Optional[str] = None
    result: Optional[str] = None
状态最⼩⽽明确：请求是什么、被路由给谁、返回了什么。
关键代码
agno ⾥这是  Team(mode="route") 的原⽣场景 ——leader 只做选择，不做任务：
from agno.team import Team
generalist = Agent(
    name="generalist",
    model=OpenAIChat(id="gpt-5-mini-mini"),
    role="Handles general Q&A.",
    instructions="Answer general knowledge questions directly.",
)
researcher = Agent(
    name="researcher",
    model=OpenAIChat(id="gpt-5-mini"),
    role="Handles research-heavy queries.",
    tools=[DuckDuckGoTools()],
    instructions="Do multi-step research using search.",
)
coder = Agent(
    name="coder",
    model=OpenAIChat(id="gpt-5-mini"),
    role="Handles Python coding tasks.",
    instructions="Write, explain and debug Python code.",
)
meta = Team(
    name="meta_controller",
    mode="route",                      # 关键：⼀次性路由
    model=OpenAIChat(id="gpt-5-mini"),
````

## PDF 第 24 页

[原页](RAW.pdf#page=24)

````text
    members=[generalist, researcher, coder],
    instructions=(
        "Choose exactly one member based on the request type: "
        "generalist for general Q&A, researcher for research-heavy queries, "
        "coder for Python coding tasks. Do not do the work yourself."
    ),
)
meta.print_response("Write a Python function to compute the LCM of two numbers.")
mode="route" 的精髓不在  graph 多复杂，⽽在于：controller ⾃⼰不做任务，只做选
择。
拓扑
它和  Blackboard 的本质区别
Meta-Controller：⼀次性路由
Blackboard：持续调度
前者像 " 分诊台 " ，后者像 " 总控台 " 。
失败模式
最核⼼的就是路由错误，因为它只路由⼀次，所以⼀旦第⼀跳错了，整个请求路径就错了，⽽
且这类错误常常不是显式报错，⽽是 " 回答得像那么回事，但⽅向错了 " 。
它为什么在⽣产⾥特别常见？
因为它⾜够简单，也⾜够有效，如果让我在⽣产系统⾥给多  agent 设计⼀个起步架构，我通
常会先选  Meta-Controller ，⽽不是⼀上来就上  Blackboard 。
````

## PDF 第 25 页

[原页](RAW.pdf#page=25)

````text
12. Ensemble ：它不是分⼯，⽽是冗余
它要解决什么问题？
前⾯的多  agent 基本都在解决 " 分⼯ " 问题， Ensemble 解决的是另⼀类问题：同⼀个问题，单
个  agent 的结论不够可靠。
你不是担⼼ " ⼀个  agent 做不完 " ，⽽是担⼼ " ⼀个  agent 看法太单⼀、偏差太⼤、幻觉太重 " 。
拓扑
标准  fan-out / fan-in ：
关键代码
agno 的  Workflow  ⽀持  Parallel step 做  fan-out ，再⽤⼀个  aggregator step 做  fan-
in ：
from agno.workflow.v2 import Workflow, Step, Parallel
class FinalRecommendation(BaseModel):
    final_recommendation: str
    confidence_score: float
    synthesis_summary: str
    identified_opportunities: List[str]
    identified_risks: List[str]
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
📎  参考实现：11_meta_controller.ipynb
````

## PDF 第 26 页

[原页](RAW.pdf#page=26)

````text
bullish = Agent(name="bullish", model=OpenAIChat(id="gpt-5-mini"),
    instructions="You are a growth-oriented bullish analyst. Argue why to invest.")
value = Agent(name="value", model=OpenAIChat(id="gpt-5-mini"),
    instructions="You are a value analyst. Focus on margin of safety.")
quant = Agent(name="quant", model=OpenAIChat(id="gpt-5-mini"),
    instructions="You are a quantitative analyst. Focus on ratios and trends.")
cio = Agent(name="cio", model=OpenAIChat(id="gpt-5-mini"),
    response_model=FinalRecommendation,
    instructions=("You are the CIO. Synthesize three analyst views into one final "
                  "recommendation. Do NOT hide disagreement — explicitly list risks."))
def run_one(agent):
    def _step(si):
        out = agent.run(si.message).content
        # Parallel 各分⽀并发写⼊共享  dict
        si.workflow_session_state.setdefault("views", {})[agent.name] = out
        return out
    return _step
def aggregate_step(si):
    views = si.workflow_session_state.get("views", {})
    body = "\n\n".join(f"[{name}]\n{view}"for name, view in views.items())
    return cio.run(f"Question: {si.message}\nAnalyst views:\n{body}").content
ensemble_wf = Workflow(
    name="ensemble",
    session_state={"views": {}},
    steps=[
        Parallel(
            name="analysts",
            steps=[
                Step(name="bullish", executor=run_one(bullish)),
                Step(name="value", executor=run_one(value)),
                Step(name="quant", executor=run_one(quant)),
            ],
        ),
        Step(name="cio_synth", executor=aggregate_step),
    ],
)
ensemble_wf.run(message="Should I buy AAPL right now?")
它和  Multi-Agent 到底差在哪？
Multi-Agent：不同  agent 做不同⼦任务
Ensemble：不同  agent 分析同⼀个问题
````

## PDF 第 27 页

[原页](RAW.pdf#page=27)

````text
前者是分⼯，后者是冗余。
新增的能⼒
⽤多视⾓和冗余来降低单次推理偏差。 和机器学习⾥的  ensemble 很像：不是因为单个模型
不能输出，⽽是因为多个模型的误差不完全相关。
失败模式
成本线性增长
多个  agent 可能共享同样的偏见
aggregator 可能强⾏合并不该合并的冲突
最终 " 综合意见 " 可能掩盖关键分歧
所以  ensemble 的关键不是 " 取平均 " ，⽽是保留冲突信息并解释冲突，这就是为什么  FinalR
ecommendation  ⾥必须有  identified_risks。
什么时候⽤？
⾼风险判断、事实核查、投资建议、复杂研究结论 —— 凡是你不想把决定押在⼀次输出上的场
景。
13. Episodic + Semantic Memory ：记忆不是把对话塞回上下⽂
记忆系统不是 " 外挂知识库 " ，⽽是  state 的外延扩展，真正重要的不是存了多少，⽽是系统如
何区分事件、事实，以及如何避免错误长期固化。
它要解决什么问题？
前⾯的架构都默认⼀个前提：当前对话结束后，系统基本失忆，⽤户要的是：记得我的偏好、
记得我们之前讨论过什么、记得哪些事实在长期上是稳定的。
这⾥有两种记忆：
Episodic memory：记住发⽣过什么（事件摘要  →  向量库）
Semantic memory：记住什么是真的（实体关系  →  图结构 / 结构化存储）
关键代码
agno 的  Memory  负责长期⽤户偏好 / 事件，AgentKnowledge  负责向量检索，两者结合
可以直接落出⼀套双记忆系统：
from agno.agent import Agent
from agno.memory.v2.memory import Memory
📎  参考实现：13_ensemble.ipynb
````

## PDF 第 28 页

[原页](RAW.pdf#page=28)

````text
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.knowledge.text import TextKnowledgeBase
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.embedder.openai import OpenAIEmbedder
from agno.storage.sqlite import SqliteStorage
# Episodic ：⽤户层⻓期记忆，⾃动从对话中抽取
memory = Memory(
    db=SqliteMemoryDb(table_name="user_memories", db_file="tmp/memory.db"),
    model=OpenAIChat(id="gpt-5-mini"),
)
# Semantic ：结构化知识库（这⾥以⽂本  + 向量库为例）
knowledge = TextKnowledgeBase(
    path="data/facts",
    vector_db=LanceDb(
        table_name="facts",
        uri="tmp/lancedb",
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    ),
)
knowledge.load(recreate=False)
mem_agent = Agent(
    name="memorized",
    model=OpenAIChat(id="gpt-5-mini"),
    memory=memory,
    enable_agentic_memory=True,          # agent 可以主动写⼊ / 检索  episodic
    enable_user_memories=True,
    knowledge=knowledge,                 # semantic
    search_knowledge=True,
    add_history_to_messages=True,
    num_history_responses=5,
    storage=SqliteStorage(table_name="sessions", db_file="tmp/sessions.db"),
    markdown=True,
)
mem_agent.print_response(
    "I'm allergic to peanuts and prefer low-carb meals. Remember that.",
    user_id="alice",
)
# 下⼀次，即使换了新  session
mem_agent.print_response(
    "Suggest a dinner plan for me.",
    user_id="alice",
)
````

## PDF 第 29 页

[原页](RAW.pdf#page=29)

````text
新增的能⼒
系统的  state 从 " 图内字段 " 扩展成：图内状态  + 图外可检索历史状态。 agent 的能⼒不再只依
赖当前上下⽂窗⼝，⽽依赖它如何从历史⾥提取相关信息。
⼯作流
memory 不再是附加模块，⽽是主控制流的⼀部分， agno 的  enable_agentic_memory=T
rue  就是把这⼀整条写回链路⾃动接上。
失败模式
错误记忆被写⼊，造成长期污染
episodic recall 召回了相似但不相关的信息
semantic graph 存⼊过时事实
抽取质量差导致记忆结构脏化
memory 让系统更强，但也让错误变得持久。
什么时候还不够？
当你发现向量检索只能 " 找相似 " ，却不能做 " 关系推理 " 时，就需要  Graph / World-Model
Memory 。
14. Graph / World-Model Memory ：当你需要的不是回忆，⽽是关系推
理
它要解决什么问题？
向量检索能回答 " 哪段历史最像现在的问题 " ，但不能天然回答 " 这个实体和那个实体之间隔了
⼏跳关系 " 。  Graph Memory 解决的是：把知识从  chunk 组织提升到关系结构。
技术核⼼
两步：
1. 从⾮结构化⽂本⾥抽实体和关系
2. 让⾃然语⾔问题转成图查询
📎  参考实现：08_episodic_with_semantic.ipynb
````

## PDF 第 30 页

[原页](RAW.pdf#page=30)

````text
Text -> Knowledge Graph -> Text-to-Cypher -> Query -> Answer
关键代码
class Node(BaseModel):
    id: str = Field(description="Unique name or identifier for the entity.")
    type: str = Field(description="Entity type, e.g., Person, Company.")
class Relationship(BaseModel):
    source: Node
    target: Node
    type: str = Field(description="Relationship verb in ALL_CAPS, e.g., WORKS_FOR, ACQUIR
class KnowledgeGraph(BaseModel):
    relationships: List[Relationship]
graph_maker = Agent(
    name="graph_maker",
    model=OpenAIChat(id="gpt-5-mini"),
    response_model=KnowledgeGraph,
    instructions=(
        "Extract entities (nodes) and relationships from the given text. "
        "Relationship type should be an ALL_CAPS verb."
    ),
)
# agno 的  Neo4j ⼯具可以直接做图查询
from agno.tools.neo4j import Neo4jTools
graph_query_agent = Agent(
    name="graph_query",
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[Neo4jTools(url="bolt://localhost:7687", user="neo4j", password="...")],
    instructions=(
        "You answer questions over a Neo4j knowledge graph. "
        "First generate a Cypher query, run it, then synthesize a natural answer. "
        "If the first query returns nothing, rewrite and retry once."
    ),
)
# 1) 抽取
kg = graph_maker.run("Tim Cook is the CEO of Apple. Apple acquired Beats in 2014.").conte
# 2) 写⼊图库（省略  write_triples ），然后查询
graph_query_agent.print_response("Which companies did Apple acquire and in which year?")
新增的能⼒
````

## PDF 第 31 页

[原页](RAW.pdf#page=31)

````text
核⼼变化是：从 " 相似性召回 " 升级到 " 结构性推理 " 。  这在企业知识问答、组织关系分析、并
购链条追踪这类问题上⾮常关键。
失败模式
抽取错误导致图污染
schema 设计不佳导致图不可⽤
Text-to-Cypher ⽣成错误查询
图查询结果正确，但  synthesis 层误读
Graph Memory 的关键不只是  LLM ，⽽是整个知识建模链条。
15. Tree-of-Thoughts ：不是让模型 " 想更多 " ，⽽是让系统 " 搜更多 "
它要解决什么问题？
真正困难的问题不是 " 链不够长 " ，⽽是 " 路径会分叉，⽽且需要回溯 " ， ToT 解决的是：把推理
从单路径⽣成，升级成对候选路径空间的搜索。
State 是什么？
class ToTState(BaseModel):
    problem: str
    active_paths: List[List["PuzzleState"]]
    solution: Optional[List["PuzzleState"]] = None
state 的单位已经不是 " ⼀个当前答案 " ，⽽是 " 多条候选路径 " 。
关键代码
经典的  wolf-goat-cabbage 谜题 —— 标准  BFS  回溯场景，在  agno ⾥， LLM 负责  ⽣成候选
动作，程序化代码负责  搜索树的扩展和剪枝。  这是  ToT ⾥重要的架构判断：不要把搜索控制
交给  LLM ，交给代码。
import copy
class PuzzleState(BaseModel):
    left_bank: frozenset = Field(default_factory=lambda: frozenset({"wolf", "goat", "cabb
    right_bank: frozenset = Field(default_factory=frozenset)
    boat_location: str = "left"
    move_description: str = "Initial state."
    class Config:
📎  参考实现：12_graph.ipynb
````

## PDF 第 32 页

[原页](RAW.pdf#page=32)

````text
        arbitrary_types_allowed = True
    def is_valid(self) -> bool:
        dangerous = [("wolf", "goat"), ("goat", "cabbage")]
        unguarded = self.left_bank if self.boat_location == "right"else self.right_bank
        return not any({a, b}.issubset(unguarded) for a, b in dangerous)
    def is_goal(self) -> bool:
        return self.right_bank == frozenset({"wolf", "goat", "cabbage"})
class Proposal(BaseModel):
    moves: List[str] = Field(description="Candidate next moves.")
proposer = Agent(
    name="proposer",
    model=OpenAIChat(id="gpt-5-mini"),
    response_model=Proposal,
    instructions="Given the current state, propose up to 3 distinct next moves.",
)
def expand(state: PuzzleState) -> List[PuzzleState]:
    # 纯程序化展开： LLM 只提供建议，代码保证搜索的正确性
    ...
def tot_solve(initial: PuzzleState, max_depth: int = 10):
    active_paths = [[initial]]
    for _ in range(max_depth):
        new_paths = []
        for path in active_paths:
            for nxt in expand(path[-1]):
                if nxt in path:
                    continue
                new_path = path + [nxt]
                if nxt.is_goal():
                    return new_path
                new_paths.append(new_path)
        active_paths = new_paths
    return None
新增的能⼒
````

## PDF 第 33 页

[原页](RAW.pdf#page=33)

````text
ToT 新增的是：把推理问题转写成搜索问题。  这和  ReAct 、 Planning 都不⼀样。前者做控制
流设计， ToT 做搜索空间设计。
失败模式
组合爆炸， ToT 不是通⽤架构，只该⽤于 " 必须回溯和搜索 " 的专⽤场景。
16. Mental Loop / Simulator ：⾏动之前，先在内部世界⾥试错
它要解决什么问题？
在机器⼈、交易、⽣产系统配置变更这类任务⾥，试错有代价。  Mental Loop 要把试错从真
实世界搬进模拟世界。
关键代码
模拟器就是⼀个普通  Python 对象，决策  agent 通过⼯具把它当成 " 可以快照  可以推进  可以回
滚 " 的沙箱：
import copy
import numpy as np
class Portfolio(BaseModel):
    cash: float = 10000.0
📎  参考实现：09_tree_of_thoughts.ipynb
````

## PDF 第 34 页

[原页](RAW.pdf#page=34)

````text
    shares: int = 0
    def value(self, price: float) -> float:
        return self.cash + self.shares * price
class MarketSimulator(BaseModel):
    day: int = 0
    price: float = 100.0
    volatility: float = 0.1
    drift: float = 0.01
    portfolio: Portfolio = Field(default_factory=Portfolio)
    class Config:
        arbitrary_types_allowed = True
    def step(self, action: str, amount: float = 0.0):
        if action == "buy":
            n = int(amount); cost = n * self.price
            if self.portfolio.cash >= cost:
                self.portfolio.shares += n; self.portfolio.cash -= cost
        elif action == "sell":
            n = min(int(amount), self.portfolio.shares)
            self.portfolio.shares -= n; self.portfolio.cash += n * self.price
        self.price *= 1 + float(np.random.normal(self.drift, self.volatility))
        self.day += 1
REAL = MarketSimulator()
def simulate_action(action: str, amount: float, horizon: int = 5) -> str:
    """Roll out an action on a forked copy of the market for `horizon` days."""
    sim = copy.deepcopy(REAL)
    sim.step(action, amount)
    for _ in range(horizon - 1):
        sim.step("hold")
    return f"Simulated value after {horizon} days: ${sim.portfolio.value(sim.price):.2f}"
def execute_action(action: str, amount: float) -> str:
    """Commit the action to the REAL market."""
    REAL.step(action, amount)
    return f"Executed: {action} {amount}. Portfolio now ${REAL.portfolio.value(REAL.price
trader = Agent(
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[simulate_action, execute_action],
    instructions=[
        "Before committing any action with execute_action, first call simulate_action.",
        "If the simulated outcome is worse than holding, do not execute.",
    ],
    show_tool_calls=True,
````

## PDF 第 35 页

[原页](RAW.pdf#page=35)

````text
)
trader.print_response("Decide whether to buy AAPL today, and how much.")
新增的能⼒
反事实执⾏（ counterfactual execution ）。  系统不再直接问 " 下⼀步做什么 " ，⽽是先问：如
果我这么做会发⽣什么？
失败模式
simulation-reality gap ，模拟器越不真实， agent 越可能做出 " 模拟⾥完美，现实⾥灾难 " 的决
定，这个架构的上限往往不是  LLM ，⽽是  simulator 的保真度。
17. Dry-Run Harness ：真正把副作⽤关进闸门⾥
安全架构的核⼼，不是让  agent 更保守，⽽是把 " 是否允许执⾏ " 做成显式控制流。  Dry-Ru
n  解决外部副作⽤，Metacognitive  解决内部边界感知，它们最好⼀起出现。
它要解决什么问题？
如果⼀个  agent 会发邮件、发帖、下单、改配置、删数据，核⼼问题是：它在执⾏前能不能
被拦住。
Dry-Run Harness 把所有真实动作都拆成两种模式： preview 和  execute 。
关键代码
agno ⾥实现  dry-run 有两个关键设计：⼯具本⾝带  dry_run 参数；Workflow  ⾥显式插
⼊⼀个⼈⼯审批  step ：
import datetime, hashlib
def publish_post(content: str, hashtags: List[str], dry_run: bool = True) -> str:
    """Publish a social media post. If dry_run=True, only preview; no side effects."""
    ts = datetime.datetime.now().isoformat()
    full = f"{content}\n\n" + " ".join(f"#{h}"for h in hashtags)
    if dry_run:
        return f"[DRY RUN @ {ts}] Would publish:\n---\n{full}\n---"
📎  参考实现：10_mental_loop.ipynb
````

## PDF 第 36 页

[原页](RAW.pdf#page=36)

````text
    post_id = hashlib.md5(full.encode()).hexdigest()[:8]
    return f"[LIVE @ {ts}] Published id={post_id}"
proposer = Agent(
    name="proposer",
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[publish_post],
    instructions=[
        "When asked to post, FIRST call publish_post with dry_run=True to preview.",
        "After the preview, stop and wait for human approval. Do NOT call dry_run=False y
    ],
    show_tool_calls=True,
)
def propose_step(si):
    return proposer.run(si.message).content
def approve_step(si):
    preview = si.previous_step_output
    print(f"\n--- PREVIEW ---\n{preview}\n---")
    decision = input("Approve and go live? (y/n): ").strip().lower()
    si.workflow_session_state["approved"] = (decision == "y")
    return decision
def commit_step(si):
    if not si.workflow_session_state.get("approved"):
        return"Rejected by human reviewer. Nothing was published."
    return proposer.run(
        "Now actually publish the same post by calling publish_post with dry_run=False."
    ).content
dryrun_wf = Workflow(
    name="dryrun",
    steps=[
        Step(name="propose", executor=propose_step),
        Step(name="approve", executor=approve_step),
        Step(name="commit", executor=commit_step),
    ],
)
新增的能⼒
````

## PDF 第 37 页

[原页](RAW.pdf#page=37)

````text
不是更智能，⽽是：让副作⽤在控制流上变成可审批对象。 很多  agent 系统的问题不在
reasoning ，⽽在  side eﬀects 。 Dry-Run 把它显式纳⼊架构。
失败模式
⼈⼯审批瓶颈
预演和真实执⾏环境不⼀致
preview ⾜够详细反⽽带来信息泄漏风险
但即便如此，这种架构在真实⽣产系统⾥⼏乎是必须的。
18. Reﬂexive Metacognitive Agent ：系统第⼀次显式思考⾃⼰的边界
它要解决什么问题？
前⾯的系统都在问 " 怎么把任务做完 " ， Metacognitive agent 先问：这个任务我到底该不该
做？  这是更⾼级的控制流，因为它不再只对外部世界建模，也开始对⾃⾝能⼒边界建模。
关键代码
class MetacognitiveAnalysis(BaseModel):
    confidence: float = Field(description="0.0~1.0, confidence in safely answering.")
    strategy: str = Field(description="'reason_directly' | 'use_tool' | 'escalate'.")
    reasoning: str
    tool_to_use: Optional[str] = None
AGENT_SELF_MODEL = {
    "knowledge_domains": ["general health", "nutrition", "exercise"],
    "tools_available": ["symptom_checker"],
    "confidence_threshold": 0.7,
    "high_risk_topics": ["prescription dosage", "emergency medical advice"],
}
self_model_agent = Agent(
    name="self_model",
    model=OpenAIChat(id="gpt-5-mini"),
    response_model=MetacognitiveAnalysis,
    instructions=(
        f"Your self-model is: {AGENT_SELF_MODEL}. "
        "For each user query, estimate confidence and pick a strategy: "
        "'reason_directly' if confidence >= threshold and topic is low-risk, "
        "'use_tool' if a matching tool exists, 'escalate' otherwise."
    ),
)
📎  参考实现：14_dry_run.ipynb
````

## PDF 第 38 页

[原页](RAW.pdf#page=38)

````text
def symptom_checker(symptoms: str) -> str:
    return f"Reference info for: {symptoms}"
responder = Agent(model=OpenAIChat(id="gpt-5-mini"), tools=[symptom_checker])
def meta_step(si):
    analysis: MetacognitiveAnalysis = self_model_agent.run(si.message).content
    si.workflow_session_state["analysis"] = analysis
    return analysis
def meta_router(si):
    analysis = si.workflow_session_state["analysis"]
    if analysis.strategy == "reason_directly":
        return [Step(name="answer", executor=lambda s: responder.run(s.message).content)]
    if analysis.strategy == "use_tool":
        return [Step(name="tool_answer",
                     executor=lambda s: responder.run(
                         f"Use the {analysis.tool_to_use} tool to help answer: {s.message
                     ).content)]
    return [Step(name="escalate",
                 executor=lambda s: "I'm not confident or allowed to answer this. Escalat
metacog_wf = Workflow(
    name="metacognitive",
    steps=[
        Step(name="self_model", executor=meta_step),
        Router(name="route_strategy", selector=meta_router),
    ],
)
新增的能⼒
````

## PDF 第 39 页

[原页](RAW.pdf#page=39)

````text
它新增的是：边界感知。  系统开始知道：我知道什么、不知道什么、需要什么⼯具、什么时
候该把问题交给⼈类。
失败模式
置信度估计不准，低估⾃⼰会过度保守，⾼估⾃⼰会在⾼风险场景下危险地⾃信。
它为什么关键？
在医疗、法律、⾦融这种领域， agent 最强的能⼒不是 " 回答 " ，⽽是 " 拒绝 " 。
19. Self-Improvement Loop ：进化回路
它要解决什么问题？
Reﬂection 只有⼀次  critique pass ，⼀个追求⾼质量输出的系统需要的是：⽣成  →  评估  →  修
订  →  再评估  →  不达标继续，也就是把质量优化做成进化回路。
关键代码
最关键的是终⽌条件， agno 的  Loop.end_condition  天然⽀持这个：
class EmailCritique(BaseModel):
    is_approved: bool
    feedback: str
class MarketingEmail(BaseModel):
    subject: str
    body: str
generator = Agent(name="email_gen", model=OpenAIChat(id="gpt-5-mini"),
    response_model=MarketingEmail,
    instructions="Write a marketing email. Follow feedback if provided.")
critic = Agent(name="email_critic", model=OpenAIChat(id="gpt-5-mini"),
    response_model=EmailCritique,
    instructions="Approve only if subject is compelling AND body has a clear CTA AND tone 
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
📎  参考实现：17_reflexive_metacognitive.ipynb
````

## PDF 第 40 页

[原页](RAW.pdf#page=40)

````text
# 跨任务：⾼质量样例库
class GoldStandardMemory:
    def __init__(self):
        self.examples: List[MarketingEmail] = []
    def few_shot_block(self) -> str:
        if not self.examples:
            return"No gold examples yet."
        return"\n\n---\n\n".join(
            f"Subject: {e.subject}\nBody:\n{e.body}"for e in self.examples[-3:]
        )
    def add(self, e: MarketingEmail):
        self.examples.append(e)
GOLD = GoldStandardMemory()
def gen_step(si):
    state = si.workflow_session_state
    prior = state.get("last_email")
    critique = state.get("last_critique")
    prompt = f"Task: {si.message}\nGold examples:\n{GOLD.few_shot_block()}\n\n"
    if prior and critique:
        prompt += (f"Previous draft:\nSubject: {prior.subject}\nBody:\n{prior.body}\n"
                   f"Critic feedback: {critique.feedback}\nRewrite to address the feedbac
    email: MarketingEmail = generator.run(prompt).content
    state["last_email"] = email
    state["revision"] = state.get("revision", 0) + 1
    return email
def critic_step(si):
    email = si.workflow_session_state["last_email"]
    verdict: EmailCritique = critic.run(
        f"Review:\nSubject: {email.subject}\nBody:\n{email.body}"
    ).content
    si.workflow_session_state["last_critique"] = verdict
    if verdict.is_approved:
        GOLD.add(email)
    return verdict
def should_stop(_outputs) -> bool:
    """Loop 终⽌： critic 批准，或达到最⼤修订次数。 """
    state = self_improve_wf.session_state
    last = state.get("last_critique")
    if last is not None and last.is_approved:
        return True
    if state.get("revision", 0) >= 3:
````

## PDF 第 41 页

[原页](RAW.pdf#page=41)

````text
        return True
    return False
self_improve_wf = Workflow(
    name="self_improve",
    session_state={"revision": 0},
    steps=[
        Loop(
            name="refine_loop",
            steps=[
                Step(name="gen", executor=gen_step),
                Step(name="critic", executor=critic_step),
            ],
            end_condition=should_stop,
        ),
    ],
)
新增的能⼒
两层：单次任务内迭代优化 + 跨任务积累⾼质量样例（GoldStandardMemory  把批准过的
结果注⼊未来⽣成），这是它和  Reﬂection 的本质区别。
失败模式
critic 标准不稳
revision 收益递减
记忆库积累低质量样本会反向污染未来⽣成
Self-Improve 不是 " 会⾃动越来越好 " ，⽽是 " 有机会在严格约束下越来越好 " 。
20. Cellular Automata ： LLM 退出主循环，智能从局部规则中涌现
它要解决什么问题？
前⾯所有架构都默认存在⼀个中⼼  agent 、⼀个主控制流、⼀个  orchestrator 。  Cellular
Automata 彻底打破这个前提：有些问题根本不需要中⼼规划，⽽适合通过局部规则产⽣全局
⾏为。
关键代码
class CellAgent(BaseModel):
    type: str  # 'EMPTY' | 'OBSTACLE' | 'GOAL'
    pathfinding_value: float = float("inf")
📎  参考实现：15_RLHF.ipynb
````

## PDF 第 42 页

[原页](RAW.pdf#page=42)

````text
    def update(self, neighbors: List["CellAgent"]):
        if self.type == "OBSTACLE":
            return
        if self.type == "GOAL":
            self.pathfinding_value = 0
            return
        m = min((n.pathfinding_value for n in neighbors), default=float("inf"))
        self.pathfinding_value = min(self.pathfinding_value, m + 1)
def neighbors_of(snapshot, r, c):
    """ 四邻（上下左右），越界跳过。 """
    H, W = len(snapshot), len(snapshot[0])
    out = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if0 <= nr < H and 0 <= nc < W:
            out.append(snapshot[nr][nc])
    return out
def run_ca(grid, steps=50):
    for _ in range(steps):
        snapshot = [[copy.deepcopy(c) for c in row] for row in grid]
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                grid[r][c].update(neighbors_of(snapshot, r, c))
在  agno ⾥， LLM 退到了纯 " 规则设计者 / 解释者 " 的位置：
rule_designer = Agent(
    name="rule_designer",
    model=OpenAIChat(id="gpt-5-mini"),
    instructions=(
        "You design local update rules for a cellular automaton. "
        "Given a high-level objective, propose a minimal Python update function "
        "that each cell will execute based only on its neighbors."
    ),
)
rule_designer.print_response(
    "Design a CA rule so that every empty cell eventually stores the shortest "
    "path length to the nearest GOAL, treating OBSTACLE as impassable."
)
新增的能⼒
这不是在现有控制流上加⼀个模块，⽽是整个范式切换：从中⼼控制转向分布式涌现。
````

## PDF 第 43 页

[原页](RAW.pdf#page=43)

````text
它和前⾯所有架构最⼤的区别
LLM 退出了执⾏主回路，它最多负责规则设计、参数选择、系统解释，真正的求解过程由⼤
量局部节点同步演化完成。
失败模式
局部规则设计不当
系统收敛慢
涌现出错误的全局结构
但⼀旦规则设计得对，它能解决很多⽤中央  planner 反⽽很笨重的问题。
21. Evaluator 不是可选项
这个项⽬反复提醒你： agent 不是只要能跑就⾏，必须能评估，⾄少有五类  evaluator ：
1. LLM-as-a-Judge：⽤独⽴  Agent 打分
2. 内置  critic：直接控制循环是否继续（Loop.end_condition）
3. 程序化验证：像  is_valid() / is_goal()  这种硬约束
4. Human-in-the-Loop：⽤⼈⼯审批做最后闸门（ Dry-Run ）
5. 演⽰式验证：⽤多场景运⾏验证系统⾏为
为什么  evaluator 是核⼼，不是附属？
因为⼀旦系统开始反思、重规划、继续迭代、决定是否执⾏、决定是否升级⼈类，你就进
⼊ " 闭环系统 " 了。  闭环系统如果没有  evaluator ，就不知道何时停、何时改、何时拒绝。
没有  evaluator 的  agent ，⼤概率只是⼀个会循环的  prompt ，不是⼀个可靠的系统。
22. 架构演化表
架构 新增的关键能⼒解决的问题 agno 对应能⼒
Reﬂection critique pass 单次⽣成质量不
稳 3 × Agent 串联成  Workflow
Tool Use world interface 模型⽆法触达真
实世界 Agent(tools=[...])
ReAct observation loop ⼯具结果不能驱
动下⼀步
Agent(tools=..., reaso
ning=True)
Planning explicit plan state 缺少全局步骤控
制
Agent(response_model=P
lan)
📎  参考实现：16_cellular_automata.ipynb
````

## PDF 第 44 页

[原页](RAW.pdf#page=44)

````text
架构 新增的关键能⼒解决的问题 agno 对应能⼒
 + Loop
PEV veriﬁcation loop 执⾏失败会静默
传播
Router
 + veriﬁer Agent
Multi-Agent role decomposition 单  prompt ⾓⾊
冲突
多  Agent  或  Team(mode="c
oordinate")
Blackboard shared workspace + dyn
amic controller
固定流⽔线不够
灵活
workflow_session_state
 + controller Router
Meta-Controller entry routing 请求类型不同需
要分诊 Team(mode="route")
Ensemble parallel redundancy 单⼀答案不够可
靠
Workflow(Parallel
(...))
 + aggregator
Episodic/Semantic
Memory long-term recall 系统跨轮失忆 Memory
 + AgentKnowledge
Graph Memory relational reasoning 相似召回不能做
关系推理
Neo4jTools
 + Cypher agent
ToT search tree 线性推理⽆法回
溯 程序化搜索  + proposer Agent
Mental Loop counterfactual execution 真实试错成本太
⾼
双⼯具  simulate_action /
execute_action
Dry-Run side-eﬀect gating 副作⽤动作不能
直接执⾏
⼯具带  dry_run 参数  + appro
val Step
Metacognitive self-boundary reasoning 系统不知道⾃⼰
不会什么
response_model=Metacog
nitiveAnalysis
 + Router
Self-Improvement iterative quality loop ⼀次优化不⾜
Loop(end_condition
=...)
 + gold memory
Cellular Automata decentralized emergenc
e
中央控制不适合
某些问题
LLM 只设计规则，程序化并⾏
更新
23. 怎么选？问你缺哪种控制能⼒，不要问哪个架构好
你缺的能⼒ 优先架构 为什么
输出质量不稳 Reﬂection 最⼩质量闭环
多步⼯具推理 ReAct 观察 - ⾏动循环最实⽤
全局步骤控制 Planning 把控制流显式化
⼯具容错 PEV 把验证接进主回路
⾓⾊分⼯ Multi-Agent 把认知拆开
````

## PDF 第 45 页

[原页](RAW.pdf#page=45)

````text
你缺的能⼒ 优先架构 为什么
动态编排 Blackboard 基于共享状态调度
请求分诊 Meta-Controller ⼀次路由最省复杂度
⾼可靠结论 Ensemble ⽤冗余降低偏差
跨轮记忆 Episodic / Semantic Memory 把历史纳⼊系统
关系推理 Graph Memory ⽀持多跳查询
回溯搜索 ToT 适合分⽀型解空间
⾏动前模拟 Mental Loop 降低真实试错成本
副作⽤审批 Dry-Run 先预演再执⾏
边界感知 Metacognitive 先判断能不能做
长期⾃我改进 Self-Improvement 质量循环  + 样例积累
去中⼼化求解 Cellular Automata ⽤局部规则换全局⾏为
如果你缺的是输出质量
先上  Reflection；需要多轮逼近和长期改进，上  Self-Improvement
如果你缺的是与世界交互
简单任务上  Tool Use；多步动态任务上  ReAct
如果你缺的是显式步骤控制
上  Planning；⼯具不可靠，再升级到  PEV
如果你缺的是⾓⾊分⼯
固定分⼯：Multi-Agent；动态持续调度：Blackboard；⼊⼝分诊：Meta-Cont
roller；同题多视⾓冗余：Ensemble
如果你缺的是长期状态
记历史事件：Episodic Memory；做关系推理：Graph / World-Model Memory
如果你缺的是求解范式
需要回溯搜索：Tree-of-Thoughts；需要先模拟后执⾏：Mental Loop；需要去
中⼼化求解：Cellular Automata
如果你缺的是安全边界
需要副作⽤审批：Dry-Run Harness；需要知道⾃⼰不能做什么：Metacognitive
Agent
24. 最终结论： Agent 架构的演化，本质上是在设计更好的控制流
看完整个项⽬并⽤  agno 重写⼀遍后，我最⼤的感受不是 "agent 真多 " ，⽽是⼀个更朴素的判
断：
````

## PDF 第 46 页

[原页](RAW.pdf#page=46)

````text
所谓  agent architecture ，不是模型能⼒表，⽽是控制流设计史。
它在不断回答同⼀组问题：什么时候该停？什么时候该继续？什么时候该重试？什么时候该换
⾓⾊？什么时候该查⼯具？什么时候该调⽤历史？什么时候该先模拟？什么时候该拒绝？什么
时候该让⼈类接管？
这些问题不依赖某⼀个框架。⽆论你底层⽤什么  DSL ，只要开始做真实的  agent 系统，就⼀
定会亲⼿长出同⼀组抽象：  Workflow.steps 表达确定性边  Router 表达条件路由  Lo
op 表达循环与终⽌条件  Parallel 表达并⾏冗余  workflow_session_state 表达显
式共享状态  Agent(tools=...)  内置  tool loop Team(mode="route")  把⼀整段分诊
逻辑改为⼀个  Team 组合
但控制流本⾝没有变。这恰恰说明这些问题不是某个框架发明出来的，⽽是真实系统演化过程
中必然会长出来的。
从这个⾓度看，这  17 种架构并不神秘。它们只是对同⼀个系统问题的  17 种不同回答。
如果让我把整篇⽂章压缩成三句话：
1. 先别迷信 " 万能  agent" ，先把状态和控制流画清楚。
2. ⼤多数系统从  ReAct 起步，但可靠系统⼀定会引⼊验证、记忆和边界控制。
3. 真正⾼级的  agent ，不是更敢做事，⽽是更知道什么时候不该做。
⼀旦你看懂这条路径，后⾯再看到任何新的 "agent 架构名词 " ，你都可以先问它三个问题：
它新增了什么  state ？
它新增了什么  router ？
它新增了什么  evaluator ？
只要这三个问题答不出来，它⼤概率就不是⼀种新架构，只是旧架构换了个名字。
参考
1 、https://github.com/FareedKhan-dev/all-agentic-architectures
2 、https://github.com/agno-agi/agno
````

## PDF 第 47 页

[原页](RAW.pdf#page=47)

````text
阅读 1 . 3 万
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
留⾔
还没有留⾔，来写⾸评
写留⾔
````

## PDF 第 48 页

[原页](RAW.pdf#page=48)

````text
````

## 采集与转写核验记录（非原文）

以下说明由本次核验添加；上方逐页文本保持文本层原样，图片与布局以PDF为准。

- PDF物理页 11,14,16,19,24,25,29,33,35,36,38：p.11、14、16、19、24、25、29、33、35、36、38图位置显示加载占位；无法恢复原图，原材料不完整
- PDF物理页 2,7,8,13,18,30,32,36,38,48：p.2与48空白，多个代码长行右侧截断；ToT expand与图谱写入明确省略，不可视为完整可运行实现
- PDF物理页 30,40,41：Graph示例关系schema缺年份字段却询问年份，写入函数省略；Self-Improve示例仅进程内样例列表且无参数训练，不等于RLHF

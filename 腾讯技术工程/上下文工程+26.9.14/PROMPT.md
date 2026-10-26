# Context_Engineering上下文工程：Prompt合集

> 来源：[归档PDF](RAW.pdf)，capture-001。摘录取自PDF可见文本层，保留提取出的字符与换行；相关页面已视觉核对，在线原文及原始附件未核实。后三部分为AI整理，未实际执行。反例与说明节选已在标题或边界中注明。

## 1. AI文章写作（笼统示例）

### Prompt原文

````text
请写⼀篇关于  AI 的⽂章
````

### 使用步骤

1. 作为基线发出该请求，与下一条约束更清晰的请求比较。

### 预期输出

一篇关于AI的文章，受众、篇幅与范围未限定。

### 使用边界与待验证点

作者用于说明输入过于笼统；输出质量不能仅靠一句请求保证。

## 2. 面向初学者的大语言模型科普

### Prompt原文

````text
请⽤⾯向初学者的
通俗语⾔，写⼀篇  800 字的关于⼤语⾔模型⼯作原理的科普⽂章
````

### 使用步骤

1. 提交原文请求，明确初学者受众及800字要求。
2. 检查解释是否通俗、准确并符合篇幅。

### 预期输出

约800字的大语言模型工作原理科普。

### 使用边界与待验证点

属于单轮写作示例；生成的技术事实仍需核对。

## 3. 客服角色（作者反例）

### Prompt原文

````text
你是⼀个有帮助的客服助⼿。请专业地处理⽤户问
题。
````

### 使用步骤

1. 只作为对照样例，与下一条原则性指令比较缺少的边界。

### 预期输出

笼统客服回复，没有明确工具或风险约束。

### 使用边界与待验证点

作者明确将其标为空洞指令，不适合作为完整客服规则。

## 4. 金融客服原则性指令

### Prompt原文

````text
## ⾓⾊：你是  XYZ ⾦融的客服助⼿，专
注处理⽀付和账户问题。 ## 核⼼原则：先确认⽤户情绪，再给解决⽅案；涉及资⾦安全（如
疑似盗刷）⽴即升级⼈⼯，不⾃⾏决策；不承诺具体赔偿⾦额，只说明流程；需要查订单才回
答，不凭猜测回答。 ## ⼯具使⽤原则： query_order 查订单状态， query_account 查账户状
态，两者不可混⽤，不确定时先问⽤户。
````

### 使用步骤

1. 核对业务角色，并确认订单与账户工具的实际接口。
2. 按原文边界处理问题；涉及资金安全时交由人工。

### 预期输出

基于查询结果的支付／账户问题回复，以及必要的人工升级。

### 使用边界与待验证点

XYZ及工具名属于示例；原文不是完整金融业务规范，本次未接入任何工具。

## 5. 编码Agent对话历史压缩

### Prompt原文

````text
You are compacting a conversation history for an AI coding agent. Preserve the following
information: 
1. The original task goal and any clariﬁcations made 
2. All completed steps and their outcomes 
3. Key decisions made and the reasoning behind them 
4. Current state: what ﬁle is being worked on, what problem remains 
5. Any unresolved errors or known constraints 
6. Any important user preferences mentioned  Compress the following into a structured
summary under 600 tokens. Do NOT include: raw tool outputs, duplicate attempts, verbose
error logs.  Output format: ## Task Overview ## Progress ## Current State ## Key Decisions
## Open Issues
````

### 使用步骤

1. 附上需要压缩的对话历史。
2. 按原文保留目标、进展、决策、当前状态、约束和偏好。
3. 将摘要与原历史对照检查，确认后再用于后续上下文。

### 预期输出

600 token以内、按五个指定标题组织的结构化摘要。

### 使用边界与待验证点

摘要可能遗漏关键证据；600 token是作者模板要求，不能保证所有任务都能无损压缩。

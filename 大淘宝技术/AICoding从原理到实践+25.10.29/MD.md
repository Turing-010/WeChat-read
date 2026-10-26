# AI Coding 长文分享：如何真正把工具用起来，从原理到实践：PDF文本转写

> 这是原始PDF文本层转写，不是学习摘要。页码为PDF物理页序；图表、代码版面和图片文字不能完整表达在此文本层。已查看图像的内容和质量问题见AI学习笔记及META.json。

[原文PDF](RAW.pdf) · [AI学习笔记](AI_AICoding从原理到实践.md) · [处理与质量记录](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
AI Coding 长文分享：如何真正把工具用起来，从原理到实
用户&内容技术 2025年10月29日 06:08 浙江
大淘宝技术 584人
践
本文从原理到实
践系
统地分享了如何高效使用AI编程工具。涵盖其底层机制（如Token
计算
、工具调用、Codebase索引与Merkle Tree）、提升对话质量的方法（如规则设
置、渐进式开
发）、实际应用场景（如代码检索、
绘图生成、问题排查），并推荐了结
合AI的编码最佳实
践，包括文档、注释、命名规范和安全
合规，旨在帮助不同经验水平
的开
发
者真正把AI工具用好。
引言
本文在编写时尽量考虑了
不同业务、不同经验、
对 AI 编程抱有
不同态度的同学的需求，但是
由于个人水平（和时间）有限，只能写个大概，希望大家都能有所收获：
AI Coding 深 度用 户 ，人码 AI 三 合一，无 需 了 解 实
践 经 验 → 了 解 底 层 原
理；
手搓
仙人，日码1000
+行
，不用 AI 依然很舒适 → 进一步提升编码效率，以
及提升编码外的效率；
团队新人，对项目代码的具体实现不太熟悉，需要边做边学 → 如何快速上手
新项目，不出锅；
...
在使用 AI 编程的过程中，我知道大家偶尔会有
如下感受或者疑问：
一口气生成整个需求代码，然后打补丁快？还是边写代码边提问快？
AI 的能力边界在哪？什么场景下适合使用？什么场景下适合手搓
？
AI 只能帮我写代码吗？能不能探索下新场景？
...
其实除了
大家，我自己在很长一段时间也有类似的疑问，对 AI 的看法也发生过多次改变；而
在最近的几个月里，我也一直在摸索如何更高效地使用 AI 进
行
编程，今天讲给大家听。
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
本文 写 于7月， 在近几 个月的时间里， AI Coding 领 域又迎 来了 很大的更 新 换代 ，Claude
Code、CodeX 等CLI 工具一样非常好用，基模的能力也上升到了新高度。总体感觉下来每家
的实力都很强，推荐大家都尝试一下。
本文主要基于 Cursor 相关原理和经验编写。由于 Claude 模型在国内被禁用，我们需要在模
型、工具上分别寻求一些替代方
案。CLI类型工具有
新出品的
Qwen Code、
iFlow，IDE 类型
的工具也有
新出品的
Q
oder。模型方面，Qwen3-Coder 的表现也非常亮眼，是不错的替代方
案。
从原理讲起，了解 AI 编程工具的能力和边界
▐ 2.1 Token计算机制
2.1.1 原理
我们知道不同 model 都
有
息，那么在 cursor 中我们的任
不同大小的上下文，上下文越
大的模型自然能接受更大的提问信
意一次聊天，大致会产生如下的 token 计算：
初始 Token 组成：初始输
用户问题 : 我们输
入的文字
入 = SystemPrompt
用户问题
Rules
+
+
+
主动添加的上下文（图片、项目目录、文件）
对话历史
+
Rules：project rule
+
user rule
+
memories
工具调用后的 Token 累积：cursor 接收用户信息后开始调用 tools 获取更为详细的信息，
并为问题回答做准备：总 Token = 初始输
入
所有
+
工具调用结果
2.1.2 举个例子
场景描述
工具来分析代码。
用户粘贴了一段代码，以及一张相关图片，询问"这个函数有什么问题？"，然后 AI 需要调用
初始Token组成
SystemPrompt
1 你是一个专业的代码审查助手，能够分析代码问题并提供改进建议...
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
2 注意：Cursor调用大模型的完整的提示词在“2.5 调用LLM的Prompt”部分，感兴趣的同学可以自
UserPrompt
1
用户输
入文字: "这个函数有什么问题？"
2
3
主动添加的上下文:
4
- 图片: [相关图片]
5
- 用户附加文件: [Line12-22]somemodule/src/main/java/com/xxx/xxx/service/Ex
6
- 项目目录: /Users/KuBo/IdeaProjects/someproject/
7
- 当前文件: somemodule/src/main/java/com/xxx/xxx/service/ExampleService.j
R
ules
1
projectrule: 多模块Maven项目，使用Java 8，包名统一为com.xxx.xxx.*...
2
3
userrule: 始终使用中文回复，不要使用
行
memories: [相关
的项目记忆和上下文信息]
尾注释，单
不超过120字符...
行
对话历史
1
2
用户: 你好，我想了解一下这个项目的结构
AI: 这是一个多模块的Maven项目，主要包含以下模块...
工具调用后的Token累积
工具调用1: 读取文件内容
1
2
3
工具调用: read
file
_
参数: target
_
file = "somemodule/src/main/java/com/xxx/xxx/service/Exampl
结果: [返回完整的Java文件内容，约2000个token]
工具调用2: 代码搜
索
1
2
3
工具调用: codebase
search
_
参数: query = "Java方法异常处理最佳实
践"
结果: [返回相关
的代码示例和最佳实
践，约1500个token]
工具调用3: 语法检查
1
2
3
工具调用: read
lints
_
参数: paths = ["somemodule/src/main/java/com/xxx/xxx/service/ExampleServ
结果: [返回linter错误信息，约300个token]
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
最终Token计算
初始输
入 = SystemPrompt(500) +
tokens
工具调用结果 = 文件内容(2000) +
搜
总Token = 1800
+
3800 = 5600 tokens
用户问题(200) +
R
ules(800) +
对话历史(300) = 1800
索结果(1500) +
语法检查(300) = 3800 tokens
实际上下文示例
M
这里就是多轮对话的第二次请求后，LL
看到的实际内容了，当然这里仅作示例，实际工程调
用时在格式和内容上都
有一些差别。
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
25
26
[SystemPrompt] 你是一个专业的代码审查助手...
[用户问题] 这个函数有什么问题？
[图片] [代码截图显示一个Java方法]
[项目目录] /Users/KuBo/IdeaProjects/someproject/
[当前文件] somemodule/src/main/java/com/xxx/xxx/service/ExampleService.j
[Rules]
- 多模块Maven项目，使用Java 8
- 始终使用中文回复
-
不超过120字符
行
...
[对话历史]
用户: 你好，我想了解一下这个项目的结构
AI: 这是一个多模块的Maven项目
...
[工具调用结果1] 文件内容:
public class ExampleService {
public String processData(String input) {
if (input == null) {
return null; // 问题：应该抛出异常而不是返回null
}
单
// ... 更多代码
}
}
[工具调用结果2] 搜
索结果:
异常处理最佳实
践建议...
[工具调用结果3] 语法检查:
Line 5: 建议使用Objects.requireNonNull()进
空值检查
行
▐ 2.2 工具调用
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
在上一部分，其实用到了很多工具，这是大语言模型与你的代码仓库进
交互的桥梁。我们知
行
道，大模型的本质工作是读取token然后吐出token，并没有
长出手来修改代码，也并不
知道
我们的私人仓库里
有什么（因为不在它的训练集中），这些问题都需要“工具调用”能力来解
决，也就是常说的Function Call。
2.2.1 搜
索
用于搜
索代码库和网络以查找相关信息的工具。
2.2.2 编辑
用于对文件和代码库进
行特定编辑的工具。
2.2.3 运
行
Chat 可以与您的终端进
交互。
行
2.2.4 MCP
聊天功能可以使用配置的 MCP 服务器与外部服务进
行
交互，例如数据库或第三方 API。
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
2.2.5 Browser
Cursor 新版本对浏览器功能做了升级，原生新增了 Brower Automation 工具，不需要再手动
配置相关MCP。它可以直接操作浏览器，对于前端自动化有一定的帮助，下面是官方演示。
00:30
00:30
▐ 2.3 代码库检索
2.3.1 为何要了解
作为一个“Coding”工具，如何理解代码仓库非常重要。Cursor 代码库工具的检索和构建，都
是经过 Codebase Indexing 流程实现的，它其实就是在对整个代码仓库做 RAG，即：将你的
代码转换为可搜
索的向量。
了解这一部分将有助于：
提示词的编写：如何提问，编写什么样的 prompt，才能让模型准确地找到它需要的代码？
代码规范：在编码时，什么样的代码风格是“模型友好”的？
想直接看结论的同学，可以跳转到“2.6 话又说回来了”这一应用部分，后文将直接结合例子回
答这些问题。
2.3.2 工作原理
在用 户 导入项目时， Cursor 会启 动一个 Codebase Indexing 流 程， 它的进 度 可 以 在
Preference - Cursor Settings - Indexing & Docs 中
看到。
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
据官方文档描述，这一步主要有 7 个步骤：
1. 你的工作区文件会与 Cursor 的服务器安全
同步，确保索引始终最新。
2. 文件被拆分为有
意义
的片段，聚焦函数、类和逻辑代码块，而非
任
意文本段。
3. 每个片段使用 AI 模型转为向量表示，生成能捕捉语义
的数学“指纹”。
4. 这些 向量嵌
入存储 在专用 的向量数据 库中，支 持 在数百 万 代 码片 段中进
行
索。
5. 当你搜
索时，查询会用与处理代码相同的 AI 模型转为向量。
6. 系
统将你的查询向量与已存储的
入向量进
行
比对，找到最相似的代码片段。
7. 你会获得包含文件位置和上下文的相关代码片段，并按与查询的语义相似度排序。
高 速相似 度搜
嵌
2.3.3 更多细节
2.3.3.1 索引构建
项目初始化阶段
扫描项目文件夹，建立文件清单
计算Merkle树哈希值，用于后续变更检测
根据.gitignore和.cursorignore规则过滤文件
执
行
初始Merkle树同步到服务器
增量同步机制
系
统每10分钟执
行
一次变更检测
通过哈希值比
较识别文件
变更
仅上传发生变更的文件，实现增量同步
服务器端处理
对同步的文件进
分块处理
行
计算文件内容的向量表示
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
并
存储到Turbop
行
uffer数据库和AWS缓存
2.3.3.2 用户查询流程
查询向量化
用户提交自然语言查询
本地计算查询的向量表示，捕获语义信息
相似度搜
索
使用Turbop
uffer数据库进
基于向量相似度找到最相关
返回混淆的文件路径和
最近邻搜
索
行
的代码片段
行
号信息
代码片段获取
客户端根据返回的路径和
行
号本地读取代码片段
确保获取的是用户环境中的实际代码内容
AI答案生成
将代码片段上传到服务器
AI模型结合用户查询和代码上下文生成最终答案
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
2.3.3.3 极致速度：Merkle Tree 增量块验证
Cursor 的代码库检索是使用RAG实现的，在召回信息完整的同时做到了极致的检索速度，体
验下来要比Claude Code 快很多。后者的代码理解方式将在“2.5 Claude Code是如何做的”
这一部分进
行介绍。为了保证这一性能优势，需要在检索的每一个步骤都保持高速，不然就会
被中间步骤卡脖子。
导入：Indexing是离线
的，核心是 Chunking & Embedding，一般在10分钟左右完成，与
仓库总代码量有关
。不过一次导入终生享受，这个时间成本并不影响体验；在indexing建
立好之前，Cursor 会通过基础工具（比
如grep）来进
行
代码检索，保证可用性。
查询：q
uery 的 embedding 和向量检索都是在线
的，可以做到秒级
。
增量导入：这里其实比
较有说法，因为我们的修改是实时的，且可能发生在任何阶段。那
么实际上就需要一种能够快速判断“哪些代码是新增的 / 被更新了”的方法。
对于“增量导入”的部分，我们介绍下 Cursor 实际使用的一种数据结构——Merkle Tree。实
际上我们常用的版本控制
工具Git的底层用的也是这种数据结构。（不过这部分跟AI无关，大伙
可以酌情跳过）
什么是Merkle Tree
默克尔树（Merkle Tree）也叫哈希树，是一种树形数据结构：
叶子节点（Leaf Node）：每个叶子节点存储的是某个数据块的加密哈希值。
非叶子节点（Branch/Inner Node）：每个非叶子节点存储的是其所有
后的哈希。
子节点哈希值拼接
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Merkle Tree 的作用
1.
高效验证
要证明某个数据块属于这棵树，只需要提供从该叶子节点到根节点路径上的"兄弟节点"哈希
值。验证复杂度为O(log n)，而不是O(n)。
2. 数据完整性保证
只要根哈希（Merkle Root）保持不变，就能确保整个数据集未被篡改。任何底层数据的修改
都会导致根哈希发生变化。
3. 增量同步
通过比
较不同版本的Merkle Tree，可以快速定位发生变化的数据块，实现高效的增量同步。﻿
Merkle Tree功能总结
高效完整性校验，防篡改
每个对象都用哈希值唯一标识，任何内容变动都会导致哈希变化。
只要根哈希（commit 哈希）没变，说明整个项目历史、内容都没被篡改。
高效对比和查找变更
```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
只需对比 tree 或 commit 的哈希，就能快速判断两次提交是否完全一致。
递归对比 tree 结构，可以高效定位到具体变动的文件和内容。
高效存储与去重
相同内容的文件或目录结构只存一份，极大节省空间。
没有
变动的部分直接复用历史对象，无需重复存储。
▐ 2.4 Cursor 调用 LLM 的 Prompt
在原理方面，这里提供了AI Coding工具调用大预言模型所使用的prompt。可以看到，它其实
跟我们平时写代码调用模型是很相似的，但是在工具调用、上下文获取上都
有针对Coding领域
非常细节的定制
化。
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
25
26
27
28
29
30
31
You are a powerful agentic AI coding assistant, powered by [some model
You are pair programming with a USER to solve their coding task.
The task may require creating a new codebase, modifying or debugging a
Each time the USER sends a message, we may automatically attach some i
This information may or may not be relevant to the coding task, it is
Your main goal is to follow the USER's instructions at each message, d
<tool
_
calling>
You have tools at your disposal to solve the coding task. Follow these
1. ALWAYS follow the tool call schema exactly as specified and make su
2. The conversation may reference tools that are no longer available.
3. **NEVER refer to tool names when speaking to the USER.** For exampl
4. Only calls tools when they are necessary. If the USER's task is gen
5. Before calling each tool, first explain to the USER why you are cal
</tool
_
calling>
<making_
code
_
changes>
When making code changes, NEVER output code to the USER, unless reques
Use the code edit tools at most once per turn.
It is *EXTREMELY* important that your generated code can be run immedi
1. Always group together edits to the same file in a single edit file
2. If you're creating the codebase from scratch, create an appropriate
3. If you're building a web app from scratch, give it a beautiful and
4. NEVER generate an extremely long hash or any non-textual code, such
5. Unless you are appending some small easy to apply edit to a file, o
6. If you've introduced (linter) errors, fix them if clear how to (or
7. If you've suggested a reasonable code
_
edit that wasn't followed by
</making_
code
_
changes>
<searching_
and
_
reading>
You have tools to search the codebase and read files. Follow these rul
1. If available, heavily prefer the semantic search tool to grep searc
2. If you need to read a file, prefer to read larger sections of the f
3. If you have found a reasonable place to edit or answer, do not cont
```

## PDF 第12页

[查看原页](RAW.pdf#page=12)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

````text
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
</searching_
and
_
reading>
<functions>
<function>{"description": "Find snippets of code from the codebase mos
<function>{"description": "Read the contents of a file. the output of
<function>{"description": "PROPOSE a command to run on behalf of the u
<function>{"description": "List the contents of a directory. The quick
<function>{"description": "Fast text-based regex search that finds exa
<function>{"description": "Use this tool to propose an edit to an exis
<function>{"description": "Fast file search based on fuzzy matching ag
<function>{"description": "Deletes a file at the specified path. The o
<function>{"description": "Calls a smarter model to apply the last edi
<function>{"description": "Search the web for real-time information ab
<function>{"description": "Retrieve the history of recent changes made
</functions>
You MUST use the following format when citing code regions or blocks:
```
startLine:endLine:filepath
// ... existing code ...
```
This is the ONLY acceptable format for code citations. The format is `
<user
_
info> The user's OS version is MacOS 12.3. The absolute path of
Answer the user's request using the relevant tool(s), if they are avai
▐ 2.5 Claude Code CLI 工具基础原理
2.5.1 国内如何用上CLI工具
对于编码工具来说，自身的工程功能固然是很重要的一方面。对
不同供应商提供的相同模型，
其Function Call能力差异可能很大，可见工程实现是很重要的一部分。不过，基模（各家旗
舰： Claude Sonnet 4.5 / GPT-5 / Qwen3 Coder / Grok-4 Code / Gemini 2.5 Pro /
Kimi K2 等等）同样是命脉一般的存在，直接影响到了这个助手是否聪明。
在介绍 Claude Code 的基础原理之前，这里先给出在Claude模型已经被禁用的当下，如何使
用百炼提供的Qwen3 Coder模型，得到几乎满血的 CLI 工具体验。由于Cursor的主要也是使
用 Claude 系列模型，也可用类似的手段以代理到 Qwen3 Coder 等更稳定的国产模型。
获取阿里云百炼提供的API-KEY
平台地址：bailian.console.aliyun.com/?tab=model#/api-key
````

## PDF 第13页

[查看原页](RAW.pdf#page=13)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
进
行
环境参数替换
Claude Code、CodeX 等常用CLI工具都支持供应商替换，拿 Claude Code来说，需要把供
应商的端点在环境变量里进
行
替换，然后把你的密匙写进去。其他工具也是类似，不过配置的
位置略有差异。
1
2
export ANTHROPIC
BASE
_
_
URL=https://dashscope.aliyuncs.com/api/v2/apps/cla
export ANTHROPIC
AUTH
TOKEN=“上面获取到的sk开头
_
_
的key”
2.5.2 模型调用Prompt实例
与 Cursor 类似，Claude Code 也有自己的一套模型调用提示词，准确来说，这是一套完整的
上下文工程。这里面有用户环境、用户问题、
系
统提示词、工作过程管理（自动生成并按
顺序
执
行
TODO）等部分。这里直接使用了其他同学的逆向结果，做了一些删减，感兴趣的话可以
在参考文献中
看到完整版。
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
25
26
27
You are Claude Code, Anthropic's official CLI for Claude. You are an i
# Proactiveness
You are allowed to be proactive, but only when the user asks you to do
1. Doing the right thing when asked, including taking actions and foll
2. Not surprising the user with actions you take without asking
3. Do not add additional code explanation summary unless requested by
# Synthetic messages
Sometimes, the conversation will contain messages like [Request interr
# Following conventions
When making changes to files, first understand the file's code convent
- NEVER assume that a given library is available, even if it is well k
- When you create a new component, first look at existing components t
- When you edit a piece of code, first look at the code's surrounding
- Always follow security best practices. Never introduce code that exp
# Task Management
You have access to the TodoWrite and TodoRead tools to help you manage
These tools are also EXTREMELY helpful for planning tasks, and for bre
# Doing tasks
The user will primarily request you perform software engineering tasks
# Tool usage policy
- When doing file search, prefer to use the Task tool in order to redu
- VERY IMPORTANT: When making multiple tool calls, you MUST use Batch
- You MUST answer concisely with fewer than 4 lines of text (not inclu
Here is useful information about the environment you are running in:
<env>
Working directory: /Users/xxx/Projects/xxx
Is directory a git repo: No
```

## PDF 第14页

[查看原页](RAW.pdf#page=14)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
28
29
30
31
32
33
34
35
36
37
38
39
40
41
Platform: macos
OS Version: XX
Today's date: XX/XX/2025
Model: someModel
</env>
<context name="directoryStructure">
Below is a snapshot of this project's file structure at the start of t
- /Users/xxx/Projects/xxx/
- CLAUDE.md
- SomeModule/
- SomeFiles
- README.md
-
...
</context>
▐ 2.6 话又说回来了
在上面的部分，我们提出了很多问题，下面将直接给出最佳实
践。
2.6.1 提升对话质量：合理利用上下文窗口
由于AI模型的上下文窗口存在容量限制，我们需要在有限空间内最大化信息价值。
Action 1：进
清晰的问题描述
行
在上面的原理部分，我们介绍了模型是如何进
行
代码库理解的（向量匹配
、意图拆解后进
模
行
搜
糊
索、调用链溯源等）。因此，在描述问题时，我们最好能给出具体的功能、文件名、
方法
名、代码块，让模型能够通过语义
检索等方式，用较短的路径找到代码，避免在检索这部分混
杂太多
弱相关内容，干扰上下文。
Action 2：把控上下文长度
现在不少工具都支持上下文占用量展示，比
比例。超出这个比例之后，工具会对历史内容进
如这里的18.0%表示之前的对话占用的上下文窗口
行
压缩，保证对话的正常进
。
行
但被压缩后的信息会缺失细节，所以建议大家在处理复杂问题时，采用上下文窗口大的模型/模
式，尽量避免压缩。
```

## PDF 第15页

[查看原页](RAW.pdf#page=15)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Action 3：尽可能地使用Revert和新开对话
省上下文是一方面，维持上下文的简洁对模型回答质量提升也是
问题跟历史对话关系
不大，就最好新开一个对话。
有帮助的。因此，如果你的新
在多轮对话中，如果有一个步骤出错，最好的方式也是会退到之前出错的版本，，基于现状重
新调整 prompt 和更新上下文；而不是通过对话继续修改。否则可能导致上下文中存在过多无
效内容。
这里回 滚 在IDE类 型 的工 具里操 作 很方 便 ， 点一下 “Revert”按
Claude Code 等 CLI 类型的工具，回滚起来就没有
commit。
钮 即 可 。不 过 如果 使用 的是
这么方便，可以考虑在中间步骤多进
行
Action 4：给出多元化的信息
我们不只可以粘代码、图片进去，还可以让模型参考网页、Git历史、
IDE 类的工具支持的比
较好，因为是在IDE环境里面，而CLI在终端中，限制
当前打开的文件等，这些
就要多一些（但更
灵活）。
上下文进阶用法
对于多工具的进阶用户，可以通过提示词构建，来使一个工具指挥另一个工具连续干活8小时
（AI：喂我花生！），中间用Markdown文本来进
行信息交换。这其实也是上下文工程的一种
用法，但是在生产中并不常用，感兴趣可以自
搜
索。行
```

## PDF 第16页

[查看原页](RAW.pdf#page=16)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
2.6.2 关
于R
ule
其实这就是一种可复用的上下文。比
如，我在整个开
发过程中，提炼出了很多共性规则（不要
写太多注释、不要动不动就生成测试文件），就可以把它们沉淀为R
ule，让模型在每次的对话
中自动复用。其核心主要是通过复用的思想来节约精力。
2.6.2.1 Cursor 中的
R
ule
Project R
ule
跟项目绑定的R
ule，它的本质是在.git的同级目录下维护一个.cursor的目录，在这里面存放自
定义
的规则文本，然后在每次会话时根据你的设置，决定要不要把这些内容贴到上下文中。可
以通过/Generate Cursor R
ules命令来自动生成。
规则 描述
Always Always included in the model context 始终包含在模型上下文中
Auto Attached
Included when files matching a glob
当引用匹配 glob 模式时包含
pattern are referenced
Agent Req
uested
R
ule is available to the AI, which decides whether to include
it. Must provide a description 规则对 AI 可用 ， AI 决定 是否 包
含，必须提供描述
ManualOnly included when explicitly mentioned using
当使用
@ruleName 明确提及时包含
@ruleName 仅
```

## PDF 第17页

[查看原页](RAW.pdf#page=17)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
User R
ule
跟用户绑定的全局设置，它与项目维度的规则类似，只不过生效范围是全局，它的对应规则文
件在用户的根目录下面。需要注意的是，这个规则的更新不是实时生效的，可能要等10分钟左
右，推测这里也用到了RAG，离线进
索引构建。
行
这里举几个我用的例子：
1. 凡是在方
案、
编码过程遇到任何争议或不确定，必须在第一时间主动告知我由我做决策。
2. 对于需要补充的信息，即使向我询问，而不是直接应用修改。
```

## PDF 第18页

[查看原页](RAW.pdf#page=18)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
3. 不要生成测试文件
4. 每次改动基于最小范围修改原则。
、
任何形式的文档、运
行测试、打印日志、使用示例，除非显式要求。
2.6.2.2 Claude Code / CodeX 中的
R
ule
在上面 的“2.5.2 模 型调用 Prompt 实 例”部 分 ， 我 们看 到 很多 模 型 的痛 点 （比
如生 成 太多
测、
非最小范围修改）问题，已经被写进了 Claude Code 的
系
统提示词中，这源于对模型和
用户体验的
深度洞察。
而至于项目维度的规则，在CLI工具中统一被整合进了使用/init指令生成的Markdown文件中，
被 存放 在项目根目录 中。Claude 生 成 的文 件 为 CLAUDE.md ， CodeX 生 成 的文 件 为
AGENT.md。
在对话中，这些文件会被完整的贴进上下文，因此如果你有自己的定制
里面。比
如我就加上了“永远使用中文”这一条。
化需求，也可以加在这
单
生成这些项目规则，本身也是通过Prompt+
工具调用进
串Prompt进去。这里使用CodeX的提示词进
举例。
行
行
的，本质上是工具自动帮你贴了一大
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
Generate a file named AGENTS.md that serves as a contributor guide for
▌ Your goal is to produce a clear, concise, and well-structured docume
▌ Follow the outline below, but adapt as needed — add sections if rele
▌
▌
▌
▌
▌
▌
▌ Document Requirements
▌ - Title the document "Repository Guidelines"
.
▌ - Use Markdown headings (#, ##, etc.) for structure.
▌ - Keep the document concise. 200-400 words is optimal.
▌ - Keep explanations short, direct, and specific to this repository.
▌ - Provide examples where helpful (commands, directory paths, naming
▌ - Maintain a professional, instructional tone.
▌ Recommended Sections
▌ Project Structure & Module Organization
▌ - Outline the project structure, including where the source code, te
▌ Build, Test, and Development Commands
```

## PDF 第19页

[查看原页](RAW.pdf#page=19)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
▌
▌
▌
▌
▌
▌
▌
▌
▌ - List key commands for building, testing, and running locally (e.g.
▌ - Briefly explain what each command does.
▌ Coding Style & Naming Conventions
▌ - Specify indentation rules, language-specific style preferences, an
▌ - Include any formatting or linting tools used.
▌ Testing Guidelines
▌ - Identify testing frameworks and coverage requirements.
▌ - State test naming conventions and how to run tests.
▌ Commit & Pull Request Guidelines
▌ - Summarize commit message conventions found in the project’s Git hi
▌ - Outline pull request requirements (descriptions, linked issues, sc
▌ (Optional) Add other sections if relevant, such as Security & Config
2.6.3 采用渐进式开
发，而不是大需求一口气梭哈
根据实
践经验，不推荐输出完
方
案后让 AI 一口气基于方
案
完成需求（非常小的需求除外），
需求越
大代码质量越烂。我的使用方式是，跟 AI 进
行结对编程，讨论具体的方
案是什么，这
个场景下的最佳实
践是什么，拆解需求后，人工控制每一个块的代码生成。生成之后，可以咨
询一下代码实现是否优雅，是否有
重构空间，根据需要进
修改。
行
总结来说，有
这些好处：
因为上下文窗口有限，任务粒度越小，AI 完成度越高
分步骤代码量便于做 Code Review
缺点就是，不够“自动”，比
自动化的需求
大家选
适合的方式即可。
择
较费脑子。当然，梭哈式的写法也可以用SPEC工作流，进
较为
行
拆解，或者通过 Multi Agent ，或者各种妙妙操作完成。不过这是另一个课题，
个人感觉 Vibe Coding 方式
不存在“完爆”，需要因场景而异；工具选
上也没有
绝对的高下
择
之分，我的朋友们就用什么的都
有
。最后
还是应该以结果论英雄，对于个体来说，自己用着顺
手就好。
```

## PDF 第20页

[查看原页](RAW.pdf#page=20)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
讲讲应用
上面说的都是一些准则类的经验，下面将结合具体场景，看一下如何把这些规则落地。以及帮
助大家了解一下，除了纯粹的写代码，AI 还可以帮我们做什么。
▐ 3.1 快速熟悉项目 & 自然语言检索代码
1
2
3
讲解一下这个项目的每个module都是用来做什么的，并且给出包依
关系图。
赖
我希望实现一个「什么什么」功能，需要修改的部分包括「这里」和「那
里」，我的代码放在哪个
我在找「某个某个」功能的实现，请帮我在仓库里
搜
寻，并给出它的核心具体代码位置和片段，并
▐ 3.2 PlantUML / Mermaid 文本绘图生成
这里是打算让AI帮忙画一下某个功能的前后端交互流程图，先是把接口请求顺序在浏览器里进
了截图：
行
然后把我的需求
+
我的判断（比
如图里
有一些接口实际上和这个需求并不相关）一起告诉AI：
```

## PDF 第21页

[查看原页](RAW.pdf#page=21)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
AI在进
行
了一长串分析之后，也是给出了比
结果展示（做了模糊处理）：
较准确的流程图。
▐ 3.3 问题排查
```

## PDF 第22页

[查看原页](RAW.pdf#page=22)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
这里是用真实遇到的一个问题举例子，这张图片是执
行
流程的产出结果出现了问题，大致定位到是图里的左侧节点有问题：
流程图的展示，当时遇到的问题是这个
由于对这个仓库并不熟悉，于是暂时交给AI帮忙翻代码排查：
```

## PDF 第23页

[查看原页](RAW.pdf#page=23)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text

```

## PDF 第24页

[查看原页](RAW.pdf#page=24)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
最后人工验证了一下，给出的问题分析和解决
情况下，这是一种快速进
检索和排查的
有
行
方
案确实
效手段。
非常详细且准确。在对于项目
不熟悉的
▐ 3.4 补充网页信息到上下文
Web
是相对来说比
较容易忽视，但是又非常好用的工具，可以通过@Web
的进
添加，也可以
行
直接粘链接进去。需要注意的是，需要进
行
权限认证的网页（如内网）无法直接被读取。
这里直接粘贴链接进去，让大模型帮忙总结文章内容，也可以基于它直接对任
意网页进
问
行
答。
推荐的 Coding 方式
```

## PDF 第25页

[查看原页](RAW.pdf#page=25)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
这里主要是一些实
践性的探索，目前尚未进
行
推广，原因是还没有找到一种提升大、好维护、
可移植的工具，团队同学的偏好也各不相同。当然，在这方面，团队内部已经有很多探索，目
前在积极进
行
投入和尝试。
▐ 4.1 rule 的
制定和优化
最基本应该包含你当前项目的技术栈使用，以及对应依
求的规范。
赖版本；除此之外应该包含编码明确要
注：使用一套统一的rule，需要统一使用cursor，可能不符合个人习惯。但是在使用其它 AI
编程工具时，维护一个项目规则文档，并在对话时手动添加至上下文，可以达到一样的效果。
▐ 4.2 文档
根目录下，存放以下内容
README.md
仓库门面，包含：简介、核心特性、快速开始、其它重要文件的说明和索引
CHANGELOG.md
需要发版的仓库可以考虑添加
包含：
新增功能
bug修复
breaking changes（破坏性变更）
注意事项等
ARCHITECTU
RE.md
架构复杂且需要多人协作的仓库可以考虑添加
包含：
整体架构
模块划分
核心逻辑流程图
```

## PDF 第26页

[查看原页](RAW.pdf#page=26)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
在项目根目录中建立/docs目录
目的：让团队成员快速理解项目
内容：兼顾实用性、
准确性、易维护性
可以包含以下内容文件
高效协作
错误码体系
错误码格式
错误码分类
详细场景
异常处理指南
可重试/不可重试
异常抛出原则
日志打印要求
常见异常案例
常用工具类
注：需根据项目内容修改，以上仅为个人推荐
、
▐ 4.3 注释和命名
1. 方法、参数等注释，尽量保证语义清晰、内容完整；
2. 可以考虑添加调用方的使用场景；
3. 适当添加
内注释，明确每个分支的场景和期望处理方式；
行
4. 命名需要清晰，无歧义；
5. AI 生成量 > 80%的文件，建议使用@author AI Assistant，注明是AI生成，便于维护和
统计。
▐ 4.4 安全
合规问题
需要根据公司规定，合规使用。
▐ 4.5 推广方式
这里是在团队内部创建了一个代码仓库，作一下示例，主要维护这些内容（仍在优化中）：
范围确定
核心代码库梳理
M
区分给人看的文档（详细）和给LL
看（核心内容）的文档
```

## PDF 第27页

[查看原页](RAW.pdf#page=27)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Docs资
产
内容指定：markdown文档内容by project定制
生产：初始化文档，暂定为各应用owner
Project R
ule
内容指定：rule内容by project定制，产出为markdown；放在仓库中
生产：初始化project rule的md文档，暂定为各应用owner
User R
ule
内容指定：产出通用部分，如团队规约，保证内容简洁；不放在仓库中
同步方式：（暂定）统一维护在一个新增仓库中，各应用中可以使用脚
步到本地
本进
一键同
行
参考文献
《Cursor 实战万字经验分享，与 AI 编码的
https://www.cnblogs.com/echolun/p/18965624
深度思考》：
《Claude Code（及 cursor） 内部工作原理窥探》：
https://www.su
perlinear.academy/c/share-your-projects/claude-code-cursor
团队介绍
本文作者库啵，来自淘天集团-用户&内容技术团队。本团队是双边电商平台的核心驱动力之
一，通过精细化运营、数据智能和技术创
新，实现用户增长与内容价值最大化。同时我们也在
持续跟进前沿技术，探索如何让技术在真实业务场景中落地，形成可复用的增长方法论与工程
实
践。
¤ 拓展阅读 ¤
3DXR技术 | 终端技术 | 音视频技术
服务端技术 | 技术质量 | 数据算法
```

## PDF 第28页

[查看原页](RAW.pdf#page=28)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
大淘宝技术
大淘宝技术官方账号
967篇原创内容
公众号
阅读 1.5万
```

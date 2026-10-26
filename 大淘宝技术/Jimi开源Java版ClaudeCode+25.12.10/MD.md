# Jimi：打造Java程序员专属的开源ClaudeCode：PDF文本转写

> 这是原始PDF文本层转写，不是学习摘要。页码为PDF物理页序；图表、代码版面和图片文字不能完整表达在此文本层。已查看图像的内容和质量问题见AI学习笔记及META.json。

[原文PDF](RAW.pdf) · [AI学习笔记](AI_Jimi开源Java版ClaudeCode.md) · [处理与质量记录](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Jimi：打造Java程序员专属的开源ClaudeCode
原创
淘特用户技术团队 2025年12月10日 01:50 浙江
大淘宝技术 9人
今年最火的技术是什么，AI；AI中最火的是什么，Agent；Agent中最火的是什么，AI-
Coding；AI-Coding中最火的是什 么，ClaudeCode。最 近看 了 蚂 蚁 关
于最 受 欢 迎的
135个AI开源项目统计，发现曾经作为移动互联网时代的编程王者Java，在AI时代已经
彻彻底底被边缘化了。作为十年Java老鸟，想为Java开源生态贡献绵薄之力，于是便
有
了本文：https://github.com/Leavesfly/Jimi。
引言：为什么Java程序员需要自己的AI代理？
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
在AI辅助编程的浪潮中，Cursor、Claude Code等工具为开
发
者带来了革命性的体验。但对
于Java生态的开
发
者来说，我们面临着一些独特的挑战：
🔧 技术栈割裂：主流AI工具多用Python或ts实现，与Java项目集成困难
📚 企业级需求：需要支持Spring Boot、Maven、
微服务等企业级框架
🔐 私有
化部署：企业对代码安全有严格要求，需要可控的本地方
案
🎯 深度定制：希望能深
入理解并定制AI代理的
为逻辑
行
Jimi 项目的诞生正是为了解决这些痛点——用纯Java技术栈，构建一个功能完整、可扩展
企业级
的AI智能代理系
统。
、
▐ Jimi的核心价值
🎓 教育友好：清晰的代码架构，完整的中文注释，让每一
行
🏢 企业级
设计：基于Spring Boot 3.2.5，支持响应式编程，生产
代码都能成为学习资源；
级质量保证；
🔌 开放生态：支持MCP协议，可集成各类外部工具和服务；
🧩 极致模块化：像搭乐高一样组合功能，每个模块职责明确，易于扩展；
💡 知
识注入：灵活的Skills系
统，让AI可以按需获取领域专业知
识。
架构之道——分层是银弹
▐ 从"积木"的角度理解Jimi
如果要建造一座智能大厦，我们需要什么？首先是坚实的地基（基础设施），然后是稳定的骨
架（核心引擎），再是灵活的功能模块（Agent和工具），最后是友好的交互界面（UI）。
Jimi的架构设计正是遵循了这样的思路：
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
这种分层设计带来了显著的优势：
🔒 底层稳定：消息总线和执
行
引擎为整个系
🎯 中层灵活：Agent和工具以及Skills系
统提供丰
统提供可靠基础
富的功能组
🚀 上层开放：支持多种LLM、自定义Agent、外部工具集成
件
▐ 核心模块一览
Jimi共包含8个核心功能域，每个域都
有明确的职责边界：
功能域 核心模块 主要职责 设计亮点
核心引擎
Agent
系
统
工具系
统
LLM集成
Skills系
统
消息总线
会话管理
JimiEngine
AgentExecutor
AgentRegistry
AgentSpecLoader
ToolRegistry
ToolRegistryFactory
LLMFactory
ChatProvider
SkillMatcher
SkillProvider
Wire
WireMessage
Sessi
on
Context
UI交互 ShellUI
OutputFormatter
任务执
与调度委托模式，单一职责
行
Agent管理与加载 YAML配置化，模板渲
工具注册与执
行 Spring集成，插件化
多模型支持Caffeine缓存，流式响应
知
识智能注入
关键词匹配，自动激活
件解耦
组
通信 响应式流，事件驱动
上下文持久化 检查点机制，智能压缩
命令
行
界面 JLine3，彩色输出
染
核心引擎——Agent执
主逻辑
行
▐ 设计理念：委托与解耦
在早期版本中，JimiEngine承担了过多的职责（执
行
代码复杂度高
、难以测试。经过重构，我们采用了委托模式：
循环、工具调用、上下文管理等），导致
JimiEngine：作为Engine接口的实现，专注于
AgentExecutor：承担主循环调度和执
行
组
件装
配和协调
逻辑，是真正的"引擎心脏
"
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 核心代码解析
让我们深
入AgentExecutor的核心逻辑，看看它是如何协调各个组
件的：
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
@Slf4j
public class AgentExecutor {
private final Agent agent;
private final Runtime runtime;
private final Context context;
private final Wire wire;
private final ToolRegistry toolRegistry;
private final Compaction compaction;
private final SkillMatcher skillMatcher;
private final SkillProvider skillProvider;
/**
* 执
行
Agent 任务的入口方法
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
53
54
55
56
57
58
59
60
*/
public Mono<Void> execute(List<ContentPart> userInput) {
return Mono.defer(() -> {
// 1.
创建检查点 0（初始状态）
return context.checkpoint(false)
// 2. 添加用户消息到上下文
.flatMap(checkpointId -> context.appendMessage(Mes
// 3.
启动Agent主循环
.then(agentLoop())
.doOnSuccess(v -> log.info("Agent execution comple
.doOnError(e -> log.error("Agent execution failed"
});
}
/**
* Agent 主循环的
单步执
行
*/
private Mono<Void> agentLoopStep(int stepNo) {
// 检查是否超过最大步数限制
int maxSteps = runtime.getConfig().getLoopControl().getMaxStep
if (stepNo > maxSteps) {
return Mono.error(new MaxStepsReachedException(maxSteps));
}
// 发送步骤开始消息（通过Wire通知UI）
wire.send(new StepBegin(stepNo, isSubagent, agentName));
return Mono.defer(() -> {
// 1. 检查上下文是否超限，必要时触发
return checkAndCompactContext()
// 2.
创建步骤检查点
压缩
.then(context.checkpoint(true))
// 3. 匹配并注入Skills（智能知
识注入）
.then(matchAndInjectSkills(stepNo))
// 4. 执
行单步：调用LLM并处理响应
.then(step())
.flatMap(finished -> {
if (finished) {
// LLM返回纯文本，没有
工具调用，循环结束
log.info("Agent loop finished at step {}"
return Mono.empty();
,
} else {
// 有
工具调用，继续下一步
return agentLoopStep(stepNo + 1);
}
});
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
61
62
63
});
}
}
设计亮点：
1. 响应式编程：使用Reactor的Mono，天然支持异步非阻塞
2. 检查点机制：每个步骤创建检查点，支持回滚和错误恢复
3. 消息总线解耦：通过Wire发送事件，UI层无需直接
耦合
4. 智能循环控制：支持最大步数限制
、连续无工具调用检测
▐ 流式响应处理的设计
LLM的流式响应（Streaming）是提升用户体验的关键。Jimi采用了累加器模式来处理流式数
据：
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
/**
* 流式累加器：用于
*/
组
装完整的Assistant消息
private static class StreamAccumulator {
StringBuilder contentBuilder = new StringBuilder(); List<ToolCall> toolCalls = new ArrayList<>(); // 累积文本内
// 累积工具调
ChatCompletionResult.Usage usage; // Token使用
// 用于临时存储正在构建的工具调用
String currentToolCallId;
String currentFunctionName;
StringBuilder currentArguments = new StringBuilder();
}
/**
* 处理流式数据块
*/
private StreamAccumulator processStreamChunk(StreamAccumulator acc, Ch
switch (chunk.getType()) {
case CONTENT:
// 文本内容：实时累加并通过Wire发送到UI
String contentDelta = chunk.getContentDelta();
acc.contentBuilder.append(contentDelta);
wire.send(new ContentPartMessage(new TextPart(contentDelta
break;
case TOOL
CALL:
_
// 工具调用：逐块累积参数JSON
handleToolCallChunk(acc, chunk);
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
29
30
31
32
33
34
35
36
37
break;
case DONE:
// 流结束：记录Token使用情况
acc.usage = chunk.getUsage();
break;
}
return acc;
}
技术亮点：
实时反馈：每个内容片段立即发送到UI，用户感知
延迟极低
容错机制：处理LLM可能先发送arguments、
后
发送id的异常情况
临时ID策略：当收到参数但没有ID时，创建临时ID确保数据不丢失
Agent
系
统——SubAgent的分工协作
▐ 多Agent协作架构
Jimi支持多种专业化Agent，每个Agent都
有明确的职责边界：
▐ Agent的配置化设计
Jimi采用YAML配置
agent.yaml示例：
+
Markdown模板的方式定义Agent，极大提升了可定制性：
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
name: "Code Agent"
description: "专业的代码实现Agent"
model: null # 继承默认模型
# 可以委托的子Agent
subagents:
- review
- test
# 可用工具列表
tools:
- read
file
_
- write
to
file
_
_
- str
_
replace
_
file
- patch
file
_
- bash
- glob
- grep
- think
# 排除的工具（从标准工具集中移除）
exclude
tools:
_
- fetch
url
_
- set
todo
list
_
_
# 系
统提示词参数（用于模板渲
染）
system
_prompt
_
args:
CODING
_
STYLE: "遵循阿里巴巴Java开
JAVA
VERSION: "17"
_
发手册"
system_prompt.md模板：
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
# 角色定位
你是一位经验丰
# 工作环境
富的Java高级
- 当前时间: ${JIMI
NOW}
_
- 工作目录: ${JIMI
WORK
_
_
DIR}
- Java版本: ${JAVA
_
- 编码规范: ${CODING
_
VERSION}
STYLE}
# 核心能力
1. 根据设计文档完成代码实现
2.
编写符合规范的注释和文档
3. 进
行
代码重构和优化
4. 处理异常情况和边界条件
# 工作流程
1. 仔细阅读需求和设计文档
2. 分析现有代码结构
3. 实现新功能或修复Bug
4.
编写必要的注释
工程师，专注于高质量代码实现。
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
18 5.
委托Review Agent进
行
代码审查
▐ Agent加载与渲
染机制
AgentRegistry 负责Agent的加载和管理：
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
32
33
34
35
36
37
@Service
public class AgentRegistry {
@Autowired
private AgentSpecLoader specLoader;
/**
* 加载Agent实例，支持模板渲
*/
染
public Mono<Agent> loadAgent(Path agentFile, Runtime runtime) {
return loadAgentSpec(agentFile).flatMap(spec -> {
// 渲
系
统提示词模板
String systemPrompt = renderSystemPrompt(
spec.getSystemPromptPath(),
spec.getSystemPromptArgs(),
runtime.getBuiltinArgs()
染
);
// 构建Agent实例
Agent agent = Agent.builder()
.name(spec.getName())
.systemPrompt(systemPrompt)
.model(spec.getModel())
.tools(processedTools)
.build();
return Mono.just(agent);
});
}
/**
* 渲
*/
染
系
统提示词（使用Apache Commons Text）
private String renderSystemPrompt(Path promptPath, Map<String, Str
BuiltinSystemPromptArgs builtinAr
String template = Files.readString(promptPath);
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
// 准备替换参数（内置参数 + 自定义
参数）
Map<String, String> substitutionMap = new HashMap<>();
substitutionMap.put("JIMI
NOW"
_
, builtinArgs.getJimiNow());
substitutionMap.put("JIMI
WORK
DIR"
_
_
, builtinArgs.getJimiWorkDi
if (args != null) {
substitutionMap.putAll(args);
}
// 执
字符串替换
行
StringSubstitutor substitutor = new StringSubstitutor(substitu
return substitutor.replace(template);
}
}
设计优势：
配置与代码分离：修改Agent
行
为无需修改代码；
模板化：支持参数替换，动态注入上下文信息；
可扩展：新增Agent只需添加配置文件。
工具系
统——能力的扩展
▐ 工具注册与执
架构
行
Jimi的工具系
统采用注册表模式，支持工具的动态注册和执
：
行
```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 工具的标准
接口设计
所有
工具都
实现统一的
Tool接口：
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
public interface Tool<P> {
/**
* 工具名称（对应LLM function calling的name）
*/
String getName();
/**
* 工具描述（告诉LLM这个工具的用途）
*/
String getDescription();
/**
* 参数类型（用于JSON Schema生成）
*/
Class<P> getParamsType();
/**
* 执
工具
行
*/
Mono<ToolResult> execute(P params);
}
以
ReadFile工具为例：
1
2
3
4
@Component
@Scope("prototype") // 每次获取时创建新实例
public class ReadFile extends AbstractTool<ReadFile.Params> {
```

## PDF 第12页

[查看原页](RAW.pdf#page=12)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
@Data
public static class Params {
@JsonProperty(required = true)
@JsonPropertyDescription("要读取的文件路径（相对或绝对路径）")
private String path;
@JsonPropertyDescription("起始
private Integer startLine;
号（从1开始）")
行
@JsonPropertyDescription("结束
private Integer endLine;
号")
行
}
@Override
protected Mono<ToolResult> executeInternal(Params params) {
return Mono.fromCallable(() -> {
Path filePath = resolveWorkPath(params.getPath());
// 验证文件存在且可读
if (!Files.exists(filePath)) {
return ToolResult.error("文件
不存在: " + params.getPath(
}
// 读取文件内容
List<String> lines = Files.readAllLines(filePath);
// 处理
范围
行
if (params.getStartLine() != null || params.getEndLine() !
int start = params.getStartLine() != null ? params.get
int end = params.getEndLine() != null ? params.getEndL
lines = lines.subList(Math.max(0, start), Math.min(lin
}
return ToolResult.success()
.withOutput(String.join("\n"
.withMessage("成功读取文件");
, lines))
});
}
}
设计亮点：
Spring集成：工具作为Spring Bean，自动依
注入；
赖
原型作用域：每次获取新实例，避免状态污
染；
审批机制：敏感工具（如文件写入
、Shell执
行
）需要审批；
响应式设计：返回Mono<ToolResult>，支持异步执
。
行
```

## PDF 第13页

[查看原页](RAW.pdf#page=13)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
LLM集成——多模型的统一抽象
▐ LLM抽象层设计
Jimi支持多种LLM提供商（OpenAI、Kimi
ChatProvider接口进
抽象：
行
、
DeepSeek、
Qwen、Ollama等），通过统一的
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
public interface ChatProvider {
/**
* 流式生成聊天完成
*/
Flux<ChatCompletionChunk> generateStream(
String systemPrompt,
List<Message> messages,
List<Object> toolSchemas
);
/**
* 获取模型名称
*/
String getModelName();
}
▐ LLM工厂与缓存机制
LLMFactory 使用Caffeine高性能缓存来管理LLM实例：
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
@Service
public class LLMFactory {
/**
*/
* LLM实例缓存（Caffeine）
private final Cache<String, LLM> llmCache;
public LLMFactory(JimiConfig config, ObjectMapper objectMapper) {
// 初始化Caffeine缓存
this.llmCache = Caffeine.newBuilder()
```

## PDF 第14页

[查看原页](RAW.pdf#page=14)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
32
33
34
35
.maximumSize(10) // 最多缓存10个模型
.expireAfterAccess(30, TimeUnit.MINUTES) // 30分钟未使用则过
.recordStats() // 记录缓存统计
.build();
}
/**
* 获取或创建LLM实例
*/
public LLM getOrCreateLLM(String modelName) {
return llmCache.get(modelName, key -> createLLM(key));
}
/**
*/
* 解析API Key（优先使用环境变量）
private String resolveApiKey(LLMProviderConfig providerConfig) {
// 构建环境变量名称：{PROVIDER
_
TYPE}_
API
KEY
_
String envVarName = providerConfig.getType().toString().toUppe
String envApiKey = System.getenv(envVarName);
return envApiKey != null ? envApiKey : providerConfig.getApiKe
}
}
设计优势：
缓存复用：避免重复创建LLM实例，提升性能；
环境变量覆盖：支持通过环境变量配置API Key，提升安全性；
Fail-fast验证：启动时验证配置，避免运
时错误。
行
Skills系
统——领域知
识的动态注入
▐ Skills系
统的设计哲学
Skills（技能包）解决了一个关键问题：如何让AI在特定领域任务中表现得更专业？
传统方法是在系
统提示词中硬编码所有知
识，但这会导致：
🚫 上下文过长：大量无关知
识占用Token
🚫 维护困难：修改知
🚫
缺乏共享：团队间无法复用知
识需要重新部署
识
Skills系
统的解决
方
案：
✅
按需激活：根据用户输
入自动匹配相关知
识
```

## PDF 第15页

[查看原页](RAW.pdf#page=15)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
✅ 模块化管理：每个Skill独立配置，易于维护
✅ 团队共享：支持全局和项目级Skill
✅
高性能：Caffeine缓存提升匹配效率
▐ Skill配置格式
每个Skill由一个 skill.yaml文件定义：
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
name: "Java Code Review Checklist"
description: "Java代码审查的完整检查清单和最佳实
scope: global
# 触发词（用于智能匹配）
triggers:
- code review
- 代码审查
- 代码质量
- quality check
# 技能内容（Markdown格式）
content: |
## Java代码审查清单
践"
### 1. 代码规范
- [ ] 命名符合规范（驼峰、常量大写等）
- [ ] 缩进和格式一致
```

## PDF 第16页

[查看原页](RAW.pdf#page=16)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
- [ ] 注释清晰且必要
### 2. 设计原则
- [ ] 遵循SOLID原则
- [ ] 单一职责原则
- [ ] 方法长度合理（建议
<50
行
）
### 3. 异常处理
- [ ] 异常不被吞掉
- [ ] 使用合适的异常类型
- [ ] 资源正确关
闭
▐ 智能匹配
SkillMatcher 实现了基于关键词的智能匹配：
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
@Service
public class SkillMatcher {
private Cache<String, List<SkillSpec>> matchCache;
/**
* 匹配用户输
*/
入，返回相关
的Skills
public List<SkillSpec> matchFromInput(List<ContentPart> userInput)
String inputText = extractText(userInput);
// 尝试从缓存获取
String cacheKey = String.valueOf(inputText.hashCode());
List<SkillSpec> cachedResult = matchCache.getIfPresent(cacheKe
if (cachedResult != null) {
return cachedResult;
}
// 执
行实际匹配
List<SkillSpec> matchedSkills = performMatch(inputText);
// 缓存结果
matchCache.put(cacheKey, matchedSkills);
return matchedSkills;
}
/**
```

## PDF 第17页

[查看原页](RAW.pdf#page=17)

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
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
* 执
匹配逻辑
行
*/
private List<SkillSpec> performMatch(String inputText) {
// 1. 提取
关键词
Set<String> keywords = extractKeywords(inputText);
// 2. 从注册表中查找候选Skills
List<SkillSpec> candidateSkills = skillRegistry.findByTriggers
// 3. 计算匹配得分并排序
return candidateSkills.stream()
.map(skill -> new ScoredSkill(skill, calculateScore(skill,
.filter(scored -> scored.score >= scoreThreshold)
.sorted(Comparator.comparingInt(ScoredSkill::getScore).rev
.limit(maxSkills)
.map(ScoredSkill::getSkill)
.collect(Collectors.toList());
}
/**
* 计算匹配得分
*
* 计分策略：
* - 触发词精确匹配：+50分
* - 触发词部分匹配：+30分
* - 名称匹配：+40分
* -
关键词在描述中出现：+10分
*/
private int calculateScore(SkillSpec skill, Set<String> keywords,
int score = 0;
// 检查触发词匹配
for (String trigger : skill.getTriggers()) {
if (keywords.contains(trigger.toLowerCase()) ||
fullText.toLowerCase().contains(trigger.toLowerCase())
score += 50;
}
}
return Math.min(score, 100);
}
}
▐ 知
识注入
```

## PDF 第18页

[查看原页](RAW.pdf#page=18)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
SkillProvider 负责将匹配的Skills注入到上下文：
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
@Service
public class SkillProvider {
/**
* 注入Skills到上下文
*/
public Mono<Void> injectSkills(Context context, List<SkillSpec> sk
// 过滤已激活的Skills
List<SkillSpec> newSkills = skills.stream()
.filter(skill -> !context.getActiveSkills().contains(skill
.collect(Collectors.toList());
if (newSkills.isEmpty()) {
return Mono.empty();
}
// 格式化Skills为系
统消息
String skillsContent = formatSkills(newSkills);
Message skillsMessage = Message.system(skillsContent);
// 添加到上下文并记录激活的Skills
return context.appendMessage(skillsMessage)
.then(context.addActiveSkills(newSkills));
}
/**
*/
* 格式化Skills为Markdown文本
private String formatSkills(List<SkillSpec> skills) {
StringBuilder sb = new StringBuilder();
sb.append("<system type=\"skills\">\n\n");
sb.append("以下技能包已根据当前任务自动激活，请在执
行
任务时遵循这些专业指
for (int i = 0; i < skills.size(); i++) {
SkillSpec skill = skills.get(i);
sb.append("### ").append(i + 1).append("
.
sb.append(skill.getContent()).append("\n\n");
if (i < skills.size() - 1) {
sb.append("
---\n\n");
}
}
sb.append("</system>");
").append(skill.
```

## PDF 第19页

[查看原页](RAW.pdf#page=19)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
44
45
46
return sb.toString();
}
}
Skills系
统的优势：
智能激活：无需手动选
，系
统自动匹配最相关
的知
择
上下文优化：只注入必要的知
识，节省Token；
团队协作：支持共享Skills库，团队经验沉淀；
持续改进：可随时更新Skills内容，无需修改代码。
识；
MCP协议集成——连接外部世界
▐ MCP协议简介
MCP（Model Context Protocol）是一个标准化的AI工具调用协议，允许AI模型与外部服务
进
行结构化通信。Jimi通过MCP集成，可以：
🗄 访问数据库：执
行SQL查询、数据分析
📁 操作文件系
统：跨平台文件管理
🔗 调用Git服务：查看提交历史、分支管理
🌐 集成GitHub：创建Issue、管理PR
▐ MCP客户端架构
▐ MCP客户端接口
```

## PDF 第20页

[查看原页](RAW.pdf#page=20)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
/**
* JSON-RPC客户端接口
*/
public interface JsonRpcClient extends AutoCloseable {
/**
* 初始化连接
*/
MCPSchema.InitializeResult initialize() throws Exception;
/**
* 获取工具列表
*/
MCPSchema.ListToolsResult listTools() throws Exception;
/**
* 调用工具
*/
MCPSchema.CallToolResult callTool(String toolName, Map<String, Obj
throws Exception;
}
HTTP实现示例：
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
public class HttpJsonRpcClient implements JsonRpcClient {
private final WebClient webClient;
@Override
public MCPSchema.CallToolResult callTool(String toolName, Map<Strin
throws Exception {
JsonRpcRequest request = JsonRpcRequest.builder()
.method("tools/call")
.params(Map.of(
"name"
, toolName,
"arguments"
, arguments
))
.build();
return sendRequest(request, MCPSchema.CallToolResult.class);
}
}
```

## PDF 第21页

[查看原页](RAW.pdf#page=21)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ MCP配置示例
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
{
"name": "database-server"
,
"description": "PostgreSQL数据库查询服务"
,
"type": "http"
,
"config": {
"url": "http://localhost:8080/mcp"
,
"headers": {
"Authorization": "Bearer ${DB
API
_
_
KEY}"
}
}
}
消息总线Wire——组
件解耦
▐ Wire的设计理念
Wire消息总线
通过发布-订阅模式
实现组
件解耦：
▐ Wire接口与实现
1
2
3
4
5
/**
* Wire消息总线
接口
*/
public interface Wire {
void send(WireMessage message);
```

## PDF 第22页

[查看原页](RAW.pdf#page=22)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
Flux<WireMessage> asFlux();
void complete();
}
/**
*/
* Wire实现（基于Reactor的Sinks）
public class WireImpl implements Wire {
private final Sinks.Many<WireMessage> sink;
public WireImpl() {
// 使用Multicast支持多订阅者
this.sink = Sinks.many().multicast().onBackpressureBuffer();
}
@Override
public void send(WireMessage message) {
sink.tryEmitNext(message);
}
@Override
public Flux<WireMessage> asFlux() {
return sink.asFlux();
}
}
▐ 消息类型体系
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
// 步骤开始消息
public class StepBegin implements WireMessage {
private int stepNumber;
private boolean isSubagent;
private String agentName;
}
// 内容部分消息（LLM流式
输出）
public class ContentPartMessage implements WireMessage {
private ContentPart contentPart;
}
// 工具调用消息
public class ToolCallMessage implements WireMessage {
private ToolCall toolCall;
}
// Skills激活消息
```

## PDF 第23页

[查看原页](RAW.pdf#page=23)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
16
17
18
19
public class SkillsActivated implements WireMessage {
private List<String> skillNames;
private int count;
}
▐ UI层的消息处理
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
public class ShellUI {
private void subscribeWire() {
wireSubscription = wire.asFlux()
.subscribe(this::handleWireMessage);
}
private void handleWireMessage(WireMessage message) {
if (message instanceof StepBegin stepBegin) {
printStatus("🤔 Step " + stepBegin.getStepNumber() + "
- T
} else if (message instanceof ContentPartMessage contentMsg) {
// 实时打印LLM输出
printAssistantText(contentMsg.getContentPart().getText());
} else if (message instanceof ToolCallMessage toolCallMsg) {
// 显示工具调用
toolVisualization.onToolCallStart(toolCallMsg.getToolCall(
} else if (message instanceof SkillsActivated skillsMsg) {
printInfo("💡 激活Skills: " + String.join("
"
,
, skillsMsg.g
}
}
}
使用示例与最佳实
践
▐ 基本使用流程
1 # 1.
启动Jimi
```

## PDF 第24页

[查看原页](RAW.pdf#page=24)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
2
3
4
5
6
7
8
9
./scripts/start.sh
# 2. 查看
帮助
/help
# 3.
开始对话
请帮我分析src/main/java目录下的代码结构
# 4. 使用专业Agent
/agent code
请帮我实现一个用户注册功能
▐ 高级使用技巧
1. 配置Skills功能
编辑 applicati
on.yml：
1
2
3
4
5
6
7
jimi:
skill:
enabled: true
auto-match: true
matching:
score-threshold: 30
max-matched-skills: 5
2. 使用YOLO模式（自动批准）
1./scripts/start.sh --yolo
3. 指定工作目录
1./scripts/start.sh --work-dir /path/to/your/project
4. 会话恢复
1
2
3
4
# 恢复上次会话
./scripts/start.sh --resume
# 使用指定会话
./scripts/start.sh --session my-project
▐ 开
发自定义Agent
```

## PDF 第25页

[查看原页](RAW.pdf#page=25)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
创建 agents/my-agent/agent.yaml ：
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
name: "My Custom Agent"
description: "我的专属Agent"
subagents:
- code
- review
tools:
- read
file
_
- write
to
file
_
_
- bash
system
_prompt
_
args:
MY
CUSTOM
_
_
PARAM: "自定义
参数值"
创建 agents/my-agent/system_prompt.md ：
1
2
3
启动时使用：
你是一位专业的${MY
CUSTOM
_
_
PARAM}助手。
当前工作目录：${JIMI
WORK
_
_
DIR}
...
1./scripts/start.sh --agent my-agent
▐ 开
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
发自定义
工具
@Component
@Scope("prototype")
public class MyCustomTool extends AbstractTool<MyCustomTool.Params> {
@Data
public static class Params {
@JsonProperty(required = true)
@JsonPropertyDescription("参数描述")
private String param1;
}
@Override
public String getName() {
return "my_
custom
_
tool";
}
```

## PDF 第26页

[查看原页](RAW.pdf#page=26)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
@Override
public String getDescription() {
return "我的自定义
工具";
}
@Override
protected Mono<ToolResult> executeInternal(Params params) {
return Mono.fromCallable(() -> {
// 工具逻辑实现
return ToolResult.success()
.withOutput("执
.withMessage("执
行结果")
行
成功");
});
}
}
在 ToolRegistryFactory 中注册：
1
2
3
4
5
public ToolRegistry createStandardRegistry(...) {
// ... existing code
registry.register(createMyCustomTool());
return registry;
}
技术架构总结与展望
▐ 核心设计模式总结
设计模式 应用位置 优势
委托模式 JimiEngine → AgentExecutor 职责分离，易于测试
工厂模式 LLMFactory, ToolRegistryFactory 对象创建与使用解耦
策略模式
ChatProvider多
实现支持多种LLM提供商
注册表模式 ToolRegistry, AgentRegistry 动态注册和查找
观察者模式 Wire消息总线
件解耦
组
通信
模板方法 AbstractTool 复用公共逻辑
原型模式 Spring Prototype Bean 避免状态污
染
```

## PDF 第27页

[查看原页](RAW.pdf#page=27)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 技术栈亮点
Spring Boot 3.2.5：现代企业级框架，依
注入，配置管理；
赖
Project Reactor：响应式编程，异步非阻塞，流式处理；
Caffeine：高性能缓存，LRU淘汰，统计功能；
JLine 3：强大的终端交互库，自动补全，语法高亮；
Jackson：JSON序列化/反序列化，支持注解；
Apache Commons Text：字符串替换，模板渲
染。
▐ 性能优化策略
1.多层缓存：
LLM实例缓存（Caffeine）
Skills匹配结果缓存
Agent规范缓存
2.并发执
：
行
多个工具调用并发执
流式响应实时推送
3.上下文压缩：
自动检测Token超限
智能压缩历史消息
4.资源管理：
行
Spring Bean作用域控
AutoCloseable资源自动释放
（Flux.merge）
▐ 未来发
展方向
短期计划
🔥
增强Skills系
统：
支持模板变量和动态内容生成
实现基于上下文的动态Skills匹配
支持Skills间的依
关系
赖
🚀 扩展工具生态：
集成更多MCP服务（GitHub, Jira, Slack等）
开
发代码分析工具（AST解析、依
分析）
赖
支持数据库Schema分析
💡 优化用户体验：
```

## PDF 第28页

[查看原页](RAW.pdf#page=28)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Web UI界面（可选）
IDE插件（IntelliJ IDEA, VS Code）
更丰
富的可视化输出
中期计划
🧠 智能化增强：
引入RAG（检索增强生成）
支持项目知
识库自动构建
上下文智能摘要
🌐 分布式支持：
多Agent并
行
分布式工具执
协作
行
云端LLM服务集成
📊 可观测性：
性能监控和指标采集
执
过程可视化
行
成本分析和优化建议
长
期愿景
🎯 企业级增强：
多租户支持
权限和审计系
统
企业知
识库集成
🔐 安全性强化：
代码安全扫描
敏感信息检测
合规性检查
🌟 生态建设：
插件市场
Skills共享平台
社区贡献机制
结语：开源的力量，Java的未来
Jimi项目
们证明了：
✅ Java完全可以胜任AI应用开
不仅仅是一个AI代理工具，更是一次对"用Java做AI"的
深度探索。通过这个项目，我
发：响应式编程、流式处理、
高性能缓存，一应俱全
```

## PDF 第29页

[查看原页](RAW.pdf#page=29)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
✅ 企业级
设计可以与AI完美结合：Spring Boot的依
赖
注入
应用提供坚实基础
✅ 模块化架构让AI系
统更易维护：清晰的职责边界、可插拔的
组
✅
开源社区的力量无穷：通过分享代码、文档和经验，让更多开
发
、
配置管理、测试框架，为AI
件设计，降
者受益
低了复杂度
给Java开
发
者的建议
如果你也对AI感兴趣，不妨从Jimi
开始：
1. Clone代码，深
入阅读：每个模块都
有
详细的注释
2. 运
行测试，理解流程：单元测试覆盖核心逻辑
3. 尝试扩展，实
践
学习：自定义Agent、工具、Skills
4. 参与贡献，共同成长：提交PR，分享经验
项目信息
GitHub仓库：https://github.com/Leavesfly/Jimi
文档中心：项目根目录docs
技术讨论：GitHub D
iscussi
ons
问题反馈：GitHub Issues
致谢
感谢以下开源项目为Jimi提供的灵感和支持：
Spring Boot - 企业级应用框架
Project Reactor - 响应式编程库
Caffeine - 高性能缓存
JLine - 终端交互库
Model Context Protocol - AI工具标准协议
团队介绍
本文作者
山泽，来自淘天集团-淘特用户技术团队。本团队主要负责淘宝
研发工作，包含：搜
索推荐、互动游戏、导购、
景，包含AI代码生成以及用Agent将电商各种场景重新做一遍的机会。
行
业&淘特C端链路的
交易等基础服务，在这里可以探索更多AI场
寻 找志 趣 相投 的您 ， 详 情 请 点 这里。https://talent.taotian.com/off-campus/positi
on-
detail?lang=zh&positi
onId=100001220005
```

## PDF 第30页

[查看原页](RAW.pdf#page=30)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
¤ 拓展阅读 ¤
3DXR技术 | 终端技术 | 音视频技术
服务端技术 | 技术质量 | 数据算法
大淘宝技术
大淘宝技术官方账号
967篇原创内容
公众号
阅读 8394
留言
写留言
还没有
留言，来写首评
```

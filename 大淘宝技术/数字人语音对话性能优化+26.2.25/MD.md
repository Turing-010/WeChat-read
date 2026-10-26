# AI真人数字人语音对话性能优化实践总结：PDF文本转写

> 这是原始PDF文本层转写，不是学习摘要。页码为PDF物理页序；图表、代码版面和图片文字不能完整表达在此文本层。已查看图像的内容和质量问题见AI学习笔记及META.json。

[原文PDF](RAW.pdf) · [AI学习笔记](AI_数字人语音对话性能优化.md) · [处理与质量记录](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
AI真人数字人语音对话性能优化实
践总结
原创
Meta技术团队 2026年2月25日 01:37 浙江
大淘宝技术 3人
本文总结了为解决 AI 数字人导购对话中的回答延迟感而进
行
的性能优化实
践。初始的对
话链路因 ASR
、LLM 和 TTS 的串
行叠加，导致平
均端到端延迟高达
5.64 秒
。为实现
数据驱动的优化，首先搭建了一套覆盖全链路的高精度性能监控体系作为基础。核心解
决
方
案是集成 Qwen Omni 一体化模型，旨在通过流式传输音频和文本来减少中间环
节，同时在客户端设计了音频窗口缓冲机制以确保嘴
型同步。最终，通过采用 ASR 后的
文本输
入 Omni 的优化方
案，系
统的平
均端到端延迟从 5644 毫秒成功降
至 1323 毫
秒，取得了 76.6% 的显著提升，并大幅改善了系
统的稳定性。
问题背景与现状
在Visi
onPro 淘宝旗舰店中，你可以与一个逼真的真人AI数字人进
行
对话，他可以为你解答店
铺的问题、商品的问题等等，能带来更好的互动体验和全
新的智能购物感受。但是，在之前与
AI数字人导购聊天的过程中，交互提示词在2万字以上的情况下，会有明显的回答延迟感。
我们经过多
组测试，得到平
的基线数据如下（人设提示词2万字
+
，每组10个会话）：
端到端延迟（ASR结束到语音首次播放）平
均 5.64 s，并且稳定性不佳；
ASR
平
均 2.28 s、LLM 首 Token 平
均 2.26 s、TTS 平
均 2.03 s，各阶段叠加造成明
显"思考时间"，用户体感明显"卡壳"；
对于用户而言，最关
心的是问完问题之后，多久能够得到数字人的回复。因此，我们核心需要
优化ASR结束到最终数字人回答的耗时。在本文中，我们完整的总结了将AI数字人语音对话端
到端链路延迟从5.64秒优化到1.32秒
的完整方
案与实战经验。
均
最终对话效果如下：
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
00:56
00:56
解决
方
案调研
在优化之前，我们先回顾一下目前 AI 数字人对话链路，它通常采用 ASR → LLM → TTS &
A2BS
的三段式串
行结构：
这种架构的痛点在于：每个环节都必须等待上一个环节完全结束（或至少积累一定 buffer）才
能开始，导致延迟逐级叠加。针对这个"5 s 以上首句延迟"的痛点，我们在多个方向和不同阶
段做过可
性评估：
行
ASR（语音转文字）优化：若直接换成"一体模型(Audi
o2Audi
o)"可减去单独的ASR环节，但
会丢字幕需求，因此保留 ASR/VAD。
LLM（大模型回复）优化：尝试对比 Qwen-Max / Omni / Plus，多维度实验确认 Omni
TTFT 具备明显优势。或者也可以使用小模型快速返回，再大模型完整回答。
TTS（文本转语音）优化：实验 1s chunk、端上缓存等手段， 或使用 Omni 音频，无需单独
TTS。
A2BS（语音转口型）优化：原本速度已经较快，但需要设置合适的整段调用；若能窗口化即
可同步嘴
型。
通信优化：把多个服务 ASR
、TTS 和 LLM 等都统一到同一台服务器，降
低服务直接
调用成
本。
不同方
案
对比：
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
原始 的导 购 对话流 程， 基线 数据 的链 路 是"ASR → LLM → TTS & A2BS"的三 段式结 构：
ASR 识别结束后
发起文本请求，获取请求之后，当
达到一定的标点符号截断，才会调用 TTS
和面部动画生成，回传结果之后，再播放音频和面部动画。采用Qwen Omni，可以Audi
o到
Audi
o，减少中间环节。
而因为字幕原因，最终我们使用的是
流 式返 回音频和文 字， 端 上 再负责补建嘴
Qwen Omni的Text→Audi
o/Text模式，让 LLM 直接
型、同 步 播放 功能 。所 以 新 的链 路 结 构为"ASR-
>LLM->Text/Audi
o->A2BS"。
性能监控系
统设计
在实施优化前，我们首先完善了性能监控体系，确保每一步改动都
关键基础设施。
有数据支撑。这是本次优化的
▐ 3.1 设计目标
全链路覆盖：从 VAD 启动到面部表情播放，覆盖所有关键节点
线程安全：支持多线程并发打点，不影响主业务逻辑
高精度时间戳：基于
std::chrono::high_resoluti
on_clock 提供毫秒级精度
多维度输出：支持实时日志、
JSON 文件
、CSV 导出、统计报表
易于扩展：新增事件类型只需修改枚举和映射函数
▐ 3.2 核心类设计
▐ 3.3 事件类型设计
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
基础链路事件
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
enum class EventType {
ASR
_
START, // VAD 检测到语音开始
ASR
_
END, // ASR 识别完成
LLM
REQUEST
_
_
START, // LLM 请求
发起
LLM
FIRST
_
_
TOKEN, // LLM 首个 token 返回
LLM
_
COMPLETE, // LLM 流式完成
TTS
REQUEST
_
_
START, // TTS 请求开始(每个 chunk)
TTS
_
RESPONSE, // TTS 响应返回
AUDIO
PLAY
_
_
START, // 音频开始播放
ANIMATION
_
START, // 表情动画开始
Omni 事件
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
Omni
STREAM
_
_
START, // Omni 流式开始
Omni
FIRST
AUDIO
_
_
_
CHUNK, // 首个音频 chunk 到达
Omni
AUDIO
_
_
CHUNK, // 音频 chunk(每个)
Omni
STREAM
_
_
COMPLETE, // 流式完成
Omni
STREAM
_
_
ERROR, // 流式错误
// A2BS 窗口化相关
Omni
AUDIO
WINDOW
_
_
_
SEALED, // 音频窗口封存
Omni
A2BS
FACIAL
_
_
_
START, // A2BS 请求开始
Omni
A2BS
FACIAL
_
_
_
RESPONSE,// A2BS 响应返回
Omni
A2BS
FACIAL
PLAY
_
_
_
_
START, // 首次嘴
型播放
Omni
AUDIO
WINDOW
_
_
_
PLAY, // 窗口音频播放
Omni
_
Omni
_
Omni
_
FACIAL
FACIAL
FACIAL
_
START, // 面部数据生成开始
_
COMPLETE, // 面部数据生成完成
_
ERROR // 面部数据生成失败
...
};
▐ 3.4 关键指标定义
基础指标
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Omni 指标
▐ 3.5 数据结构设计
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
// 单次请求的性能数据
struct RequestPerformance {
int64
_
t requestId;
std::string inputType; // "voice" or "text"
std::vector<std::pair<EventType, int64
_
t>> timeline;
std::map<EventType, std::string> metadata;
// 计算后的指标
int64
t asr
duration
_
_
_
ms;
int64
t llm
ttft
_
_
_
ms;
int64
t llm
total
_
_
_
ms;
int64
t end
to
end
_
_
_
_
ms;
int64
t end
to
end
bs
_
_
_
_
_
ms;
int64
t Omni
first
audio
_
_
_
_
int64
t tts
_
_
avg_
ms;
int32
t tts
_
_
count;
ms;
};
// 全局统计数据
struct PerformanceStatistics {
int32
t total
_
_
requests;
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
// 均值/最大/最小
double avg_
asr
_
ms, max
asr
_
_
ms, min
asr
_
_
ms;
double avg_
llm
ttft
ms, max
llm
ttft
_
_
_
_
_
ms, min
llm
ttft
_
_
_
ms;
double avg_
end
to
end
ms, max
end
to
end
_
_
_
_
_
_
_
ms, min
end
to
end
_
_
_
_
ms;
// P95/P99,
反映稳定性
double p95
end
to
end
_
_
_
_
ms, p99
end
to
end
_
_
_
_
ms;
double p95
llm
ttft
_
_
_
ms, p99
llm
ttft
_
_
_
ms;
double p95
Omni
first
audio
_
_
_
_
ms, p99
Omni
first
audio
_
_
_
_
ms;
double p95
end
to
end
bs
_
_
_
_
_
ms, p99
end
to
end
bs
_
_
_
_
_
ms;
// Omni 统计
double avg_
Omni
first
audio
_
_
_
ms;
double min
Omni
first
audio
_
_
_
_
ms;
double max
Omni
first
audio
_
_
_
_
ms;
double avg_
end
to
end
bs
_
_
_
_
ms;
double min
end
to
end
bs
_
_
_
_
_
ms;
double max
end
to
end
bs
_
_
_
_
_
ms;
};
▐ 3.6 实现要点
线程安全
使用
std::mutex m_Mutex：保护共享资源
std::lock_guardstd::mutex lock(m_Mutex);：RAII 方式自动上锁/解锁，防止死锁或遗
漏释放
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
class PerformanceMonitor {
private:
std::mutex m
_
Mutex;
std::map<int64
_
t, RequestPerformance> m
_
Requests;
public:
void RecordEvent(int64
_
t requestId, EventType type,
const std::string& metadata = "") {
std::lock
_guard<std::mutex> lock(m
_
Mutex);
// ... 记录逻辑
}
};
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
自动计算触发
在关键事件到达时自动触发指标计算：
AUDIO_PLAY_START: 计算 End-to-End
Omni_A2BS_FACIAL_PLAY_START: 计算 End-to-End-BS
多格式
输出
实时日志格式:
1
========== Performance Report for Request 1 ==========
2
Input Type: Voice
3
Timeline:
4
[269806374 ms] ASR
START
_
5
[269809542 ms] ASR
_
END - {"text":"给我介绍一下伯希和"}
6
[269810133 ms] LLM
FIRST
_
_
TOKEN - 伯
7
[269810374 ms] Omni
FIRST
AUDIO
CHUNK
_
_
_
8
[269810385 ms] AUDIO
PLAY
START
_
_
9
Performance Metrics:
10
ASR Duration: 3168 ms
11
LLM TTFT: 590 ms
12
End-to-End: 843 ms
13
End-to-End-BS: 1856 ms
14
Omni First Audio: 241 ms
JSON 文件
1
{
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
(ExportAllToJSON)格式:
"session": "20251113
150748"
_
,
"total
_
requests": 31,
"requests": [
{
"requestId": 1,
"durations": {
"asr
duration
_
_
ms": 3168,
"llm
ttft
_
_
ms": 590,
"end
to
end
_
_
_
ms": 843,
"end
to
end
bs
_
_
_
_
ms": 1856,
"Omni
first
audio
ms": 241
_
_
_
},
"timeline": [...]
}
],
"statistics": {
"total
_
requests": 31,
"asr": {"avg_
ms": 2449.7,
"max
_
ms": 3868,
"min
_
ms": 1284},
"llm": {
"avg_
ttft
_
ms": 968.5,
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
"p95
ttft
_
_
ms": 1683.0,
"p99
ttft
ms": 1920.0
_
_
},
"Omni
first
audio": {
_
_
"avg_
ms": 1250.0,
"p95
_
ms": 1450.0,
"p99
ms": 1500.0
_
},
"end
to
end
bs": {
_
_
_
"avg_
ms": 1856.6,
"p95
_
ms": 2100.0,
"p99
ms": 2300.0
_
}
}
}
统计报表
( LogStatisticsReport )格式:
1
2
3
4
5
6
7
8
9
==================== Performance Statistics Report ====================
Total Requests: 31
ASR Performance: avg=2449.7ms, min=1284ms, max=3868ms
LLM TTFT: avg=968.5ms, min=640ms, max=1920ms, P95=1683ms, P99=1920ms
Omni First Audio: avg=1250.0ms, min=890ms, max=2314ms, P95=1450ms, P99=
End-to-End Latency: avg=1264.5ms, min=890ms, max=2314ms, P95=1683ms, P9
End-to-End-BS Latency: avg=1856.6ms, min=1500ms, max=2300ms, P95=2100ms
TTS Performance: avg=N/A (Omni mode)
======================================================================
▐ 3.7 配置化管理
创建 PerformanceConfig.h 统一控制编译开关：
1
2
3
#ifndef PERFORMANCE
MONITORING
_
_
ENABLED
#define PERFORMANCE
MONITORING
_
_
ENABLED 1
#endif
需要打点的文件统一引入。
▐ 3.8 使用示例
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

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
26
// 1. 记录简单事件
PerformanceMonitor::GetInstance()->RecordEvent(
requestId,
EventType::ASR
START
_
);
// 2. 记录带元数据的事件
nlohmann::json metadata;
metadata["text"] = "用户问题";
PerformanceMonitor::GetInstance()->RecordEvent(
requestId,
EventType::ASR
_
END,
metadata.dump()
);
// 3. 记录窗口化 A2BS
metadata["windowIndex"] = windowIdx;
metadata["audioDuration"] = duration;
PerformanceMonitor::GetInstance()->RecordEvent(
requestId,
EventType::Omni
A2BS
FACIAL
_
_
_
START,
metadata.dump()
);
// 4. 触发报告(在 LLM
COMPLETE 时)
_
PerformanceMonitor::GetInstance()->LogSummary(requestId);
// 5. 导出全局统计
PerformanceMonitor::GetInstance()->LogStatisticsReport();
PerformanceMonitor::GetInstance()->ExportAllToJSON("/path/to/output");
技术方
案详细设计
基于完善的监控体系，我们开始实施 Omni 链路改造。
▐ 4.1 配置化入口与 Omni 开关
JSON 中新增 character_bs（嘴
型角色）以及
Omni相关内容) 相关
设置：
1
{
2
"model
_
name": "qwen3-omni-flash"
3
"voice": "Cherry"
,
4
"character
_
bs": "yuhe"
,
Omni_audi
o.enabled (后续可能配置更多与
,
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
5
6
"Omni
audio": {
_
"enabled": true
7
}
8
}
▐ 4.2 播放与同步流程
```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text

```

## PDF 第12页

[查看原页](RAW.pdf#page=12)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 4.3 音频窗口缓冲 + 串
A2BS
行
对于Omni的语音返回，我们需要调用服务端A2BS接口，生成对应的表情。Omni返回的每个
chunkSzie 在 20480字节，如果每次返回都进
行
请求，那么表情生成的会非常不自然，会有
明显的不连续。在原始的链路中，是根据文本断
句到标点符号进
请求，对应语音的返回，通
行
常用户说话1～2秒即为完整的句子。
所以我们设计为按
也会针对性进
行
其关键结构如下：
采样率累积 1~2 秒音频窗口，达到目标窗口时长再触发A2BS。此外，算法
平滑。
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
// `OmniA2BSHelper
`
struct OmniA2BSConfig {
float targetDurationSeconds = 1.0f; // 目标窗口时长
float minDurationSeconds = 0.01f; // 最小窗口时长
int32
_
t sampleRate = 24000;
};
struct AudioWindow {
int32
_
t windowIndex = 0; // 每个窗口记录 `
windowIndex
`，便于打点与回放排
std::vector<std::string> base64Chunks; // Base64 音频块
std::vector<int16
_
t> pcmSamples; // PCM 音频样本
std::string mergedBase64; // 合并后的 Base64
int32
_
t sampleRate = 24000;
bool base64Finalized = false;
void Append(const std::string &base64Chunk,
const int16
_
t *samples,
size
_
t sampleCount);
float GetDurationSeconds() const;
void FinalizeBase64();
std::string ConsumeMergedBase64();
};
struct AudioWindowQueue {
explicit AudioWindowQueue(const OmniA2BSConfig &cfg);
std::shared
_ptr<AudioWindow> SealReadyWindow();
std::shared
_ptr<AudioWindow> SealRemainingWindow();
float CurrentDurationSeconds() const;
bool HasCurrentWindow() const;
private:
void EnsureWindowLocked();
OmniA2BSConfig config;
```

## PDF 第13页

[查看原页](RAW.pdf#page=13)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
30
31
32
33
mutable std::mutex mutex;
std::shared
_ptr<AudioWindow> currentWindow;
int32
_
t nextWindowIndex = 0;
};
优化效果数据对比
基于伯希和导购业务对话场景，对于一组数据会询问以后问题，每次三组数据：
1. 手套多少钱？
2. 介绍一下伯希和品牌
3. 怎
么购买？
4. 这个帽子有哪些颜色，材质是什么？
5. 美丽奴羊毛是什么意思？
6. 这个伯希和头灯的流明是多少？
7. 这个围巾有哪些颜色？
8. 还
有哪些东西可以购买？
9. 手套是什么材质？
10. 现在有什么优惠？
▐ 6.1 详细数据对比
采用不同的接口或者策略迭代演进多次，得到以下数据对比：
```

## PDF 第14页

[查看原页](RAW.pdf#page=14)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
其中，第5组数据的考虑是基于，因为用户说话需要字幕，ASR是必须的，所以想到Omni也可
以从输
入音频，到切换为输
入文本，同样保留输出为音频和文本。测试Omni
入文本，相较
输
于
入音频处理速度更快。
输
总体来看，之前性能的瓶颈，一个是大模型返回的速度更慢，另外一个是每次TTS占用的时间
更长，虽然A2BS累积也会导致一定的延迟，但不是主要的延迟来源。
对于整体解决
方
案，完整的性能监控打点机制
合适的模型，端测针对新模型增加输
入
语音表情同步的处理，保障链路的正确性。
是优化的基础，具体实施时，一方面，我们用更
输出链路，另一方面，端测针对A2BS进
行
窗口累积和
▐ 6.2 关键指标改善
关键指标数据：
P95/P99 稳定性分析：
结论：不仅平
均延迟大幅降
低，P95/P99 也控制在合理范围，用户体验稳定性显著提升。
▐ 6.5 各阶段耗时分布对比
```

## PDF 第15页

[查看原页](RAW.pdf#page=15)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
基线链路：
Omni 链路：
展望
在之后的优化中，也设想了一些方向：
1. 自动化测试体系：
录制标准问句集（10-20 个典型问题）
CI/C
D 集成性能回归测试
2. 自部署链路：
研究 Omni 模型自部署可
性
行
对比
延迟、成本、维护复杂度
3. 端上推理：
小模型快速响应首句（<500ms TTFT）
TTS / A2BS 端上推理可
性
行
4. 双模型加速：
小模型快速生成首句
大模型补充完整回答
用户感知"秒回"体验
5. 预录制：
提前准备高频回答的音频/嘴
型
缓存常见问答的 facialSamples
总结
通过本次优化，我们不仅将端到端延迟从 5.64s 降
立了一套完整的性能监控与优化体系
至 1.32s（76.6% 提升），更重要的是建
。不仅适用于当前的 Omni 链路，也为后续的自部署、端
```

## PDF 第16页

[查看原页](RAW.pdf#page=16)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
上推理、双模型加速等探索奠定了基础。性能监控体系
化优化效果，真正做到"用数据说话"。
的建立，让我们能够快速定位问题、量
后记
值得一提的是，使用 Qwen Omni 模型也有局限，只支持官方音色输出，而不
像我们通过TTS
可以自由生成任
意音色。对于通用场景，我们需要使用特定人的声音，那么就需要有音色复刻
的能力，同时有流式
输出的能力。25年11月中旬，百炼发布的的
Qwen-TTS-Realtime模型，
可以实时复刻声音并且流式
输出，可以同时满足上诉两个需求。在后续自定义音色的场景下，
我们可以采用任
意LLM模型加TTS-Realtime的模式，模拟Omni的流程，LLM流式
输出的内
容通过WebSocket与TTS-Realtime交互，流式的生成自定义音色的TTS。时间上会增加些许
的网络通信延迟。所以在不同的场景业务下，我们可以采用不同的解决
方
案。
团队介绍
本文作者揽清，来自淘天集团-Meta技术团队。本团队目前负责面向消费场景的3D/XR基础技
术建设和创
新应用探索，创造以手机及XR 新设备为载体的消费购物新体验。团队在端智能、
端云协同、商品三维重建、真人三维重建、3D引擎、XR引擎等方面有着深厚的技术积累，先
后
发布深度学习引擎MNN、商品三维重建工具Object Drawer、3D真人数字人TaoAvatar、
端云协同系
统Walle等。团队在OSDI、MLSys、CVPR
、ICCV、NeurIPS、TPAMI等顶级
学
术会议和期
刊上发
表多篇论文。欢迎视觉算法、3D/XR引擎、深度学习引擎研发、终端研发等
领域的优秀人才加入，共同走进3D数字新时代。
¤ 拓展阅读 ¤
3DXR技术 | 终端技术 | 音视频技术
服务端技术 | 技术质量 | 数据算法
大淘宝技术大淘宝技术官方账号
967篇原创内容
```

## PDF 第17页

[查看原页](RAW.pdf#page=17)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
公众号
阅读 3060
留言 1
写留言
扬帆起航 陕西 3月10日
学习了，正在搞数字人
```

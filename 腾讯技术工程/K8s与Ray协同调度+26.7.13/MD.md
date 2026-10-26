# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
腾讯 Ray 团队实践： K8s  + Ray 如何⽀撑超⼤规模 AI  Workload
Jul  13 , 2026 , 2 : 36  AM⼴东腾讯技术⼯程 18  listened
作者： charliecli
⼀、 ⼤模型时代 AI  基础设施的技术栈演进
要理解这⼀全新的调度范式，⾸先需要审视当前⼤模型基础设施的技术栈现状。借助蚂蚁开
源技术委员会绘制的 AI  Infra  开源⽣态全景图 [ 1 ]，我们可以全⾯了解当下 AI  Infra  领域的
主要开源项⽬。
从这张全景图中可以提炼出⼀条典型的 AI  Infra  技术栈：Ray  + PyTorch  + vLLM。值得
⼀提的是，这三个项⽬⽬前均⾪属于 PyTorch  基⾦会（其中 Ray  于 2025  年 PyTorch  ⼤
会上正式作为托管项⽬加⼊）。在此之上，再叠加⼯业界事实标准的部署与调度底
座 K8s，便构成了 K8s  + Ray  + PyTorch  + vLLM 的⻩⾦组合。这套技术栈贯穿⼤模型
⽣命周期的全链路，涵盖数据处理、预训练、后训练、在线推理与 Agent  等场景。
随着⼤模型时代的到来， AI  基础设施（ AI  Infra ）正在经历深刻的变⾰。⾯对⽇益复杂的
计算需求，传统上与单⼀计算范式深度耦合的调度系统已难以应对全局性挑战。本⽂结合
开源社区的演进趋势与⼯业界的超⼤规模落地实践，深⼊探讨 Ray  的技术定位与核⼼设计
逻辑，并阐述它如何与 Kubernetes （以下简称 K8s ）进⾏协同设计（ co - design ），共同
构建⼤模型时代 AI  Workload  调度的通⽤范式。 注：⽂章的图⽚内容来源于腾讯 Ray  团
队在 Qcon  全球软件开发⼤会的分享：
 https :// qcon . infoq . cn / 2026 / beijing / presentation / 7002
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
为更直观地理解这套技术栈的运作⽅式，我们以强化学习（RLHF）为例。当前主流的 RL
训练框架普遍采⽤"训推分离"架构：
训练端：依托 PyTorch  ⽣态（如 Megatron 、 DeepSpeed ）提供⾼性能训练能⼒。
推理端：以 vLLM  作为核⼼推理后端（ Backend ）。
编排与调度：由 Ray  串联全局，承担训推流程的编排以及⻆⾊间的复杂通信。
底层基座： K8s  作为应⽤部署的事实标准，提供底层物理资源⽀撑。
⽬前，业界 90 % 以上的 RL  训练框架均构建于这套 K8s  + Ray  + PyTorch  + vLLM  ⻩⾦
组合之上。关于该组合的深度探讨，可参⻅四个项⽬的技术负责⼈在 Ray  Summit  2025  上
的对谈 [ 2 ]，本⽂不再赘述。
这套技术栈也已经过开源社区的真实检验。从 2021 — 2025  年的开源活跃度（以 Commit
数为指标）来看：
作为 AI  应⽤时代最关键的推理引擎， vLLM  在过去⼀年贡献了超过 8000  个 Commit ，活
跃度极⾼； Kubernetes  始终保持极⾼且稳定的活跃度，与其云原⽣部署事实标准的地位相
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
称；⽽ Ray  作为通⽤计算引擎，活跃度已明显超越 Spark 、 Flink  等传统⼤数据计算引擎。
让 Ray  在近两年迎来爆发的，正是它在两类核⼼场景中的不可替代性：多模态数据处
理 与 后训练/强化学习。下图梳理了基于 Ray  构建的 AI  Infra  开源项⽬，可以看出 Ray
在 数据处理 与 后训练/强化学习 这两个⽅向上的⽣态最为活跃。
此外，我们也汇总了 Ray  在国内主要企业的落地情况：
如今，国内头部⼚商（包括 DeepSeek 、⽉之暗⾯等）在多模态数据处理上⼏乎全⾯采⽤
Ray ； 90 % 以上的 RL  训练框架基于 Ray  构建；主流云⼚商均已提供 Ray  托管服务；阿⾥
等企业也开始探索基于 Ray  构建 Agent  Sandbox 。在⾮ AI  场景⽅⾯，蚂蚁集团早在 2017
— 2018  年便已将 Ray  应⽤于图计算与隐私计算。
接下来，我们将从 AI  Workload  调度的视⻆，深⼊解析⼤模型时代的 AI  Infra  为何选择
Ray ，以及 Ray  究竟解决了哪些传统计算引擎难以应对的调度痛点。
⼆、 基于 Ray  的 AI  Workload  调度
我们⾸先通过两个典型场景，归纳当下 AI  Workload  提出的调度需求。
1 . 多模态数据处理
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
下图展示了多模态数据处理的典型 Pipeline ：系统需要持续读取、处理并输出⼤批量多模态
数据。整条 Pipeline  由多个 Stage  串联组成，其中既包含 CPU  密集型算⼦（如抽帧、格
式转换），也包含强依赖 GPU  的算⼦（如 OCR 、语⾳识别、⼤语⾔模型推理）。所有算
⼦需要在统⼀的资源池内参与调度。
这带来了三⼤挑战：
异构调度： CPU  与 GPU  算⼦需要被⾼效地匹配到对应的异构节点；
动态分配：需根据实时负载动态调整各 Stage  的资源量与并发度，以打破吞吐瓶颈；
⾼容错：由于链路⻓、耗时久，单点故障（如 OOM 、 GPU  Error 、 Spot  Instance  回收）⼏
乎不可避免。因此容错粒度必须下探到 Stage 、 Pod  乃⾄进程级，避免单点故障拖垮整条
Pipeline 。
2 . 强化学习（ RLHF ）
以 RLHF  中⼀次典型的 PPO  Training  Step  为例：⽤户的 Prompt  经 Actor  推理⽣成
Response  后，需并发分发给 Reference 、 Reward  与 Critic  进⾏打分评估，再经
Advantage  计算回传给 Actor  与 Critic  完成参数更新。
这本质上是⼀个多异构⻆⾊的协同调度问题。它不仅涉及多种⻆⾊（其中 Actor  还可能进
⼀步拆分为训练与推理两部分），⽽且各⻆⾊依赖的运⾏时完全不同（例如推理需拉起
vLLM / SGLang ，训练需加载 FSDP / Megatron ），并发设置与资源需求也各不相同。更复
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
杂的是，任务流转并⾮简单的线性 DAG ，⽽是需要在多⻆⾊之间以复杂的多播
（ multicast ）形式传递。
⾯对后训练/ RLHF  中"异构、多⻆⾊协同"的调度需求，预训练阶段⻓期沿⽤的计算范式变
得难以匹配。主流预训练框架（如 FSDP 、 Megatron ）通常采⽤ Multi - Controller  /
SPMD（ Single  Program , Multiple  Data ） 范式，要求每个计算单元运⾏同构进程，并
依赖同步 Barrier  与集合通信。这种范式存在三⽅⾯局限：灵活性差（难以表达异构⻆
⾊）、容错率低（单点故障会导致整个通信组崩溃）、缺少⼀个能够以全局视⻆统⼀编排复
杂任务流的中⼼⻆⾊。
为突破这⼀限制，⼤模型时代的强化学习框架（ 如 veRL [ 3 ]、 SkyRL [ 4 ] ）纷纷转
向 Single - Controller  / MPMD （ Multiple  Program , Multiple  Data ） 范式：引⼊⼀个
中⼼ Driver （ Single - Controller ）来统⼀编排多个异构⻆⾊。 Driver  能够以全局视⻆组织
跨⻆⾊的复杂任务流；各异构⻆⾊内部仍可保留 SPMD  架构以获取局部⾼性能。借助中⼼
Driver ，异构⻆⾊之间得以松耦合，容错也能在⻆⾊粒度上独⽴完成。
3 . AI  Workload  调度需求⼩结
基于上述两个典型场景，我们将⼤模型时代 AI  Workload  的调度需求归纳为四点：
异构资源：将异构算⼦/⻆⾊⾼效地调度到异构节点上
动态分配：根据实时负载，为每个算⼦/⻆⾊动态分配计算资源，避免出现局部吞吐瓶颈
⾼容错：局部故障不影响全局任务，出错的计算单元⽀持⾃动重新调度并恢复状态
原⽣⽀持 Single - Controller：由 Single - Controller  统⼀编排跨⻆⾊/跨算⼦的复杂任务流
4 . Ray  核⼼ API  设计
本节通过 Ray  的核⼼ API ，展示上述四项调度需求如何在 Ray  中被⼀⼀满⾜。下⾯的
Python  代码⽚段简要模拟了 RLHF  训推分离场景：
import ray
def main():
    # 主函数中声明当前进程为中⼼  Driver
    ray.init()
    
    # 定义⼀个  Rollout ⻆⾊  ( 类），该⻆⾊的每个实例需要：
    # 1. 分配  2 个  CPU 和  1 个  GPU
    # 2. 出错后⽆限次⾃动重启
    @ray.remote(num_cpus=2, num_gpus=1, max_restarts=-1)
    class RolloutWorker:
        def __init__(self):
            # 如果当前实例为重启状态（⾮⾸次创建）
            if ray.get_runtime_context().was_current_actor_reconstructed:
                # ⾃定义状态恢复⾏为
                self._recover_state()
                
        def generate(self, prompt):
            return"Hi there"
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
            
    # 定义⼀个  Trainer ⻆⾊（类），该⻆⾊的每个实例需要分配  2 个  GPU
    @ray.remote(num_gpus=2)
    class Trainer:
        def fit(self, experience):
            return 0
        
    # 创建  2 个  RolloutWorker 远程实例，组成  rollout worker group
    rollout_worker_group = [RolloutWorker.remote() for _ in range(2)]
    
    # 创建  1 个  Trainer 远程实例
    trainer = Trainer.remote()
    # 开始  RL 训练流程
    while True:
        for rollout_worker in rollout_worker_group:
            # 远程调⽤  ( 异步 ) RolloutWorker 实例的  generate ⽅法
            response = rollout_worker.generate.remote("Hello")
            # 将  RolloutWorker 实例的  response 派发给  Trainer 实例
            ret = trainer.fit.remote(response)
            
        # 动态增加远程实例（提升  rollout 并发度）
        rollout_worker_group.append(RolloutWorker.remote())
在上述代码中，我们⾸先通过 ray.init 将当前进程声明为中⼼ Driver （Single -
Controller）。然后通过 @ray.remote 装饰器定义异构⻆⾊（类定义），并声明每个⻆
⾊实例的资源与容错需求。对每个⻆⾊，我们都可以通过 remote() 接⼝创建任意数量的
远程实例（进程），并按需分组管理。在训练循环中，可以调⽤任意远程实例的⽅法，并将
上游返回值（ObjectRef）派发给指定下游实例，从⽽编排任意形式的任务流。运⾏过程
中也可以动态增减⻆⾊实例，以调节各⻆⾊的并发度。
本质上， Ray  作为分布式计算引擎，其调度的核⼼对象是"进程级计算单元"。在进程粒度
上， Ray  同时实现了 异构资源调度、动态分配 与 ⾼容错 能⼒。中⼼ Driver （Single -
Controller）则可充分利⽤这些调度能⼒，灵活编排任务流。
5 . 分布式计算引擎对⽐：调度能⼒
总结完 AI  Workload  的调度需求与 Ray  的对应⽀持之后，我们进⼀步将 Ray  与其他主流
分布式计算引擎（ Spark 、 Flink 、 PyTorch ）在调度能⼒上进⾏对⽐：
Spark Flink PyTorch Ray
计算范式 BSP （批处理） 流式 Dataflow SPMD ⽆范式（通⽤分
布式）
异构资源 粗粒度（ Stage  内同
构）
粗粒度（ Slot  切
分） 不⽀持 细粒度（进程
级）
动态分配 粗粒度（ AQE ， Stag
e  间⽣效） ⽀持 不⽀持（静态通
信组）
细粒度（进程
级）
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
Spark Flink PyTorch Ray
容错 粗粒度（ RDD  Linea
ge  重算）
粗粒度（ Checkpoi
nt  回滚）
粗粒度（整组重
启）
细粒度（进程
级）
Single - Contr
oller ⽀持 ⽀持 不⽀持 ⽀持
从计算范式来看， Spark  绑定了 BSP  批处理， Flink  绑定了流式 Dataflow ， PyTorch  绑定
了 SPMD ；⽽ Ray  本身是⽆范式的——基于其提供的进程级计算单元，⽤户可以根据业务
形态⾃由构建任意计算范式。反过来看，正因为 Spark 、 Flink 、 PyTorch  与固定计算范式
深度耦合，它们在 异构资源调度、动态分配 与 容错能⼒ ⽅⾯均缺乏⾜够细粒度的⽀持，
难以全⾯覆盖⼤模型时代 AI  Workload  的多样化需求。
综合来看， Ray  凭借进程级调度的灵活性，成为复杂 AI  Workload  调度的最优解。
6 . Ray  架构与调度实现
在本章最后，我们简要介绍⼀下 Ray  的整体架构与调度实现。
Ray  集群架构如上图所示。其中， Head  节点上运⾏ Global  Control  Store （ GCS ），负责
集群元数据管理与节点状态同步；每个 Worker  节点上运⾏ Raylet ，负责调度决策与本地
进程管理。当⽤户的中⼼ Driver  创建⻆⾊实例时，调度会经历以下流程（实际略有差异，
此处仅作示意）：
1 . 调度请求⾸先发送⾄本地 Raylet ，由其做出调度决策，选择⽬标节点
2 . 调度请求被转发⾄⽬标节点的 Raylet
3 . ⽬标节点 Raylet  根据本地资源状态决定是否接受请求；若接受，则在本地创建 Worker  进
程并运⾏⻆⾊实例
4 . 调度完成后， Driver  即可通过 gRPC （或 RDMA ）直接调⽤远程实例的⽅法。
⽬前， Raylet  内置了多种调度策略，包括 Round - Robin  调度、按堆叠⽔位调度、
Node / Label  亲和性调度、 Gang  Scheduling  以及 Data  Locality  调度，⽤户可以根据业务
场景的调度需求⾃由调配。对更多技术细节感兴趣的读者可以参考 Ray  官⽅⽂档 [ 5 ]。
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
三、 K8s  + Ray  的协同调度范式
⽬前， Ray  的主流⽣产部署⽅式都构建在 K8s  之上。在近⼏届 Ray  Summit  全球峰会上，
AWS 、 Microsoft 、 Google  等主流云⼚商也相继披露了各⾃基于 K8s  + Ray  的部署⽅案。
为什么必须引⼊ K8s ？
K8s  作为企业级基础设施，能够⾼效、统⼀地管理⼤规模物理资源池，并提供容器化部署、
服务发现、存储编排，以及成熟的监控、运维与权限体系。借助 K8s  的成熟⽣态， Ray  才
能快速在⽣产环境中实现稳定、规模化的落地。
K8s  & Ray ：职责分⼯
当采⽤ K8s  结合 Ray  的部署⽅式时，两者的职责分⼯如下所示：
K8s Ray
定位 物理资源调度与管理 应⽤层调度与编排
资源管理对象 ⼤规模物理节点资源 Ray  Cluster  内的资源
⽣命周期管理 容器/ Pod Worker  进程
调度对象 Pod  →  物理节点 Worker  进程 →  Ray  Node  ( Pod )
API  形态 YAML  声明式 Python  编程式
从定位上来说， K8s  是物理资源调度与管理，⽽ Ray  在其之上充当应⽤层调度与编排。从
调度上来说， K8s  负责将 Pod  调度到物理节点上，整个流程涉及 API  Server 、
Scheduler 、 Kubelet  等多个组件以及状态同步/持久化操作；⽽ Ray  则以⼆层调度的⽅
式，负责将 Worker  进程调度到 Pod （ Ray  Node ）上，调度策略更加贴合上层任务的需
求，整体流程更加轻量。从 API  设计上来说， K8s  是 YAML  声明式的，更⾯向集群管理/
运维⼈员；⽽ Ray  提供编程式接⼝，更适合分布式应⽤的研发⼈员。
K8s  & Ray ：协同调度
将 K8s  与 Ray  结合做协同调度时，整体流程可以概括为： K8s  负责将资源从统⼀资源池中
分配给 Ray ；⽽ Ray  负责将分配到的资源以更细粒度分配给上层任务。
为了将 Ray  ⽆缝接⼊ K8s  ⽣态， Ray  开源社区提供了 KubeRay  Operator 。⽤户提交⾃定
义的 RayCluster CR  后，由 KubeRay  Operator  负责持续调谐，创建并维护对应的 Ray
集群。 Ray  集群包含 Head  节点和任意数量、异构规格的 Worker  节点，并⽀持运⾏时的
⾃动扩缩容。 Ray  集群内的资源则进⼀步由 Ray  Scheduler  以轻量、细粒度的⽅式分配给
上层任务。
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
如上图所示，通过 K8s  →  KubeRay  →  Ray  Scheduler  这条⾃底向上、由粗到细的协同调
度链路，资源可以被稳定、⾼效、灵活地分配给 AI  任务。
四、 K8s  + Ray  在腾讯的落地实践
从开源社区的视⻆来看， K8s  →  KubeRay  →  Ray  这套协同调度⽅案已经相当成熟。然⽽，
当我们将它真正落地到腾讯内部，尤其是⾯对企业级的超⼤规模集群时，现实远⽐想象复
杂。
在腾讯 TEG  内部， Ray  平台的整体架构涉及多个层级。最底层是峰峦 K8s  云原⽣架构，
作为统⼀算⼒平台管理海量异构算⼒资源，并提供联邦调度、智能调度等能⼒。中间层涵盖
完整的 Ray  ⽣态：从 Ray  调度内核，到数据处理、训练、在线服务三⼤⾼阶框架能⼒，再
到 DAGFlow  离在线⼀体化的服务封装。上层是数据平台与机器学习平台，承接各业务线的
具体需求。
⾸先，我们要⾯对的复杂性来⾃底层峰峦 K8s  云原⽣架构。这套架构有⼏个关键特点：
K8s  物理集群不直接向上暴露，由联邦层进⾏统⼀管理
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
⽣产环境存在上百个 K8s  物理集群，以 CPU  算⼒与 GPU  算⼒维度分离
WeData  数据平台与太极 AI  平台分别维护两套独⽴的 K8s  基础设施
这些特点给 Ray  的落地带来了显著挑战： Ray  提供的是异构融合计算能⼒，需要 K8s  云原
⽣层供给" CPU  + GPU "混合资源，⽽这些资源往往分散在不同的 K8s  物理集群中；但社区
版 KubeRay  仅⽀持 RayCluster  在单⼀ K8s  物理集群内部署与调度。
1 . 核⼼挑战：云原⽣联邦架构的演进
针对底层 K8s  架构现状，我们⾸要的⽬标是⽀持 RayCluster  跨 K8s  集群部署。在技术选
型阶段，我们对以下三种⽅案进⾏了深⼊评估：
1 . ⼆层调度⽅案：在各 K8s  集群中预申请⼤量 Pod  常驻，并在这些 Pod  之上构建⼀层⾃定
义调度器来调度 RayCluster 。该⽅案引⼊了额外的调度层，使整个系统从" K8s  + Ray "的两
层调度演变为" K8s  + 中间层 + Ray "的三层调度，显著增加了系统复杂度与调优难度。
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
2 . 平台层 Standalone  组⽹⽅案：在平台侧直接调度多个 K8s  集群的 Deployment  形成多个
Pod  组，并在每个 Pod  内部启动 Ray  进程，指定其中⼀个节点为 Head ，以 Standalone
⽅式完成组⽹。该⽅案虽然没有引⼊额外的调度层，但放弃了 KubeRay  的能⼒，需要在平
台层重新构建⼤量替代逻辑。
3 . KubeRay  联邦⽅案：保留原⽣ KubeRay ，并在其之上扩展⽀持跨集群联邦。
我们希望尽可能地兼容并复⽤开源社区的已有能⼒，因此最终选择了⽅案 3 ——扩展
KubeRay  以⽀持集群联邦。在落地过程中， KubeRay  联邦架构经历了两个演进阶段：
阶段⼀： Virtual  Kubelet （ VK ）架构
为实现跨集群组⽹，我们构建了第⼀版基于 Virtual  Kubelet （ VK ）的架构：在 CPU  集群
上保留完整的 KubeRay  能⼒，并通过 VK  将太极集群的 GPU  资源抽象为虚拟 Kubelet 。
创建 GPU  Pod  的实际链路是： KubeRay  调⽤ VK ， VK  再调⽤ ModelService  创建太极服
务，最终由太极服务拉起真正的 Pod 。该⽅案在 TEG  内部成功落地，但在规模化推⼴时暴
露出明显瓶颈：架构依赖倒置（底层 VK  反向依赖上层服务），调⽤链路冗⻓——每创建⼀
个 GPU  Pod  都要触发⼀次太极服务创建。在后期的业务落地中，当 RayCluster  节点数超
过 100  时，太极链路便会承受较⼤压⼒，难以满⾜⽣产需求。
阶段⼆： KubeRay  联邦架构
考虑到 VK  架构的瓶颈，我们进⼀步推进了更合理的 KubeRay  联邦架构。该架构在多个
K8s  物理集群中并发部署 KubeRay  Workload ，并通过配置约束仅由其中⼀个 Workload
启动 GCS （ Global  Control  Store ），其余 Workload  的节点均作为 Worker  节点组加⼊同
⼀ Ray  集群。在此基础上，我们还实现了联邦集群的 Autoscaling  能⼒，借助联邦机制完
成全局资源弹性。
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
完成该改造后，我们实现了异构资源调度的统⼀—— CPU  与 GPU  算⼒可以通过同⼀个⼊
⼝灵活组⽹，单集群规模可达万卡以上；同时 Wedata  数据平台与太极 AI  平台得以复⽤相
同的调度链路，达成了 Data  + AI  的调度统⼀。
2 . 跨层协同设计：跨层弹性调度
解决了基础的跨集群组⽹问题后，我们开始直⾯业务在规模化推⼴中遇到的真实痛点。在多
模态数据处理场景中，我们发现业务⽅往往难以根据产能要求直接评估出所需的 CPU / GPU
规格与数量；并且在任务运⾏前也⽆法准确预知瓶颈所在（例如华南 CPU  与华北 GPU  跨
地域协同导致的 IO  带宽瓶颈，或 GPU  节点上 CPU  预处理资源不⾜导致 GPU  利⽤率低
下），使得运⾏时效率难以保障。
为此，我们设计了跨层弹性调度机制：业务⽅⽆需再纠结资源规格，只需提交"算⼦"与"预
期产能"，由 Ray  在运⾏时动态完成资源匹配。
整体流程如下：⽤户算⼦和预期产能通过业务平台提交后，由智能调度器输出推荐配置并下
发⾄ K8s ， KubeRay  Operator  通过跨 K8s  联邦调度创建出初始 Ray  集群。任务运⾏过程
中，系统会进⾏三级⾃动调优：
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
1 . 动态扩缩容：根据 Ray  集群资源⽔位与任务负载情况，实时调整异构 Ray  节点（ Pod ）的
数量，避免⻓时间资源空转或数据堆积。
2 . Pod  重调度：对出现隐患（例如 GPU  ECC  Error 、磁盘空间不⾜等）的 Ray  节点触发重新
调度。
3 . 任务重调度：若上述两级调整仍⽆法达到预期产能，则对整个任务进⾏重新调度，由 K8s
层重新做智能资源池决策后任务继续执⾏。
每⼀级⾃动调优都需要 Ray  任务调度层与 K8s  资源调度层协同处理。通过这⼀系列闭环反
馈，系统可⾃动将任务调整⾄最佳运⾏状态。
3 . 跨层协同设计：跨层⾃动化容灾
除了资源配置，稳定性是业务的另⼀⼤需求。这⾥我们以对故障⾼度敏感的强化学习场景为
例。
在现有的强化学习业务中， RL  框架层与 K8s  算⼒层之间缺乏故障协同处理，主要表现为两
类问题：
1 . 当 K8s  算⼒层检测并屏蔽故障卡后， RL  框架⽆法及时感知，往往要等到训练任务失败、并
经⼈⼯确认后才能介⼊处理。
2 . RL  训练任务因故障卡失败后，⽆法⾃动通知 K8s  算⼒层做调度屏蔽，导致任务再次拉起时
可能再次命中同⼀张故障卡，反复失败。
为此，我们打造了跨层⾃动化容灾⽅案，覆盖故障感知、故障标记与故障处理三个环节。
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
全⽅位故障感知：在 Ray  Worker  节点内，由 Dashboard  Agent  周期性检测关键资源指标
（如磁盘、 GPU  健康度等）；在 Head  节点内，由 Train  Monitor  基于训练任务⽇志感知
异常；在 K8s  算⼒层，由定期巡检发现故障卡。
统⼀故障标记：任意组件感知到故障后，都可通过 Ray  Dashboard  提供的开放接⼝对故障
节点进⾏统⼀标记。
故障节点替换与任务续训：当训练任务⽆法推进⽽触发重启时，所有被标记的故障节点会
被⾃动替换，并在 K8s  层完成故障卡屏蔽；新任务拉起时将⾃动避开所有已知故障节点。
通过这⼀闭环机制，故障从"被动等待⼈⼯介⼊"转变为"⾃动感知—⾃动隔离—⾃动恢复"，
显著提升了⼤规模 RL  训练任务的稳定性。
五、 未来展望
通过上述跨层协同调度的实践，我们打通了 K8s  与 Ray ，沉淀出⼀套⾏之有效的 AI
Workload  调度通⽤范式。⾯向未来，我们将在以下三个⽅向持续深耕：
1 . 更原⽣的 Ray  联邦架构：当前的 KubeRay  联邦⽅案仍需要接⼊层感知，在不同场景间部
署仍需迁移成本；未来希望将这部分能⼒收敛进 K8s  + Ray  技术栈内部，进⼀步提升易⽤
性与普适性。
2 . 更通⽤的分布式底座：⾯向多模态数据处理、预训练、强化学习、在线推理、 Agent  应⽤
等场景，构建更通⽤的分布式底座与平台，强化调度、通信、存储等通⽤分布式能⼒。
3 . 更统⼀的 Agentic  RL  Infra：在"训练 + 推理"统⼀到 Ray  计算范式的基础上，进⼀步覆盖
Agentic  RL  场景中更⼴泛的调度统⼀问题，例如 Agent  与 Sandbox  运⾏环境的统⼀编
排。
当 K8s  遇⻅ Ray ，⼤模型时代的 AI  Workload  调度正在开启新的篇章。期待更多开发者加
⼊我们，共同⻅证并参与这场 AI  基础设施的变⾰。
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
References
[ 1 ] Open Source LLM Development Landscape
[ 2 ] Ray Summit 2025 Keynote: AI OSS Stack Panel with vLLM + PyTorch + Kubernetes
[ 3 ] verl: Volcano Engine Reinforcement Learning for LLMs
[ 4 ] SkyRL: A Modular Full-stack RL Library for LLMs
[ 5 ] Ray Official Docs
关于我们
我们是腾讯 Ray  团队， 为公司内的⼤数据和机器学习业务提供规模化的分布式调度与计算
底座。 我们团队的优势是会结合“ GPU  算⼒ + K8s  + Ray  + 训练/推理框架”多层能⼒进⾏
co - design ， 并深度对接平台提供⼀站式的产品化能⼒。
团队⾪属于腾讯 TEG  数据计算平台部，部⻔负责司内统⼀⼤数据和机器学习的数据智能融
合平台建设，为⼤数据、机器学习业务提供全⾯⾼效的 PaaS 平台底座，围绕数据和算⼒，
构建规模化的⼤数据和机器学习融合平台的全栈式服务能⼒。
我们正在 招聘 Ray  分布式调度与 计算⼯程师，感兴趣的 朋友请通
过 graysong @ tencent . com 联系。
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
````

## PDF 第 16 页

[原页](RAW.pdf#page=16)

````text
阅读 8709
留⾔
还没有留⾔，来写⾸评
写留⾔
````


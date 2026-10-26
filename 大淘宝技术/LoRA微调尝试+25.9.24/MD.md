# 一位淘宝工程同学的大模型LoRA微调尝试

来源：[RAW.pdf](RAW.pdf)，capture-001。

这是PDF文本层按物理页码转写，不是AI总结。图片未嵌入；图内文字、截图、公式、表格及代码排版可能未提取或不可靠；源PDF中存在的右侧裁切不补写。实际复核范围详见META.json。

## PDF物理页 1

⼀位淘宝⼯程同学的⼤模型         LoRA微调尝试


原创 ⽤户场景营销技术  ⼤淘宝技术  2025年9⽉24⽇ 01:35浙江 13⼈












 本⽂主要介绍了⼤模型时代下，如何通过 LoRA （Low-Rank Adaptation）这⼀参数⾼
 效微调技术，实现对⼤模型的轻量级定制。⽂章从微调的基本概念出发，详细阐述了
 LoRA 的原理、优势与局限性，并结合本地原⽣实现（Transformers + PEF T）和百炼
 平台两种⽅式，展示了在⼩样本、低资源场景下的实战流程。结果表明，LoRA 能以极低
 的计算成本让通⽤⼤模型有效学习业务知识，显著提升其在特定任务中的表现，真正实现
 “让⼤模型懂业务”，推动 AI 从“可⽤”⾛向“好⽤”。







                        前⾔



如今⼤模型时代，深刻重塑了很多⾏业的业务形态与技术架构。从智能客服到内容⽣成，从代
码辅助到推荐系统，⼤模型正以前所未有的速度渗透到互联⽹技术的各个领域，成为驱动创新
的核⼼引擎。其强⼤的泛化能⼒和上下⽂理解⽔平，使得许多过去需要复杂⼯程与规则设计的
任务，如今只需⼀次“提示”即可完成。




然⽽，尽管⼤模型展现出惊⼈的通⽤能⼒，对⼤多数开发者和业务⽅⽽⾔，它仍是⼀个“⿊盒           ”
——我们只能调⽤其预训练时所掌握的知识与⾏为模式，难以⼲预其内部逻辑，也          ⽆法直接引
导模型适应特定场景的表达习惯、术语体系或业务规则。在⽣产环境中，这种 “能⼒固定          ”的
特性带来了明显的局限：模型输出可能偏离业务预期，难以保证⼀致性，更         ⽆法随业务演进⽽
持续进化。




⾯对这⼀挑战，模型微调（   F ine-tu ning）提供了⼀条关键路径。尤其是以 LoRA 等为代表的
参数⾼效微调技术（  PEF T），在不改变主⼲模型的前提下，仅通过训练少量新增参      数，即可
实现对⼤模型⾏为的精准定   制。这不仅⼤幅降低   了计算成 本与技术 ⻔槛，更 让业 务开发者能 够
基于⾃身积累 的⾼ 质量数据 ，赋予 通⽤⼤模型 “专属 ”的业务理解能⼒。本  ⽂将围绕 LoRA微调
技术展开， 探讨 其在⼩样本 、低资源 场景下的实  践价值，展示如何利  ⽤业务数据  对⼤模型进⾏
轻量级定 制，真正实现 “让⼤模型 懂 业务”，推动 AI 从“可⽤”⾛向“好⽤”，从 “通⽤”迈向“专
属”。

## PDF物理页 2

                          微调



▐  什么是微调



⼤模  型 的微 调（ F ine-tu ning）  ， 是指在⼀个已经 预  训  练好的⼤模  型  （⽐
如 G  PT、 D eepSeek、BERT、Llama等）基础上，针对特定任务、领域或数据进⾏进⼀步  训
练。微调通 常通过在⽬标   数据集上 继续训练模型  权 重，使模型更适应  该任务，从⽽提升   下 游任
务的表现。




简单来说 ，预训练 让模型掌握通⽤知识，微调让模型适应      某 个具体⽤ 例。LLM   微调是⼀个有监
督学习过程，即  有监督  微调(SF T)，通常语⾔模型的初始训练是⽆监督     的，但微调是有监督
的。



▐  微调的分类



按照⽬ 标任务
  标准微调（任务微调）   ：针对某⼀具体任务进⾏微调（如分类、问答、摘要等         ）。
  领域微调：针对某⼀特定领域数据进⾏微调（如医疗、法律、⾦融等          ） 。
  指令微 调： 通过⼤量的「  指令-响应 」数据 集（ 如Alpaca, Baize等）对模型进⾏微调，使
  其能够按照⾃然语⾔指令完成多种任务。




按参数 调整⽅ 式
  全参数微 调（ F u ll-parameterTu ning）：对所有模型参数进⾏更新。
  部分参 数微调（ Repurposing）：只更新部分参数， ⽐如最 后 ⼀层、分 类头等 。
  参数⾼ 效微 调（ParameterEﬃcientF ine-Tu ning, PEFT）：引⼊少量额外可训练参数，
  冻结 原模型 绝⼤部 分参 数，如LoRA、Adapter、Prefix Tu ning等，主要⽬的是⽤很少量
  新参数即实现任务适配。



▐  常⻅微调⽅ 法



全参数 微调
  直接在⽬标数据集上继续训练所有模型参数，效果好但耗资源⼤，对硬件要求⾼，             不易迁

  移。

## PDF物理页 3

参数⾼ 效微 调（ PEFT）
  LoRA（Low-Rank Adaptation）：通过在部分参数上引⼊低秩矩阵，仅训练这些新        增的
  低秩参数，⼤⼤减少训练所需参数量和显存消耗         。

  Adapter：在原有⽹络层之间插⼊⼩型新⽹络模块并仅训练这些模块参数。
  PrefixTu ning / PromptTu ning：在输⼊或模型内部插⼊可训练的参数向量（  前 缀、提
  示） ，主⽹络参数保持不变    。





                          LoRA微调




▐  什么是 LoRA



LoRA(Low-RankAdaptationof LLM  s)，即 LLM  s的低秩适应，是参数⾼效微调最常⽤的⽅
法。



▐  原理



LoRA的核⼼思想是：冻结预训练的基座模型（         Base M  odel），在其某些层（如注意⼒中
的 Q、K、V 投影）上，额外添加低秩矩阵（      A和 B）作为可训练参数，⽤于学习任务特       定的增
量调整 。
  原始基座模型的权重 全程保持冻结、未修改。
  训练过程中，只有 LoRA 引⼊的少量新增参数（       如 lora_A, lora_B）被更新。
LoRA的本质就是⽤更少的训练参数来近似 LLM      全参数微调所得的增量参数，从⽽达到        使⽤更
少显存占⽤的⾼效微调。




LoRA的核⼼思路就是，直接 freeze基座模型的全部参数，然后额外给模型增加⼀个扰动
的 modu le，来模拟 finetu ne 之后参数改变的效果。如此⼀来，只要这些扰动的 modu le参
数量够 ⼩且推 理 够 快 ，就不会影响模 型 整 体的 inference 成 本 ，且可 以⼤幅 地缩减 模
型 finetu ne的开销，因为我们只需要训练极⼩量的⼀部分参数即可       。




基座模型只参与训练过程中的前向传播，反向传播更新参数的只有 LoRA             的插⼊的adapter参
数。

## PDF物理页 4

  保留原来预训练   好的权 重 W不动；
  旁路 插⼊⼀个低秩矩阵 BA   ，对 W  的输出做⼀个可  学习的微 ⼩ 增量；
  只训练 A 、B 这两组 很⼩ 的参数， 就能 让模型适  配新任务。




上⾯是简化  的示意图 ，实 际 的 Transformer由很多线性投影（ 如 Q、K、V、O、F F N 的W₁、
W₂ 等）组成， 每个都是⾃  ⼰ 的 d₁ × d₂ 矩阵。 LoRA 是把这些⼤矩阵 W  逐个冻结，然后在
它们上 ⾯叠 加⼀个低秩增量 ΔW    =  BA。 因此，严格来说  是对模型  ⾥的每个⼤矩   阵 都做 ⼀
次 rank =  r（远⼩于 d₁, d₂）的低秩更新。




训练省资源的根本原因
  原来若 要微调 W ，需要存和反向传播 d₁·d₂ 个参数；

  LoRA只训练 A(r × d₂)和 B(d₁ × r)，参数量变成 2·r·max(d₁,d₂)，当 r≪ min(d₁, d₂) 时
  可省 100× 乃⾄ 10 000× 的显存和梯度计算 ；
  W冻结 → 不 必存动量/ 梯度 ， 也不⽤进⾏前后   两次 matmu l⽐较差分，⼤幅  降低显 存与算
  ⼒。




  推理 过程



核⼼机制：  权重增量叠加  （W eight Addition）。

LoRA（Low-RankAdaptation）在推理时，并不是“绕道 ”或“替换”，⽽是：  将 LoRA学习到
的增量权重，加到原始预训练模型的对应权重上。
数学表达：
对于⼀个原始权  重 矩阵  W∈Rd×kW∈ Rd×k，LoRA引⼊低秩分  解：

ΔW = AB其中 A∈Rd×r , B∈Rr×k , r≪dΔW=AB其中  A∈Rd×r, B∈Rr×k, r≪d

## PDF物理页 5

推理时的实  际权重为：

W new=W+ΔW=W+ABWnew=W+ΔW=W+AB

然后使⽤ W newWnew进⾏前 向计算 。




两种推 理模 式：


        模式                  说明                 特点


1. 推理时动态叠加（On-the   加载原始模 型 + LoRA 权    可⽤，但慢
fly）                重，实时计算 W +ΔW W +ΔW

2. 合并后推理（M  ergedInfe将 LoRA 权重 合并到原始模   推理更快、更稳定
rence）              型中，⽣成⼀个新模型，直
                    接推理

⼀般采⽤合并后⽣成新的模型来进⾏推理，同时可以保留原始模型。




  优劣势



LoRA 的优势



优势        说 明


资源成本低     仅需训练少量参数（    如 QKV投影层），  节省 G  PU显存和算⼒


训练速度快     梯度计算集中在⼩模块，训练效率显著提升


          ⼀个基础模型 + 多个 LoRA  权重（ 每个⼏ M  B~⼏百 M  B），便于版本管理
存储友好      和部署



灵活 切换任    可动态加载不同 LoRA   权重，实现多业务场景快速切换

务


保护原始模
          原模型冻结，避免灾难性遗忘，保证通⽤能⼒
型





LoRA 的局限性


劣势            说 明

## PDF物理页 6

 性能略低于全参数        在复杂任务上可能稍逊于全量微调，但差距通常可控（               <5%）
 微调


 依赖基础模型质量        LoRA⽆法修复基础模型的根本缺陷，微调效果受限于预训练能⼒


 适配层选择敏感         效果受插⼊位置（如仅 attention    、F F N等）影响，需实验调优


 推理需额外集成         需⽀持 LoRA  加载的推理框架（如 H  u ggingF ace + PEF T、vLLM、lla
                 ma.cpp等）





▐  实战




LoRA微调⽬前有多 种 ⽅     式实 现 ， Transformers + PEF T原⽣实 现 ， LLaM  A-F actory、
Axolotl等框 架实 现 ， 以 及 借 助 百 炼 等 封装好的可    视 化界⾯ 平 台   实 现。本  ⽂ 主 要 尝 试
了 Transformers + PEF T原⽣实现，以  及公司⽣产   中更有可能⽤到的百炼平       台 实现 。




  原 ⽣ 微调




使⽤ Transformers + PEF T原⽣实现。




环境 搭建

1. transformers+peft+datasets

注意：  ⼏个库  的版本之间    有协同  关系，随意安装版本       可能导致不    兼 容问题，可在H  u gging
F ace的官⽅⽂ 档 中查看  推荐 版本 。

代码 ：


 1 pip install --upgrade torch==2.1.0+cpu torchvision==0.16.0+cpu --index-
 2 pip install -U transformers==4.38.2 peft==0.10.0 datasets==2.18.0 \
 3             accelerate sentencepiece safetensors tqdm



2. 模型准备

这⾥考虑  到微调是在     mac本地运  ⾏，  算⼒有限，所以使⽤了       较⼩ 的 D eepSeek-R1-D istill-

Qwen-1.5B作为基座  模型。使⽤ H  u gging F ace或 M  odelscope等下载模型到 本地 即可  。




数据 处理
训练数据：
准备好数据   ⽂件 lora_seckill_qa.jsonl，格式使⽤如下 instru ction-response格式。

## PDF物理页 7

  1 {"instrucAon":   "埋点时主要记录哪些事件？           ","response":"  使⽤的是    xx埋点框架，埋点有分
 2  {"instrucAon":   "xxxxxxxxxxxxxxxxxx   ？ ","response"  :"xxxxxxxxxxxxxxx"   }



处 理 脚 本 ：


   1  import json
   2  from datasets import Dataset
   3  from transformers import AutoTokenizer
   4  # 正确读取    jsonl
   5  with open( "lora_seckill_qa.jsonl"    , "r", encoding=   "utf-8" ) as f:
   6  raw_data = [json.loads(line) for line in f if line.strip()]
   7  # 如果是单轮格式可直接⽤
   8  # dataset = Dataset.from_list(raw_data)
   9  # 若是  conversation 格式（如       [{"conversation":[...]}]），需展开
  10  def conversation_to_list(item):
  11  out = []
  12  for turn in item[  "conversation"]:
  13  instr = turn.get(  "system"  , "") +  "\n"  + turn["input"  ] if
  14  turn.get( "system" ) else turn[  "input"  ]
  15  out.append({
  16  "instruction"  : instr.strip(),
  17  "response" : turn[ "output"  ].strip()
  18  })
  19  return out
  20  # 如果你的    raw_data 已经是单轮格式就跳过这⼀段
  21  all_samples = []
  22  if "conversation"   in raw_data[0]:
  23  for d in raw_data:
  24  all_samples.extend(conversation_to_list(d))
  25  dataset = Dataset.from_list(all_samples)
  26  else:
  27  dataset = Dataset.from_list(raw_data)
 28
  29  # 保存分词器
 30   tokenizer = AutoTokenizer.from_pretrained(
  31  "/Users/shawn/Documents/AI-dev/models/deepseek/deepseek-ai/DeepSeek-R1
  32  Distill-Qwen-7B",
 33   trust_remote_code=True,
 34   local_files_only=True
 35   )
 36   tokenizer.save_pretrained(    "./tokenizer")
  37  # 保存处理后的数据集
 38   dataset.save_to_disk(   "./processed_dataset_ms"    )
 39   print( "预处理完成，已保存！         ")

## PDF物理页 8

训练参数
训练脚   本 ：


   1  import torch
   2  from datasets import load_from_disk
   3  from transformers import AutoTokenizer, AutoModelForCausalLM,
   4  TrainingArguments, Trainer, default_data_collator
   5  from peft import get_peft_model, LoraConfig
   6  import random
   7  # 1. 加载数据集
   8  dataset = load_from_disk("./processed_dataset_ms"         )
   9  # 2. 样本随机打乱
  10  dataset = dataset.shuffle(seed=42)
  11  # 3. 分词器
  12  tokenizer = AutoTokenizer.from_pretrained(        "./tokenizer", local_files_o
  13  def generate_and_tokenize_prompt(batch):
  14  texts = [
  15  f"""<s>### Instruction:
  16  {instruction}
  17  ### Response:
  18  {response}
  19  </s>"""
  20  for instruction, response in zip(batch[       "instruction"],
  21  batch["response"   ])
  22  ]
  23  out = tokenizer(
  24  texts,
  25  max_length=256,
  26  padding= "max_length",
  27  truncation=True,
  28  add_special_tokens=False,
  29  return_tensors=None,
  30  )
  31  # Loss  忽略  paddingp.
  32  out[ "labels" ] = [
  33  [tok if tok != tokenizer.pad_token_id        else  -100 for tok in label]
  34  for label in out["input_ids"]
  35  ]
  36  return out
  37  tokenized_dataset = dataset.map(
  38  generate_and_tokenize_prompt,
  39  batched=True,
  40  remove_columns=dataset.column_names,
  41  desc="Tokenizing"
  42  )

## PDF物理页 9

43  # 4.  加载基座模型（如设备有限可指定              CPU/其他  device ）
44  model = AutoModelForCausalLM.from_pretrained(
45  "/Users/shawn/Documents/AI-dev/models/deepseek/deepseek-ai/DeepSeek-R1
46  Distill-Qwen-7B",
47  torch_dtype=torch.bfloat16,      # MPS、 A100 等建议⽤     bfloat16
48  local_files_only=True,
49  trust_remote_code=True
50  )
51  # 5. LoRA   配置
52  lora_config = LoraConfig(
53  r=8,
54  lora_alpha=16,
55  target_modules=["q_proj"    , "v_proj",   "k_proj" , "o_proj"  ],
56  lora_dropout=0.05, #    或 0,  稳定死记记忆；推荐⼩数据降            dropout
57  bias= "none",
58  task_type=  "CAUSAL_LM"
59  )
60  model = get_peft_model(model, lora_config)
61  model.print_trainable_parameters()
62  # 6.  训练参数
63  training_args = TrainingArguments(
64  output_dir="./results_ms"    ,
65  per_device_train_batch_size=2,
66  gradient_accumulation_steps=1,
67  learning_rate=3e-4,
68  num_train_epochs=8,
69  logging_dir="./logs_ms",
70  save_steps=100,
71  save_total_limit=3,
72  logging_steps=10,
73  overwrite_output_dir=True,
74  report_to=None,
75  fp16=False
76  )
77  trainer = Trainer(
78  model=model,
79  args=training_args,
80  train_dataset=tokenized_dataset,
81  data_collator=default_data_collator,
82  )
83  # 7.  训练与⾃动采样输出
84  trainer.train()
85  # 8.  保存模型与    tokenizer
86  model.save_pretrained(    "./deepseek-7b-lora_ms"    )
87  tokenizer.save_pretrained("./deepseek-7b-lora_ms")
88  print( "训练完成。     ")

## PDF物理页 10

 89






参数 解析
LoRA配置 参数（ lora_config）
1. r= 8
  含义 ： LoRA中低秩矩阵的秩    （rank），⽤于近似   原始权重矩阵   。
  作⽤：  控制新增参数量，显     著降 低训练显存消耗    。

  影响：
    r太⼩ → ⽋ 拟合 ，表 达能⼒不  ⾜
    r太⼤ → 接近 全量微调，   失去 LoRA 优势
  常⻅值  ：4~ 64，根据任务  复杂度  调整（如简单任务⽤ r= 8   ， 复杂任务可⽤ r= 32 ）




2. lora_alpha= 16
  含义：  LoRA权重的缩放因⼦，控制低秩矩阵对输出的影响强度。
  作 ⽤： 调节LoRA 分 ⽀的贡 献程度  ，类 似 “学习率 系数”。
  影响：
    推荐保持 alpha / r≥ 1（如 r= 8, alpha= 16→ ⽐值为 2）
    值过⼤ → 容易过拟合；值过⼩ → 影响微弱
  建议：初试设置 alpha =  2  × r



3. target_modu les= ["q_proj","v_proj","k_proj","o_proj"]
  含义：指定在哪些模块上应⽤ LoRA       （通常是注意⼒层的投影层       ）。
  作⽤：精准控制适配范围，节省计算资源。
  常⻅选择：
    LLaM  A系列：["q_proj", "k_proj", "v_proj", "o_proj"]
    BERT类： ["qu ery", "valu e", "key", "dense"]
  影响：
    仅作⽤于部分模块 → 可能限制模型适应能⼒
    可根据模型结构扩展（     如加⼊ u p_proj, down_proj）



4. lora_dropou t= 0.05

  含义：  LoRA层的 D ropou t概率，⽤于正则化。
  作⽤：防⽌过拟合，提升泛化能⼒。
  影响：
    值越⼤ → 正则化越强
    ⼩数据集建议：   0.1~ 0.2
    ⼤数据集可设为 0   或 0.05
  注意：若训练不稳定，可尝试增加 dropou t

## PDF物理页 11

5. bias= "none"
  含义：是否在 LoRA    层中引⼊偏置项。
  选项：
    "none"：不加偏置（推荐起点      ）
    "all"：所有模块加偏置
    "lora_only"：仅 LoRA层加偏置
  影响：
    加偏置可能略微提升效果，但增加参数量
  建议：从 "none" 开始，效果不佳再尝试 "lora_only"



6. task_type= "CAU SAL_LM  "
  含义：指定任务类型，影响损失函数和标签处理⽅式。
  常⽤类型：
    "CAU SAL_LM  "：⾃回归语⾔模型（    如 G  PT、LLaM  A⽣成任务 ）
    "SEQ_CLS"：序列分类（如情感分析        ）
    "TOKEN_CLS"：  Token级分类（如命名实体识别）
    "SEQ_2_SEQ_LM  "：Seq2Seq任务（如翻译、摘要      ）
  注意：必须与任务匹配，否则训练会出错




训练参数（   training_args）


 参数                          值                说明


 ou tpu t_dir                "./resu lts_ms"  保存模型检查点、⽇志等⽂件
                                              的⽬录

 per_device_train_batch_size  2               每个设备上的 batchsize，显
                                              存不⾜时可减⼩


                                              梯度累积步数，等效增⼤ batc
 gradient_accu mu lation_steps 1              hsize（如设为 4 → 实际 batc
                                              h =  8）

                                              学习率，  LoRA推荐范围   ：
 learning_rate               3e-4
                                              1e-4~1e-3

 nu m_train_epochs            8               训练轮数，⼀般从 3~10    开 始调
                                              整

                                              ⽇志保存路径，可⽤于
 logging_dir                 "./logs_ms"
                                              TensorBoard可视化

## PDF物理页 12

                                               每隔多少 step  保存⼀次
 save_steps                   100
                                               checkpoint


 save_total_limit              3               最多保留⼏个 checkpoint，    ⾃
                                               动删除旧的


 logging_steps                10               每隔多少 step  输出⼀次⽇志，
                                               便于监控


 overwrite_ou tpu t_dir       Tru e            若⽬录存在则覆盖，避免⼿动
                                               清理

                                               不连接远程报告⼯具（       如
 report_to                    None
                                               wandb 、tensorboard）

                                               是否启⽤ F P16半精度训练
                                               ✅  ⽀持设备建议开启（节省显
 fp16                         F alse           存 + 加速）

                                               ⚠  若开启需确保模型



 场景                                  建议配置

 ⼩数据集微调                              r= 8, alpha= 16, dropou t= 0.1, epochs= 5~
                                     10

 ⼤数据集微调                              r= 16~32, alpha= 32, dropou t= 0.05 , lr= 2
                                     e-4

 显存受限                                减⼩ batch_size，启⽤ fp16，使⽤ gradien
                                     t_accu mu lation

 快速实验                                overwrite_ou tpu t_dir= Tru e, logging_ste
                                     ps= 10, save_steps= 50




训练成  本

使⽤ 1000条 左 右数据  微 调qwen3-14b 的模 型 ， ⼀次训  练 成 本预 计 10元左  右 。可 以 看 到模型微
调本 ⾝ 的成本并不    算很⾼，即使    换参数量更⼤的模型以        及更多的数据。后续的部        署 、推理成本
才是⼤头。

## PDF物理页 13

测试脚   本


   1  import torch
   2  from transformers import AutoModelForCausalLM, AutoTokenizer
   3  from peft import PeftModel
   4  # 路径设置
   5  BASE_PATH =   "/Users/shawn/Documents/AI-dev/models/deepseek/deepseekai/
   6  DeepSeek-R1-Distill-Qwen-7B"
   7  LORA_PATH =   "./deepseek-7b-lora_ms"
   8  # 加载分词器
   9  tokenizer = AutoTokenizer.from_pretrained(
  10  BASE_PATH,
  11  local_files_only=True,
  12  trust_remote_code=True
  13  )
  14  # === 严格分离模型实例         ===
  15  # 原始模型
  16  model_base = AutoModelForCausalLM.from_pretrained(
  17  BASE_PATH,
  18  device_map=  "mps" ,
  19  torch_dtype=torch.bfloat16,
  20  local_files_only=True,
  21  trust_remote_code=True
  22  )
  23  # 微调后的模型（       Base + LoRA 适配器）
  24  model_base_for_lora = AutoModelForCausalLM.from_pretrained(
  25  BASE_PATH,
  26  device_map=  "mps" ,
  27  torch_dtype=torch.bfloat16,
  28  local_files_only=True,

## PDF物理页 14

29  trust_remote_code=True
30  )
31  model_lora = PeftModel.from_pretrained(
32  model_base_for_lora,
33  LORA_PATH
34  )
35  def format_prompt_one_round(user_input: str) -> str:
36  return f"<s>### Instruction:\n{user_input}\n### Response:\n"
37  def generate_single(model, prompt, tokenizer, max_new_tokens=200):
38  inputs = tokenizer(prompt, return_tensors="pt")
39  for k, v in inputs.items():
40  inputs[k] = v.to(model.device)
41  with torch.no_grad():
42  outputs = model.generate(
43  **inputs,
44  max_new_tokens=max_new_tokens,
45  temperature=0.7,
46  top_p=0.9,
47  do_sample=True,
48  eos_token_id=tokenizer.eos_token_id
49  )
50  full_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
51  reply = full_output[len(prompt):]
52  # 截断下⼀个分隔符，保证只输出新⽣成内容
53  for sep in ["<s>"  , "</s>"  , "###" ]:
54  if sep in reply:
55  reply = reply.split(sep)[0]
56  return reply.strip()
57  def main():
58  print( "="*40)
59  print( "DeepSeek 模型微调前      /后  单轮对话对⽐（严格模型物理分离版）                ")
60  print( "="*40)
61  print( "输⼊exit   退出。   \n" )
62  while True:
63  user_input = input("你说：      ").strip()
64  if user_input.lower() in {"exit"     , "quit" }:
65  print( "对话结束   ~  再⻅！   ")
66  break
67  prompt = format_prompt_one_round(user_input)
68  # 原始模型推理
69  base_reply = generate_single(model_base, prompt, tokenizer)
70  # LoRA 微调后模型推理
71  lora_reply = generate_single(model_lora, prompt, tokenizer)
72  print( "\n-------------------------------"     )
73  print( "【原模型     输出】  ↓\n"  + base_reply)
74  print( "\n【微调后输出】       ↓\n" + lora_reply)

## PDF物理页 15

 75  print("-------------------------------")
 76  if __name__ == "__main__":
 77  main()
 78






测试 结 果 case：

可以 看 到原模型完全    ⽆法  感知到业务   相关的知识，⽽微调后       的模型   已经 有效的学到了（     注 ： 由
于数据  量⼩ ， 且模型  本身 参数量也   ⼩ ， 做演示的微调结果存在⼀定的过         拟合  ）















  百 炼 平台 微 调




数据 准 备
根据 百炼 的训练数据示     例格式准备数据































百炼训练数据格式



  1 {“messages": [{"role": "system", "content": "You are a professional e-c
  2 title analyst. Given a long product title, output ONLY the core product

## PDF物理页 16

  3  name (1-5 words) without any other text."}, {"role": "user", "content"
  4  商品标题中提取最核⼼的商品主体，直接输出主体名，不要加其它词：【⿊旗】⼼语⾁松原味辣
  5  味1kg 烘焙⾯包蛋糕寿司原料商⽤⾁松⼩⻉           "}, {"role": "assistant", "content": "⾁
  6  "}]}
  7  {"messages": [{"role": "system", "content": "You are a professional e-c
  8  title analyst. Given a long product title, output ONLY the core product
  9  name (1-5 words) without any other text."}, {"role": "user", "content"
 10  列商品标题中提取最核⼼的商品主体，直接输出主体名，不要加其它词：夏季⽵枕⽚成⼈藤凉席冰
 11  丝枕头套单⼈⼉童⽵枕席藤枕芯套⼀对拍           2"}, {"role": "assistant", "content": "枕






训练 参 数



























参数跟原⽣实现的参数基本⼀致，可以参考上述的训练参数解析及百炼的⽂                          档。




评测
1. 创建评测  数据 集
创建 ⽅ 式同  训练数据，使⽤     百炼  模 版

## PDF物理页 17

2.选择评测⽅式，开始评测
有三种评测⽅式
 ⼈⼯评 测
特点：经过⼈⼯校验打 分，在很多应⽤ 场景下是相对准确 的；同时⽐较主 观，在⼀些场景下 可
能不够标准化，且⼈⼒消耗 较⾼。






























 模型评 测

## PDF物理页 18

特点：适 合评测⽂ 本⽣ 成类，可以调整 prompt 来对⾃⼰ 微调后模型的回  答要点 进⾏打 分，利
⽤另⼀个⼤模型的能⼒，实现    灵活打 分，但是⽐较依赖  模型的能⼒以  及 prompt，同时分数有
时也不够标准化  。

## PDF物理页 19

 基线评 测
通过预置的算 法来对模型的特定⽅向能⼒进⾏标准化评   测。































⼿动测试结果
左侧为微调后的模型， 右侧 为原始模型，其对商品主体  识别的能⼒得 到提升。

## PDF物理页 20

                        总结




LoRA（Low-RankAdaptation）微调技术为业务开发场景提供了⾼效、低成本的⼤模型 定制
化路径， 展现出显 著优势：
  训练成本低，效果出⾊
   显存占 ⽤少：仅需微调少量新增参数，可在消费级 G  PU  上完成训练， 降低硬件⻔ 槛 。
   训练速度 快：参数更新量⼩  ，⽀持 快速迭代，适 合业务 团队敏捷试错 。
   性能接近全 量微调：在多种任务中表现   优异 ，效果逼近全 参数微调，性价⽐极  ⾼
  部署灵活，易于管理
   适配器轻 量化： LoRA 权重⽂件通常仅⼏⼗ M  B，便于存储、传输与版本 管理。
   多任务 共享主⼲： ⽀持“⼀个基础 模型 + 多个 LoRA适配器”的模式，实现不 同业 务线
   共⽤底座 模型，提升资源利  ⽤率。
  稳定可靠，⻛险可控
   缓解过 拟合：在⼩样本  场景下表现更 稳 定，有效 避免全 参数微调带来的灾  难性遗忘或
   过拟合问题。
   保护原始模型：不  修改主⼲参数，仅通过   低秩增量进⾏适  配，提升 模型 鲁棒与可维护
   性。




核⼼价值 ：让⼤模 型真正“懂业 务”
LoRA 微调的轻量与⾼效，使得业务开发者能   够基于⾃身积累   的⾼质量业务数据  （如客服对
话、商品描述 、内部 流程⽂ 本等），对⼤模型进⾏   快速定制化训练。这不仅⼤幅降低    了 AI 落

地的技术 ⻔槛，更 让模型输出更可  控、更精准、更  贴近 实际业务需 求。未来，我们  将 持续探
索 LoRA在真实业务场景中的应⽤，  例如智能推荐、⾃  动化⽂ 案⽣成、研发提效等⽅  向，以数
据驱动 + 模型微调的⽅式，助⼒业务增⻓与技术   升级。

## PDF物理页 21

                                参考资料




  LoRA:Low-RankAdaptationofLargeLangu ageM  odels：
  https://arxiv.org/abs/2106.09685

  QLoRA: Efficient F inetu ning of Qu antized LLM  s：https://arxiv.org/abs/2305.14314

  P-Tu ningv2:PromptTu ningCanBeComparabletoF ine-

  tu ningUniversallyAcrossScalesandTasks：https://arxiv.org/abs/2110.07602

  ⽂献阅读：    LoRA: Low-RankAdaptationofLargeLangu ageM  odels：
  https://blog.csdn.net/codename_cys/article/details/135318389?
  spm= 1001.2014.3001.5502

  ⼤模型炼丹术：⼤模型微调总结及实现：             https://zhu anlan.zhihu .com/p/673789772

  ⼤模型⾼效微调-LoRA      原理详解和训练过程深⼊分析

  ： https://zhu anlan.zhihu .com/p/702629428

  百炼官⽅⽂档：https://bailian.console.aliyu n.com/?tab= doc#/doc/?
  type= model&u rl= 2844735





                                团队介绍




本⽂作者霄杨，来⾃淘天集团-⽤户场景营销技术团队。⼀⽀专注于探索AI等前沿技术与营销
业务技术的融合，深度结合⽤户场景与营销业务的技术团队。依托⼤淘宝丰富的⽤户⽣态和多
元化的消费场景，致⼒于通过技术创新提升⽤户体验，优化个性化营销能⼒，助⼒业务持续增
⻓。通过AI驱动的精准推荐、场景化表达与动态策略调控，我们为⽤户创造更⾃然、更智能的
购物旅程，为营销业务提供⾼效、敏捷的技术⽀撑，助⼒淘宝构建以⽤户为中⼼的全域营销技
术体系。我们坚信技术是连接⽤户与价值的桥梁，持续探索创新边界，让营销更懂⽤户，⽤技
术点亮每⼀个关键⽤户体验瞬间。







                               ¤ 拓展阅读    ¤



                      3DXR技术   | 终端技术    |  ⾳视频技术

                      服务端技术     |  技术质量   |  数据算法

## PDF物理页 22

     ⼤淘宝技术
     ⼤淘宝技术官⽅账号
     968篇原创内容


 公众号









阅读 7130





留⾔


写留⾔





                      还没有留⾔，来写⾸评

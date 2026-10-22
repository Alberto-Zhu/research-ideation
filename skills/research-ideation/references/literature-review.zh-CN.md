# 科研构思与创新机制：文献调研及 skill 转化

[English](literature-review.md) | **简体中文**

核验日期：2026-10-22。范围为文献驱动的科研构思、类比迁移、候选演化，以及构思质量与执行效用评估。
这是按方法相关性选取的研究综述，不是穷尽性系统综述。仅使用论文、官方会议页面、作者代码及原始摘要作为技术依据。
审阅深度明确区分方法章节与摘要；未将无法访问的正文记为已精读。机器可读条目见 [bibliography.json](bibliography.json)。

## 目录

1. 方法谱系
2. 十三篇核心工作
3. 关键取舍
4. 本 skill 的综合设计
5. 使用边界

## 1. 方法谱系

| 方法线 | 代表工作 | 在 skill 中的对应操作 |
|---|---|---|
| 文献证据与近邻限制 | P01、P02、P03、P04 | 证据账本、近似方法、具体失败机制 |
| 跨领域结构迁移与facet组合 | P01、P05、P07、P13 | 共享结构、适配操作、失效边界 |
| 研究轨迹与候选演化 | P06、P08 | 演进链、匿名对比、有上限的修订 |
| 实验执行与可靠性 | P09、P11、P12 | 最小鉴别实验、预算和停止规则 |
| 人类/模型评估边界 | P01、P10、P11 | 独立评审、可行性分离、保留不确定性 |

## 2. 十三篇核心工作

### P01 · IdeaScientist: Orchestrating Agents for Grounded Scientific Ideation

- 作者与版本：Jiarui Liu et al.；arXiv preprint, v2 (2026-10-09)。
- 原始来源：[论文 / 官方页面](https://arxiv.org/abs/2610.04074v2)。
- 本次核验深度：full_text_sections。
- 核心内容：分阶段产物与人类论文重建参考支持各角色训练；主结果评估科研方案，未执行方案实验。
- 转化为操作：阶段化证据与机制迁移；借鉴流程，不声称复现GRPO训练。

### P02 · SciMON: Scientific Inspiration Machines Optimized for Novelty

- 作者与版本：Qingyun Wang, Doug Downey, Heng Ji, Tom Hope；ACL 2024。
- 原始来源：[论文 / 官方页面](https://aclanthology.org/2024.acl-long.18/)。
- 本次核验深度：abstract。
- 核心内容：检索已有论文作为灵感，再反复对照先前工作修订候选想法。
- 转化为操作：将新颖性检索设为反复执行的检查，而非一次自评。

### P03 · ResearchAgent: Iterative Research Idea Generation over Scientific Literature with Large Language Models

- 作者与版本：Jinheon Baek et al.；NAACL 2025。
- 原始来源：[论文 / 官方页面](https://aclanthology.org/2025.naacl-long.342/)。
- 本次核验深度：abstract。
- 核心内容：从核心论文出发，通过论文关系和共享实体扩展知识，并由评审反馈迭代问题、方法与实验。
- 转化为操作：先找到近邻文献和概念，再分离生成与评审。

### P04 · SciPIP: An LLM-based Scientific Paper Idea Proposer

- 作者与版本：Wenxiao Wang et al.；arXiv preprint, v2 (2025-02-17)。
- 原始来源：[论文 / 官方页面](https://arxiv.org/abs/2410.23166v2)。
- 本次核验深度：full_text_sections。
- 核心内容：结合语义、关键词与共现关系检索；将文献驱动生成与模型内部知识驱动生成整合。
- 转化为操作：用多类检索和不同生成路线扩大覆盖，最终逐一补齐证据。

### P05 · Human-LLM Compound System for Scientific Ideation through Facet Recombination and Novelty Evaluation

- 作者与版本：Marissa Radensky et al.；arXiv preprint, v7 (2026-05-16); Scideator。
- 原始来源：[论文 / 官方页面](https://arxiv.org/abs/2409.14634v7)。
- 本次核验深度：full_text_sections。
- 核心内容：围绕目的、机制、评估三个facet组织文献与想法，并按概念距离检索类比文献。
- 转化为操作：按结构化facet组合机制；避免仅交换领域名。记录论文标题随版本变化。

### P06 · Chain of Ideas: Revolutionizing Research Via Novel Idea Development with LLM Agents

- 作者与版本：Long Li et al.；Findings of EMNLP 2025。
- 原始来源：[论文 / 官方页面](https://aclanthology.org/2025.findings-emnlp.477/)。
- 本次核验深度：abstract。
- 核心内容：按研究演进链组织文献，帮助理解方法如何逐步解决限制，并提出Idea Arena评估协议。
- 转化为操作：整理最近方法的限制与后继改进链；比较候选时统一细节。

### P07 · MOOSE-Chem: Large Language Models for Rediscovering Unseen Chemistry Scientific Hypotheses

- 作者与版本：Zonglin Yang et al.；ICLR 2025; arXiv v6 (2025-10-27)。
- 原始来源：[论文 / 官方页面](https://arxiv.org/abs/2410.07076v6)。
- 本次核验深度：abstract。
- 核心内容：将假设发现分成灵感检索、假设组合和质量排序；在51篇化学论文形成的基准上进行重发现评估。
- 转化为操作：分开检查灵感质量、组合逻辑与排序；相似重发现不等于新实验成功。

### P08 · Accelerating scientific discovery with Co-Scientist

- 作者与版本：Juraj Gottweis et al.；Nature, published 2026-05-19。
- 原始来源：[论文 / 官方页面](https://www.nature.com/articles/s41586-026-10644-y)。
- 本次核验深度：full_text_sections。
- 核心内容：专门角色生成、反思、排名、演化与聚类假设，以竞赛反馈和元评审改进后续搜索。
- 转化为操作：采用有限轮候选演化、去重和批评汇总；不将Elo当成科学真值。

### P09 · The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search

- 作者与版本：Yutaro Yamada et al.；arXiv preprint, v1。
- 原始来源：[论文 / 官方页面](https://arxiv.org/abs/2504.08066v1)。
- 本次核验深度：abstract。
- 核心内容：贯通假设、实验、分析与论文写作，以实验管理角色和渐进式树搜索探索方案。
- 转化为操作：将入选构思交接到小规模实验；保留执行日志与失败分支。

### P10 · Can LLMs Generate Novel Research Ideas? A Large-Scale Human Study with 100+ NLP Researchers

- 作者与版本：Chenglei Si, Diyi Yang, Tatsunori Hashimoto；ICLR 2025。
- 原始来源：[论文 / 官方页面](https://proceedings.iclr.cc/paper_files/paper/2025/hash/ea94957d81b1c1caf87ef5319fa6b467-Abstract-Conference.html)。
- 本次核验深度：abstract。
- 核心内容：在特定受控人类评测中，LLM方案被评为更新颖，但可行性略弱。
- 转化为操作：分开评估新颖性与可行性；不将结果推广为所有领域的结论。

### P11 · The Ideation-Execution Gap: Execution Outcomes of LLM-Generated versus Human Research Ideas

- 作者与版本：Chenglei Si, Tatsunori Hashimoto, Diyi Yang；ICLR 2026; arXiv first posted 2025。
- 原始来源：[论文 / 官方页面](https://arxiv.org/abs/2506.20803)。
- 本次核验深度：abstract。
- 核心内容：43位专家执行随机分配的想法；LLM想法执行后的评审下降更大，初始优势缩小。
- 转化为操作：每个核心机制必须附最小鉴别实验、反证条件和停止规则。

### P12 · ResearchGym: Evaluating Language Model Agents on Real-World AI Research

- 作者与版本：Aniketh Garikaparthi, Manasi Patwardhan, Arman Cohan；ICLR 2026 Agents in the Wild Workshop; arXiv v2。
- 原始来源：[论文 / 官方页面](https://arxiv.org/abs/2602.15112v2)。
- 本次核验深度：abstract。
- 核心内容：在固定数据、评估与基线的容器任务中评测完整科研，揭示长程执行的可靠性与资源管理问题。
- 转化为操作：固定评估边界并安排有信息增益的小实验；保留超时和失败结果。

### P13 · SciAgents: Automating Scientific Discovery Through Bioinspired Multi-Agent Intelligent Graph Reasoning

- 作者与版本：Alireza Ghafarollahi, Markus J. Buehler；Advanced Materials 37, e2413523。
- 原始来源：[论文 / 官方页面](https://doi.org/10.1002/adma.202413523)。
- 本次核验深度：primary_search_abstract_only。
- 核心内容：结合本体知识图谱、语言模型和多智能体推理，探索生物启发材料中的跨学科联系。
- 转化为操作：可选用概念与机制关系图辅助跨域检索；关系存在不能直接证明因果或可迁移。

## 3. 关键取舍

**检索充分性与创新距离。** 只检索同一任务，容易得到常规延伸；只检索远域，容易忽略已有近邻方法。
因此先读近邻确认空白，再按共享挑战检索远域，最后回到目标领域查重（P01–P05）。
“语义距离远”不自动构成创新，必须指出缺失的关键技术步骤。

**生成多样性与可执行性。** 结合多条生成路线可以增加候选覆盖；竞赛排名和评审也可能偏好表达成熟的方案。
因此按技术操作去重，统一比较细节，单独评审资源和数据假设（P04、P06、P08、P10）。
预算档位、候选数和0–4分rubric是本skill的工程默认，不是文献中的通用最优值。

**方案评分与实际效用。** IdeaScientist的主要实验比较构思方案；其同骨干Base与Trained总体分数为73.5和74.6，
对照DeepScientist为60.6。由此可见流程有重要贡献，RL的额外收益需与流程收益区分。
P11和P12进一步提示：在执行中，假设质量、资源管理、实现和评估可靠性都会影响结果。
因此将proposal_only、preliminary_validated、independently_validated分开；所有预测都配反证条件。

**受控检索与记忆污染。** P01和P07采用时间控制的重发现设计，但检索截止日期与模型参数知识是不同边界。
进行回溯评测时应报告模型知识风险，并隐藏目标方法及结果；普通科研检索应覆盖当前文献。

**分角色与真正独立。** 分工能使中间产物可检查；一个模型顺序扮演角色仍不等于独立盲评。
本skill同时支持单智能体与可选独立角色，并要求如实标记独立性。
它不需要重新训练角色、构建百万论文库或部署指定模型。

## 4. 本 skill 的综合设计

1. 固定问题、输入输出、资源和评估契约。
2. 保留检索记录和带定位的来源证据。
3. 从近邻方法推导普通方案，在候选生成前冻结。
4. 用结构迁移、facet组合、假设变化与简化等不同路线生成机制。
5. 分别评估新颖性、证据、逻辑、可行性和可检验性。
6. 用最小鉴别实验区分新机制与简单替代解释。
7. 保留否定意见、失败候选和实际验证状态。

以上为面向本地智能体的原创流程综合。引用用于说明设计依据；没有复制或分发论文全文、作者代码或训练权重，
也没有声称这一组合已经经过论文级实验验证。

## 5. 使用边界

调用时重新检索当前任务的近邻工作。本调研不替代领域专家核验，也不构成新颖性保证。
摘要级依据只能支持相应范围的判断；核心机制与创新性判断应读取原文方法部分。
P13正文访问受限，仅据原始摘要检索核验其高层设计。
Scideator在不同版本采用不同标题，本表采用arXiv v7的标题，保留系统名以便检索。

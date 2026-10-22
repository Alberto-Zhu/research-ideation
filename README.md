# Research Ideation · 科研构思与创新 skill

面向本地智能体的文献驱动科研构思流程：从研究问题、证据和近邻限制出发，
生成可检验的科学假设、解释或方法，并形成可执行的验证方案。

面向算法与计算研究、实验科学、理论研究以及社会科学中的观测研究。
适用于科研选题、科学假设生成、论文idea改进、创新性审查和研究设计。
核心指令遵循通用 `SKILL.md` 格式；可以由一个智能体顺序执行，
也可以在支持分工的环境中使用独立角色。生成与审查使用宿主智能体已有的模型和工具。

## 安装

要求：Git、Python 3.10+，以及支持读取本地 skill 的智能体。

```bash
git clone https://github.com/Alberto-Zhu/research-ideation.git
cd research-ideation
python tools/install_skill.py --agent codex
```

安装到 Codex 的用户级 skills 目录：默认 `~/.codex/skills/research-ideation`；
设置了 `CODEX_HOME` 时使用其下的 `skills` 目录。Windows 与 Linux/macOS 使用相同的 Python 命令。
在客户端重新加载 skills 或开启新会话后调用。

也可安装到 Claude Code 或指定的 skills 父目录：

```bash
python tools/install_skill.py --agent claude
python tools/install_skill.py --dest /path/to/agent/skills
```

已有安装时默认拒绝覆盖。显式使用 `--force` 会先在同级保留旧目录备份。
也可以手动复制 `skills/research-ideation` 到智能体读取的 skills 目录。
对于只支持说明文件的智能体，直接让它读取该目录中的 `SKILL.md`。
实际自动发现行为以客户端支持情况为准。

## 调用示例

```text
使用 $research-ideation，围绕我提供的研究问题和相关论文提出研究方案。
先检索当前近邻文献，找到有证据的方法局限，再生成6个不同机制，
筛选2–3个方向。给出关键创新步骤、最强反对意见、可证伪预测、
根据学科选择最小实验、证明义务或观测识别设计，并说明资源、假设和停止规则。
研究问题与约束如下：……
```

```text
使用 $research-ideation 审查我的idea。
重点检查它是否能由已有方法常规推导得到，并设计最便宜的鉴别实验。
```

默认提供 quick / standard / deep 三档预算。无联网工具时可以分析已提供的论文，
并明确标记文献覆盖范围和未核验的新颖性。

## 工作方式

1. 固定问题、失败案例、输入输出、资源和评估契约。
2. 建立有页码/章节定位的来源与检索记录。
3. 总结研究空白，先冻结能由已有方法得到的普通方案。
4. 通过跨领域结构迁移、facet组合等路线生成不同技术机制。
5. 分别审查新颖性、证据、逻辑、可行性和可检验性。
6. 输出最小鉴别验证、反证条件、停止规则和执行交接。

`run.json` 保留证据、候选、评审和选择依据。
`report.md` 供人阅读。`baselines.lock.json` 检查普通方案是否在生成后被修改。
这一锁文件不证明真正盲评，也不提供可信时间戳。

可选的本地辅助命令：

```bash
python skills/research-ideation/scripts/ideation.py init --out ./runs/demo --problem "研究问题" --challenge "现有方法的失败情形"
python skills/research-ideation/scripts/ideation.py freeze-baselines --out ./runs/demo
python skills/research-ideation/scripts/ideation.py validate --out ./runs/demo --stage final
```

先由智能体填写字段，再冻结普通方案，之后生成候选。
脚本只管理和检查产物结构；实际检索、推理和写作由宿主智能体完成。

## 研究依据

核验日期：2026-10-22。整理13篇核心工作：
IdeaScientist、SciMON、ResearchAgent、SciPIP、Scideator、Chain of Ideas、
MOOSE-Chem、Co-Scientist、The AI Scientist-v2，以及人类评估、
Ideation–Execution Gap、ResearchGym、SciAgents。

- [中文文献综述与方法对照](skills/research-ideation/references/literature-review.md)
- [机器可读文献条目](skills/research-ideation/references/bibliography.json)
- [完整 skill](skills/research-ideation/SKILL.md)
- [评审准则](skills/research-ideation/references/evaluation.md)
- [跨学科示例](skills/research-ideation/references/cross-domain-examples.md)

采用论文公开思想进行原创流程综合，未分发论文全文、作者代码、数据或模型权重。
文献笔记标明版本和审阅深度。本skill没有重训IdeaScientist角色，
也没有实现其百万文献库或GRPO优化。0–4评分和预算档位是工程默认。

## 检查

```bash
python -m unittest discover -s tests -v
```

自动检查覆盖引用一致性、冻结内容变更、时间截止条件、评审状态和安装保护。
通过这些检查代表结构一致；科学正确性、全球新颖性和实际收益仍需证据与实验。
运行结果和用户输入默认留在本地，不会自动上传、发布、调用付费API或训练模型。

原创说明与工具代码使用 MIT License；被引用工作保留各自权利。

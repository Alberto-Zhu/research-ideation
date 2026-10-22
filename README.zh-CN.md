# Research Ideation · 科研构思与创新

[English](README.md) | **简体中文**

面向本地 AI 智能体的文献驱动科研构思 skill。从研究问题和相关文献出发，发现科学空白，提出假设或方法，并形成可证伪的验证方案。

适用于计算研究、实验科学、理论研究及社会科学中的观测研究，支持科研选题、idea 改进、创新性审查和研究设计。采用通用 `SKILL.md` 格式，可以由单个智能体顺序执行，也可以按需使用专门角色。模型和研究工具由宿主智能体提供。

## 安装

要求：Git、Python 3.10+，以及支持读取本地 skill 的智能体。

```bash
git clone https://github.com/Alberto-Zhu/research-ideation.git
cd research-ideation
python tools/install_skill.py --agent codex
```

Codex 默认安装位置为 `~/.codex/skills/research-ideation`；设置了 `CODEX_HOME` 时，使用其下的 `skills` 目录。Windows、Linux 和 macOS 使用相同的 Python 命令。安装后请重新加载客户端 skills 或开启新会话。

也可以安装到 Claude Code，或指定 skills 父目录：

```bash
python tools/install_skill.py --agent claude
python tools/install_skill.py --dest /path/to/agent/skills
```

默认拒绝覆盖已有安装。显式使用 `--force` 时，会先将旧目录保留为同级备份，再执行替换。

也可以手动复制 `skills/research-ideation` 到智能体的 skills 目录。如果客户端不支持自动发现，直接让它读取其中的 `SKILL.md`。实际自动发现行为取决于客户端支持情况。

## 使用方式

```text
使用 $research-ideation，围绕我的研究问题和起始论文提出研究方向。
先检索最接近的已有工作，找出有证据支持的研究空白，再生成六个不同的机制或假设，
筛选两到三个方向。说明实质创新、最强反对意见和可证伪预测。
根据学科选择最小实验、证明义务、反例搜索或观测识别设计，
并明确资源、假设和停止规则。

研究问题与约束：……
```

审查已有 idea：

```text
使用 $research-ideation 审查我的 idea。
检查核心贡献是否能由已有工作常规推导得到，并设计成本最低的鉴别验证。
```

可选择 `quick`、`standard` 或 `deep` 控制检索和修订预算。离线时可以分析已提供的论文，并明确记录文献覆盖范围及尚未核验的新颖性。

## 工作流程

1. 固定科学问题、未解现象或失败情形、资源和评估契约。
2. 建立带页码或章节定位的来源账本，记录实际检索过程。
3. 发现有依据的研究空白，先冻结能从已有工作推导的普通方案。
4. 通过跨学科迁移、facet 组合等路线生成不同假设或机制。
5. 分别审查新颖性、证据、逻辑、可行性和可检验性。
6. 输出最小鉴别验证、反证条件、停止规则和执行交接方案。

验证方式随研究问题选择：计算比较、受控实验、理论证明与反例，或观测识别。尚未证明的公式、数值界和新结论必须标为猜想或待推导目标。

## 运行产物与辅助命令

| 文件 | 用途 |
|---|---|
| `run.json` | 研究契约、来源、空白、候选、评审和选择依据 |
| `report.md` | 便于阅读的研究方案 |
| `search-log.jsonl` | 实际检索词、日期和来源编号 |
| `baselines.lock.json` | 检查冻结的普通方案是否被修改 |

锁文件只检查内容一致性，不证明真正盲评，也不提供可信时间戳。

初始化任务：

```bash
python skills/research-ideation/scripts/ideation.py init --out ./runs/demo --problem "研究问题" --challenge "未解决的挑战"
```

先让智能体填写研究契约、证据和普通方案，再冻结这些方案；冻结后生成候选：

```bash
python skills/research-ideation/scripts/ideation.py freeze-baselines --out ./runs/demo
```

检查探索草案或完整方案：

```bash
python skills/research-ideation/scripts/ideation.py validate --out ./runs/demo --stage draft
python skills/research-ideation/scripts/ideation.py validate --out ./runs/demo --stage final
```

草案检查允许明确的证据缺口，但会拒绝未知引用编号和结构不一致；最终检查要求补齐证据与评审记录。脚本负责产物管理和结构检查，实际检索、推理和写作由宿主智能体完成。

## 研究依据

文献核验日期：**2026年10月22日**。整理了13篇核心工作：

IdeaScientist、SciMON、ResearchAgent、SciPIP、Scideator、Chain of Ideas、MOOSE-Chem、Co-Scientist、The AI Scientist-v2、Can LLMs Generate Novel Research Ideas?、The Ideation–Execution Gap、ResearchGym 和 SciAgents。

- [中文文献综述与方法对照](skills/research-ideation/references/literature-review.zh-CN.md)（[English](skills/research-ideation/references/literature-review.md)）
- [机器可读文献条目](skills/research-ideation/references/bibliography.json)
- [完整 skill 指令](skills/research-ideation/SKILL.md)
- [评审准则](skills/research-ideation/references/evaluation.md)
- [跨学科示例](skills/research-ideation/references/cross-domain-examples.md)

本项目依据公开研究思想进行原创流程综合，未分发论文全文、作者代码、数据集或模型权重。文献笔记标明论文版本和审阅深度。本 skill 没有复现 IdeaScientist 的角色训练、百万论文库或 GRPO 训练；0–4 分评审准则和预算档位属于工程默认设置。

## 检查与边界

```bash
python -m unittest discover -s tests -v
```

自动检查覆盖引用一致性、冻结内容变更、时间截止条件、评审状态、探索草案、理论验证证据记录和安装保护。

检查通过表示产物结构一致；科学正确性、全球新颖性和实际价值仍需证据及相应验证。运行产物和用户输入默认留在本地；辅助工具不会自动上传或发布这些内容，也不会自动调用付费 API 或训练模型。

## 许可

原创说明与辅助代码采用 [MIT License](LICENSE)，被引用工作保留各自权利。

# Harness Skills

[English](README.md)

Harness Skills 是一个用于启动和运行项目级 Agent Harness 的 Codex plugin。

它的目标不是替代业务项目，也不是单纯提供一组 workflow skills，而是把任意项目初始化成一个 Agent 可以稳定接管的受控工作环境：有项目上下文、规格、计划、可执行命令、guardrails、run 记录、本地 gate 和评估闭环。

## 一句话定位

```text
harness-skills
= Codex plugin
= Agent Harness 启动脚手架
= 项目级控制系统模板
= workflow skills + local gates + run artifacts
```

## 适合什么时候用

- 新项目只有一句话想法，需要先澄清再进入实现。
- 老项目希望补一套 Agent 可读的 `AGENTS.md` 和 `harness/` 工作区。
- 团队希望 Agent 的每次任务都有 spec、plan、执行证据和评估记录。
- 你不想只靠 Agent 口头说“完成了”，而是希望用本地 checker 检查关键 gate。
- 你希望简单任务轻量走，复杂任务完整闭环走。

## 安装

通过 Git marketplace 安装：

```text
codex plugin marketplace add wcxcw/harness-skills --ref main
codex plugin add harness-skills@harness-skills
```

## 主要入口

| Skill | 用途 |
| --- | --- |
| [`agent-harness`](plugins/harness-skills/skills/agent-harness/SKILL.md) | 初始化、运行和维护项目级 harness 的主入口。 |
| [`workflows`](plugins/harness-skills/skills/workflows/SKILL.md) | 闭环工作流集合：澄清、规格、计划、执行、调试、review、验证和收尾。 |
| [`meta`](plugins/harness-skills/skills/meta/SKILL.md) | 维护和改进 Harness 自身 skills。 |

## 它会生成什么

默认 `core` 脚手架会在目标项目中生成：

```text
AGENTS.md
harness/
├── context/
│   └── project-brief.md
├── controls/
│   └── gates.md
├── tools/
│   └── commands.md
├── guardrails/
│   └── boundaries.md
├── scripts/
│   └── check_run.py
└── runs/
```

也可以直接运行脚手架脚本：

```text
python3 plugins/harness-skills/skills/agent-harness/scripts/init_harness.py --project /path/to/project --language zh-CN
```

## 工作闭环

完整 run 的生命周期是：

```text
intake/design
  -> spec
  -> plan
  -> before-implementation gate
  -> execute
  -> review
  -> verification
  -> evaluation
  -> harness feedback
```

对应的 run artifacts：

| 文件 | 用途 |
| --- | --- |
| `workflow.md` | 记录使用过的 skills、生命周期决策和 gate 状态。 |
| `design.md` | 收敛问题、目标用户、推荐方向、MVP、非目标和开放问题。 |
| `spec.md` | 目标、范围、假设、验收标准、验证方式和所需证据。 |
| `plan.md` | 任务顺序、依赖、可能修改的文件、验证方式和证据要求。 |
| `execution-log.md` | 修改文件、执行命令、测试结果、失败信息和跳过的检查。 |
| `review.md` | review 范围、发现、处理结果和剩余风险。 |
| `evaluation.md` | 验收结果、验证结果、review 状态、残留风险和 harness 反馈。 |

## 分级闭环

每次任务都应选择能安全控制工作的最小 tier。

一个 run 对应一个用户目标，不对应 agent 的每次尝试。针对同一目标的返修、
补测试、补验证和小调整，应继续追加到当前 active run，直到用户验收或该 run
关闭。只有目标改变、范围明显扩大，或用户明确开始新任务时，才新建 run。

### XS

适合很小的文档、配置或低风险修改。

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── execution-log.md
└── evaluation.md
```

### Standard

适合大多数功能、bugfix 和结构化修改。

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── workflow.md
├── spec.md
├── plan.md
├── execution-log.md
└── evaluation.md
```

### Full

适合新功能、greenfield、产品方向、复杂 bug 或高风险修改。

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── input.md
├── workflow.md
├── design.md
├── spec.md
├── plan.md
├── execution-log.md
├── review.md
└── evaluation.md
```

## 本地 Gate

目标项目会生成 `harness/scripts/check_run.py`，用于在实现前和交付前检查当前 run 是否满足所选 tier 的最低要求。

Workflow skills 可以帮助 Agent 做事，但不能绕过项目本地 gate。

## 初始化模式

| 模式 | 使用场景 | 默认行为 |
| --- | --- | --- |
| `greenfield` | 空项目或一句话项目想法 | 先澄清方向，再生成项目简介、规格和计划。 |
| `brownfield` | 已有源码、README、测试、CI 或依赖配置 | 先只读发现，再保守补充 harness 文件。 |
| `existing-harness` | 已存在 `AGENTS.md` 或 `harness/` | 保留现有约定，补齐缺口，避免覆盖。 |

## 输出语言

- 用户用中文描述项目时，生成的 `AGENTS.md`、`harness/context/*`、`workflow.md`、`design.md`、`spec.md`、`plan.md` 和 run 记录默认使用中文。
- 命令、路径、包名、框架名和 API 名称保持原文。
- 老项目优先尊重已有文档语言；新增 run 记录可以跟随用户语言。

## 延伸阅读

- [Harness Engineering 介绍](docs/Harness%20Engineering.zh-CN.md)

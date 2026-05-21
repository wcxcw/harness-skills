# Harness Skills

[English](README.md)

用于创建和运行项目级 Agent Harness 的 Codex Skill Pack。

Harness Engineering 的目标，是给 Agent 提供一个受控的项目工作环境：规格、上下文、可执行命令、guardrails、run 记录和评估闭环。这个 Skill Pack 把这套结构沉淀成可复用的 Codex skills 和模板。

## 延伸阅读

- [Harness Engineering 介绍](docs/Harness%20Engineering.zh-CN.md)

## 它能做什么

- 生成项目级 `AGENTS.md` 和 `harness/` 工作区
- 兼容新项目、已有代码库和已有 harness
- 把想法收敛、规格、计划、执行记录、验证和评估统一放进 harness 流程
- 每次 run 后，Agent 可以基于执行证据和用户确认的决策提出或执行小范围 harness 更新

## 核心原则

- 先澄清，再编码
- 实现前先确认产品形态和内容/数据范围
- 实现前先确认技术栈和核心方案
- 先规格，再实现
- 把工作拆成小而可验证的任务
- 完成必须有证据
- 将 run 结果反哺到 harness

## 包含的 Skills

| Skill | 用途 |
| --- | --- |
| [`agent-harness`](skills/agent-harness/SKILL.md) | 主编排 skill，用于初始化、运行和维护 harness。 |
| [`idea-refine`](skills/idea-refine/SKILL.md) | 把原始想法收敛成简洁的 `idea.md`。 |
| [`spec-driven-development`](skills/spec-driven-development/SKILL.md) | 把不清晰的工作转成 run 级 `spec.md`。 |
| [`task-planning`](skills/task-planning/SKILL.md) | 把确认后的 spec 拆成 `plan.md` 中有范围、有顺序、可验证的任务。 |

## 使用方式

使用下面三个入口之一。`agent-harness` 会根据项目状态选择 `greenfield`、`brownfield` 或 `existing-harness` 模式。

### 新项目

```text
Use agent-harness to start a new project from this idea: a lightweight habit tracker for remote teams.
```

### 老项目

```text
Use agent-harness to initialize an Agent Harness for this existing codebase.
```

### 执行任务

```text
Use agent-harness to run this task through the harness: add tag filtering to the issue list.
```

## 仓库结构

```text
harness-skills/
├── README.md
├── README.zh-CN.md
├── docs/
└── skills/
    ├── agent-harness/
    ├── idea-refine/
    ├── spec-driven-development/
    └── task-planning/
```

主入口：

```text
skills/agent-harness/SKILL.md
```

主 skill 使用的模板：

```text
skills/agent-harness/assets/templates/
```

## 初始化模式

| 模式 | 使用场景 | 默认行为 |
| --- | --- | --- |
| `greenfield`（新项目） | 空项目或一句话项目想法 | 按需先收敛想法，生成项目简介，再产出可执行的规格和计划。 |
| `brownfield`（老项目） | 已有源码、项目配置、测试、CI 或 README | 先做只读发现，记录项目事实，再保守补充 harness 文件。 |
| `existing-harness`（已有 harness） | 已存在 `AGENTS.md` 或 `harness/` | 保留现有 harness 内容，补齐缺口，避免覆盖既有约定。 |

## 生成的 Harness

默认脚手架使用最小的 `core` 配置：

```text
AGENTS.md                         Agent 入口和 harness 索引
harness/                          项目级 Agent Harness 工作区
├── context/
│   ├── project-brief.md          项目想法、用户、目标、MVP 和假设
│   └── initialization-notes.md    初始化模式、发现事实、未知项和决策
├── tools/
│   └── commands.md               已确认的项目命令及来源
├── feedback/
│   └── verification.md           验证流程和完成证据要求
├── guardrails/
│   └── boundaries.md             范围、权限和安全边界
├── evals/
│   └── task-scorecard.md         完成度、质量、风险和 harness 反馈
└── runs/
    └──                           每次任务的运行记录
```

扩展文件只在需要时创建：

| 配置 / 场景 | 额外文件 |
| --- | --- |
| `brownfield`（老项目上下文） | `harness/context/repo-map.md`、`harness/context/architecture.md`、`harness/context/coding-conventions.md`、`harness/context/dependency-notes.md` |
| 扩展安全边界 | `harness/guardrails/permissions.md`、`harness/guardrails/rollback.md` |
| 扩展评估 | `harness/evals/acceptance-checklist.md`、`harness/evals/regression-checklist.md` |
| 规格模板 | `harness/specs/feature-template.md`、`harness/specs/bugfix-template.md` |
| `full` | 所有内置模板 |

## Run 记录

每次 Agent 任务建议创建一个 run 目录：

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── input.md
├── idea.md
├── spec.md
├── plan.md
├── execution-log.md
└── evaluation.md
```

只有当 run 使用了 idea refinement 时，才需要 `idea.md`。

| 文件 | 用途 |
| --- | --- |
| `input.md` | 记录用户原始需求。 |
| `idea.md` | 记录收敛后的问题、方向、关键假设、MVP 范围和不做事项。 |
| `spec.md` | 记录目标、范围、假设、验收标准、验证方式和所需证据。 |
| `plan.md` | 记录任务顺序、依赖关系、可能修改的文件、验证方式和所需证据。 |
| `execution-log.md` | 记录修改文件、执行命令、测试结果、失败信息和跳过的检查。 |
| `evaluation.md` | 记录是否满足规格、回归风险、残留风险和 harness 反馈。 |

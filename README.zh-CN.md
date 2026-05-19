# Harness Skills

[English](README.md)

这是一个用于在真实软件项目中实践 Harness Engineering 的 Codex Skill Pack。

Harness Engineering 的目标，是给 Agent 提供一个受控的项目工作环境：明确的规格、经过整理的上下文、可执行的工具、反馈闭环、安全边界、评估标准，以及可复盘的运行记录。这个 Skill Pack 把初始化和运行这套流程所需的 Skill 打包在一起。

## 延伸阅读

- [Harness Engineering 介绍](docs/Harness%20Engineering.zh-CN.md)

## 这个 Skill Pack 能做什么

当你希望 Codex 完成以下工作时，可以使用这个 Skill Pack：

- 创建或更新项目级 `AGENTS.md`
- 初始化 `harness/` 目录
- 兼容新项目、已有代码库和已有 harness 的初始化
- 把原始想法收敛成可执行的一页概念说明
- 在编码前把需求转成规格
- 把规格拆成小而可验证的任务
- 让实现过程遵守明确的 guardrails
- 记录每次 Agent run，方便 review 和复盘

推荐工作流：

```text
用户需求
-> 想法收敛（按需）
-> 规格说明
-> 执行计划
-> 任务实现
-> 验证
-> Run 记录
-> 评估
-> 改进 Harness
```

## 包含的 Skills

| Skill | 用途 |
| --- | --- |
| `agent-harness-bootstrap` | 主编排 Skill，用于初始化和运行 Harness Engineering 工作流。 |
| `idea-refine` | 把原始想法收敛成一页概念说明，再进入规格阶段。 |
| `spec-driven-development` | 把模糊、多文件或重要任务转成可 review 的规格说明。 |
| `planning-and-task-breakdown` | 把确认后的规格拆成有顺序、可验证的实现任务。 |

## 仓库结构

```text
harness-skills/
├── README.md
├── README.zh-CN.md
└── skills/
    ├── agent-harness-bootstrap/
    ├── idea-refine/
    ├── spec-driven-development/
    └── planning-and-task-breakdown/
```

主入口是：

```text
skills/agent-harness-bootstrap/SKILL.md
```

该 Skill 使用的 Harness 模板位于：

```text
skills/agent-harness-bootstrap/assets/templates/
```

## 使用方式

只保留三个入口。Skill 会根据项目状态自动选择 `greenfield`、`brownfield` 或 `existing-harness` 模式。

### 新项目

从一句话想法启动：

```text
Use agent-harness-bootstrap to start a new project from this idea: a lightweight habit tracker for remote teams.
```

### 老项目

在已有代码库中初始化或刷新 harness：

```text
Use agent-harness-bootstrap to initialize an Agent Harness for this existing codebase.
```

### 执行任务

把 feature、bugfix、实现步骤或 harness 改进交给 harness 流程执行：

```text
Use agent-harness-bootstrap to run this task through the harness: add tag filtering to the issue list.
```

## 生成的 Harness 结构

初始化流程支持三种模式：

| 模式 | 使用场景 | 默认行为 |
| --- | --- | --- |
| `greenfield` | 空项目或一句话项目想法 | 按需先收敛想法，生成 project brief，再产出可执行 spec 和 plan。 |
| `brownfield` | 已有源码、manifest、测试、CI 或 README | 先做只读发现，记录项目事实，再保守补充 harness 文件。 |
| `existing-harness` | 已存在 `AGENTS.md` 或 `harness/` | 保留现有 harness 内容，补齐缺口，避免覆盖既有约定。 |

初始化后会在目标项目中生成类似结构：

```text
AGENTS.md
harness/
├── specs/
│   ├── feature-template.md
│   └── bugfix-template.md
├── context/
│   ├── project-brief.md
│   ├── initialization-notes.md
│   ├── repo-map.md
│   ├── architecture.md
│   ├── coding-conventions.md
│   └── dependency-notes.md
├── tools/
│   ├── commands.md
│   └── verification.md
├── guardrails/
│   ├── permissions.md
│   ├── boundaries.md
│   └── rollback.md
├── evals/
│   ├── acceptance-checklist.md
│   ├── regression-checklist.md
│   └── task-scorecard.md
└── runs/
```

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

这些文件的用途：

| 文件 | 用途 |
| --- | --- |
| `input.md` | 记录用户原始需求。 |
| `idea.md` | 记录收敛后的问题、方向、关键假设、MVP 范围和不做事项。 |
| `spec.md` | 记录目标、边界、验收标准和未决问题。 |
| `plan.md` | 记录任务拆解、依赖关系和验证方式。 |
| `execution-log.md` | 记录修改文件、执行命令、测试结果和失败信息。 |
| `evaluation.md` | 记录是否满足规格、是否有回归风险以及后续建议。 |

# Harness Skills

这是一个用于在真实软件项目中实践 Harness Engineering 的 Codex Skill Pack。

Harness Engineering 的目标，是给 Agent 提供一个受控的项目工作环境：明确的规格、经过整理的上下文、可执行的工具、反馈闭环、安全边界、评估标准，以及可复盘的运行记录。这个 Skill Pack 把初始化和运行这套流程所需的 Skill 打包在一起。

## 这个 Skill Pack 能做什么

当你希望 Codex 完成以下工作时，可以使用这个 Skill Pack：

- 创建或更新项目级 `Agents.md`
- 初始化 `harness/` 目录
- 在编码前把需求转成规格
- 把规格拆成小而可验证的任务
- 让实现过程遵守明确的 guardrails
- 记录每次 Agent run，方便 review 和复盘
- 在运行时支持的情况下，验证浏览器侧行为

推荐工作流：

```text
用户需求
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
| `spec-driven-development` | 把模糊、多文件或重要任务转成可 review 的规格说明。 |
| `planning-and-task-breakdown` | 把确认后的规格拆成有顺序、可验证的实现任务。 |
| `browser-testing-with-devtools` | 指导 Web 项目进行真实浏览器验证。 |

## 仓库结构

```text
harness-skills/
├── README.md
├── README.zh-CN.md
└── skills/
    ├── agent-harness-bootstrap/
    ├── spec-driven-development/
    ├── planning-and-task-breakdown/
    └── browser-testing-with-devtools/
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

在一个项目中初始化 Harness Engineering：

```text
Use agent-harness-bootstrap to initialize an Agent Harness for this project.
```

为一个具体任务创建 run：

```text
Use agent-harness-bootstrap to create a harness run for this task: add tag filtering to the issue list.
```

基于已有 run 执行实现：

```text
Use agent-harness-bootstrap to implement the current harness run and record execution-log.md and evaluation.md.
```

根据失败或噪声较多的 run 改进 Harness：

```text
Use agent-harness-bootstrap to review the latest run and update the harness guardrails, commands, or context.
```

## 生成的 Harness 结构

初始化后会在目标项目中生成类似结构：

```text
Agents.md
harness/
├── specs/
│   ├── feature-template.md
│   └── bugfix-template.md
├── context/
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
├── spec.md
├── plan.md
├── execution-log.md
└── evaluation.md
```

这些文件的用途：

| 文件 | 用途 |
| --- | --- |
| `input.md` | 记录用户原始需求。 |
| `spec.md` | 记录目标、边界、验收标准和未决问题。 |
| `plan.md` | 记录任务拆解、依赖关系和验证方式。 |
| `execution-log.md` | 记录修改文件、执行命令、测试结果和失败信息。 |
| `evaluation.md` | 记录是否满足规格、是否有回归风险以及后续建议。 |

## 运行时说明

这个仓库已经包含上面列出的所有 Skill 目录，但部分 Skill 仍然依赖用户 Codex 环境中的运行时能力：

- `browser-testing-with-devtools` 需要浏览器和 DevTools 能力。

把 Skill 文件打包在一起，可以让它们一起分发；但这不等于保证每台机器都有对应的外部运行时、MCP server、浏览器集成或 DevTools 依赖。

## 发布说明

这个 pack 会把当前本地环境中的 Skill 作为 vendored dependency 一起打包。公开发布前，需要检查这些 Skill 和相关资源的授权与再分发条件，尤其是：

- `browser-testing-with-devtools`

如果授权不清楚或不允许再分发，建议只发布 `agent-harness-bootstrap`，并把其它 Skill 写成前置依赖。

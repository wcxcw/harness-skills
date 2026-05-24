# AGENTS.md

这是本项目 Agent Harness 的入口文件。它索引项目目标、上下文、可执行命令、反馈记录、安全边界和评估标准，供 Agent 和维护者共同使用。

## Harness 分层

| 分层 | 用途 | 文件 |
| --- | --- | --- |
| Context | 项目简介 | [harness/context/project-brief.md](harness/context/project-brief.md) |
| Context | 初始化记录 | [harness/context/initialization-notes.md](harness/context/initialization-notes.md) |
| Tools | 已确认命令 | [harness/tools/commands.md](harness/tools/commands.md) |
| Feedback | 验证流程 | [harness/feedback/verification.md](harness/feedback/verification.md) |
| Feedback | Run 记录 | [harness/runs/](harness/runs/) |
| Guardrails | 工作边界 | [harness/guardrails/boundaries.md](harness/guardrails/boundaries.md) |
| Evaluation | 任务评分表 | [harness/evals/task-scorecard.md](harness/evals/task-scorecard.md) |

## 可选 Harness 文件

仅在项目需要时创建：

- 老项目上下文：`harness/context/repo-map.md`、`harness/context/architecture.md`、`harness/context/coding-conventions.md`、`harness/context/dependency-notes.md`
- 扩展边界：`harness/guardrails/permissions.md`、`harness/guardrails/rollback.md`
- 扩展评估：`harness/evals/acceptance-checklist.md`、`harness/evals/regression-checklist.md`
- 规格模板：`harness/specs/feature-template.md`、`harness/specs/bugfix-template.md`

## 初始化模式

- `greenfield`：新项目或一句话想法。先读 `project-brief.md`、`initialization-notes.md`，再读当前 run 的 `idea.md`、`spec.md`、`plan.md`。
- `brownfield`：已有代码库。先读需要的 `harness/context/*`，再读现有 README、配置、CI、包管理文件，最后读当前 run。
- `existing-harness`：已有 `AGENTS.md` 或 `harness/`。默认保留既有约定，除非用户明确要求重写。

## 语言策略

- Harness 文件应使用用户主要使用的语言。
- 如果用户用中文描述项目，`idea.md`、`spec.md`、`plan.md`、run 记录和 harness 上下文默认使用中文。
- 代码标识符、命令、文件路径、库名和框架名保持原文。
- 如果项目已有文档语言，以现有项目语言为准；双语团队可以保留必要英文术语，但不要让主要说明变成英文模板。

## Run 约定

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── input.md
├── idea.md
├── spec.md
├── plan.md
├── execution-log.md
└── evaluation.md
```

只有任务从原始想法开始并使用了 idea refinement 时，才需要 `idea.md`。

## 工作原则

- 先澄清，再编码：把模糊请求转成明确目标、约束和成功标准。
- 先确认产品形态：面向用户、核心流程、信息架构、内容或数据来源、更新方式、MVP 质量标准必须明确。
- 先确认关键技术决策：技术栈、运行时、数据模型、核心架构、外部服务、部署目标和主要平台选择必须确认，或作为非编码决策任务处理。
- 先规格，再实现：非平凡任务必须以当前 run 的 `spec.md` 为准。
- 拆成小而可验证的任务：每个任务要有范围、可能修改的文件、依赖和验证方式。
- 完成必须有证据：命令、检查、失败和跳过原因都要记录到当前 run。
- 控制范围：避免无关重构、猜测式抽象和规格外行为。
- 从运行结果改进 harness：重复失败、上下文缺失或规则不清，应反馈到规范文件。
- 规范 harness 文件属于仓库共享资产，不是个人本地约定。

## 协作和版本控制

- 提交规范 harness 文件：`AGENTS.md`、`harness/context/`、`harness/tools/`、`harness/feedback/`、`harness/guardrails/` 和 `harness/evals/`。
- `harness/runs/` 是任务记录。只提交对 review、审计、新人理解、未来上下文、架构决策或复杂 bug 复盘有价值的 run 目录。
- 不要把个人本地 harness 副本当作事实来源。团队共享的 Agent 行为应来自仓库里的 harness。
- 普通功能或 bugfix 任务中，先把 harness 改进建议写到当前 run 的 `evaluation.md`；除非流程明确允许，不要直接改规范 harness 文件。
- 只有在明确的 harness maintenance、用户要求初始化/改进 harness，或需要根据仓库证据修正事实错误时，才修改规范 harness 文件。
- 多人仓库中，建议用 review 规则或 CODEOWNERS 保护 `AGENTS.md` 和规范 `harness/` 目录。
- 如果多数 run 记录不需要进仓库，可以忽略 `harness/runs/*`，保留 `harness/runs/.gitkeep`，需要保留的 run 再单独 force-add。

## 引导式初始化

当项目只有一句话想法、产品形态不清、技术栈未定，或用户希望先讨论方向时，不要直接写应用代码。使用 `idea-refine` 提问并生成 `idea.md`。

用户回答后，先更新 `project-brief.md` 和 `initialization-notes.md`，再生成 `idea.md`、`spec.md` 和 `plan.md`。如果仍有关键问题未确认，先把它作为 `plan.md` 的第一个非编码任务。

## 实现门槛

当 `spec.md` 或 `plan.md` 仍有未解决的阻塞问题时，不要写应用代码。阻塞问题包括目标用户、内容/数据范围、信息架构、核心体验、成功标准、技术栈、框架、运行时、数据模型、认证、外部服务、部署目标和核心用户行为。

如果用户希望暂缓决定，把该决策列为 `plan.md` 的第一个非编码任务。解决后再进入实现任务。

## Agent 工作流

1. 从 `harness/context/initialization-notes.md` 判断初始化模式。
2. 根据用户语言和项目文档语言确定本次输出语言。
3. 新项目先读 `project-brief.md`，再读当前 run 的 `idea.md`、`spec.md` 和 `plan.md`。
4. 老项目先读需要的 `harness/context/` 文件，再读现有项目文档和配置，最后读当前 run。
5. 只加载完成任务所需的上下文。
6. 编辑前检查 guardrails。
7. 编辑应用代码前确认没有未解决的阻塞问题。
8. 一次执行一个小任务。
9. 运行已确认的验证命令。
10. 声称完成前，把证据记录到当前 run。
11. 交付前更新 evaluation。
12. 检查 `Context Updates`、`execution-log.md` 和 `evaluation.md` 是否暴露了 harness 缺口。
13. 只有在用户要求维护 harness、当前流程允许，或发现仓库事实性错误时，才更新规范 harness 文件；否则列出建议等待确认。

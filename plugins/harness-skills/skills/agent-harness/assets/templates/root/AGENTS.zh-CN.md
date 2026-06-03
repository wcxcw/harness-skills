# AGENTS.md

本项目使用 Agent Harness。Agent 工作时，以以下文件作为共享事实来源。

## 优先阅读

1. `harness/context/project-brief.md`
2. `harness/controls/gates.md`
3. `harness/tools/commands.md`
4. `harness/guardrails/boundaries.md`
5. 如果存在 active run，再阅读 `harness/runs/` 下对应目录

## 核心规则

- 产品、技术或范围决策不清楚时，先澄清再实现。
- 每次任务选择能安全控制工作的最小 run tier。
- 非平凡任务应创建 run，并记录 `spec.md`、`plan.md`、`execution-log.md` 和 `evaluation.md`。
- 命令、手动检查、失败、跳过原因和残留风险都要写入当前 run。
- 存在 active run 时，实现前和完成前使用 `harness/scripts/check_run.py`。
- 不要编造项目命令；未知命令记录到 `harness/tools/commands.md`。
- 修改范围必须贴合已确认的 spec 和 plan。
- 不要绕过 `harness/guardrails/boundaries.md`。

## Run 分级

```text
xs:       execution-log.md + evaluation.md
standard: workflow.md + spec.md + plan.md + execution-log.md + evaluation.md
full:     input.md + workflow.md + design.md + spec.md + plan.md + execution-log.md + review.md + evaluation.md
```

只有当产品方向、架构、数据、安全、CI、依赖或 review 风险足够高时，才使用 `full`。

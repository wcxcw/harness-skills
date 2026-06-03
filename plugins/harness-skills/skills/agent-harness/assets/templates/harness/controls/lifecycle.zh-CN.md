# 生命周期

Harness 生命周期是 agentic work 的完整闭环。Workflow skills 可以辅助执行每个阶段，但是否允许继续由本地 gate 决定。

## 阶段

| 阶段 | Workflow skill | 必要 artifact | Gate |
| --- | --- | --- | --- |
| Intake | `brainstorming` | `workflow.md`、`design.md` | 方向已获用户确认 |
| Spec | `writing-specs` | `spec.md` | 没有未解决的阻塞决策 |
| Plan | `writing-plans` | `plan.md` | 任务映射到验收标准 |
| Preflight | `agent-harness` | Gate output | `check_run.py --stage before-implementation` 通过 |
| Execute | `executing-plans`、`test-driven-development` 或 `systematic-debugging` | `execution-log.md` | 验证证据已记录 |
| Review | `requesting-code-review` | `review.md` | Review 发现已处理或记录 |
| Verify | `verification-before-completion` | `execution-log.md` | 命令或手动检查已记录 |
| Finish | `finishing-run` | `evaluation.md` | `check_run.py --stage before-completion` 通过 |
| Improve | `agent-harness` 或 `writing-skills` | Harness 更新建议 | 规范文件变更前先记录反馈 |

## Run Artifact 契约

使用能安全控制工作的最小等级：

### XS

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── execution-log.md
└── evaluation.md
```

### Standard

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── workflow.md
├── spec.md
├── plan.md
├── execution-log.md
└── evaluation.md
```

### Full

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

新功能、greenfield 或产品方向使用 `design.md`。狭窄 bugfix 如果 `spec.md` 已包含复现、期望行为和范围，可以跳过 `design.md`。`full` run 或风险足够高时使用 `review.md`。

## 继续规则

必要 artifact 或 gate 缺失时，不要进入下一阶段。如果某个阶段被有意跳过，在 `workflow.md` 中记录原因，并确保下一个 gate 仍然通过。

# 门槛

门槛用于把 harness 建议变成可检查项。Agent 应在实现前和交付前使用这些门槛。

## 分级

| 等级 | 使用场景 | 必要 run artifacts |
| --- | --- | --- |
| `xs` | 极小文档/配置/单文件改动，没有产品或技术决策 | `execution-log.md`、`evaluation.md` |
| `standard` | 普通功能、范围明确的 bugfix、多文件但风险可控的修改 | `workflow.md`、`spec.md`、`plan.md`、`execution-log.md`、`evaluation.md` |
| `full` | greenfield、新产品/功能方向、架构/数据/安全/CI/依赖风险 | `workflow.md`、`design.md`、`spec.md`、`plan.md`、`execution-log.md`、`review.md`、`evaluation.md` |

## Run 边界

一个 run 应覆盖一个用户目标的完整生命周期，包括验收前用户要求的返修和补验证。
不要因为同一目标下的小修复新建 run。只有目标改变、范围明显扩大、上一个 run
已关闭，或用户明确开始另一个任务时，才新建 run。

## 实现前

对于 `standard` 和 `full` run，编辑应用代码前必须通过这些检查：

- `harness/runs/<run>/spec.md` 存在。
- `harness/runs/<run>/plan.md` 存在。
- `harness/runs/<run>/workflow.md` 存在，并记录使用的 skills 和 gate 状态。
- `full` run 的 `harness/runs/<run>/design.md` 存在。
- `spec.md` 包含目标、范围、非目标、验收标准、验证方式和待确认问题。
- `plan.md` 包含有顺序的任务和验证方式。
- `spec.md` 和 `plan.md` 不包含 `Needs decision`、`需要决策` 或 `TBD` 等阻塞标记。

推荐本地检查：

```text
python3 harness/scripts/check_run.py harness/runs/<run> --stage before-implementation --tier standard
```

## 交付前

声称完成前，当前 run 必须通过这些检查：

- `execution-log.md` 存在。
- `full` run 的 `review.md` 存在，并记录 review 发现或“无”。
- `evaluation.md` 存在。
- `execution-log.md` 记录已执行的命令或手动检查及其结果。
- `evaluation.md` 记录验收状态、残留风险和 harness 反馈。
- 跳过的验证必须说明原因。

推荐本地检查：

```text
python3 harness/scripts/check_run.py harness/runs/<run> --stage before-completion --tier standard
```

## 门槛失败

- 如果因为缺少决策而失败，停止实现，先解决决策。
- 如果因为缺少证据而失败，运行相关验证，或记录为什么不能运行。
- 如果某个门槛不适用，在当前 run 中记录原因。

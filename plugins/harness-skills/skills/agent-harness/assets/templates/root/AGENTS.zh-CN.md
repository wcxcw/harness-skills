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
- 没有 active run 时，明确、低风险的微小改动不要创建 run。
- no-run 微小改动必须同时满足：请求明确、影响局部、不改变行为、不需要决策、能用一次小检查验证、可以局部回滚。
- 例子：修正错别字、改一句文案、把某个选择器字号从 `18px` 改成 `16px`、调整一个间距/颜色 token。
- 不属于微小改动： “优化首页视觉”、“调整整体字体层级”、跨页面修改、行为变化，或任何需要设计/产品/技术决策的任务。
- 微小改动直接修改，运行最小相关检查，并在回复中说明结果。
- 需要 run 时，选择能安全控制工作的最小 run tier。
- 一个 run 对应一个用户目标，不对应 agent 的一次尝试。
- 同一目标的返修、补测试、补验证和小调整，继续使用当前 active run。
- 只有目标改变、范围明显扩大、上一个 run 已关闭，或用户明确开始新任务时，才新建 run。
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

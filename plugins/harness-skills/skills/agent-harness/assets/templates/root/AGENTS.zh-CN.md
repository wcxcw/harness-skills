# AGENTS.md

本项目使用 Agent Harness。Agent 工作时，以以下文件作为共享事实来源。

## 优先阅读

1. `harness/context/project-brief.md`
2. `harness/controls/gates.md`
3. `harness/tools/commands.md`
4. `harness/guardrails/boundaries.md`
5. 只有当请求属于某个 active run 时，才阅读 `harness/runs/` 下对应目录

## 上下文加载

- 不要批量读取 `harness/context/*` 或 `harness/runs/*`。
- `harness/context/project-brief.md` 可以默认读取；维护或更新该文件时，只保留短项目摘要，不要写入详细状态、历史记录或长设计内容。
- 只在当前任务需要时读取额外 context 文件，并先明确读取原因。
- 优先用定向搜索或按章节读取，避免整文件加载大型上下文。
- 已完成 run 是历史记录；只有用户询问历史或当前任务依赖该 run 时才读取。

## 核心规则

- 产品、技术或范围决策不清楚时，先澄清再实现。
- Run 是否需要、分级和边界以 `harness/controls/gates.md` 为准。
- 如果 gates 判定为 no-run 微小改动，直接修改，运行最小相关检查，并在回复中说明结果。
- 如果需要 run，选择最小安全 tier，并保持一个用户目标对应一个 active run；同一目标后续修改追加到该 run。
- 非平凡任务应创建 run，并记录 `spec.md`、`plan.md`、`execution-log.md` 和 `evaluation.md`。
- 命令、手动检查、失败、跳过原因和残留风险都要写入当前 run。
- 存在 active run 时，实现前和完成前使用 `harness/scripts/check_run.py`。
- 不要编造项目命令；未知命令记录到 `harness/tools/commands.md`。
- 修改范围必须贴合已确认的 spec 和 plan。
- 不要绕过 `harness/guardrails/boundaries.md`。

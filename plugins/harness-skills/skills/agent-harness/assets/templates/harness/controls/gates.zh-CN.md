# 门槛

门槛用于把 harness 建议变成可检查项。Agent 应在实现前和交付前使用这些门槛。
当风险影响 tier、review 深度或验证范围时，使用 `harness/controls/risk-matrix.md`。

## Run 前共识对齐

目标或重大决策不清楚时，先不要创建 run。邀请用户显式调用 `$grilling`，一次确认一个决策且不创建文件。用户确认共同理解后，再创建 run，并在 `spec.md` 中记录该确认。

## 分级

只有需要 run 时才选择 run tier。no-run 微小改动必须同时满足：请求明确、影响
局部、不改变行为、不需要决策、能用一次小检查验证、可以局部回滚。例子：错别字、
一句文案、一个明确选择器的字号修改、一个间距/颜色 token。非微小改动：宽泛视觉
优化、整体字体层级调整、跨页面修改、行为变化，或需要设计/产品/技术决策的任务。

| 等级 | 使用场景 | 必要 run artifacts |
| --- | --- | --- |
| `xs` | 仍需要 run 记录的小改动，例如低风险配置/文档/代码修改，并需要验证证据 | `execution-log.md`、`evaluation.md` |
| `standard` | 普通功能、范围明确的 bugfix、多文件但风险可控的修改 | `workflow.md`、`spec.md`、`plan.md`、`execution-log.md`、`evaluation.md` |
| `full` | greenfield、新产品/功能方向、架构/数据/安全/CI/依赖风险 | `input.md`、`workflow.md`、`spec.md`、`plan.md`、`execution-log.md`、`review.md`、`evaluation.md` |

支持会话绑定时，各 tier 还会记录 `run-state.json`。上表是工作流要求；检查器不会自动验证全部所列文件或内容真实性。

## Run 边界

一个 run 应覆盖一个用户目标，包括后续返修、小调整和补验证。没有 active run 时，
先判断是否满足上述 no-run 微小改动条件；满足则直接修改。否则若相关 run 已关闭，
继续工作前显式恢复并绑定当前会话，追加本轮 review 和验证证据、更新
`evaluation.md` 并保留历史，再重新执行适用的完成前门槛；不能把旧结论当成本轮
证据。恢复时保留原 Git 基线，可能包含无关提交，需要核对实际变更范围。根据任务
上下文确定对应 run，不按目录新旧推断，不覆盖其他会话正在使用的 run。仅因 run
已关闭不应新建；目标改变、范围
明显扩大，或用户要求独立记录时才新建 run。

## 实现前

对于 `standard` 和 `full` run，编辑应用代码前必须通过这些检查：

- `harness/runs/<run>/spec.md` 存在。
- `harness/runs/<run>/plan.md` 存在。
- `harness/runs/<run>/workflow.md` 存在，并记录使用的 skills 和 gate 状态。
- `spec.md` 包含共识确认、目标、范围、非目标、验收标准、验证方式和待确认问题。
- `spec.md` 记录共同理解及其来源。用户已经明确的请求可作为其中已明确决策的对齐依据，记录来源即可，无需重复确认；实现前应解决实际阻塞的未决事项。
- `plan.md` 包含有顺序的任务和验证方式。
- `spec.md` 和 `plan.md` 不包含 `Needs decision`、`需要决策` 或 `TBD` 等阻塞标记。

推荐本地检查：

```text
python3 harness/scripts/check_run.py harness/runs/<run> --stage before-implementation --tier standard
```

## 交付前

声称完成前，当前 run 必须通过这些检查：

- `execution-log.md` 存在。
- `full` run 的 `review.md` 存在，并包含 `Review 范围`、`发现`、`处理结果`、`剩余风险` 四个语义章节（也接受对应的规范英文标题）。
- `evaluation.md` 存在。
- `execution-log.md` 记录已执行的命令或手动检查及其结果。
- 应用代码变更已执行代码质量 review；适用时执行前端/后端质量 review，或已记录跳过原因。
- Critical 和 Important review 发现已修复、被用户明确接受，或记录为残留风险。
- `evaluation.md` 记录验收状态、残留风险和 harness 反馈。
- 跳过的验证必须说明原因。
- Stop hook 只兜底复查当前 session 显式标记为 `verifying` 的 run，不扫描最近的历史 run。

推荐本地检查：

```text
python3 harness/scripts/check_run.py harness/runs/<run> --stage before-completion --tier standard
```

## 门槛失败

- 如果因为缺少决策而失败，停止实现，先解决决策。
- 如果因为缺少证据而失败，运行相关验证，或记录为什么不能运行。
- 如果某个门槛不适用，在当前 run 中记录原因。

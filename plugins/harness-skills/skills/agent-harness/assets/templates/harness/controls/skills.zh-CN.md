# Skill 兼容

本项目 harness 是项目事实、门槛、命令和完成证据的事实来源。Workflow skills 可以作为工作流辅助，但不能替代本地 harness 门槛。

## 阶段映射

| Harness 阶段 | 必要 workflow skill | 可兼容的外部 skill 模式 |
| --- | --- | --- |
| Intake | `brainstorming` | brainstorming |
| Spec | `writing-specs` | planning-oriented discovery |
| Plan | `writing-plans` | writing-plans |
| Context | `context-budget` | context-budget |
| Preflight | `agent-harness` | local gate check |
| 实现 | `executing-plans` | test-driven-development when practical |
| 调试 | `systematic-debugging` | systematic-debugging |
| Review | `requesting-code-review` | requesting-code-review |
| Reviewer 角色 | `code-reviewer` | code reviewer subagent |
| 质量 Review | `code-quality-review`、`frontend-quality-review`、`backend-quality-review` | coding standards、frontend/backend patterns |
| Review 处理 | `receiving-code-review` | receiving-code-review |
| 完成 | `verification-before-completion`、`finishing-run` | verification-before-completion |
| Harness 改进 | `writing-skills` | writing-skills when improving skills |

## 规则

- 只有当外部 skill 能帮助满足本地 spec、plan、gate 或验证要求时才使用。
- 不要把外部 skill 当成绕过 `harness/controls/gates.md` 的批准。
- 当外部 skill 或工作流实质影响了任务，在 `workflow.md` 中记录。
- 如果外部 skill 与项目命令、guardrails 或用户指令冲突，以本地 harness 为准；冲突重要时先询问。

## 推荐 Run 记录

当外部 skill pack 影响了工作方式，在 `workflow.md` 中增加简短记录：

```text
## Skills Used
- brainstorming
- writing-specs
- writing-plans

## Gates
- before-implementation: pending
- before-completion: pending
```

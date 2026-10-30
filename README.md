# Harness
Harness 是一个用于启动和运行项目级 Agent Harness 的 Codex plugin。

它的目标不是替代业务项目，也不是单纯提供一组 workflow skills，而是把任意项目初始化成一个 Agent 可以稳定接管的受控工作环境：有项目上下文、规格、计划、可执行命令、guardrails、run 记录、本地 gate 和评估闭环。

## 一句话定位

```text
harness
= Codex plugin
= Agent Harness 启动脚手架
= 项目级控制系统模板
= workflow skills + local gates + run artifacts
```

## 适合什么时候用

- 新项目只有一句话想法，需要先澄清再进入实现。
- 老项目希望补一套 Agent 可读的 `AGENTS.md` 和 `harness/` 工作区。
- 团队希望按任务风险保留适当的规格、计划和验证记录。
- 你不想只靠 Agent 口头说“完成了”，而是希望用本地 checker 检查关键 gate。
- 你希望简单任务轻量走，复杂任务完整闭环走。

## 结构图
![harness-skills-architecture.svg](docs/assets/harness-skills-architecture.svg)

## 安装

通过 Git marketplace 安装：

```text
codex plugin marketplace add wcxcw/harness-skills --ref main
codex plugin add harness@harness
```

本仓库的 `.agents/plugins/marketplace.json` 同时用于仓库内本地发现和 Git marketplace 发布。
在本仓库开发时直接使用自动发现的本地来源，不要在同一项目中再次添加
`wcxcw/harness-skills`；在其他项目中使用上面的命令安装远程来源。

如果之前安装过 `harness-skills@harness-skills`，更新 marketplace 后请安装
`harness@harness`，并检查旧插件是否仍启用，避免两套 hooks 同时运行。新插件的
hooks 需要按 Codex 提示检查信任状态；已有项目的 `harness/` 和 run 记录应予保留。
具体升级、配置继承和 hook 信任行为取决于客户端，需在安装后确认。

安装或启用插件不会自动信任 hooks：在 Codex 中审阅并信任当前 hook 定义后，
在新会话确认 SessionStart 提醒和所需 Skill 可见。没有可用的 Stop hook 时，
按工作流执行本地 gate，并在通过后显式关闭 run。

## 主要入口

| Skill | 用途 |
| --- | --- |
| [`agent-harness`](plugins/harness-skills/skills/agent-harness/SKILL.md)（Manage Project Harness） | 初始化、运行和维护项目级 harness 的主入口。 |
| [`grilling`](plugins/harness-skills/skills/workflows/grilling/SKILL.md) | 用户显式调用的 run 前共识对齐；一次确认一个决策，不创建文件。 |
| [`workflows`](plugins/harness-skills/skills/workflows/SKILL.md) | 闭环工作流集合：规格、计划、执行、调试、review、验证和收尾。 |
| [`meta`](plugins/harness-skills/skills/meta/SKILL.md) | 维护和改进 Harness 自身 skills。 |

## 它会生成什么

默认 `core` 脚手架会在目标项目中生成：

```text
AGENTS.md
harness/
├── context/
│   ├── project-brief.md
│   └── coding-conventions.md
├── controls/
│   ├── gates.md
│   └── risk-matrix.md
├── tools/
│   └── commands.md
├── guardrails/
│   └── boundaries.md
├── evals/
│   └── task-scorecard.md
├── scripts/
│   └── check_run.py
└── runs/
```

在本仓库源码目录中，也可以直接运行脚手架脚本：

```text
python3 plugins/harness-skills/skills/agent-harness/scripts/init_harness.py --project /path/to/project --language zh-CN
```

初始化前可只读发现项目清单、npm scripts 和 CI 文件：

```bash
python3 plugins/harness-skills/skills/agent-harness/scripts/discover_project.py --project /path/to/project
```

以上两条路径从本仓库源码目录执行；已安装插件的用户可直接调用主 Skill。
发现结果只代表文件或命令已声明，不代表命令已执行、安全或在当前环境可用。
根据任务需要和权限评估是否验证，不自动安装依赖、启动服务或执行部署。
初始化会保留已有文件；对于无法识别的非空 `harness/`，先检查其用途，只有明确
要在其中建立本插件的 Harness 时才使用 `--adopt-existing`。

## 工作闭环

需求模糊时，可以先显式调用 `$grilling`；它在 run 外完成共识对齐，不创建文件。明确的用户指令也可以作为对齐来源，无需重复确认。完整 run 的流程为：

```text
grilling（可选、run 外）
  -> 明确需求与必要决策
  -> spec
  -> plan
  -> before-implementation gate
  -> execute
  -> review
  -> evaluation 草稿
  -> verification
  -> 更新 evaluation 并复查 gate
  -> harness feedback
```

对应的 run artifacts：

| 文件 | 用途 |
| --- | --- |
| `workflow.md` | 记录使用过的 skills、生命周期决策和 gate 状态。 |
| `spec.md` | 共识来源、用户确认、目标、范围、产品/技术决策、验收标准、验证方式和所需证据。 |
| `plan.md` | 任务顺序、依赖、可能修改的文件、验证方式和证据要求。 |
| `execution-log.md` | 修改文件、执行命令、测试结果、失败信息和跳过的检查。 |
| `review.md` | review 范围、发现、处理结果和剩余风险。 |
| `evaluation.md` | 验收结果、验证结果、review 状态、残留风险和 harness 反馈。 |

应用代码变更可以使用质量 workflow：

| Skill | 用途 |
| --- | --- |
| `code-quality-review` | 检查可维护性、结构、本地约定、注释、日志和可测试性。 |
| `frontend-quality-review` | 检查前端组件边界、状态/数据分离、响应式、可访问性和浏览器证据。 |
| `backend-quality-review` | 检查后端边界、输入校验、日志、错误处理和可运维性。 |
| `code-reviewer` | 提供针对性 review 清单；按实际方式记录独立审查或自查。 |
| `receiving-code-review` | 在同一个 active run 中处理 review 反馈并记录验证证据。 |
| `context-budget` | 在上下文文件或历史 run 较多时控制选择性读取。 |

插件级 hooks 和脚本提供更强约束：

| 能力 | 用途 |
| --- | --- |
| `hooks/hooks.json` | SessionStart 上下文提醒，以及 Stop 阶段 harness gate。 |
| `scripts/quality_check.py` | 检查变更范围和 review 记录，并提示可能的结构或日志问题。 |
| `skills/agent-harness/scripts/discover_project.py` | 只读发现常见项目清单、npm scripts 和 CI 文件。 |
| `harness/controls/risk-matrix.md` | 风险分级，用于 tier、review 深度和证据强度选择。 |

## 分级闭环

需要 run 时，选择能安全控制工作的最小 tier。

no-run 直接修改必须同时满足微小改动条件：请求明确、影响局部、不改变行为、
不需要决策、能用一次小检查验证、可以局部回滚。例子：错别字、一句文案、一个
明确选择器的字号修改、一个间距/颜色 token。宽泛视觉优化、整体字体层级调整、
跨页面修改、行为变化，或需要设计/产品/技术决策的任务，应使用最小 run tier。

一个 run 对应一个用户目标，不对应 agent 的每次尝试。针对同一目标的返修、
补测试、补验证和小调整，应继续追加到当前 active run，直到用户验收或该 run
关闭。只有目标改变、范围明显扩大，或用户明确开始新任务时，才新建 run。

### XS

适合仍需要 run 记录的小改动，例如低风险文档/配置/代码修改，并需要验证证据。

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── execution-log.md
├── run-state.json
└── evaluation.md
```

### Standard

适合大多数功能、bugfix 和结构化修改。

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── workflow.md
├── spec.md
├── plan.md
├── execution-log.md
├── run-state.json
└── evaluation.md
```

### Full

适合新功能、greenfield、产品方向、复杂 bug 或高风险修改。

```text
harness/runs/YYYY-MM-DD-short-task-name/
├── input.md
├── workflow.md
├── spec.md
├── plan.md
├── execution-log.md
├── review.md
├── run-state.json
└── evaluation.md
```

`run-state.json` 在支持会话绑定时生成；各 tier 的工作流要求和检查器实际验证范围并不完全相同，具体以项目本地 gate 为准。

## 本地 Gate

目标项目会生成 `harness/scripts/check_run.py`，用于在实现前和交付前检查当前 run 是否满足所选 tier 的最低要求。

Workflow skills 可以帮助 Agent 做事，但不能绕过项目本地 gate。

完成检查会校验记录中有带内容的命令或手动检查、结果和评价字段；它只检查
结构，不证明测试通过、验收完成或 review 充分。日志和大组件等启发式结果是
提示，不能替代对具体代码的判断。

Run 生命周期由各 run 目录内的 `run-state.json` 显式记录。Stop hook
只复查当前 session 标记为 `verifying` 的 run；纯交流、`active`、
`reviewing`、`closed`、旧版无状态 run 和其他 session 的 run 都不会触发
completion gate。禁止再按 run 目录修改时间推断当前任务。
创建或恢复 run 后应在修改前设置 `active`：在 Git 仓库内，它会记录当时的 HEAD
作为质量检查基线。检查包含基线后的已提交改动及工作区变更，不能判断改动归属。
旧 run、没有 Git 或基线不可用时会提示检查范围限制，需要人工补充审查。
Stop 被拦截后会再次检查；若再次失败，为避免无限循环会显示警告并保留
`verifying`，不能把该 run 视为完成。

插件升级后，如果只需把新的 gate Schema 同步到一个已经初始化的项目，可在本仓库源码目录使用：

```bash
python3 plugins/harness-skills/skills/agent-harness/scripts/init_harness.py \
  --project /path/to/project \
  --update-checker
```

该选项会覆盖目标项目现有的 `harness/scripts/check_run.py`，请先检查是否有项目专属修改；不会覆盖 `AGENTS.md`、context、controls 或其他本地约定。旧 run 的记录格式可能需要补充后才能通过新检查。

## 初始化模式

| 模式 | 使用场景 | 默认行为 |
| --- | --- | --- |
| `greenfield` | 空项目或一句话项目想法 | 需求或关键决策不清时邀请显式调用 `$grilling`，再按需要生成项目简介、规格和计划。 |
| `brownfield` | 已有源码、README、测试、CI 或依赖配置 | 先只读发现，再保守补充 harness 文件。 |
| `existing-harness` | 已识别的项目 Harness | 保留现有约定，补齐缺口，避免覆盖。 |

## 测试和效果评估

本仓库使用 `python3 -m unittest discover -s tests -v`；GitHub Actions 会在 Python
3.10 和 3.13 上运行同一套测试。评估插件对实际开发的帮助时，可在隔离副本上
选择同一批明确任务，分别记录是否启用插件、任务结果、验证证据、人工介入和
耗时。保持环境和验收标准一致；样本不足或尚未运行时，不推断净收益。

## 输出语言

- 用户用中文描述项目时，生成的 `AGENTS.md`、`harness/context/*`、`workflow.md`、`spec.md`、`plan.md` 和 run 记录默认使用中文。
- 命令、路径、包名、框架名和 API 名称保持原文。
- 老项目优先尊重已有文档语言；新增 run 记录可以跟随用户语言。

## 延伸阅读

- [Harness Engineering 介绍](docs/Harness%20Engineering.zh-CN.md)

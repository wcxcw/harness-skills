# Harness Engineering 简介

Harness 是模型之外支持 Agent 完成任务的环境和机制，例如上下文、工具、权限边界、验证和反馈。Harness Engineering 关注如何设计和维护这些机制，让 Agent 的工作更可理解、可验证、可持续改进。它可以提高可靠性，但不能保证 Agent 不犯错。

Prompt Engineering 关注怎样表达指令；Context Engineering 关注向模型提供什么信息；Harness Engineering 进一步关注 Agent 如何在真实环境中使用信息、调用工具、获得反馈并受约束。这些实践相互配合，边界并非严格划分。

## 为什么需要 Harness

- **上下文有限且会变化**：长任务可能包含过时方案、临时假设或相互冲突的决策。让 Agent 按需找到当前项目事实，比反复塞入全部历史更可靠。
- **跨会话需要可接续的状态**：上下文压缩可能遗漏细节，重要决策、进度和验证证据应有项目内的记录。
- **结果需要外部反馈**：Agent 自评不能代替测试、运行结果、review 和用户反馈；能够访问真实反馈有助于发现实现中的问题。

## 从引导到反馈

一个实用的 Harness 可以组合以下能力：

| 能力 | 作用 |
| --- | --- |
| 目标与范围 | 让 Agent 知道要解决什么、哪些内容不在范围内，以及如何验收。 |
| 项目上下文 | 提供可发现的架构、代码约定和项目事实，按任务需要读取。 |
| 工具与环境 | 让 Agent 找到可用的测试、构建、运行和排查方式。 |
| 边界 | 明确权限、数据、安全和项目约束。 |
| 反馈与评估 | 检查实际结果、记录风险，并把值得复用的经验反馈到项目中。 |

这些能力形成循环：**理解目标 → 执行 → 获取反馈 → 修正 → 根据证据改进环境**。约束应与项目风险相匹配；对简单任务，流程本身也应保持轻量。

## 本插件如何应用

Harness 插件帮助项目建立上下文、工作流记录、本地 gate 和反馈入口。它使用 Codex 提供的 Agent 运行环境，不会仅凭生成目录就保证项目可以运行或业务行为正确。

- 初始化时，先发现项目已有的代码、规则和命令，再保守地补齐需要的文件。
- 微小改动可不创建 run；需要记录时按风险选择 XS、Standard 或 Full。不是每个 tier 都要求 spec、plan 和 review。
- 根据改动选择项目已有的测试、构建、浏览器或其他验证方式，记录实际结果和未验证的风险。
- 本地 checker 和 hook 主要检查约定的结构与最低证据；证据真实性、验收和审查质量仍需判断。
- run 中发现的项目知识、命令或流程问题可以记录为 Harness Feedback，并在授权范围内验证和改进。

当前默认生成的目录、各 tier 的要求和具体命令以 [README](../README.md) 为准。项目可以根据自身需要保留额外文档和检查，而不必照搬固定模板。

## 参考

- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)：项目知识、工具、约束和反馈的实践。
- [Effective harnesses for long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)：跨会话状态与渐进式任务执行的实践。

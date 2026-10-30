# 命令

发现项目事实后再替换占位内容。不要运行标记为 `Unknown` 或 `Not applicable` 的命令。

状态含义：`Discovered` 表示有明确项目来源；`Inferred` 表示尚未确认的推测；
`Verified` 表示已在注明的环境执行并记录日期和结果；`Failed` 表示验证未通过。
在备注中记录工作目录、前提、来源、副作用、验证环境和证据。不要运行 `Inferred`
命令；只有项目证据支持时才能标记 `Not applicable`。保留已有项目使用的
`Confirmed` 等状态，但不要把它当作当前环境刚执行成功的证据。只运行与任务相关、
已了解副作用和前提条件且符合授权范围的命令。

| 用途 | 命令 | 状态 | 来源 | 备注 |
| --- | --- | --- | --- | --- |
| 安装 | `TBD` | Unknown | 未发现 | 仅在从项目文件或用户输入确认后替换。 |
| 开发服务 | `TBD` | Unknown | 未发现 | 已知时补充 host/port。 |
| Lint | `TBD` | Unknown | 未发现 | 只有项目证据支持时才标记为 `Not applicable`。 |
| 测试 | `TBD` | Unknown | 未发现 | 每次 run 优先使用最小相关测试命令。 |
| 构建 | `TBD` | Unknown | 未发现 | 如果项目不需要构建，标记为 `Not applicable`。 |
| 手动验证 | `TBD` | Unknown | 未发现 | 当命令验证不足时，描述项目专属检查。 |

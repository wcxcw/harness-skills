# 项目协作指南

Harness 是为 Codex 项目提供上下文、工作流和本地门槛的插件；本仓库本身是插件源码，不是生成后的目标项目。

- 安装方式、插件入口和用户工作流见 `README.md`；概念说明见 `docs/Harness Engineering.zh-CN.md`。
- 插件清单位于 `plugins/harness-skills/.codex-plugin/plugin.json`；Skill、脚本和目标项目模板位于同一插件目录下。
- 使用 Python 3 标准库，运行 `python3 -m unittest discover -s tests -v`；CI 在 `.github/workflows/tests.yml`。
- 修改生成模板或门槛时，同步检查相关 Skill、README 和测试，保留目标项目已有约定与中英文模板的一致性。
- `vendor/superpowers/` 是第三方参考快照；保留其许可和来源说明，不把它当成本插件对用户的工作流指令。
- 项目当前版本以插件清单为准；需要发布时按实际情况核对安装、升级和 hook 信任状态。

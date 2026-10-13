# Codex 基本用法

> 整理日期：2026-10-13
> 依据：本机安装的 `codex-cli 0.162.1`（`codex --help` 等命令实测）+ `~/.codex/config.toml`
> 说明：本次整理时本机网络无法解析 `developers.openai.com`，故未能抓取官方文档，内容以本机实测行为为准。

## 一、运行形态

| 形态 | 命令 | 用途 |
| --- | --- | --- |
| 交互式 TUI | `codex` 或 `codex "初始提示"` | 日常对话式编码，带命令菜单 |
| 非交互 | `codex exec "..."`（别名 `codex e`） | 脚本 / CI，提示可来自 stdin |
| 代码审查 | `codex review` | 对改动做 code review |
| 云端任务 | `codex cloud`（experimental） | 提交 / 查看 / 应用云端任务 |
| 会话管理 | `resume` / `fork` / `archive` / `delete` | 恢复、分叉、归档、删除历史会话 |

`codex exec` 把提示作为参数传入；若使用 `-` 或 stdin 被管道输入，则从 stdin 读取内容。

## 二、核心概念（决定行为的三件事）

- **沙箱** `-s, --sandbox`：控制模型执行 shell 命令时的文件 / 网络权限。
  - `read-only`：只读
  - `workspace-write`：工作区可写（默认常用）
  - `danger-full-access`：完全访问
- **审批** `-a, --ask-for-approval`：
  - `on-request`：模型自行决定何时请求人工批准
  - `never`：从不询问
  - `--dangerously-bypass-approvals-and-sandbox`：跳过全部沙箱与确认，**仅在外部已隔离环境使用**
- **模型** `-m, --model`；`--oss` + `--local-provider ollama|lmstudio` 走本地模型。

## 三、常用全局参数

- `-C <DIR>`：指定工作根目录
- `--add-dir <DIR>`：追加可写目录
- `--worktree`：在托管 Git worktree 中运行
- `-c key=value`：临时覆盖配置（点号路径，如 `-c model="gpt-5"`）
- `-p, --profile <name>`：叠加 `$CODEX_HOME/<name>.config.toml`
- `--search`：启用实时联网搜索工具
- `-i, --image <FILE>`：附带图片
- `--strict-config`：配置含未知字段时报错
- `--no-alt-screen`：禁用备用屏幕，保留终端滚动历史
- `--remote <ADDR>`：TUI 连接远端 app-server

## 四、常用子命令

| 命令 | 说明 |
| --- | --- |
| `codex login` / `status` / `logout` | 登录态管理（支持 `--with-api-key`、`--device-auth`） |
| `codex mcp add\|list\|get\|remove\|login` | 管理外部 MCP 服务器 |
| `codex plugin add\|list\|marketplace\|remove` | 插件市场与安装 |
| `codex features list\|enable\|disable` | 查看 / 切换功能开关 |
| `codex sandbox <cmd>` | 在 Codex 沙箱里直接跑命令 |
| `codex doctor [--json\|--summary]` | 诊断安装、配置、鉴权与运行时健康 |
| `codex apply <task_id>` | 应用云端任务产生的 diff |
| `codex completion <shell>` | 生成 shell 补全脚本 |
| `codex update` / `codex debug` | 升级 / 调试工具 |

`codex review` 常用参数：`--uncommitted`（审查未提交改动）、`--base <branch>`、`--commit <sha>`、`--title <title>`。

## 五、交互式斜杠命令

输入 `/` 会弹出命令菜单，本机二进制中确认存在的命令包括：

- 会话控制：`/new`、`/resume`、`/fork`、`/archive`、`/delete`、`/side`、`/plan`、`/compact`、`/clear`、`/quit`
- 配置：`/model`、`/approvals`、`/permissions`、`/status`、`/title`、`/theme`、`/experimental`
- 代码：`/review`、`/diff`、`/copy`、`/undo`、`/raw`、`/init`（生成 `AGENTS.md`）
- 扩展与数据：`/mcp`、`/apps`、`/plugins`、`/skills`、`/agent`、`/voice`、`/mention`
- 其他：`/feedback`、`/logout`、`/help`

## 六、配置与扩展层级（从轻到重）

1. 一次性约束 → 直接写在当前提示 / 线程里
2. 仓库约定 → `AGENTS.md`（支持嵌套子目录，就近生效）
3. 项目级 → `.codex/config.toml`；个人默认 → 全局 `~/.codex/config.toml`
4. 可复用工作流 → Skill
5. 可分发组合 → Plugin
6. 外部实时数据 / 操作 → MCP 连接器

## 七、认证

- 交互登录：`codex login`（可选 `--device-auth`）
- API Key：`printenv OPENAI_API_KEY | codex login --with-api-key`
- 查询状态：`codex login status`
- 注意：API Key 不等于 ChatGPT / Codex 云端 / 连接器 / 账号权限。

## 八、本机现状

- 版本：`codex-cli 0.162.1`，路径 `~/.nvm/versions/node/v22.23.1/bin/codex`
- 配置 `~/.codex/config.toml` 使用自定义 provider：
  - `model = "deepseek-v4-1-flash"`
  - `model_provider = "arkcli-coding-plan"`，指向火山方舟 Coding Plan（`wire_api = "responses"`）
- `codex login status`：未登录（走自定义 provider，不依赖 OpenAI 登录）
- 尚未配置任何 MCP 服务器
- 已启用的功能开关举例：`apps`、`browser_use`、`goals`、`fast_mode`

## 九、参考来源

- 本机 `codex --help` 及各子命令 `--help` 输出
- `~/.codex/config.toml`、`~/.codex/version.json`
- 官方文档：`https://developers.openai.com/codex/`（本次未能访问）

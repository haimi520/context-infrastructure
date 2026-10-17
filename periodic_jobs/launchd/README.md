# Launchd 配置指南（macOS）

cron 在 macOS 上属于 legacy 机制，睡眠时任务会被跳过且没有补跑；launchd 是 macOS 原生方案，
配合 24 小时开机的 Mac mini（`servers` 属性省电休眠恢复后仍能按日程触发）。

本目录包含脚本化安装的 agent 定义；迁移动线参考 `docs/CRONTAB.md` 的时间线，等价替换为 launchd。

## 文件清单

| 文件 | 作用 |
|------|------|
| `com.contextinfra.opencode-server.plist` | 常驻 OpenCode Server（127.0.0.1:4096，KeepAlive） |
| `com.contextinfra.heartbeat-observer.plist` | 每日 08:00 运行 L1 Observer（写 OBSERVATIONS.md） |
| `com.contextinfra.heartbeat-reflector.plist` | 每周日 09:00 运行 L2 Reflector（记忆晋升 + GC） |
| `run_with_env.sh` | 包装器：source 仓库根目录 `.env` 后用 `.venv/bin/python` 执行脚本 |
| `install.sh` / `uninstall` | 一键安装/反安装到 `~/Library/LaunchAgents` |

## 安装与卸载

```bash
cd periodic_jobs/launchd
./install.sh          # 安装并立即拉起 server
./install.sh uninstall
```

## 验证

```bash
launchctl list | grep contextinfra
curl -s -u "opencode:$OPENCODE_PASSWORD" http://localhost:4096/api/session
```

- server 的 `OPENCODE_SERVER_PASSWORD` 固定在 plist 的 EnvironmentVariables 里，
  与仓库根目录 `.env` 的 `OPENCODE_PASSWORD` 保持一致（不入库）。
- 日志写在仓库 `logs/`（已 gitignore）：`opencode_server.log` / `observer.log` / `reflector.log`。

## 已知事项

1. **v2 API 兼容**：当前 opencode 版本将 API 挂在 `/api/*` 前缀下，响应包 `{"data": ...}`，
   发送 prompt 用 `POST /session/:id/prompt`。`src/v0/opencode_client.py` 已做 v1/v2 双兼容。
2. **模型回落**：v2 的 prompt `model` 参数当前不被 server 采纳，会回落到 OpenCode
   集成的默认免费池（实测 `opencode/nemotron-3.5-super-vl-free`）。要固定高质量模型，
   待后续 opencode 版本或 agent 级别 model 配置支持后调整。
3. **Gmail 依赖**：`crontab_monitor` / `ai_news_survey` / `send_email` 依赖 Gmail SMTP，
   在境内网络不可达。接入替代邮件通道（如 QQ/163 SMTP 或自有邮件网关）后再补 launchd agent。
4. **Observer 幂等**：observer 在 OBSERVATIONS.md 已有 `Date: <当日>` 条目时自动跳过；
   手动补跑某天可这样调用：
   ```bash
   .venv/bin/python periodic_jobs/ai_heartbeat/src/v0/observer.py 2026-10-17
   ```

## 与 CRONTAB.md 的对应关系

`docs/CRONTAB.md` 描述的时间线（Session Sync / Observer / Reflector / Monitor / News Survey）
依然适用；macOS 上将 cron 条目换成对应的 launchd plist 即可，路径同 `docs/CRONTAB.md`。

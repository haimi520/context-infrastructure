# Memory Observations

这是三层记忆系统的 L1/L2 层。每日观察由 `periodic_jobs/ai_heartbeat/src/v0/observer.py` 自动写入，每周由 `reflector.py` 整理和蒸馏。

## 格式说明

每个日期条目格式如下：

```
Date: YYYY-MM-DD

🔴 High: [方法论/约束] 描述
🟡 Medium: [项目状态/决策] 描述
🟢 Low: [任务流水] 描述
```

### 优先级定义

- **🔴 High**：跨项目通用的经验教训、硬性约束、影响系统架构的重大决策。永久保留，候选晋升为 axiom 或 skill。
- **🟡 Medium**：活跃项目的关键进展、技术决策背景、未来几周仍需参考的信息。
- **🟢 Low**：日常任务流水、瞬时 debug 记录、临时上下文。定期垃圾回收。

## 如何加载记忆

不要全文加载这个文件（可能很大）。按需检索：

```bash
# 搜索特定主题
grep -n "关键词" contexts/memory/OBSERVATIONS.md

# 搜索最近 N 天
grep -A 20 "Date: $(date -v-7d +%Y-%m-%d)" contexts/memory/OBSERVATIONS.md
```

或使用语义搜索做跨日期语义检索（安装 [semantic-search-skill](https://github.com/grapeot/semantic-search-skill)）。

---

<!-- 以下是记录区域，由 observer.py 自动追加 -->

Date: 2026-10-17

🟡 Medium: [活跃项目状态] context-infrastructure 工作空间的 L3 约束与记忆系统已就绪：rules/SOUL.md、rules/USER.md、rules/WORKSPACE.md、rules/COMMUNICATION.md、rules/skills/INDEX.md 已到位；contexts/memory/OBSERVATIONS.md 作为 L1/L2 记忆层建立，periodic_jobs/ai_heartbeat/docs/KNOWLEDGE_BASE.md 定义了 Observer/Reflector SOP；rules/USER.md 已按 hill（老明）画像个性化（称呼、时区 CST、技术兴趣聚焦反垃圾邮件网关与 AI 开发）。
🟡 Medium: [活跃项目状态] 心跳基础设施从 cron 迁至 macOS launchd：periodic_jobs/launchd/ 新增 com.contextinfra.heartbeat-observer.plist、com.contextinfra.heartbeat-reflector.plist、com.contextinfra.opencode-server.plist，以及 install.sh、run_with_env.sh、README.md；periodic_jobs/ai_heartbeat/src/v0/observer.py 支持 WORKSPACE_ROOT 与 OPENCODE_MODEL，periodic_jobs/ai_heartbeat/src/v0/opencode_client.py 增加 /api/* 前缀路由的 v2 API 兼容并保留 v1 回退；docs/CRONTAB.md 已指向 launchd 部署。
🟢 Low: [任务流水] 执行 2026-10-17 L1 Observer 任务，扫描根目录变动（contexts/、adhoc_jobs/、tools/、periodic_jobs/、rules/）；未发现 contexts/blog/content/ 或 contexts/life_record/ 目录，故无博客/生活记录条目过滤；本条目以 append 方式写入 contexts/memory/OBSERVATIONS.md，未修改 rules/ 下任何文件，未执行 L2 Reflector 任务。

Date: 2026-10-18

🔴 High: [角色隔离] 仅执行 L1 Observer 任务，读取 periodic_jobs/ai_heartbeat/docs/KNOWLEDGE_BASE.md SOP 与 L3 约束（rules/SOUL.md、rules/USER.md、rules/WORKSPACE.md、rules/COMMUNICATION.md、rules/skills/INDEX.md），未修改 rules/ 下任何文件，未执行 L2 Reflector 规则晋升或垃圾回收，遵循 Observer/Reflector 独立阶段原则。
🟡 Medium: [活跃项目状态] 根目录扫描完成：periodic_jobs/ai_heartbeat/docs/PRD.md 为心跳项目新增需求文档；rules/axioms/ 下 43 条公理与 rules/skills/ 下 40 余技能文件构成 L3 约束与可复用能力体系；tools/ 下 opencode_job.py、send_email_to_myself.py、semantic_search/ 等工具脚本已就绪。
🟢 Low: [任务流水] 执行 2026-10-18 L1 Observer 任务：扫描 contexts/、periodic_jobs/、rules/、tools/、adhoc_jobs/ 变动；未发现 contexts/blog/content/ 或 contexts/life_record/ 目录，故无博客/生活记录条目过滤；以 append 方式写入 contexts/memory/OBSERVATIONS.md。

Date: 2026-10-18

🔴 High: [硬性约束/底线] launchd 心跳作业的 plist 与日志路径已由 `/Users/mingyu/Documents/Deepseek/context-infrastructure/` 迁至仓库根目录 `/Users/mingyu/context-infra/repo/`，periodic_jobs/launchd/com.contextinfra.heartbeat-observer.plist 与 periodic_jobs/launchd/com.contextinfra.heartbeat-reflector.plist 中的脚本与 StandardOut/StandardErrorPath 已更正；periodic_jobs/launchd/com.contextinfra.opencode-server.plist 已删除，opencode 后台服务不再由独立 launchd plist 托管。
🟡 Medium: [活跃项目状态/技术决策] periodic_jobs/launchd/run_with_env.sh 新增 ensure_opencode_service，在执行目标脚本前自动通过 `opencode service start/status` 解析 opencode v2 后台服务监听 URL，导出 OPENCODE_BASE_URL（/api 前缀）并从 ~/.config/opencode/service.json 读取 OPENCODE_PASSWORD，observer.py/reflector.py 可依赖后台服务可用；.gitignore 新增 `.worktrees/`，将 git worktree 隔离目录排除在版本控制之外。
🟢 Low: [任务流水] 执行 2026-10-18 L1 Observer 任务，扫描根目录变动（git diff + 昨日后 mtime 文件）；contexts/ 下未发现 contexts/blog/content/ 与 contexts/life_record/，故无博客/生活记录条目过滤；logs/ 下 observer.log、reflector.log 等今日被触及，属运行时噪声，不计入记忆；本条目以 append 方式写入 contexts/memory/OBSERVATIONS.md，未修改 rules/ 下任何文件，未执行 L2 Reflector 任务。

Date: 2026-10-19

🟡 Medium: [技术决策/基础设施] 心跳作业模型固定：opencode 顶层配置（仓库外的 ~/.config/opencode/opencode.jsonc）设置 "model": "volcengine/ark-code-latest" 后，v2 后台服务需重启才生效；重启前心跳 prompt 跑在免费池默认模型上，重启后经 smoke session 验证助理模型已切换，observer/reflector 输出质量基线由此锁定。
🟡 Medium: [架构局部变更] tools/send_email_to_myself.py 完成通用 SMTP 化：新增 SMTP_HOST/PORT/USERNAME/PASSWORD/SSL/FROM/TO 环境变量，SMTP_SSL=yes 走 465 SSL 端口、否则 587 STARTTLS，支持逗号分隔多收件人，并保留 GMAIL_* 变量向后兼容回退；.env.example 同步重写邮件配置段（自有邮件网关 / QQ / 163 均可接入），为对接 hill 自有反垃圾邮件网关场景铺路。
🟡 Medium: [技术决策] tools/semantic_search 从本地 LM Studio 单点依赖解耦：tools/semantic_search/search/cli.py 与 tools/semantic_search/search/embedding.py 的 endpoint、model、api_key 改为读取 SEMANTIC_EMBEDDING_ENDPOINT/MODEL/API_KEY 环境变量（默认值仍指向 localhost:1234 本地端点）；.env.example 记录 SiliconFlow 免费档 BAAI/bge-m3 配置（需 siliconflow.cn 注册实名拿 key）。
🟢 Low: [任务流水] 执行 2026-10-19 L1 Observer 任务：读取 periodic_jobs/ai_heartbeat/docs/KNOWLEDGE_BASE.md 与 L3 约束（rules/SOUL.md、rules/USER.md、rules/WORKSPACE.md、rules/COMMUNICATION.md）；以 find -newermt + git log/show 扫描根目录变动，今日实际内容变更为 commit 456e585（5 个文件，+51/-21）；噪声过滤：.env（gitignored，含本地凭据不记录内容）、logs/、.pytest_cache/、contexts/daily_records/ 均排除；contexts/blog/content/ 与 contexts/life_record/ 目录不存在，无博客/生活记录条目；本条目以 append 方式写入 contexts/memory/OBSERVATIONS.md，未修改 rules/ 下任何文件，未执行 L2 Reflector 任务。

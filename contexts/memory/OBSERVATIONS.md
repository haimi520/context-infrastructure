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

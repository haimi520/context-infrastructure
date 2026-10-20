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

Date: 2026-10-20

🔴 High: [硬性约束/密钥管理] 工作区密钥存放约定变更：.env 不再保存明文敏感值，真值入 macOS 钥匙串（service 约定 CONTEXTINFRA_<NAME>、account=$USER；网页门户账密用 CONTEXTINFRA_PORTAL_<站点>），tools/secret_helper.py 提供统一 get_secret()（环境变量优先、钥匙串回落），periodic_jobs/launchd/run_with_env.sh 在作业启动时自动回填 SMTP_PASSWORD、SEMANTIC_EMBEDDING_API_KEY、OPENDOOR_API_KEY、WUCUR_API_KEY；tools/send_email_to_myself.py、tools/semantic_search/search/cli.py、tools/semantic_search/search/embedding.py、tools/generate_image.py 已全部切换到该通道，.env.example 仅保留空键位与钥匙串操作说明。
🟡 Medium: [基础设施/活跃项目状态] AI 会话每日自动归档上线：periodic_jobs/launchd/com.contextinfra.session-export.plist 每日 04:00 运行 ~/context-infra/ecosystem/ai_session_export/export_sessions.py，覆盖 opencode、claude-code、codex、antigravity、dsh（deepseek-harness）、hermes 六个来源，增量状态存 contexts/ai_sessions/.export_state.json，归档产物落 contexts/ai_sessions/<source>/（私有不入库；10-19 已完成回填，dsh 196 个会话、hermes 约 1.3 万条目）；今日 04:00 首次定时触发成功（logs/session_export.log 显示 hermes scanned=5293 exported=0，无新增）。ecosystem 另落地 writing-skill（external-prose-lint CLI 已入根 .venv）与 share-pages 两个仓库，rules/skills/INDEX.md 已更新路由。
🟡 Medium: [架构局部变更] 报告分享链路从私有服务器 rsync 迁至 GitHub Pages：新增 tools/publish_report.sh（pandoc 一键生成自包含 HTML，支持 --indexed/--push，PAGES_REPO_DIR 指向 ecosystem/share-pages 本地 clone），清单与索引页改由 adhoc_jobs/share_site/manifest.json 与 adhoc_jobs/share_site/gen_index.py 管理，发布地址 https://haimi520.github.io/share/<slug>.html；rules/skills/share_report.md 增补 GitHub Pages 本地适配段，原 adhoc_jobs/yage_share/ 私有仓流程标记停用。
🟡 Medium: [新工具] tools/generate_image.py 新增文生图 CLI：默认 SiliconFlow Kolors 免费档，兼容 OpenAI 形状响应（url 与 b64_json 两种返回），并按 api-base 自动路由选取 OPENDOOR_API_KEY 或 WUCUR_API_KEY，密钥经 tools/secret_helper.py 读取；.env.example 同步补充图像生成配置段。
🟢 Low: [任务流水] 执行 2026-10-20 L1 Observer：读取 periodic_jobs/ai_heartbeat/docs/KNOWLEDGE_BASE.md 与 L3 约束（rules/SOUL.md、rules/USER.md、rules/WORKSPACE.md、rules/COMMUNICATION.md）；截至 08:00 今日无新 commit（HEAD=3271603），本次补记 10-19 下午 observer 之后落地的 11 个 commit（64f905a..3271603：generate_image、钥匙串迁移、session-export、GitHub Pages 管线等）；噪声过滤 logs/、contexts/ai_sessions/.export_state.json（运行时状态）、contexts/daily_records/、.env（gitignored 含凭据）；contexts/blog/content/ 与 contexts/life_record/ 不存在，无博客/生活记录条目；本条目以 append 写入 contexts/memory/OBSERVATIONS.md，未修改 rules/ 下任何文件，未执行 L2 Reflector 任务。

Date: 2026-09-13

🔴 High: [经验教训/自查] 对抗式自查中先"发现缺陷"再回退的案例：曾判定 MailFrom 重置总超时预算是 bug，重新按"每封邮件"语义推演后确认重置本就正确（同封邮件后续阶段不重置才是关键），回退改动并改补真正有价值的边界测试（同封 EOH 阶段预算不被续期）——自查结论本身也要被质疑，先推演语义再动代码。(mined from contexts/ai_sessions/dsh/20260913_109_实现_M1_internal_milter_骨架_d_j_接入_增量组装_socket_a.md)
🔴 High: [硬性约束/Go 配置] 严格配置解析中显式零值绝不能被默认值洗白：需逐键记录"键是否显式给出"，只对缺席键补默认；未知键解析期一律拒绝。gopkg.in/yaml v3 自定义 UnmarshalYAML 对同类型 `value.Decode(&parsed)` 会无限递归，须用辅助匿名结构体或逐键解码规避。(mined from contexts/ai_sessions/dsh/20260913_109_实现_M1_internal_milter_骨架_d_j_接入_增量组装_socket_a.md)
🔴 High: [安全设计] 被剥离/忽略的输入仍须占用资源预算：入站伪造 X-SpamsQR-Trace 头虽不进判定视图，其字节仍计入 HeaderBytes 预算，否则攻击者可用伪造头免费占额度。(mined from contexts/ai_sessions/dsh/20260913_110_实现_M2_快判_fastpath_X_SpamsQR_Trace_检测矩阵_Prefetche.md)
🔴 High: [安全设计] 防伪造信头的标准做法：EOM 注入我方签名头前先倒序剥除入站所有同名伪造头；签名用审计 HMAC 密钥环经 HKDF-SHA256 派生（info 钉死、kid 随版本、当前+上一 kid 受信），篡改/过期按"无 Trace 全量检测"处理，不引入新密钥面。(mined from contexts/ai_sessions/dsh/20260913_110_实现_M2_快判_fastpath_X_SpamsQR_Trace_检测矩阵_Prefetche.md)
🟡 Medium: [技术决策/spamsqr] M1 milter 骨架（PR #147）：d--j/go-milter v0.10.2 接入，unix 0660/环回 TCP 双形态 + 约 70 行自写 sd_listen_fds（无第三方依赖），256 信号量过载整条连接放行、panic 全 recover、dns 200ms/eoh 300ms/总 1s 分阶段预算 fail-open；healthz 子状态用 api 层 DTO 不传染 d--j 类型；macOS unix socket 路径有 104 字符上限，测试需注意。(mined from contexts/ai_sessions/dsh/20260913_109_实现_M1_internal_milter_骨架_d_j_接入_增量组装_socket_a.md)
🟡 Medium: [经验教训/协议适配] d--j/go-milter 回调的信封地址带 `<>`，与 qf 裸地址/SMTP 裸地址匹配前必须在 milter 侧规范化，否则检测器按裸地址匹配会全部失配（黑盒测试暴露的真实实现 bug）。(mined from contexts/ai_sessions/dsh/20260913_110_实现_M2_快判_fastpath_X_SpamsQR_Trace_检测矩阵_Prefetche.md)
🟡 Medium: [技术决策/spamsqr] M2 fastpath 检测矩阵（PR #148）：milter 与队列共用同一批检测器实例和同一 policy.Provider 保证口径一致；SPF Evaluate 支持 Prefetched 短路，DMARC 内部复用同一 Evaluate 自动受益；中性类型（PrefetchedFacts/MilterTrace）定义在 scanner 包防导入环；EOH 阶段只产事实永不拒收。仓库首个 qf 回写为 H 行删除器，兼容 H?/H?F?/裸形态+折叠续行，其余字节逐字保留，allow/隔离释放出站前剥 Trace、隔离/拒绝/归档留存保留取证。(mined from contexts/ai_sessions/dsh/20260913_110_实现_M2_快判_fastpath_X_SpamsQR_Trace_检测矩阵_Prefetche.md)

Date: 2026-09-14

🔴 High: [硬性约束/PostgreSQL] PG `inet::text` 返回带 `/32` 后缀文本，会导致解析和 JOIN 失败；INET 参数用 `$1::inet` 传入、读出统一用 `host()` 去后缀。`INSERT ... ON CONFLICT` 的冲突动作必须在单语句内完成——冲突后事务已 abort，不能在同一事务继续 UPDATE。(mined from contexts/ai_sessions/dsh/20260914_105_实现_C2_IP_封禁域与_030_迁移_ip_bans_NOTIFY_内存视图_s.md)
🔴 High: [经验教训/迁移] 迁移不仅加表加列，还要核验真实迁移链中的权限形态：实测发现早期迁移（023）的默认 GRANT ALL 链会给应用角色留下不该有的 DELETE，领域不变量"历史行不物理删除"须在新迁移里显式 REVOKE 收窄，并用 has_table_privilege 双断言测试钉死真实链权限（而非只测新建库）。(mined from contexts/ai_sessions/dsh/20260914_105_实现_C2_IP_封禁域与_030_迁移_ip_bans_NOTIFY_内存视图_s.md)
🔴 High: [经验教训/并发合并] 多实例指标合并幂等：分桶快照合并用 GREATEST 防乱序旧快照把 gauge 回退；部分唯一索引做"活跃部分唯一"实现 upsert 幂等（ON CONFLICT DO NOTHING，冲突只累加 hit_count 不刷 TTL）；NOTIFY 增量必须配全量对账（1s）+ 断线重连追赶，且 LISTEN 的 onReady 回调是健康翻转依据——连接完成 LISTEN 注册前发出的 NOTIFY 会丢失。(mined from contexts/ai_sessions/dsh/20260914_105_实现_C2_IP_封禁域与_030_迁移_ip_bans_NOTIFY_内存视图_s.md)
🔴 High: [经验教训/测试假绿] shell 测试里 `jq -e` 对空输入会误判退出码 0（假绿）：curl body 因 bash 引号损坏变成非法 JSON→400→响应为空，断言却通过，连锁掩盖后续场景失败。HTTP 断言必须加非空/HTTP 状态码断言，不能只信 jq 管道退出码。(mined from contexts/ai_sessions/dsh/20260914_106_实现_C3_milter_连接特征接线_封禁管理面_带外_CLI_审计.md)
🔴 High: [安全设计/取证] 异步落库先预选 ID：连接越阈时先在内存预选 ban_id 再异步写库，550 审计可先于 PG 提交引用同一 ban_id，保证取证互查链不断（通道满/写失败路径的完整降级链在后续 triage 中被发现仍有缺口，见 09-15 #153）。(mined from contexts/ai_sessions/dsh/20260914_106_实现_C3_milter_连接特征接线_封禁管理面_带外_CLI_审计.md)
🔴 High: [经验教训/计数语义] 滑动窗口计数器三要点：①"增点再比对"实现"第 N+1 封越阈"语义，联合判定（A-13/A-14）时任一现值已达阈则两者都不增点；②gauge 归还只能减自己实际增过点的连接，observe 模式越阈不增点却标 counted 会净减他人名额导致方向偏松漏判（该 bug 在 09-15 triage 中实锤）；③判定热路径保持纯内存零 IO，封禁写入由调用方异步执行。Start 须幂等防重复调用致 Wait 挂起。(mined from contexts/ai_sessions/dsh/20260914_108_实现_C1_连接特征计数核心_精确滑窗_并发_gauge_主.md)
🔴 High: [架构模式/降级] 事件写库降级链标准形态：PG 主写失败→本地 SQLite 缓冲（PRAGMA 自动补列兼容老缓冲文件）→恢复后 UPSERT 同步，空串/无值字段归一为 SQL NULL（空动作/kid→NULL、无快判分→spam_score NULL）；读取老行必须容错 NULL（NullString/NullFloat64）；迁移含存量行 UPDATE 回填且两遍幂等。观测/审计写库失败绝不改 SMTP 应答（fail-open）。(mined from contexts/ai_sessions/dsh/20260914_111_实现_M3_029_迁移_MilterEventSink_双阶段事件列_降级.md)
🔴 High: [硬性约束/Sendmail] sendmail .mc 文件注释必须用 `dnl`：普通 `#` 行会被 m4 宏展开，注释中裸写的 INPUT_MAIL_FILTER 被零参调用产生空 `X, ` 过滤器定义致 sendmail 拒载。Connect 阶段 milter 拒绝在真实 MTA 表现为问候期 554（EHLO 之前），信封阶段才是 550——e2e 断言不能混用。不可解析发件域需 `accept_unresolvable_domains`，否则 check_mail 先于 milter 回 553。(mined from contexts/ai_sessions/dsh/20260914_112_实现_M4_Sendmail_挂接交付_docker_e2e_inbound_cf_systemd_so.md)
🟡 Medium: [经验教训/测试设施] 队列巡检测试的 Claim/Nack 循环必须按 queue ID 去重：Claim 后 Nack 把文件还原为 qf，下一轮又领到同一封→无限循环直到 OOM（exit 137）。容器以 root 跑会绕过 chmod 0555 等权限检查产生伪影失败，权限类测试须用非 root 用户复跑确认。(mined from contexts/ai_sessions/dsh/20260914_112_实现_M4_Sendmail_挂接交付_docker_e2e_inbound_cf_systemd_so.md)
🟡 Medium: [技术决策/spamsqr] C2 封禁域（PR #151）：128 位排序区间内存视图（atomic 不可变快照、零 PG 查询、IPv4-mapped 等价、惰性过期）+ NOTIFY 增量/1s 对账/60s sweeper 逐条审计；双 Coordinator 交叉流量 ≤2 轮收敛。C3 判定门（PR #153）为六步链：环回豁免→trusted_cidrs→邮件侧 ip allow→活跃封禁 550→A-13/A-14 越阈先封后拒→既有 FastPath，MAIL FROM 复查、EOH 喂 A-12（越阈只封不拒当前邮件）。(mined from contexts/ai_sessions/dsh/20260914_105_实现_C2_IP_封禁域与_030_迁移_ip_bans_NOTIFY_内存视图_s.md)
🟡 Medium: [经验教训/Go CLI] Go flag 包遇位置参数即停解析，CLI 需支持 `<ip> --yes` 任意顺序时要手动提取参数；测试里 MySQL/PG 等 DSN 的 `$$` 会被 bash 当 PID 展开，复杂验证 SQL 应写成脚本文件执行而非层层内联转义。(mined from contexts/ai_sessions/dsh/20260914_106_实现_C3_milter_连接特征接线_封禁管理面_带外_CLI_审计.md)
🟡 Medium: [技术决策/spamsqr] M3 MilterEventSink（PR #149）：reject/discard/tempfail 以 `M`+时间相关 ULID（27 字符 ≤VARCHAR(32)，与 qf* 命名空间隔离）写 stage=milter 稀疏行，复用同一缓冲设施；审计逐条事件 + fastpath_error 分钟级聚合。M4（PR #150）交付 inbound.cf（无 F=R/F=T 真 fail-open，T=2s/2s/3s 大于内部 1s 预算）、systemd socket（Wants 非 Requisite）、docker e2e（真实 Sendmail 8.17+swaks 四场景 22 断言，compose profile 门控），M1–M4 全部合入 master。(mined from contexts/ai_sessions/dsh/20260914_111_实现_M3_029_迁移_MilterEventSink_双阶段事件列_降级.md)
🟡 Medium: [环境/Docker Desktop] 本机 Docker Desktop 反复出现容器卡 Created、bind mount/virtiofs 故障、重启后端口转发代理未就绪等 flaky 行为；可靠绕行：`compose up --no-start` + 手动 `docker start`、docker cp 同步源码替代挂载、本机交叉编译 linux 二进制再做小上下文镜像；CI Linux runner 无此问题。(mined from contexts/ai_sessions/dsh/20260914_112_实现_M4_Sendmail_挂接交付_docker_e2e_inbound_cf_systemd_so.md)

Date: 2026-09-15

🔴 High: [架构模式/兜底] 实时路径与兜底路径必须共用同一套归一化/判定/写入组件：A-12 mail_events 兜底聚合任务与实时路径同一 CanonicalSubject、同一 ObserveMessage、同一 BanService，豁免口径（环回/trusted_cidrs/allow）也一致，否则两条路径会产出不同结论；查询按复合索引并以 EXPLAIN 断言固化执行计划。(mined from contexts/ai_sessions/dsh/20260915_107_实现_C4_A_12_mail_events_聚合兜底_access_db_适配器_阻断部.md)
🔴 High: [经验教训/测试替身] 测试替身必须忠实复刻产品的主动语义：e2e 内存封禁器只有惰性 TTL 而产品有主动 sweeper，access_db map 在 milter 之前抢先拒绝后连接到不了 milter，惰性过期永不触发，map 残留连锁导致场景失败。替身行为差异本身会制造假 bug。(mined from contexts/ai_sessions/dsh/20260915_107_实现_C4_A_12_mail_events_聚合兜底_access_db_适配器_阻断部.md)
🔴 High: [硬性约束/配置校验] fail-closed 与 fail-open 的边界：可执行外部命令的配置（render_user 非空时 makemap_cmd 必须绝对路径）属启动校验拒启动，不能做成运行时降级；而观察/改写/审计等运行期失败才 fail-open（原文照投 + 日志 + 指标 + healthz 子状态 + 事件标记）。外部文件渲染走临时文件/fsync/原子改名，事件唤醒用 cap=1 非阻塞信号（合并不丢、永不阻塞），失败只告警不回滚（旧 map 偏严继续挡）。(mined from contexts/ai_sessions/dsh/20260915_107_实现_C4_A_12_mail_events_聚合兜底_access_db_适配器_阻断部.md)
🔴 High: [硬性约束/qf 改写] 投递前 qf 改写层固定五步顺序（剥 Trace→剥入站伪头→注我方 Authentication-Results→label 三头→Subject 幂等前缀），在 worker"归档之后、事件之前"一次原子重写（temp+fsync+rename），df 一个字节不动，归档 .eml 永远是原文；释放路径复用同一层但只剥离不注 A-R（释放不重扫、metadata 不落库、禁止重算/DNS）。Subject 前缀 MIME 解码后检测、原 RFC2047 编码词不重编码。qf H 行 flags 解析不能把值中的 `?`（RFC2047 编码词）误判为 flags 分隔符。(mined from contexts/ai_sessions/dsh/20260915_115_实现_D2_投递前_qf_改写层_剥_Trace_伪头_注_Authentica.md)
🔴 High: [安全设计/DSN] DSN 对齐闸门 fail-closed：SPF pass（身份域非空）或 DMARC 对齐 + 信封域 MX/无 MX 退化 A/AAAA 可达（DNS 超时即不可达）+ 非空合法反向路径才发 DSN，temperror/none/缺信号一律不发（防背散射）。退信先落 spool 后提交 reject、独立 goroutine 五级指数退避（1m/5m/30m/2h/6h）、重扫幂等保证一封至多一 DSN（Nack 场景）、状态双通道回填（SQLite 未同步行优先→PG）防 sent 回退。(mined from contexts/ai_sessions/dsh/20260915_116_实现_D3_RFC3464_DSN_全链_对齐闸门_报文构造_10025_提.md)
🔴 High: [经验教训/邮件构造] 构造/过滤信头白名单时不能用 map 直接索引：`net/mail` 会把信头键规范化（Message-ID→Message-Id），大小写不一致即漏字段，须用 `Header.Values()` 遍历。RFC3464 DSN 信头白名单子集超 64KiB 截断、Diagnostic 只放通用文案+总分（不泄内部规则细节）。(mined from contexts/ai_sessions/dsh/20260915_116_实现_D3_RFC3464_DSN_全链_对齐闸门_报文构造_10025_提.md)
🔴 High: [方法论/triage] 合并前 triage 的价值实证：对 CI 全绿的大型功能 PR 仍独立核验（不采信作者自述、子代理结论也要亲自最小复现），实锤三个真 bug——observe gauge 串减漏判（违反"只偏严不漏放"）、预选 ban_id 失败路径取证链断裂、Connect 零值地址缺 IsValid 守卫致幻影键；诊断≠修复，用临时 worktree/纯内存测试复现后即删，业务分支零改动，结论拆成三张 bug 票（#155/#156/#157）带可测验收标准交付。(mined from contexts/ai_sessions/dsh/20260915_153_C3_milter_连接特征接线_封禁管理面_带外_CLI_审计指标_2.md)
🔴 High: [硬性约束/GitHub 流程] 堆叠 PR（stacked PR）合并事故：PR 显示 MERGED 但 base 是未入 master 的特性分支时，整块代码实际游离主干——GitHub 只在 base 分支被删除时才自动 retarget，base 未删则不触发，源 issue 却按"合入后自动 retarget"的预期关闭。合流规范须写明：base 入 master 后立即删分支，或人工确认 retarget；合并后用 `git ls-tree`/净 diff 文件数断言代码确在 master。(mined from contexts/ai_sessions/dsh/20260915_154_feat_ipban_C4_mail_events_兜底聚合_access_db_适配器_阻断部署.md)
🟡 Medium: [环境/沙箱方案] DSH macOS seatbelt 沙箱可写路径硬编码为项目目录、/tmp、$TMPDIR 且无白名单配置，但工作区外可读可执行。一劳永逸布局：只读工具链（Go SDK、libpq/psql bottle 解压）放 `~/.dsh-toolchain/` + `~/.local/bin` 软链；可写缓存放 `$TMPDIR`（按用户跨会话稳定）+ 只读种子用 APFS 克隆 `cp -Rc` 秒级冷恢复；BASH_ENV 引导脚本在每个 `bash -c` 自动设 PATH/GOPATH/GOCACHE/GOPROXY=goproxy.cn。launchctl setenv 在沙箱内静默失败，GUI 启动须在普通终端执行。(mined from contexts/ai_sessions/dsh/20260915_116_实现_D3_RFC3464_DSN_全链_对齐闸门_报文构造_10025_提.md)
🟡 Medium: [技术决策/spamsqr] D1 处置枚举（PR #159，031 迁移：label/discard + label_at 分数带）；D2 改写层（PR #160，032 迁移 + healthz disposition 子状态不动 200/503 + rewrite_failures_total 指标，下游 #99/N1 迁移号顺延 033 并在 #120 留言衔接）；D3 DSN（PR #161，map 约束的 outbound.* 指标更名待 N1/#120 落地，按先例留言告知而非自行等待）。跨票迁移号顺延与接口更名须显式在下游票留告知评论。(mined from contexts/ai_sessions/dsh/20260915_114_实现_D1_处置枚举扩_label_discard_label_at_分数带_规则_d.md)
🟡 Medium: [经验教训/triage] triage 首轮即便 CI 全绿也不放松：PR #153 首轮诊断用本地 Go 跑纯内存最小复现实锤 observe 模式阈值 2 时第 4 连接漏信号（红），并验证"一行修"后三包回归全绿再写 Agent Brief；待维护者拍板时标签不猜着转、可暂时停留但须写明等待项，二次 triage 再独立复验首轮结论无一误报后才落 ready-for-agent。(mined from contexts/ai_sessions/dsh/20260915_153_C3_milter_连接特征接线_封禁管理面_带外_CLI_审计指标.md)
🟡 Medium: [技术决策/spamsqr] access_db 适配器（PR #154/#158）：全量重渲染 `<IP>\tREJECT` + `-T<TMPF>` 热读支持 release/expire 撤销，render_user 走 `sudo -n` 最小特权助手，NOTIFY 跨实例扇出；e2e 场景⑧验证停掉 milter 后已封 IP 仍 REJECT、解除后无需重启 sendmail 热放行（八场景 41 断言）。C1–C4 连接特征四票至此全部交付。(mined from contexts/ai_sessions/dsh/20260915_107_实现_C4_A_12_mail_events_聚合兜底_access_db_适配器_阻断部.md)

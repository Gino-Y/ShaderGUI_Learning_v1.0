# Token 节省率报表

## 结论

在当前项目中，让 Cursor Codex 接手长执行任务，并通过 `.agent/STATE.md`、`.agent/handoff/CURSOR_HANDOFF.md`、`.agent/memory/YYYY-MM-DD.md` 回传摘要，预计可为原生 Codex 节省 **55% 到 80%** 的恢复与排查 token。

推荐目标值：

```text
常规交接节省率：60%+
高质量交接节省率：75%+
低质量交接节省率：可能低于 30%，甚至反向增加消耗
```

## 估算模型

Token 消耗分为三类：

| 场景 | 原生 Codex 直接执行 | Cursor 执行后交接 | 预计节省 |
| :--- | :--- | :--- | :--- |
| 读取全项目状态 | 8k-20k | 1k-3k | 65%-85% |
| 反复看报错与修复 | 10k-40k | 1k-5k 摘要 | 70%-90% |
| DAG/规则一致性检查 | 5k-15k | 2k-6k | 40%-70% |
| 代码差异定位 | 8k-25k | 3k-8k | 50%-70% |
| 最终验证收尾 | 3k-8k | 1k-3k | 50%-65% |

综合估算：

```text
无交接：约 34k-108k token
有结构化交接：约 8k-25k token
节省率：约 55%-80%
```

## 节省率公式

```text
Token 节省率 = (无交接预计 token - 结构化交接 token) / 无交接预计 token
```

示例：

```text
无交接预计：60,000 token
结构化交接：15,000 token
节省率 = (60,000 - 15,000) / 60,000 = 75%
```

## 高质量交接标准

Cursor 每轮结束后只保留必要信息：

- 当前目标
- 已完成事项
- 修改文件清单
- DAG 是否受影响
- 已运行验证命令与结果
- 未完成/阻塞
- 下一步建议

推荐读取入口：

```text
.agent/STATE.md
.agent/handoff/CURSOR_HANDOFF.md
.agent/memory/YYYY-MM-DD.md
docs/Skill_Chain_DAG.md
scripts/verify_course.py
```

## 低质量交接的 token 风险

以下情况会显著降低节省率：

- 不更新 `.agent/STATE.md`
- 不写 `CURSOR_HANDOFF.md`
- 把完整终端日志贴进 memory
- 只写“已完成”，不列修改文件
- 改了 DAG 但没更新 `docs/Skill_Chain_DAG.md`
- 修改 `CourseApp/` 但忘记同步 `.agent/templates/course-app/`
- 验证失败但只记录结论，不记录失败命令

风险估算：

```text
高质量交接：节省 65%-80%
普通交接：节省 45%-60%
低质量交接：节省 0%-30%
无交接或错误交接：可能增加 20%-50% token 消耗
```

## 当前项目建议

本项目已经具备良好的 token 节省基础：

- 有 `.agent/STATE.md`
- 有 `.agent/handoff/CURSOR_HANDOFF.md`
- 有 `.agent/memory/YYYY-MM-DD.md`
- DAG 文档集中在 `docs/Skill_Chain_DAG.md`
- 验证入口集中在 `scripts/verify_course.py`
- MVP 模板已拆到 `.agent/templates/`

建议后续目标：

```text
每次 Cursor 接手后，原生 Codex 恢复读取不超过 5 个文件。
每次 handoff 控制在 80-160 行内。
每次 memory 追加控制在 8-12 行内。
终端日志只写结果，不贴全文。
```

## 目标指标

| 指标 | 推荐值 |
| :--- | :--- |
| 恢复读取文件数 | 3-5 个 |
| handoff 长度 | 80-160 行 |
| memory 单条长度 | 8-12 行 |
| 恢复 token 预算 | 5k-15k |
| 目标节省率 | 60%-75% |

## 最终建议

将 Cursor 用作长执行与局部修复代理，将原生 Codex 用作 DAG 守门、架构一致性和最终闭环代理。只要 Cursor 严格维护 handoff，预计长期可稳定节省 **约 2/3 的原生 Codex token**。

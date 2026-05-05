# AI Task Bootstrap Pointer

**本文件是指针文件（Pointer File），不受跨平台限制影响，不会被平台违规守卫移除或剪切。**

## 用途

本文件用于引导 AI 平台在每次操作任何任务前，必须先读取项目规则。

## 强制引导

**每次开始任何任务前，AI 必须执行以下操作：**

1. 读取 `.agent/rules.md`（项目 AI 行为规则）
2. 读取 `.agent/SKILL.md`（ShaderGUI Expert Skill）
3. 确认理解规则后，再开始执行任务

## 规则位置

- **主规则文件**：`.agent/rules.md`
- **Skill 定义**：`.agent/SKILL.md`
- **状态文件**：`.agent/STATE.md`
- **Handoff 协议**：`.agent/handoff/HANDOFF_PROTOCOL.md`

## 重要提醒

- `.agent/` 是唯一可信源
- 禁止将 `.cursor/`、`.workbuddy/` 作为规则、资产、Skill、workflow 或 prompt 来源
- 本文件只是指针，不是规则/资产/Skill 源

## 跨平台兼容性

本文件受 `platform_violation_guard.py` 的指针文件豁免保护，不会被误判为违规资产。

---

**AI 平台注意：操作任何任务前，请先读 `.agent/rules.md`！**

# ShaderGUI_Learning_v1.0 继续开发计划

**日期**: 2026-05-04  
**目标**: 将动画表演节点接入 DAG，完成 MVP 集成，避免"双规"问题

---

## 📊 当前状况分析

### ✅ 已完成的工作

1. **原生表演节点系统** (P0-P4 全部完成)
   - ✅ `scripts/visual_spec_schema.py` - 定义 VisualSpec Schema
   - ✅ `CourseApp/src/components/nodes/` - 10 个原生表演节点组件
   - ✅ `CourseApp/src/components/nodes/PerformanceNode.vue` - 表演节点调度器
   - ✅ `CourseApp/src/components/SlideCanvas.vue` - 集成 PerformanceNode
   - ✅ `scripts/build_visual_from_spec.py` - 从故事板生成 visualSpec
   - ✅ `scripts/validate_visual.py` - 验证 visualSpec

2. **Git 快照规范**
   - ✅ `.agent/rules.md` - 已添加 "Git 快照与回滚规范"

3. **Lottie 方案废弃**
   - ✅ 已清除所有 Lottie 遗留文件
   - ✅ 已回滚到 Lottie 集成前状态

### ❌ 未完成的 работ

1. **DAG 集成** (核心问题)
   - ❌ `StoryboardMCP.prepare_storyboard_contract()` 未生成 `visualSpec`
   - ❌ `storyboard-contract.json` 中没有 `visualSpec` 字段
   - ❌ `flow_engine.py` 的 `FlowState` 没有 `visualSpec` 字段
   - ❌ 动画表演节点未接入 DAG 流程

2. **MVP 验证**
   - ❌ 未运行 `verify_course.py`
   - ❌ 未运行 `npm run build`
   - ❌ 未执行浏览器验证

3. **"双规"问题**
   - ❌ 未更新 DAG 文档 (`docs/Skill_Chain_DAG.md`)
   - ❌ 未提交 AI 平台交叉开发汇报文件

4. **favicon 404 错误**
   - ⚠️ `CourseApp/public/favicon.svg` 已创建
   - ⚠️ 需要修改 `CourseApp/index.html` 引用 favicon.svg

---

## 🎯 开发计划 (8 个阶段)

### 阶段 0: Git 快照 (按照新规范)

**目标**: 在修改前创建快照，确保可回滚

**步骤**:
```powershell
# 1. 检查工作区状态
git status

# 2. 添加所有改动
git add .

# 3. 创建快照
git commit -m "Snapshot: Pre-VisualSpec-Integration - Before connecting animation nodes to DAG"
```

**验证**: `git log --oneline -5` 查看快照是否创建成功

---

### 阶段 1: 修改 StoryboardMCP (核心)

**目标**: 让 `StoryboardMCP` 生成 `visualSpec` 字段

**文件**: `.agent/mcp_servers/storyboard_mcp.py`

**修改内容**:
1. 导入 `visual_spec_schema` 和 `build_visual_from_spec`
2. 在 `prepare_storyboard_contract()` 方法中，为每个 cue 添加 `visualSpec`
3. 调用 `build_visual_for_cue(cue)` 生成 `visualSpec`

**示例代码**:
```python
# 在 storyboard_mcp.py 顶部添加
from scripts.visual_spec_schema import VisualSpec, AnimationType
from scripts.build_visual_from_spec import build_visual_for_cue

# 在 prepare_storyboard_contract() 方法中，构建 storyboard_slides 时
for index, slide in enumerate(module_slides):
    # ... 现有代码 ...
    
    # 为每个 cue 添加 visualSpec
    motion_cues = StoryboardMCP._motion_cues(workspace, kind, points, subtitle_path)
    for cue in motion_cues:
        cue["visualSpec"] = build_visual_for_cue(cue)
    
    storyboard_slides.append({
        # ... 现有字段 ...
        "motionCues": motion_cues,
    })
```

**验证**: 
- 运行 `python .agent/flow_engine.py --mode test --stage storyboard --scope module --module Module_01`
- 检查 `CourseApp/src/data/storyboard-contract.json` 中是否有 `visualSpec` 字段

---

### 阶段 2: 更新 flow_engine.py

**目标**: 将 `visualSpec` 集成到 DAG 流程

**文件**: `.agent/flow_engine.py`

**修改内容**:
1. 在 `FlowState` 数据类中添加 `visual_spec_file` 字段
2. 在 `STORYBOARD_READY` 状态处理中，记录 `visualSpec` 生成结果

**示例代码**:
```python
@dataclass
class FlowState:
    # ... 现有字段 ...
    visual_spec_file: str | None = None
    
# 在 run() 方法中，STORYBOARD_READY 状态
if state.status == "STORYBOARD_READY":
    # ... 现有代码 ...
    state.storyboard_file = res.get("storyboard_file")
    state.visual_spec_file = res.get("visual_spec_file")  # 新增
```

**验证**: 
- 运行 `python .agent/flow_engine.py --mode production --scope module --module Module_01`
- 检查是否顺利通过 `STORYBOARD_READY` 阶段

---

### 阶段 3: 验证 DAG 集成

**目标**: 确保 `visualSpec` 正确传递到前端

**验证清单**:
- [ ] `storyboard-contract.json` 中每个 cue 都有 `visualSpec` 字段
- [ ] `visualSpec` 包含 `composition`、`animation`、`layout`、`typography` 四个维度
- [ ] `visualSpec.animation.type` 是有效的动画类型 (如 `neural-core`、`cyber-grid` 等)
- [ ] `SlideCanvas.vue` 能正确接收 `visualSpec` prop
- [ ] `PerformanceNode.vue` 能正确渲染对应的动画组件

**测试命令**:
```powershell
# 1. 验证 storyboard-contract.json
python scripts/validate_visual.py --file CourseApp/src/data/storyboard-contract.json

# 2. 启动开发服务器
npm --prefix CourseApp run dev

# 3. 浏览器访问 http://localhost:5173/，检查动画是否渲染
```

---

### 阶段 4: 运行验证脚本

**目标**: 执行最小验证闭环

**命令**:
```powershell
# 1. 验证课程契约
python scripts/verify_course.py

# 2. 构建 Vue SPA
npm --prefix CourseApp run build
```

**预期结果**:
- ✅ `verify_course.py` 通过 (0 错误)
- ✅ `npm run build` 成功 (无编译错误)

**如果失败**:
- 检查错误信息，修复问题
- 重新运行验证，直到通过

---

### 阶段 5: 浏览器验证

**目标**: 手动验证前端渲染

**验证清单**:
- [ ] 访问 `http://localhost:5173/`
- [ ] 进入 `/module/Module_01/slide/p00`
- [ ] 检查动画表演节点是否渲染
- [ ] 播放音频，检查动画是否跟随字幕事件触发
- [ ] 检查 `favicon.svg` 是否正确显示 (如果已修复 `index.html`)

**如果发现问题**:
- 检查浏览器控制台错误
- 检查 `visualSpec` 传递到 `PerformanceNode` 的数据是否正确
- 检查 10 个表演节点组件是否正常工作

---

### 阶段 6: 更新 DAG 文档 (避免"双规"问题 1)

**目标**: 更新 `docs/Skill_Chain_DAG.md`，反映 `visualSpec` 集成

**修改内容**:
1. 在 DAG 总览的 mermaid 图中，添加 `visualSpec` 生成节点
2. 在"节点职责"表格中，更新 `StoryboardMCP` 的输出，添加 `visualSpec`
3. 在"运行时契约"章节，添加 `visualSpec` 的传递路径

**示例修改**:
```markdown
## DAG 总览

```mermaid
flowchart TD
  A["教学计划"] --> B["CourseMCP"]
  B --> C["MVPMCP"]
  C --> D["StoryboardMCP: 分镜头契约 + visualSpec"]  # 修改
  D --> E["V0MCP"]
  # ... 其他节点 ...
```

## 节点职责

| 节点 | 输入 | 输出 | 验收 |
| --- | --- | --- | --- |
| `StoryboardMCP` | slides、subtitles | `storyboard-contract.json` (包含 visualSpec) | motionCues 包含 visualSpec |
```

**验证**: 
- 检查 `docs/Skill_Chain_DAG.md` 是否同步更新
- 检查 `.agent/rules.md` 是否同步更新 (如果涉及规则变更)

---

### 阶段 7: 提交 AI 平台交叉开发汇报 (避免"双规"问题 2)

**目标**: 创建并提交叉开发汇报文件

**文件**: `.agent/reports/cross_platform_development_report_2026-05-04.md`

**内容**:
1. 汇报本次开发工作 (原生表演节点系统)
2. 汇报 DAG 集成工作 (visualSpec)
3. 汇报避免"双规"问题的措施
4. 汇报验证结果

**提交到 Git**:
```powershell
git add .agent/reports/cross_platform_development_report_2026-05-04.md
git commit -m "Report: AI Platform Cross-Development Report - VisualSpec Integration"
```

---

### 阶段 8: Git 快照 (完成后)

**目标**: 在完成所有工作后创建快照

**命令**:
```powershell
git add .
git commit -m "Snapshot: Post-VisualSpec-Integration - Completed DAG integration and verification"
```

---

## 🚨 风险与应对

### 风险 1: `StoryboardMCP` 修改影响现有功能

**应对**:
- 修改前创建 Git 快照 (阶段 0)
- 修改后运行完整验证 (阶段 4)
- 如果失败，立即回滚 (`git reset --hard <snapshot-hash>`)

### 风险 2: `visualSpec` 生成逻辑错误

**应对**:
- 编写单元测试 for `build_visual_for_cue()`
- 在 `StoryboardMCP.prepare_storyboard_contract()` 中添加验证
- 如果 `visualSpec` 生成失败，返回错误信息，不生成 `storyboard-contract.json`

### 风险 3: 前端渲染错误

**应对**:
- 检查 `SlideCanvas.vue` 的 `visualSpec` prop 传递
- 检查 `PerformanceNode.vue` 的组件映射
- 检查 10 个表演节点组件的导入路径

---

## 📅 时间估算

| 阶段 | 预计时间 | 依赖 |
|------|----------|------|
| 阶段 0: Git 快照 | 5 分钟 | 无 |
| 阶段 1: 修改 StoryboardMCP | 30 分钟 | 阶段 0 |
| 阶段 2: 更新 flow_engine.py | 15 分钟 | 阶段 1 |
| 阶段 3: 验证 DAG 集成 | 30 分钟 | 阶段 2 |
| 阶段 4: 运行验证脚本 | 15 分钟 | 阶段 3 |
| 阶段 5: 浏览器验证 | 30 分钟 | 阶段 4 |
| 阶段 6: 更新 DAG 文档 | 20 分钟 | 阶段 5 |
| 阶段 7: 提交交叉开发汇报 | 15 分钟 | 阶段 6 |
| 阶段 8: Git 快照 | 5 分钟 | 阶段 7 |
| **总计** | **2.5 小时** | |

---

## ✅ 完成标准

1. ✅ `storyboard-contract.json` 中包含 `visualSpec` 字段
2. ✅ `flow_engine.py` 成功生成包含 `visualSpec` 的故事板
3. ✅ `verify_course.py` 验证通过 (0 错误)
4. ✅ `npm run build` 构建成功
5. ✅ 浏览器验证通过 (动画正确渲染)
6. ✅ `docs/Skill_Chain_DAG.md` 已更新
7. ✅ AI 平台交叉开发汇报已提交
8. ✅ Git 快照已创建

---

## 📝 附录: 相关文件清单

### 需要修改的文件

1. `.agent/mcp_servers/storyboard_mcp.py` - 添加 visualSpec 生成逻辑
2. `.agent/flow_engine.py` - 添加 visualSpec 到 FlowState
3. `docs/Skill_Chain_DAG.md` - 更新 DAG 图示和节点职责

### 需要验证的文件

1. `CourseApp/src/data/storyboard-contract.json` - 检查 visualSpec 字段
2. `CourseApp/src/components/SlideCanvas.vue` - 检查 visualSpec prop
3. `CourseApp/src/components/nodes/PerformanceNode.vue` - 检查组件映射

### 需要创建的文件

1. `.agent/reports/cross_platform_development_report_2026-05-04.md` - 交叉开发汇报

---

**计划制定人**: WorkBuddy AI  
**计划日期**: 2026-05-04  
**预计完成日期**: 2026-05-04 (同一天，如果顺利)

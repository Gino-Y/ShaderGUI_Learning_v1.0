# DAG 流程与 visualSpecs 集成说明

## DAG 流程概述

`flow_engine.py` 定义了 ShaderGUI 课程的 DAG（有向无环图）流程，包括以下阶段：

1. **PREREQ**: 检查源材料与 .agent 规则
2. **V0_READY**: 验证 v0 API Key
3. **CLEANUP_BEFORE_MVP_READY**: 清理旧产物
4. **MVP_PRODUCTS_READY**: 生成 MVP 产物（CourseApp / CourseContent / scripts）
5. **MANIFEST_READY**: 检查课程 manifest
6. **STORYBOARD_READY**: 准备叙事故事板契约（**已集成 visualSpecs**）
7. **V0_PROTOTYPE_READY**: 创建 v0 React 原型与设计规则
8. **DESIGN_READY**: 准备设计契约
9. **TRANSCRIPTS_READY**: 检查逐字稿
10. **AUDIO_READY**: 生成讲解音频
11. **STITCHED**: Stitch 音频、字幕与播放器运行时
12. **VERIFY_READY**: 验证产物
13. **BUILD_READY**: 构建静态站点
14. **AUDIT_READY**: 审计合规
15. **DEPLOY_READY**: 部署

## visualSpecs 集成详情

### 集成位置
- **节点**: `STORYBOARD_READY`（阶段 6）
- **文件**: `.agent/mcp_servers/storyboard_mcp.py`
- **方法**: `StoryboardMCP.prepare_storyboard_contract()`

### 集成方式
1. **动态生成**: `prepare_storyboard_contract()` 方法现在为每个 slide 动态生成 `visualSpecs` 字段（不是硬编码）
2. **嵌入函数**: `build_visual_for_cue()` 和 `build_visual_specs_for_slide()` 作为 `StoryboardMCP` 的静态方法嵌入，避免跨目录导入问题
3. **验证**: `validate_storyboard_contract()` 方法添加了对 `visualSpecs` 字段的验证

### visualSpecs 结构
每个 `visualSpec` 包含以下字段：
- `cueId`: cue 标识符
- `trigger`: 触发条件（类型、时间码、段索引）
- `timeRange`: 时间范围（开始、结束、持续时间）
- `target`: 目标元素
- `contentBeat`: 内容节拍
- `sourceSubtitleText`: 源字幕文本
- `knowledgeFocus`: 知识焦点（id、标签、语义角色、学习者收获）
- `animation`: 动画规格（类型、持续时间、缓动、参数）
- `dynamicGuidance`: 动态指导（主要效果、注意模式、高亮目标等）
- `compositionBeat`: 构图节拍（帧区域、主体、摄像机动作等）
- `shotInstruction`: 镜头指令
- `focusInstruction`: 焦点指令
- `implementationHint`: 实现提示
- `purpose`: 目的

### 验证规则
- `visualSpecs` 必须是一个数组
- 每个 `visualSpec` 必须包含必要字段（`cueId`, `trigger`, `timeRange`, `target`, `contentBeat`, `knowledgeFocus`, `animation`, `dynamicGuidance`, `compositionBeat`）
- `trigger.type` 必须是 `"subtitle-segment"`
- `timeRange.start` < `timeRange.end`
- `animation.type`, `animation.durationMs`, `animation.easing` 必须存在
- `dynamicGuidance.primaryEffect`, `dynamicGuidance.attentionPattern`, `dynamicGuidance.highlightTarget` 必须存在且非空
- `compositionBeat.frameZone`, `compositionBeat.subject`, `compositionBeat.cameraAction`, `compositionBeat.spatialChange`, `compositionBeat.continuityRule` 必须存在且非空

## 使用示例

### 生成 visualSpecs
```python
from pathlib import Path
from agent.mcp_servers.storyboard_mcp import StoryboardMCP

workspace = Path(".")
result = StoryboardMCP.prepare_storyboard_contract(workspace, "Module_01")
print(result.get("status"))  # 应该是 "success"
```

### 验证 visualSpecs
```python
result = StoryboardMCP.validate_storyboard_contract(
    workspace, "Module_01", "CourseApp/src/data/storyboard-contract.json"
)
print(result.get("status"))  # 应该是 "success"
```

## 修改历史

- **2026-05-04**: 集成 `visualSpecs` 到 `storyboard` 节点（提交 `1cf11a0` 和 `bd28a30`）
  - 嵌入 `build_visual_for_cue()` 和 `build_visual_specs_for_slide()` 作为静态方法
  - 修改 `prepare_storyboard_contract()` 生成 `visualSpecs` 字段
  - 修改 `validate_storyboard_contract()` 验证 `visualSpecs` 字段
  - 验证通过：`Validate status: success`, `Validation passed!`

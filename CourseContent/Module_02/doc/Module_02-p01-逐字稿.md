# 只给用户他需要的：智能 UI 联动 —— 逐字稿

> 好的面板不是"能改所有参数"，而是"在当前配置下，只展示有意义的参数"。条件显示是专业感的核心来源。

## 核心观点

- **问题**：枚举切换后，某些参数对当前配置无意义，但还显示着，干扰判断
- **思路**：监听关键属性（Toggle/Enum），用 `EditorGUILayout.BeginFadeGroup` 或 `DisabledScope` 控制显隐
- **金句**："专业感 = 让美术感觉『这个面板懂我在做什么』。"

## 条件显示三板斧

| 技术 | 适用场景 | 用户体验 |
|------|----------|----------|
| `EditorGUILayout.BeginFadeGroup` | 展开/收起动画 | 顺滑，专业 |
| `EditorGUILayout.DisabledScope` | 参数不可用但需可见 | 灰显，不混乱 |
| `if (showAdvanced) { ... }` | 完全隐藏高级参数 | 简洁，但可能找不到 |

## 代码示例

```csharp
// ✅ 智能联动：Enum 切换控制参数组显隐
bool useRamp = (_RampMode.floatValue == 1);
EditorGUILayout.BeginFadeGroup(ref useRamp);
{
    MaterialEditor.TextureProperty("_RampTex");
    MaterialEditor.ColorProperty("_RampColor");
}
EditorGUILayout.EndFadeGroup();

// ✅ 安全禁用：参数存在但当前配置不适用
using (new EditorGUILayout.DisabledScope(!useRamp))
{
    MaterialEditor.RangeProperty("_RampBlend", "Ramp 混合");
}
```

## 工程实践建议

1. **联动逻辑写在 OnGUI 顶部**：先算 `bool showXX`，再统一用 `if (showXX)` 控制绘制
2. **避免深嵌套**：联动层级不超过 2 层，否则代码难维护
3. **给美术"高级选项"入口**：用 `EditorGUILayout.Foldout` 收起不常用参数
4. **联动状态写注释**：`// 当 _RampMode==1 时显示 Ramp 参数` —— 3 个月后你自己看得懂

# 告别参数地狱：逻辑化的分组设计 —— 逐字稿

> 参数多是 ShaderGUI 的常态，但"多"不等于"乱"。本节课教你用信息架构思维，把一堆属性变成有序面板。

## 核心观点

- **问题**：Shader 属性多了，默认面板是一维长列表，美术不知道什么是什么
- **思路**：按渲染逻辑分组，用 UI 边界（Vertical/Horizontal）建立视觉层次
- **金句**："好的 GUI 不是把参数都摆出来，而是让美术知道先填什么、后填什么。"

## 分组设计三原则

| 原则 | 做法 | 效果 |
|------|------|------|
| 功能内聚 | 把有关联的属性放一组 | 美术理解成本降低 |
| 顺序合理 | 按渲染顺序：贴图 → 颜色 → 光照 → 高级 | 符合思维习惯 |
| 视觉边界 | BeginVertical + BoxStyle 画分组框 | 一眼看清结构 |

## 代码示例

```csharp
// ✅ 按渲染逻辑分组
public override void OnGUI(MaterialEditor editor, MaterialProperty[] props)
{
    // 第一层：主贴图与颜色
    EditorGUILayout.BeginVertical(EditorStyles.helpBox);
    MaterialEditor.TextureProperty("_MainTex");
    MaterialEditor.ColorProperty("_Color");
    EditorGUILayout.EndVertical();

    // 第二层：光照参数
    EditorGUILayout.BeginVertical(EditorStyles.helpBox);
    MaterialEditor.RangeProperty("_Glossiness");
    MaterialEditor.RangeProperty("_Metallic");
    EditorGUILayout.EndVertical();
}
```

## 工程实践建议

1. **先画架构图，再写 OnGUI**：在纸上把分组画出来，再动手
2. **用 `EditorStyles.helpBox` 做分组框**：自带内边距，视觉效果专业
3. **分组标题用 `LabelField` + `Space`**：清晰且不会误触
4. **避免嵌套超过 2 层**：过深的嵌套反而增加认知负担

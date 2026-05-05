# 阶段6：封装工具类（Refactoring Utility）—— 逐字稿

> 如果我们每个 ShaderGUI 都手写一遍 `EditorGUILayout.BeginVertical("box")`，代码会变得冗长且难以维护。作为开发者，我们要学会抽象。通过封装一套基础的工具函数，我们可以像搭积木一样，在 5 分钟内搭建出一个专业级的材质面板。记住，一致性是专业感的来源。

## 重构动作

- 封装 `DrawProp(prop, label)`
- 封装 `DrawTex(prop, label)`
- 封装 `BeginGroup / EndGroup`

## 工具类示例代码

```csharp
public static class ShaderGUIUtil
{
    public static void DrawProp(MaterialProperty prop, string label)
    {
        if (prop == null) return;
        EditorGUILayout.PropertyField(prop, new GUIContent(label));
    }

    public static void DrawTex(MaterialProperty tex, string label)
    {
        if (tex == null) return;
        editor.TextureProperty(tex, label);
    }

    public static void BeginGroup(string title)
    {
        EditorGUILayout.BeginVertical("box");
        EditorGUILayout.LabelField(title, EditorStyles.boldLabel);
    }

    public static void EndGroup()
    {
        EditorGUILayout.EndVertical();
    }
}
```

## 工程价值

- **提高编写效率**：新增 ShaderGUI 时只需调用工具函数
- **视觉高度统一**：所有面板使用相同的分组样式和间距
- **降低维护成本**：修改工具类即可全局生效
- **减少 Bug**：集中处理 null 检查和边界情况

## 最佳实践

1. 工具类做成 `public static`，无需实例化
2. 每个 Draw 方法都做 null 检查
3. 用 `EditorStyles.boldLabel` 统一标题样式
4. 分组间距用 `EditorGUILayout.Space()` 控制

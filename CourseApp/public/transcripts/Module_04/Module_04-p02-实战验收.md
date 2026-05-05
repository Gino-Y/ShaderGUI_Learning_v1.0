# 阶段11：实战验收：M_Outline_Fitting_h01 —— 逐字稿

> 最后，我们将所有的知识点汇聚到 `M_Outline_Fitting_h01` 这个案例中。这不再是一个简单的 Shader 练习，而是一个符合工业化标准的材质工具。从这一刻起，你不再只是在"写 Shader"，你是在为团队定义一套"创作标准"。当我们把这份 GUI 交付给美术同学时，我们交付的是效率和信心。

## 验收标准清单

| # | 验收项 | 标准 |
|---|--------|------|
| 1 | **分组清晰** | Shape / Clip / Motion / Color 逻辑分明 |
| 2 | **安全可靠** | 删除 Shader 中任意属性，面板不崩溃 |
| 3 | **美术友好** | 关键参数有 `HelpBox` 说明，支持彩虹色动态联动 |
| 4 | **性能同步** | 自动根据 Toggle 开启/关闭 Shader 变体（Keywords） |

## 完整示例代码

```csharp
public class M_Outline_Fitting_h01_GUI : ShaderGUI
{
    private static readonly HashSet<string> ManagedProps = new HashSet<string>();

    public override void OnGUI(MaterialEditor editor, MaterialProperty[] props)
    {
        ManagedProps.Clear();

        // 形体组
        EditorGUILayout.BeginVertical("box");
        EditorGUILayout.LabelField("Shape", EditorStyles.boldLabel);
        DrawProp(FindPropertySafe("_OutlineWidth", props), "描边宽度", ManagedProps);
        DrawProp(FindPropertySafe("_OutlineColor", props), "描边颜色", ManagedProps);
        EditorGUILayout.EndVertical();

        // 裁剪组
        EditorGUILayout.BeginVertical("box");
        EditorGUILayout.LabelField("Clip", EditorStyles.boldLabel);
        DrawProp(FindPropertySafe("_ClipThreshold", props), "裁剪阈值", ManagedProps);
        EditorGUILayout.EndVertical();

        // 动态组
        EditorGUILayout.BeginVertical("box");
        EditorGUILayout.LabelField("Motion", EditorStyles.boldLabel);
        DrawProp(FindPropertySafe("_MotionSpeed", props), "运动速度", ManagedProps);
        EditorGUILayout.EndVertical();

        // 颜色组
        EditorGUILayout.BeginVertical("box");
        EditorGUILayout.LabelField("Color", EditorStyles.boldLabel);
        DrawProp(FindPropertySafe("_Color", props), "主颜色", ManagedProps);
        DrawProp(FindPropertySafe("_UseRainbow", props), "启用彩虹色", ManagedProps);
        EditorGUILayout.EndVertical();

        // 渲染状态同步
        EditorGUI.BeginChangeCheck();
        editor.PropertiesGUI(props);
        if (EditorGUI.EndChangeCheck())
        {
            foreach (var target in editor.targets)
            {
                SyncRenderState(target as Material);
            }
        }

        // 兜底：绘制未被管理的属性
        foreach (var prop in props)
        {
            if (!ManagedProps.Contains(prop.name))
                editor.ShaderProperty(prop, prop.displayName);
        }
    }

    private static void SyncRenderState(Material mat)
    {
        bool isTransparent = mat.GetFloat("_Mode") > 0.5f;
        mat.SetInt("_SrcBlend", isTransparent ? (int)BlendMode.SrcAlpha : (int)BlendMode.One);
        mat.SetInt("_DstBlend", isTransparent ? (int)BlendMode.OneMinusSrcAlpha : (int)BlendMode.Zero);
        mat.SetInt("_ZWrite", isTransparent ? 0 : 1);
        mat.renderQueue = isTransparent ? 3000 : 2000;
    }
}
```

## 关键要点回顾

1. **分组清晰**：用 `BeginVertical("box")` 建立视觉边界
2. **Safe 查找**：`FindPropertySafe` 防止属性缺失导致崩溃
3. **ManagedProps 追踪**：确保无遗漏、无重复
4. **渲染状态同步**：`EditorGUI.BeginChangeCheck()` 检测变化并自动写入
5. **兜底绘制**：循环遍历 props，将未被管理的属性以默认方式显示

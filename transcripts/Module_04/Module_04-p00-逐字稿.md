# 渲染状态同步：让 GUI 替人思考 —— 逐字稿

> 你有没有遇到过这种情况：美术在面板里把混合模式从 Alpha 混合改成了加法混合，结果渲染出来颜色完全不对，一查才发现是 Blend 状态没同步。更糟糕的是，这种错误往往不会报错，只会在画面上留下难以察觉的瑕疵，直到上线前才被发现。问题的根源在于：ShaderGUI 只管显示属性，不管渲染状态，而这个空白，正好由我们来填补。

## 核心观点

- **痛点**：属性值和渲染状态分离，美术在面板里改了混合模式，但底层的 Blend、ZWrite、RenderQueue 没有跟着变，导致画面错误且难以排查。这种 bug 最可怕的地方在于，它不崩溃、不报错，但画面就是不对
- **核心思路**：在 OnGUI 的末尾，统一检测关键属性的变化，然后自动把值写入材质的渲染状态，让面板成为渲染状态的唯一真理来源。美术只需要关心业务逻辑，不需要记住哪组状态配哪个效果
- **收益**：美术不需要理解 Blend 指令，不需要手动匹配状态，选一个模式，所有状态自动就位。同时，这套机制也让 Shader 的迭代更安全，因为状态的同步逻辑集中在 GUI 代码里，修改一处，全局生效
- **金句**："好的工具不是让人多做一步，而是让人少想一步。"

## 代码示例

```csharp
// 在 OnGUI 末尾调用同步方法
public override void OnGUI(MaterialEditor editor, MaterialProperty[] props)
{
    // ... 绘制自定义属性 ...

    // 末尾同步渲染状态
    SyncRenderState(targets);
}

void SyncRenderState(Object[] targets)
{
    foreach (Material m in targets)
    {
        // 根据 _BlendMode 的值自动设置 Blend
        int blendMode = (int)m.GetFloat("_BlendMode");
        switch (blendMode)
        {
            case 0: // Alpha 混合
                m.SetFloat("_SrcBlend", (float)UnityEngine.Rendering.BlendMode.SrcAlpha);
                m.SetFloat("_DstBlend", (float)UnityEngine.Rendering.BlendMode.OneMinusSrcAlpha);
                break;
            case 1: // 加法混合
                m.SetFloat("_SrcBlend", (float)UnityEngine.Rendering.BlendMode.One);
                m.SetFloat("_DstBlend", (float)UnityEngine.Rendering.BlendMode.One);
                break;
            case 2: // 乘法混合
                m.SetFloat("_SrcBlend", (float)UnityEngine.Rendering.BlendMode.DstColor);
                m.SetFloat("_DstBlend", (float)UnityEngine.Rendering.BlendMode.Zero);
                break;
        }

        // 同步 ZWrite
        int zwrite = (int)m.GetFloat("_ZWriteMode");
        m.SetFloat("_ZWrite", zwrite > 0 ? 1 : 0);

        // 同步 RenderQueue
        int queue = (int)m.GetFloat("_RenderQueue");
        m.renderQueue = queue;
    }
}
```

对应 Shader 端的配套写法，渲染状态由属性驱动，而不是硬编码：

```hlsl
Properties
{
    [HideInInspector] _SrcBlend ("__SrcBlend", Float) = 1
    [HideInInspector] _DstBlend ("__DstBlend", Float) = 0
    [HideInInspector] _ZWrite ("__ZWrite", Float) = 1
}

SubShader
{
    Blend [_SrcBlend] [_DstBlend]
    ZWrite [_ZWrite]
    // ... pass ...
}
```

## 工程实践建议

1. **集中同步**：把所有渲染状态同步逻辑放在一个方法里，在 OnGUI 末尾统一调用。这样逻辑清晰，也方便后续扩展新的状态同步。如果同步逻辑散落在各个属性回调里，维护成本会成倍增加

2. **用 Undo 包裹修改**：在修改材质属性前，务必调用 Undo.RecordObject，否则美术的撤销操作会失效，这是最容易踩的坑。记住，只要是改了材质的值，就要先 Record，再修改

3. **批量处理多选材质**：targets 字段可能包含多个选中的材质，同步时必须用 foreach 遍历所有材质，不能只处理第一个。美术经常会多选材质批量调整，如果只处理第一个，其余材质就会处于不一致状态

4. **Shader 端用 HideInInspector**：_SrcBlend、_DstBlend 等驱动渲染状态的属性，在 Shader 里用 HideInInspector 标记，让 GUI 全权接管，避免美术手动修改造成不一致。这些属性是内部实现细节，不应该暴露给美术

5. **性能保持轻量**：OnGUI 每帧都可能调用，同步逻辑必须轻量，避免在循环里做字符串操作或反射调用。如果同步逻辑复杂，可以考虑加脏标记，只有属性真正变化时才执行同步

6. **用 SetShaderPassEnabled 控制 Pass**：除了 Blend 和 ZWrite，有些效果还需要动态开关某些 Pass，可以在同步方法里一并处理，保持逻辑内聚。这样美术在一个面板里就能控制所有相关状态，不需要跳到多个地方设置

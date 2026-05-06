# Managed Properties：面板的行政管理 —— 逐字稿

> 在前面两节课里，我们学会了如何查找属性、如何绘制控件。但当一个 ShaderGUI 代码变得越来越长，你有没有遇到过这种情况：某个属性明明在 Shader 里定义了，但面板里就是没画出来？或者更糟，同一个属性被画了两次？今天我们要解决的，就是面板参数的"行政管理"问题——谁来管、怎么管、如何确保不漏不重。

## 核心观点

- **注册机制**：所有需要自定义绘制的属性，必须显式注册到管理列表中
- **自动补位**：未注册的属性由基类自动兜底绘制，确保不遗漏
- **去重保障**：通过已绘制属性集合，防止同一属性被多次绘制
- **金句**："好的面板管理，不是画了多少，而是没画的永远不会超过一个。"

## 注册与补位流程

整个流程分三步：

第一步，子类在 OnGUI 中显式调用 FindPropertySafe 获取需要的属性，并存入成员变量。

第二步，子类调用注册方法，将该属性名登记到"已管理列表"中。

第三步，基类在子类绘制完成后，遍历所有 props，只绘制那些不在"已管理列表"中的属性。

结果：注册过的属性按自定义逻辑绘制，未注册的属性自动补位，绝不重复。

## 对比表

| 方案 | 注册机制 | 未注册属性 | 重复绘制风险 |
|------|----------|------------|--------------|
| 无管理 | 无 | 直接丢失不绘制 | 高 |
| 手动管理 | 靠记忆 | 容易遗漏 | 中 |
| Managed Properties | 显式注册 | 自动补位绘制 | 零 |

## 代码示例

```csharp
// 注册机制核心：记录哪些属性已经被管理
private HashSet<string> _managedProps = new HashSet<string>();

void RegisterProp(string name)
{
    _managedProps.Add(name);
}

// 自动补位：绘制所有未被管理的属性
void DrawUnmanagedProps(MaterialProperty[] props)
{
    foreach (var prop in props)
    {
        if (!_managedProps.Contains(prop.name))
            MaterialEditor.DefaultShaderProperty(prop);
    }
}
```

## 工程实践建议

1. 在 ShaderGUI 基类中实现注册机制和自动补位逻辑，所有子类继承此机制
2. 每个子模块的 OnGUI 必须先注册自己要管的属性，再执行绘制
3. 用 HashSet 而非 List 存储已管理属性名，查找效率更高，且天然去重
4. 在 Editor 日志中输出未管理的属性列表，方便排查遗漏
5. 对于 _Color、_MainTex 等通用属性，建立全局注册规范，避免多人协作时重复绘制

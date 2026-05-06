# 版本迁移：如何让旧资产不碎掉？—— 逐字稿

在实际工程中，Shader 是会不断迭代的。

我见过太多团队遇到这样的噩梦：某天改了 Shader 的一个属性名，结果整个项目几百个材质球全部报错，美术同学打开材质面板看到一片空白，直接崩溃。

这就是我们今天要讨论的问题：版本迁移。如何在 Shader 升级时，让旧资产不碎掉？

## 核心观点

- **属性名 Fallback**：新旧属性名共存，旧名称作为备用
- **语义映射**：通过语义而非名称来识别属性意图
- **静默升级策略**：打开材质时自动迁移，用户无感知

## 三个策略详解

### 1. 属性名 Fallback

当你想把一个属性从 _Color 改名为 _BaseColor 时，不要直接改。正确的做法分三步：

第一步，在 Shader 里保留旧属性名作为兼容层，同时添加新的属性名。

第二步，在 ShaderGUI 里，先查找新属性名，如果找不到，再 Fallback 到旧属性名。

第三步，给美术一段时间过渡，等所有材质都升级后，再移除旧属性名。

代码示例：

```csharp
// Fallback 查找策略
MaterialProperty colorProp = FindPropertySafe("_BaseColor", props)
                        ?? FindPropertySafe("_Color", props);

if (colorProp != null)
{
    editor.ShaderProperty(colorProp, "Base Color");
}
```

### 2. 语义映射

有时候，我们改的不仅仅是属性名，而是整个属性的语义。比如，原来用一个 _Shininess 浮点数控制高光，现在改成用 _Smoothness 和 _Metallic 两个属性。

这时候，我们需要建立语义映射关系：

- 旧属性 _Shininess 的值范围可能是 0 到 128
- 新属性 _Smoothness 的值范围是 0 到 1
- 我们需要一个转换函数：smoothness 等于 shininess 除以 128

在 ShaderGUI 里，我们可以在 OnGUI 里检测旧属性的存在，然后自动计算并设置新属性的值。

### 3. 静默升级策略

最好的升级，是用户感知不到的升级。

实现静默升级的关键是：在 ShaderGUI 的 OnGUI 里，检测材质的版本号。如果版本号低于当前 Shader 版本，就执行迁移逻辑，然后更新版本号。

代码示例：

```csharp
// 静默升级策略
void CheckAndUpgradeMaterial(Material material)
{
    int version = material.GetInt("_Version");

    if (version < 2)
    {
        // 执行版本 1 到 2 的迁移
        if (material.HasProperty("_Shininess"))
        {
            float shininess = material.GetFloat("_Shininess");
            material.SetFloat("_Smoothness", shininess / 128.0f);
        }
        material.SetInt("_Version", 2);
    }
}
```

## 对比表

| 策略 | 侵入性 | 用户体验 | 维护成本 |
|------|--------|----------|----------|
| 属性名 Fallback | 低 | 无感知 | 低 |
| 语义映射 | 中 | 可能需要手动调整 | 中 |
| 静默升级 | 低 | 无感知 | 高（需要维护迁移逻辑） |

## 工程实践建议

1. 永远不要直接删除或重命名 Shader 中的属性，使用 Fallback 策略
2. 在 Shader 里添加 _Version 属性，记录材质版本号
3. 在 ShaderGUI 的 OnGUI 开头，调用升级检查函数
4. 升级逻辑要幂等：多次执行不会产生副作用
5. 保留至少一个大版本的向后兼容性

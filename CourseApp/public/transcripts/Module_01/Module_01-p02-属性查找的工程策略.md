# 阶段3：属性查找的工程策略 —— 逐字稿

> 在实际工程中，我们推荐使用 Safe 模式。为什么？因为 Shader 会迭代。如果你的 GUI 写死了必须有某个属性，而 Shader 删除了它，整个材质面板就会报错变成一片空白。这就是为什么我们要封装 `FindPropertySafe` 这种工具函数，它是我们工程健壮性的第一道防线。

## 核心观点

- **Required 模式**：强绑定，属性缺失时抛出异常，面板空白
- **Safe 模式**：弱绑定，属性缺失时返回 null，优雅跳过
- **金句**："鲁棒性始于对 null 的妥善处理。"

## 对比表

| 模式 | 绑定强度 | 缺失时行为 | 适用场景 |
|------|----------|------------|----------|
| Required 模式 | 强绑定 | 抛出异常，面板空白 | 内部严苛标准 |
| Safe 模式 | 弱绑定 | 返回 null，优雅跳过 | 多版本兼容 |

## 代码示例

```csharp
// ❌ Required 模式（危险）
var prop = FindProperty("_Color", props);  // 属性不存在直接崩

// ✅ Safe 模式（推荐）
MaterialProperty FindPropertySafe(string name, MaterialProperty[] props)
{
    int idx = FindPropertyIndex(name, props);
    return idx >= 0 ? props[idx] : null;
}
```

## 工程实践建议

1. 始终使用 Safe 模式查找属性
2. 对返回 null 的属性做优雅降级处理
3. 在面板底部绘制"未被管理"的属性作为兜底
4. 用 HashSet<string> 追踪已被子模块管理的属性名

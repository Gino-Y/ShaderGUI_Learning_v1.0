# 像搭积木一样构建材质面板 —— 逐字稿

> 你有没有遇到过这种情况：一个 ShaderGUI 脚本写了上千行，所有属性的绘制逻辑全都堆在 OnGUI 里。改一个地方，整块面板都要跟着改。后期维护的时候，光是找到某段绘制代码藏在哪一行，就要花半天时间。这就是我们要引入模块化思维的原因。
>
> 把材质面板想象成一个乐高模型。你不会用一整块大塑料去捏一个模型，而是用一块一块标准积木拼出来。每一块积木只做一件事，拼起来却可以千变万化。在 ShaderGUI 里，每一块积木就是一个静态功能类。比如颜色模块，只管颜色属性的查找和绘制。法线贴图模块，只管法线贴图的绘制逻辑。它们之间互不干扰，各自独立。
>
> 静态功能类的核心设计原则是无状态。既然是静态方法，就不要保存任何实例字段。所有需要的数据，都通过参数传进来。这样每个方法调用都是独立的，不会出现状态污染，也方便做单元测试。
>
> 那么，每个模块应该暴露什么样的接口？我们推荐统一命名为 DrawProperties。这个静态方法接受两个参数：一个是 MaterialProperty 数组，也就是当前材质的所有属性。另一个是 MaterialEditor，用来执行具体的绘制操作。
>
> 为什么是这两个参数？因为绘制一个属性，你需要知道属性在哪，还需要一个编辑器来把它画出来。MaterialProperty 告诉你有什么，MaterialEditor 帮你画出来。这个组合刚好够用，又不会多。
>
> 有了 DrawProperties 方法之后，主类的 OnGUI 就变得非常干净。你只需要按顺序调用各个模块的 DrawProperties，就像搭积木一样，一块一块叠上去。想加功能，加一行调用。想删功能，删一行调用。不需要动任何绘制逻辑。
>
> 这种设计的另一个好处是复用。如果你有多个 Shader 共享相同的功能模块，比如都需要一个颜色模块，那你只需要写一次 BaseColorModule，然后在多个 ShaderGUI 里调用它。改一处，全生效。
>
> 当然，模块化也不是没有代价的。模块之间的绘制顺序需要你手动管理，哪个模块先画、哪个后画，要在 OnGUI 里排好。另外，如果某些属性是多个模块共享的，比如一个贴图既被基础模块使用，又被高级模块使用，那你需要约定好由哪个模块负责绘制，避免重复。但在这个代价和一千行堆在一起的 OnGUI 比起来，显然是模块化更划算。

## 核心观点

- **模块化思维**：将材质面板拆分为独立功能模块，每个模块负责一类属性的绘制，互不干扰
- **静态功能类设计**：用无状态的静态类封装绘制逻辑，通过参数传入所有依赖，易复用、易测试
- **DrawProperties 统一入口**：每个模块暴露相同签名的静态方法，参数是 MaterialProperty 数组和 MaterialEditor

## 代码示例

```csharp
// 模块一：基础颜色模块
public static class BaseColorModule
{
    public static void DrawProperties(MaterialProperty[] props, MaterialEditor editor)
    {
        MaterialProperty color = FindPropertySafe("_Color", props);
        if (color != null)
            editor.ColorProperty(color, "Base Color");
    }
}

// 模块二：法线贴图模块
public static class NormalMapModule
{
    public static void DrawProperties(MaterialProperty[] props, MaterialEditor editor)
    {
        MaterialProperty normalMap = FindPropertySafe("_NormalMap", props);
        if (normalMap != null)
            editor.TextureProperty(normalMap, "Normal Map");
    }
}

// 主 GUI：像搭积木一样组装
public override void OnGUI(MaterialEditor editor, MaterialProperty[] props)
{
    BaseColorModule.DrawProperties(props, editor);
    NormalMapModule.DrawProperties(props, editor);
}
```

## 工程实践建议

1. 每个功能模块放在独立的静态类中，文件名与模块名对应，方便查找
2. DrawProperties 方法签名保持一致，方便用反射或委托统一调用
3. 模块内部只查找自己关心的属性，不依赖其他模块的状态
4. 用 Shader 关键字或编辑器宏控制模块是否启用，实现条件绘制

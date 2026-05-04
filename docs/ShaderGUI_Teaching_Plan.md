# ShaderGUI 专家成长之路：完整教学计划与 PPT 讲稿

> **定位**：这不是一份代码教程，而是一套 **"从工具使用者到工具定义者"** 的思维模型培训体系。

---

## 一、核心课程目标

| 层次 | 目标 |
| :--- | :--- |
| **认知层** | 理解 ShaderGUI 是 Shader 的"交互契约"而非简单的 UI |
| **技术层** | 精通属性查找、分组布局、渲染状态同步 |
| **工程层** | 建立模块化、高鲁棒性（不报错）、版本兼容的代码架构 |

---

## 二、教学计划地图（4 大模块）

| 模块 | 课题 | 核心价值 |
| :--- | :--- | :--- |
| **模块一：解构** | 最小可行性 GUI 与属性契约 | 解决"能跑通"的问题 |
| **模块二：重构** | 布局艺术与条件显示 | 解决"好用、直观"的问题 |
| **模块三：进化** | 模块化复用与 Managed Properties | 解决"大规模协作与维护"的问题 |
| **模块四：治理** | 渲染状态同步与版本兼容 | 解决"资产迁移与技术债"的问题 |

---

## 三、模块一：解构 —— 建立 Shader 与 UI 的第一连接点

### 阶段 1：什么是 ShaderGUI？（定义与契约）

**标题**：ShaderGUI：不仅仅是换个皮

**核心观点**：
- **默认 Inspector 的痛点**：参数堆叠、语义模糊、缺乏逻辑依赖
- **ShaderGUI 的本质**：它是 Shader 参数系统的前端工程层
- **职责**：组织参数、校验数据、解释含义、同步状态

**讲稿**：
> 各位，当我们谈论 ShaderGUI 时，很多人觉得只是为了让面板好看一点。但从软件工程角度看，Shader 是底层逻辑，而 ShaderGUI 是交互接口。没有 GUI 的 Shader 就像是没有说明书的复杂仪器，美术同学在面对几十个参数时会感到巨大的认知负担。我们要做的，是为 Shader 穿上一层智慧的外壳。

---

### 阶段 2：最小可行性架构（代码骨架）

**标题**：编写第一个自定义材质面板

**关键代码展示**：
```csharp
// C# 侧：继承 ShaderGUI 并重写 OnGUI
public class MyGUI : ShaderGUI
{
    public override void OnGUI(MaterialEditor editor, MaterialProperty[] props)
    {
        // 在这里掌控一切
    }
}
```

```hlsl
// Shader 侧：最底部绑定自定义 Editor
CustomEditor "MyGUI"
```

**底层逻辑**：重写 `OnGUI` 是夺回面板控制权的第一步。

**讲稿**：
> 要实现自定义面板，我们只需要做两件事：第一，在 C# 中继承 `ShaderGUI` 类并重写 `OnGUI` 方法；第二，在 Shader 代码的最下方通过 `CustomEditor` 字符串进行绑定。这是所有高级功能的基石。

---

### 阶段 3：属性查找的工程策略（Required vs Safe）

**标题**：如何安全地获取参数？

**对比表**：

| 模式 | 绑定强度 | 缺失时行为 | 适用场景 |
| :--- | :--- | :--- | :--- |
| **Required 模式** | 强绑定 | 抛出异常，面板空白 | 内部严苛标准 |
| **Safe 模式** | 弱绑定 | 返回 `null`，优雅跳过 | 多版本兼容 |

**代码示例**：
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

**金句**：**"鲁棒性始于对 null 的妥善处理。"**

**讲稿**：
> 在实际工程中，我们推荐使用 Safe 模式。为什么？因为 Shader 会迭代。如果你的 GUI 写死了必须有某个属性，而 Shader 删除了它，整个材质面板就会报错变成一片空白。这就是为什么我们要封装 `FindPropertySafe` 这种工具函数，它是我们工程健壮性的第一道防线。

---

## 四、模块二：重构 —— 布局艺术与条件显示

### 阶段 4：信息架构：为什么要分组？

**标题**：告别参数地狱：逻辑化的分组设计

**核心观点**：
- **视觉热区**：美术的第一眼应该看到最重要的参数（如 Main Color）
- **心流体验**：按照渲染逻辑（形体 → 纹理 → 动态 → 颜色）排列，符合直觉
- **UI 容器**：使用 `BeginVertical("box")` 创建视觉边界

**设计案例**：将 `M_Outline_Fitting_h01` 拆分为 **Shape（形体）**、**Clip（裁剪）**、**Motion（动态）**、**Color（颜色）** 四大支柱。

**讲稿**：
> 如果一个 Shader 有 20 个参数，直接平铺在 Inspector 里，美术调参时就像在垃圾堆里找钥匙。在重构阶段，我们的第一个任务是"分类"。我们要把原本散乱的数据，通过代码逻辑封装进"盒子"里。这不只是为了美观，更是为了建立一套通用的调参语言，让不同的美术同学打开材质球时，都能瞬间明白调参的先后顺序。

---

### 阶段 5：条件显示：隐藏干扰项

**标题**：只给用户他需要的：智能 UI 联动

**关键技术**：
- **状态判断**：读取 Toggle 或 Enum 的值
- **动态剔除**：`if (useDissolve) { DrawDissolveParams(); }`
- **禁用范围**：`EditorGUI.DisabledScope` 的应用场景

**代码示例**：
```csharp
var useDissolve = FindPropertySafe("_UseDissolve", props);
bool dissolveEnabled = useDissolve != null && useDissolve.floatValue > 0.5f;

// Toggle 控制参数组的显隐
if (dissolveEnabled)
{
    EditorGUILayout.BeginVertical("box");
    DrawProp(FindPropertySafe("_DissolveTex", props),    "溶解贴图");
    DrawProp(FindPropertySafe("_DissolveHardness", props), "溶解硬度");
    EditorGUILayout.EndVertical();
}
```

**讲稿**：
> 最好的 UI 是"会呼吸"的。当你没有勾选"溶解（Dissolve）"功能时，面板上就不应该出现溶解贴图和溶解硬度等参数。通过 C# 的逻辑控制，我们可以让 Inspector 动态变化。这在工程上叫做"按需展示"，它能极大地降低美术同学的犯错率，因为他们永远只能看到和当前功能相关的参数。

---

### 阶段 6：封装工具类（Refactoring Utility）

**标题**：拒绝代码重复：打造 ShaderGUI 工具箱

**重构动作**：
- 封装 `DrawProp(prop, label)`
- 封装 `DrawTex(prop, label)`
- 封装 `BeginGroup / EndGroup`

**工程价值**：提高编写效率，保证整个项目 ShaderGUI 的视觉高度统一。

**讲稿**：
> 如果我们每个 ShaderGUI 都手写一遍 `EditorGUILayout.BeginVertical("box")`，代码会变得冗长且难以维护。作为开发者，我们要学会抽象。通过封装一套基础的工具函数，我们可以像搭积木一样，在 5 分钟内搭建出一个专业级的材质面板。记住，一致性是专业感的来源。

---

## 五、模块三：进化 —— 模块化复用与组件化思维

### 阶段 7：模块化：Shader 功能组件化

**标题**：像搭积木一样构建材质面板

**核心概念**：
- **静态功能类**：如 `OutlineShaderGUI.cs`、`CrystalShaderGUI.cs`
- **函数签名设计**：`public static void DrawProperties(MaterialEditor editor, MaterialProperty[] props)`

**工程场景**：当一个角色 Shader 同时包含"描边"、"溶解"、"侧光"时，直接调用对应的静态方法。

**代码示例**：
```csharp
public class CharacterMainGUI : ShaderGUI
{
    public override void OnGUI(MaterialEditor editor, MaterialProperty[] props)
    {
        // 描边模块
        OutlineModule.DrawProperties(editor, props, managedProps);
        // 溶解模块
        DissolveModule.DrawProperties(editor, props, managedProps);
        // 侧光模块
        RimLightModule.DrawProperties(editor, props, managedProps);
    }
}
```

**讲稿**：
> 在大型项目中，功能往往是跨 Shader 复用的。比如"描边"功能可能会出现在 10 个不同的 Shader 里。如果我们为每个 Shader 都写一遍描边的 UI 逻辑，一旦描边功能升级，我们要改 10 个地方。进阶的做法是"组件化"，将描边 UI 逻辑封装成独立的模块，主 GUI 只需要一行代码进行调用。

---

### 阶段 8：Managed Properties：防止重复绘制

**标题**：Managed Properties：面板的行政管理

**核心机制**：
- **注册机制**：子模块声明自己"管理"了哪些属性
- **自动补位**：主 GUI 最后统一绘制那些"漏掉"的参数

**工程目标**：确保所有 Shader 属性在面板上都有位置，且不重复。

**代码示例**：
```csharp
var managedProps = new HashSet<string>();

// 子模块绘制时将自己管理的属性名注册进去
OutlineModule.DrawProperties(editor, props, managedProps);
// managedProps 此时包含了 "_OutlineColor", "_OutlineWidth" 等

// 主 GUI 最后绘制"剩余"的属性
foreach (var prop in props)
{
    if (!managedProps.Contains(prop.name))
        editor.ShaderProperty(prop, prop.displayName);
}
```

**讲稿**：
> 模块化带来的一个挑战是：如何确保不漏掉参数？我们引入了 `Managed Properties` 概念。每个子模块（如描边模块）会领走属于它的参数。主面板最后会检查一下："还有谁没被领走？"，剩下的参数将按默认方式显示。这种"闭环管理"保证了我们工具的严谨性。

---

## 六、模块四：治理 —— 渲染状态同步与版本迁移

### 阶段 9：渲染状态同步：自动化的"幕后推手"

**标题**：渲染状态同步：让 GUI 替人思考

**核心痛点**：
- 美术手动改 `Blend`、`ZWrite` 极易出错，导致显示异常
- Shader 关键字（Keywords）与 UI 状态脱节

**解决方案**：
- 在 `OnGUI` 尾部检测属性变化
- 使用 `material.SetInt` 或 `EnableKeyword` 自动同步渲染状态
- **案例**：选择"Transparent"预设，GUI 自动写入 `SrcAlpha`、`OneMinusSrcAlpha` 并设置 `RenderQueue`

**代码示例**：
```csharp
// 在 OnGUI 末尾做状态同步
EditorGUI.BeginChangeCheck();
// ... 绘制所有属性 ...
if (EditorGUI.EndChangeCheck())
{
    foreach (var target in editor.targets)
    {
        var mat = target as Material;
        SyncRenderingStates(mat);
    }
}

void SyncRenderingStates(Material mat)
{
    bool isTransparent = mat.GetFloat("_Mode") > 0.5f;
    mat.SetInt("_SrcBlend",   isTransparent ? (int)UnityEngine.Rendering.BlendMode.SrcAlpha : (int)UnityEngine.Rendering.BlendMode.One);
    mat.SetInt("_DstBlend",   isTransparent ? (int)UnityEngine.Rendering.BlendMode.OneMinusSrcAlpha : (int)UnityEngine.Rendering.BlendMode.Zero);
    mat.SetInt("_ZWrite",     isTransparent ? 0 : 1);
    mat.renderQueue = isTransparent ? 3000 : 2000;
}
```

**讲稿**：
> 很多时候，Shader 效果不对是因为美术不小心改动了一个隐藏的渲染参数，比如把深度写入关了。在治理阶段，我们要把这些"危险"的操作收口。通过 ShaderGUI，我们可以实现"一键配置"——当用户在下拉框选择"加法混合"时，后台自动把所有的混合因子和渲染队列设置好。这种"自动治理"能减少项目 30% 以上的材质报错报修。

---

### 阶段 10：版本兼容：优雅处理"技术债"

**标题**：版本迁移：如何让旧资产不"碎掉"？

**核心策略**：
- **属性名 Fallback**：`FindFirstProperty("_NewName", "_OldName")`
- **语义映射**：旧版本的 0-1 范围如何平滑映射到新版本的指数曲线
- **静默升级**：在 Inspector 打开时，后台自动完成旧参数到新参数的迁移

**代码示例**：
```csharp
MaterialProperty FindWithFallback(string[] names, MaterialProperty[] props)
{
    foreach (var name in names)
    {
        int idx = FindPropertyIndex(name, props);
        if (idx >= 0) return props[idx];
    }
    return null;
}

// 使用：优先读新名，自动兼容旧名
var speedProp = FindWithFallback(new[]{ "_SpeedGlobal", "_SpeedGlobe" }, props);
```

**工程金句**：**"好的工具不应该在升级时惩罚老用户。"**

**讲稿**：
> 项目研发两年后，你发现某个属性名拼错了（比如 `_SpeedGlobe`），你想改成正确的 `_SpeedGlobal`。如果你直接改 Shader，成千上万个旧材质球的数据就会丢失。ShaderGUI 的"治理"能力在这里体现——我们写一段 Fallback 逻辑，优先读新名，没新名读旧名，并在后台偷偷帮用户把数据存到新名里。这就是所谓的"静默迁移"，它是大型项目平稳迭代的关键。

---

### 阶段 11：实战验收：M_Outline_Fitting_h01

**标题**：最终实战：构建专业级描边材质面板

**验收标准清单**：

| # | 验收项 | 标准 |
| :--- | :--- | :--- |
| 1 | **分组清晰** | Shape / Clip / Motion / Color 逻辑分明 |
| 2 | **安全可靠** | 删除 Shader 中任意属性，面板不崩溃 |
| 3 | **美术友好** | 关键参数有 `HelpBox` 说明，支持彩虹色动态联动 |
| 4 | **性能同步** | 自动根据 Toggle 开启/关闭 Shader 变体（Keywords） |

**讲稿**：
> 最后，我们将所有的知识点汇聚到 `M_Outline_Fitting_h01` 这个案例中。这不再是一个简单的 Shader 练习，而是一个符合工业化标准的材质工具。从这一刻起，你不再只是在"写 Shader"，你是在为团队定义一套"创作标准"。当我们把这份 GUI 交付给美术同学时，我们交付的是效率和信心。

---

## 七、元认知总结（阶段 12）

**标题**：ShaderGUI 进阶思维路线图

**路线图**：

```
第一步（解构）  ──>  理解属性契约，实现 FindProperty
     ↓
第二步（重构）  ──>  建立信息架构，实现分组与联动
     ↓
第三步（进化）  ──>  组件化思考，实现模块化复用
     ↓
第四步（治理）  ──>  关注生命周期，实现状态同步与版本迁移
```

**讲稿**：
> 学习 ShaderGUI 的过程，本质上是学习如何处理"人、机器、资产"三者关系的过程。代码是死的，但交互逻辑是活的。希望这门课能帮你开启"工程化开发"的大门，让你在 TA 的道路上不仅能做出绚丽的特效，更能搭建出稳健的流水线。谢谢大家！

---

## 八、Gems 系统提示词（System Prompt）配置建议

当你将本教学计划内化到 AI Gems / Custom GPT 时，建议配置以下核心逻辑：

### 强制追问规则
> 在给出代码前，先问用户：
> - "这个参数是给美术调的还是程序调的？"
> - "它属于哪个逻辑分组（Shape / Clip / Motion / Color）？"

### 错误捕捉规则
> 当用户贴出一段没有 `null` 检查的 `FindProperty` 代码时，必须给出警告并展示 `Safe` 模式。

### 费曼检查规则
> 定期让用户解释：
> - "为什么我们要用静态类来封装描边模块？"
> - "Managed Properties 机制解决了什么问题？"

---

*文档生成日期：2026-04-29 | 版本 v1.0*

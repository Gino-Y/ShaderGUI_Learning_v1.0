# Storyboard Brief

- Provider mode: `storyboard-local-spec`
- Module: `ADP_ACCUMULATED`
- Source: `{'slides': 'CourseApp/src/data/slides.json', 'explorations': 'CourseApp/src/data/explorations.json', 'quizzes': 'CourseApp/src/data/quizzes.json'}`
- Role: Film-style storyboard layer before visual design.
- Goal: Guide layout, palette, and subtitle-triggered motion for teaching expression.

## Scenes

### Module_01 / p00

- Route: `/module/Module_01/slide/p00`
- Title: ShaderGUI：不仅仅是换个皮
- Purpose: Use this scene to make learners understand 'ShaderGUI：不仅仅是换个皮' through the content beats: ShaderGUI 是 Shader 参数系统的前端工程层 / 不是简单的 UI 美化.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:09.56 segment 0: reveal-focus -> content-beat (ShaderGUI 是 Shader 参数系统的前端工程层); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: ShaderGUI 是 Shader 参数系统的前端工程层
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“ShaderGUI 是 Shader 参数系统的前端工程层”，弱化其他内容；旁白：ShaderGUI 是 Shader 参数系统的前端工程层。
  - `cue-02` 00:09.56-00:15.56 segment 1: reveal-focus -> content-beat (不是简单的 UI 美化); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 不是简单的 UI 美化
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“不是简单的 UI 美化”，弱化其他内容；旁白：不是简单的 UI 美化。

### Module_01 / p01

- Route: `/module/Module_01/slide/p01`
- Title: 编写第一个自定义材质面板
- Purpose: Use this scene to make learners understand '编写第一个自定义材质面板' through the content beats: 继承 ShaderGUI / 重写 OnGUI / 通过 CustomEditor 绑定.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:05.56 segment 0: reveal-focus -> content-beat (继承 ShaderGUI); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 继承 ShaderGUI
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“继承 ShaderGUI”，弱化其他内容；旁白：继承 ShaderGUI。
  - `cue-02` 00:05.56-00:14.67 segment 1: reveal-focus -> content-beat (重写 OnGUI); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 重写 OnGUI
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“重写 OnGUI”，弱化其他内容；旁白：重写 OnGUI。
  - `cue-03` 00:14.67-00:22.22 segment 2: reveal-focus -> content-beat (通过 CustomEditor 绑定); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 通过 CustomEditor 绑定
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“通过 CustomEditor 绑定”，弱化其他内容；旁白：通过 CustomEditor 绑定。

### Module_01 / p02

- Route: `/module/Module_01/slide/p02`
- Title: 如何安全地获取参数？
- Purpose: Use this scene to make learners understand '如何安全地获取参数？' through the content beats: Required 模式的风险 / Safe 模式的安全获取 / 封装 FindPropertySafe 工具函数.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:04.89 segment 0: reveal-focus -> content-beat (Required 模式的风险); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: Required 模式的风险
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“Required 模式的风险”，弱化其他内容；旁白：Required 模式的风险。
  - `cue-02` 00:04.89-00:06.09 segment 1: reveal-focus -> content-beat (Safe 模式的安全获取); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: Safe 模式的安全获取
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“Safe 模式的安全获取”，弱化其他内容；旁白：Safe 模式的安全获取。
  - `cue-03` 00:06.09-00:09.20 segment 2: reveal-focus -> content-beat (封装 FindPropertySafe 工具函数); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 封装 FindPropertySafe 工具函数
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“封装 FindPropertySafe 工具函数”，弱化其他内容；旁白：封装 FindPropertySafe 工具函数。

### Module_02 / p00

- Route: `/module/Module_02/slide/p00`
- Title: 告别参数地狱：逻辑化的分组设计
- Purpose: Use this scene to make learners understand '告别参数地狱：逻辑化的分组设计' through the content beats: 信息架构设计 / BeginVertical 创建视觉边界 / 按渲染逻辑排列参数.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:06.67 segment 0: reveal-focus -> content-beat (信息架构设计); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 信息架构设计
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“信息架构设计”，弱化其他内容；旁白：信息架构设计。
  - `cue-02` 00:06.67-00:12.22 segment 1: reveal-focus -> content-beat (BeginVertical 创建视觉边界); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: BeginVertical 创建视觉边界
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“BeginVertical 创建视觉边界”，弱化其他内容；旁白：BeginVertical 创建视觉边界。
  - `cue-03` 00:12.22-00:37.11 segment 2: reveal-focus -> content-beat (按渲染逻辑排列参数); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 按渲染逻辑排列参数
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“按渲染逻辑排列参数”，弱化其他内容；旁白：按渲染逻辑排列参数。

### Module_02 / p01

- Route: `/module/Module_02/slide/p01`
- Title: 只给用户他需要的：智能 UI 联动
- Purpose: Use this scene to make learners understand '只给用户他需要的：智能 UI 联动' through the content beats: 条件显示技术 / Toggle/Enum 控制参数组显隐 / EditorGUI.DisabledScope 应用.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:08.00 segment 0: reveal-focus -> content-beat (条件显示技术); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 条件显示技术
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“条件显示技术”，弱化其他内容；旁白：条件显示技术。
  - `cue-02` 00:08.00-00:11.11 segment 1: reveal-focus -> content-beat (Toggle/Enum 控制参数组显隐); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: Toggle/Enum 控制参数组显隐
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“Toggle/Enum 控制参数组显隐”，弱化其他内容；旁白：Toggle/Enum 控制参数组显隐。
  - `cue-03` 00:11.11-00:26.22 segment 2: reveal-focus -> content-beat (EditorGUI.DisabledScope 应用); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: EditorGUI.DisabledScope 应用
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“EditorGUI.DisabledScope 应用”，弱化其他内容；旁白：EditorGUI.DisabledScope 应用。

### Module_02 / p02

- Route: `/module/Module_02/slide/p02`
- Title: 拒绝代码重复：打造 ShaderGUI 工具箱
- Purpose: Use this scene to make learners understand '拒绝代码重复：打造 ShaderGUI 工具箱' through the content beats: 封装 DrawProp / DrawTex / BeginGroup 工具类 / 提高编写效率 / 视觉统一性.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:08.67 segment 0: reveal-focus -> content-beat (封装 DrawProp / DrawTex / BeginGroup 工具类); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 封装 DrawProp / DrawTex / BeginGroup 工具类
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“封装 DrawProp / DrawTex / BeginGroup 工具类”，弱化其他内容；旁白：封装 DrawProp / DrawTex / BeginGroup 工具类。
  - `cue-02` 00:08.67-00:16.22 segment 1: reveal-focus -> content-beat (提高编写效率); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 提高编写效率
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“提高编写效率”，弱化其他内容；旁白：提高编写效率。
  - `cue-03` 00:16.22-00:19.33 segment 2: reveal-focus -> content-beat (视觉统一性); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 视觉统一性
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“视觉统一性”，弱化其他内容；旁白：视觉统一性。

### Module_03 / p00

- Route: `/module/Module_03/slide/p00`
- Title: 像搭积木一样构建材质面板
- Purpose: Use this scene to make learners understand '像搭积木一样构建材质面板' through the content beats: 模块化思维 / 静态功能类设计 / DrawProperties 静态方法.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:01.80 segment 0: reveal-focus -> content-beat (模块化思维); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 模块化思维
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“模块化思维”，弱化其他内容；旁白：模块化思维。
  - `cue-02` 00:00.00-00:01.80 segment 1: reveal-focus -> content-beat (静态功能类设计); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 静态功能类设计
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“静态功能类设计”，弱化其他内容；旁白：静态功能类设计。
  - `cue-03` 00:00.00-00:01.80 segment 2: reveal-focus -> content-beat (DrawProperties 静态方法); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: DrawProperties 静态方法
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“DrawProperties 静态方法”，弱化其他内容；旁白：DrawProperties 静态方法。

### Module_03 / p01

- Route: `/module/Module_03/slide/p01`
- Title: Managed Properties：面板的行政管理
- Purpose: Use this scene to make learners understand 'Managed Properties：面板的行政管理' through the content beats: 注册机制与自动补位 / 确保不漏掉参数 / 不重复绘制.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:01.80 segment 0: reveal-focus -> content-beat (注册机制与自动补位); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 注册机制与自动补位
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“注册机制与自动补位”，弱化其他内容；旁白：注册机制与自动补位。
  - `cue-02` 00:00.00-00:01.80 segment 1: reveal-focus -> content-beat (确保不漏掉参数); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 确保不漏掉参数
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“确保不漏掉参数”，弱化其他内容；旁白：确保不漏掉参数。
  - `cue-03` 00:00.00-00:01.80 segment 2: reveal-focus -> content-beat (不重复绘制); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 不重复绘制
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“不重复绘制”，弱化其他内容；旁白：不重复绘制。

### Module_04 / p00

- Route: `/module/Module_04/slide/p00`
- Title: 渲染状态同步：让 GUI 替人思考
- Purpose: Use this scene to make learners understand '渲染状态同步：让 GUI 替人思考' through the content beats: 在 OnGUI 末尾检测属性变化 / 自动同步 Blend、ZWrite、RenderQueue.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:01.80 segment 0: reveal-focus -> content-beat (在 OnGUI 末尾检测属性变化); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 在 OnGUI 末尾检测属性变化
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“在 OnGUI 末尾检测属性变化”，弱化其他内容；旁白：在 OnGUI 末尾检测属性变化。
  - `cue-02` 00:00.00-00:01.80 segment 1: reveal-focus -> content-beat (自动同步 Blend、ZWrite、RenderQueue); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 自动同步 Blend、ZWrite、RenderQueue
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“自动同步 Blend、ZWrite、RenderQueue”，弱化其他内容；旁白：自动同步 Blend、ZWrite、RenderQueue。

### Module_04 / p01

- Route: `/module/Module_04/slide/p01`
- Title: 版本迁移：如何让旧资产不碎掉？
- Purpose: Use this scene to make learners understand '版本迁移：如何让旧资产不碎掉？' through the content beats: 属性名 Fallback / 语义映射 / 静默升级策略.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:01.80 segment 0: reveal-focus -> content-beat (属性名 Fallback); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 属性名 Fallback
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“属性名 Fallback”，弱化其他内容；旁白：属性名 Fallback。
  - `cue-02` 00:00.00-00:01.80 segment 1: reveal-focus -> content-beat (语义映射); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 语义映射
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“语义映射”，弱化其他内容；旁白：语义映射。
  - `cue-03` 00:00.00-00:01.80 segment 2: reveal-focus -> content-beat (静默升级策略); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 静默升级策略
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“静默升级策略”，弱化其他内容；旁白：静默升级策略。

### Module_04 / p02

- Route: `/module/Module_04/slide/p02`
- Title: 最终实战：构建专业级描边材质面板
- Purpose: Use this scene to make learners understand '最终实战：构建专业级描边材质面板' through the content beats: 分组清晰 / 安全可靠 / 美术友好.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:01.80 segment 0: reveal-focus -> content-beat (分组清晰); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 分组清晰
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“分组清晰”，弱化其他内容；旁白：分组清晰。
  - `cue-02` 00:00.00-00:01.80 segment 1: reveal-focus -> content-beat (安全可靠); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 安全可靠
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“安全可靠”，弱化其他内容；旁白：安全可靠。
  - `cue-03` 00:00.00-00:01.80 segment 2: reveal-focus -> content-beat (美术友好); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 美术友好
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“美术友好”，弱化其他内容；旁白：美术友好。
  - `cue-04` 00:00.00-00:01.80 segment 3: reveal-focus -> content-beat (性能同步); focus `knowledge-04` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 性能同步
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“性能同步”，弱化其他内容；旁白：性能同步。

### Module_04 / p03

- Route: `/module/Module_04/slide/p03`
- Title: ShaderGUI 进阶思维路线图
- Purpose: Use this scene to make learners understand 'ShaderGUI 进阶思维路线图' through the content beats: 解构阶段 / 重构阶段 / 进化阶段.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:01.80 segment 0: reveal-focus -> content-beat (解构阶段); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 解构阶段
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“解构阶段”，弱化其他内容；旁白：解构阶段。
  - `cue-02` 00:00.00-00:01.80 segment 1: reveal-focus -> content-beat (重构阶段); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 重构阶段
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“重构阶段”，弱化其他内容；旁白：重构阶段。
  - `cue-03` 00:00.00-00:01.80 segment 2: reveal-focus -> content-beat (进化阶段); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 进化阶段
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“进化阶段”，弱化其他内容；旁白：进化阶段。
  - `cue-04` 00:00.00-00:01.80 segment 3: reveal-focus -> content-beat (治理阶段); focus `knowledge-04` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 治理阶段
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“治理阶段”，弱化其他内容；旁白：治理阶段。

## Interactive Screens

### explore-p01-property-grouping - 探索页

- Route: `/module/Module_01/slide/p01/explore`
- Purpose: Let learners manipulate ShaderGUI property grouping variables as a subpage of the current lesson, without consuming a main slide number.
- Layout: interactive property grouping lab
- Composition: wide interactive workbench / breadcrumb -> controls -> live feedback -> return to lesson
- Realtime cues: 3
- Handoff target: `CourseApp/src/views/ExploreView.vue`

### explore-p02-property-grouping - 属性查找实战

- Route: `/module/Module_01/slide/p02/explore`
- Purpose: Let learners manipulate ShaderGUI property grouping variables as a subpage of the current lesson, without consuming a main slide number.
- Layout: interactive property grouping lab
- Composition: wide interactive workbench / breadcrumb -> controls -> live feedback -> return to lesson
- Realtime cues: 3
- Handoff target: `CourseApp/src/views/ExploreView.vue`

### quiz - 做题页

- Route: `/module/Module_01/quiz`
- Purpose: Let learners answer one focused question at a time, with randomized question order, randomized options, automatic progression, and a final score review.
- Layout: single active question card
- Composition: medium close assessment card / breadcrumb -> question type/progress -> question stem -> options -> submit
- Realtime cues: 5
- Handoff target: `CourseApp/src/views/QuizView.vue`

### explore-p01-smart-ui-linkage - 智能 UI 联动实验

- Route: `/module/Module_02/slide/p01/explore`
- Purpose: Let learners manipulate ShaderGUI property grouping variables as a subpage of the current lesson, without consuming a main slide number.
- Layout: interactive property grouping lab
- Composition: wide interactive workbench / breadcrumb -> controls -> live feedback -> return to lesson
- Realtime cues: 3
- Handoff target: `CourseApp/src/views/ExploreView.vue`

### quiz - 做题页

- Route: `/module/Module_02/quiz`
- Purpose: Let learners answer one focused question at a time, with randomized question order, randomized options, automatic progression, and a final score review.
- Layout: single active question card
- Composition: medium close assessment card / breadcrumb -> question type/progress -> question stem -> options -> submit
- Realtime cues: 5
- Handoff target: `CourseApp/src/views/QuizView.vue`

### explore-p00-modular-assembly - 模块化组装实验

- Route: `/module/Module_03/slide/p00/explore`
- Purpose: Let learners manipulate ShaderGUI property grouping variables as a subpage of the current lesson, without consuming a main slide number.
- Layout: interactive property grouping lab
- Composition: wide interactive workbench / breadcrumb -> controls -> live feedback -> return to lesson
- Realtime cues: 3
- Handoff target: `CourseApp/src/views/ExploreView.vue`

### quiz - 做题页

- Route: `/module/Module_03/quiz`
- Purpose: Let learners answer one focused question at a time, with randomized question order, randomized options, automatic progression, and a final score review.
- Layout: single active question card
- Composition: medium close assessment card / breadcrumb -> question type/progress -> question stem -> options -> submit
- Realtime cues: 5
- Handoff target: `CourseApp/src/views/QuizView.vue`

### explore-p02-render-state-playground - 渲染状态调试试验场

- Route: `/module/Module_04/slide/p02/explore`
- Purpose: Let learners manipulate ShaderGUI property grouping variables as a subpage of the current lesson, without consuming a main slide number.
- Layout: interactive property grouping lab
- Composition: wide interactive workbench / breadcrumb -> controls -> live feedback -> return to lesson
- Realtime cues: 3
- Handoff target: `CourseApp/src/views/ExploreView.vue`

### quiz - 做题页

- Route: `/module/Module_04/quiz`
- Purpose: Let learners answer one focused question at a time, with randomized question order, randomized options, automatic progression, and a final score review.
- Layout: single active question card
- Composition: medium close assessment card / breadcrumb -> question type/progress -> question stem -> options -> submit
- Realtime cues: 5
- Handoff target: `CourseApp/src/views/QuizView.vue`

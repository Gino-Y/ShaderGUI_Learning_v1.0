自定义 ShaderGUI 的最小架构其实很直接。
C Sharp 侧创建一个类，继承 ShaderGUI，并重写 OnGUI 方法。Shader 侧在文件底部用 CustomEditor 绑定这个类。完成这两步之后，材质面板的绘制权就回到了我们手里。
后面的分组布局、条件显示、FindPropertySafe、渲染状态同步，都是建立在这个入口之上的工程能力。

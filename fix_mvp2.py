"""一次性修复 mvp_mcp.py 的语法损坏"""
import re

path = r"D:\Works\Web\ShaderGUI_Learning_v1.0\.agent\mcp_servers\mvp_mcp.py"
with open(path, encoding="utf-8") as f:
    content = f.read()

# 定位问题区域：找到损坏的 generate_products 方法体
# 正确结构：try / except / return / 方法结束
# 当前损坏：except 缩进错误，_ensure_audio 签名掉进 except 块里

# 策略：找到 `try:` 开始的位置，一直到 `_ensure_audio` 的正确开始位置
# 然后重建整个 generate_products 方法

# 找到 try: 的行号
lines = content.split('\n')
in_generate = False
try_start = -1
for i, line in enumerate(lines):
    if 'def generate_products(' in line and not in_generate:
        in_generate = True
    if in_generate and line.strip() == 'try:':
        try_start = i
        break

print(f"try: found at line {try_start + 1}")

# 找到 _ensure_audio 的正确方法签名位置（在 generate_products 之后）
# 当前文件中它损坏了，我们直接重建 generate_products 方法

# 方案：用正则找到 generate_products 的完整正确版本，替换掉损坏版本
# 先从文件中提取好的部分：import、其他方法等

# 找到 generate_products 方法开始的位置
gen_start = -1
gen_end = -1
for i, line in enumerate(lines):
    if 'def generate_products(' in line:
        gen_start = i
    # 下一个 @staticmethod 是 _ensure_audio 的开始
    if gen_start >= 0 and i > gen_start and line.strip() == '@staticmethod':
        gen_end = i
        break

print(f"generate_products: lines {gen_start+1} to {gen_end}")

if gen_start >= 0 and gen_end >= 0:
    # 重建 generate_products 方法（正确版本）
    new_method = '''    @staticmethod
    def generate_products(workspace: Path, module: str) -> dict:
        try:
            source = MVPMCP._load_module_source(workspace, module)
            slide_ids = MVPMCP._resolve_mvp_slide_ids(workspace, module, source["slides"])
            source["slides"] = [slide for slide in source["slides"] if slide["slideId"] in slide_ids]
            cleaned = MVPMCP._clean_mvp_products(workspace, module)
            MVPMCP._write_course_app(workspace, module, source)
            MVPMCP._copy_course_content(workspace, module, source["slides"])
            MVPMCP._write_scripts(workspace)
            install = subprocess.run(
                ["npm.cmd", "install"],
                cwd=str(workspace / "CourseApp"),
                text=True,
                encoding="utf-8",
                errors="replace",
                capture_output=True,
            )
            if install.returncode != 0:
                return {"status": "error", "message": install.stdout.strip() + "\\n" + install.stderr.strip()}
            # 加固：MVP 后自动检查并生成音频（不调用 storyboard，由 flow engine 调度）
            audio_result = MVPMCP._ensure_audio(workspace, module)
            if audio_result["status"] != "success":
                print(f"[MVP Harden] Audio generation failed: {audio_result.get('message')}")
        except Exception as exc:
            return {"status": "error", "message": f"MVP generation failed: {exc}"}
        return {
            "status": "success",
            "module": module,
            "app": str(workspace / "CourseApp"),
            "content": str(workspace / "CourseContent" / module),
            "scripts": str(workspace / "scripts"),
            "slide_ids": slide_ids,
            "slide_count": len(slide_ids),
            "cleaned": cleaned,
        }'''

    # 替换
    new_lines = lines[:gen_start] + [new_method] + lines[gen_end:]
    content = '\n'.join(new_lines)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed generate_products method")
else:
    print("ERROR: could not locate method boundaries")

# 验证语法
import py_compile
try:
    py_compile.compile(path, doraise=True)
    print("Syntax OK!")
except py_compile.PyCompileError as e:
    print(f"Syntax ERROR: {e}")

"""审计并修复 mvp_mcp.py 的模板覆盖逻辑"""
import re

path = r"D:\Works\Web\ShaderGUI_Learning_v1.0\.agent\mcp_servers\mvp_mcp.py"
with open(path, encoding="utf-8") as f:
    content = f.read()

# --- 修复 1：移除 MVP 里对 storyboard 的直接调用 ---
# 找到并删除 "加固 2" 整个 try/except 块
pattern1 = re.compile(
    r'\s*# 加固 2.*?try:.*?StoryboardMCP\..*?except Exception as sb_exc:.*?print\(f"\[MVP Harden\].*?"\)\s*',
    re.DOTALL
)
m = pattern1.search(content)
if m:
    content = content[:m.start()] + "\n" + content[m.end():]
    print("Removed storyboard call from MVP (fix 1)")
else:
    print("WARN: pattern1 not found, trying manual...")
    # 手动定位
    lines = content.split('\n')
    new_lines = []
    skip = False
    for line in lines:
        if '# 加固 2' in line:
            skip = True
        elif skip and 'except Exception as sb_exc:' in line:
            skip = False
            continue
        if skip:
            continue
        new_lines.append(line)
    content = '\n'.join(new_lines)
    print("Removed via line scan (fix 1)")

# --- 修复 2：_copy_template_tree 改为不覆盖已存在的非模板文件 ---
# 在 shutil.copy2 之前检查目标是否存在
old_copy = '            dst = target_dir / rel\n            dst.parent.mkdir(parents=True, exist_ok=True)\n            shutil.copy2(src, dst)'
new_copy = '            dst = target_dir / rel\n            dst.parent.mkdir(parents=True, exist_ok=True)\n            if dst.exists():\n                continue  # 不覆盖已存在的文件（防止节点漂移）\n            shutil.copy2(src, dst)'
if old_copy in content:
    content = content.replace(old_copy, new_copy, 1)
    print("Fixed _copy_template_tree (fix 2): skip existing files")
else:
    print("WARN: old_copy pattern not found")
    # 找实际内容
    idx = content.find('shutil.copy2(src, dst)')
    if idx >= 0:
        print("Found shutil.copy2 at index", idx)
        # 手动替换
        before = content[:idx]
        after = content[idx:]
        # 在 dst.parent.mkdir 之后插入检查
        pass  # 太复杂，直接用 Write 重写整个函数

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Done. Validating syntax...")
import py_compile
py_compile.compile(path, doraise=True)
print("Syntax OK")

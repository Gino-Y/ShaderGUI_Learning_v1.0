# Lottie 动画集成方案（故事板驱动·全自动）

> 核心原则：故事板（StoryboardMCP）主导，AI 自动生成或自动收集，禁止 AE/设计制作等人工操作
> 目标：分镜字段直接驱动 Lottie 资产生成，全链路无人工介入

---

## 一、架构总览

### 1.1 核心流程（全自动化）

```
StoryboardMCP（故事板）
  ↓ 输出：motionCues[] + lottieSpec（AI 生成的结构化规格）
  ↓
LottieAssetGenerator（资产生成器）
  ├─ 通道 A：AI 直接生成合法 Lottie JSON（Bodymovin 格式）
  └─ 通道 B：自动收集（调用 LottieFiles API 等公开资源）
  ↓
LottieValidator（验证器）
  ↓ 验证：Schema 合法性、体积、性能、与 cue 对齐
  ↓
StitchMCP → Build → 交付
```

### 1.2 故事板主导的含义

| 传统流程（禁止） | 本方案（故事板驱动） |
|--------------|-------------------|
| AE 设计师手动制作 | ❌ 禁止 |
| 人工导出 Bodymovin | ❌ 禁止 |
| 人工命名 Markers | ❌ 禁止 |
| 故事板只写"意图" | ❌ 不够 |
| **故事板直接输出 Lottie 规格** | ✅ 本方案 |
| **AI 自动生成 JSON** | ✅ 本方案 |
| **自动收集公开资源** | ✅ 本方案 |

---

## 二、故事板字段设计（核心）

### 2.1 扩展 `storyboard-contract.json`

```json
{
  "slides": [
    {
      "slideId": "p01",
      "motionCues": [
        {
          "cueId": "cue-01",
          "timeRange": [0, 3.5],
          "knowledgeFocus": { "label": "ShaderGUI 作用" },
          "dynamicGuidance": {
            "kind": "lottie-animation",
            "lottieSpec": {
              "source": "generate",   // generate | collect
              "animationType": "concept-intro",
              "semanticTags": ["shadergui", "technical-artist", "workflow"],
              "duration": 3.5,
              "frameRate": 30,
              "markers": [
                { "name": "intro", "time": 0 },
                { "name": "highlight", "time": 1.2 }
              ],
              "layers": [
                {
                  "name": "shader-flow-bg",
                  "type": "shape",
                  "keyframes": [
                    { "time": 0, "opacity": 0 },
                    { "time": 0.5, "opacity": 1 }
                  ]
                }
              ],
              "codeHighlightSync": {
                "field": "ShaderGUI",
                "syncMode": "marker",   // marker | time-range
                "markerName": "highlight"
              }
            }
          }
        }
      ]
    }
  ]
}
```

### 2.2 字段说明（故事板 → Lottie 直接映射）

| 故事板字段 | Lottie JSON 对应 | 说明 |
|-----------|----------------|------|
| `lottieSpec.source` | 生成通道选择 | `generate`（AI 生成）或 `collect`（自动收集） |
| `lottieSpec.animationType` | 动画模板选择 | 决定用哪个底层模板 |
| `lottieSpec.semanticTags` | 搜索/生成关键词 | 用于通道 B 的 API 查询 |
| `lottieSpec.duration` | `op` 字段 | 动画总时长 |
| `lottieSpec.frameRate` | `fr` 字段 | 帧率 |
| `lottieSpec.markers[].name` | `markers` 数组 | 与 `cueId` 直接映射 |
| `lottieSpec.layers[]` | `layers` 数组 | AI 生成的具体图层定义 |
| `lottieSpec.codeHighlightSync` | 与代码高亮联动 | 控制 Lottie 与代码高亮的同步时机 |

---

## 三、通道设计（全自动化）

### 通道 A：AI 直接生成 Lottie JSON

#### 3.1.1 生成流程

```
AI Prompt（结构化输入）
  ↓
输出：LottieSpec（中间格式，合法 JSON）
  ↓
LottieJSONBuilder（Python 脚本）
  ↓ 根据 LottieSpec 拼装合法 Bodymovin JSON
  ↓
输出：/lottie/Module_XX/pYY.json
```

#### 3.1.2 AI Prompt 设计（关键）

```python
# 输入（来自故事板）
lottie_spec = {
  "animationType": "concept-intro",
  "duration": 3.5,
  "frameRate": 30,
  "semanticTags": ["shadergui", "technical-artist"],
  "markers": [{"name": "intro", "time": 0}, ...],
  "layers": [...]  # 故事板已定义图层语义
}

# AI 任务（禁止自由生成，必须按模板）
task = f"""
你是一个 Lottie JSON 生成器。根据以下规格，生成合法的 Bodymovin JSON。

# 强制规则
1. 必须严格遵循 Bodymovin JSON Schema（附件）
2. 每个图层必须有对应的 keyframes
3. markers 数组必须与规格中的 markers 完全一致
4. 禁止生成非法字段
5. 输出必须是合法 JSON（可通过 json.loads 解析）

# 输入规格
{json.dumps(lottie_spec, indent=2)}

# 输出格式
{
  "v": "5.7.0",
  "fr": 30,
  "op": 105,
  "markers": [...],
  "layers": [...]
}
"""
```

#### 3.1.3 LottieJSONBuilder 脚本

```python
# scripts/build_lottie_from_spec.py
import json
import sys
from pathlib import Path

def build_lottie_json(spec: dict) -> dict:
    """根据 LottieSpec 生成合法 Bodymovin JSON"""
    
    # 1. 基础字段
    lottie = {
        "v": "5.7.0",
        "fr": spec["frameRate"],
        "op": int(spec["duration"] * spec["frameRate"]),
        "ip": 0,
        "w": 512,
        "h": 512,
        "markers": spec.get("markers", []),
        "layers": []
    }
    
    # 2. 图层生成（根据 spec.layers[]）
    for idx, layer_spec in enumerate(spec["layers"]):
        layer = {
            "ty": 4,  # 形状图层
            "nm": layer_spec["name"],
            "sr": 1,
            "ks": build_keyframes(layer_spec["keyframes"]),
            "shapes": build_shapes(layer_spec)
        }
        lottie["layers"].append(layer)
    
    # 3. Schema 校验
    validate_against_schema(lottie)
    
    return lottie

def validate_against_schema(json_data: dict):
    """校验 Bodymovin JSON Schema"""
    # 使用 lottie-js 的 schema 或手写校验逻辑
    required_fields = ["v", "fr", "op", "ip", "w", "h", "layers"]
    for field in required_fields:
        if field not in json_data:
            raise ValueError(f"缺少必需字段: {field}")
```

#### 3.1.4 验收标准（通道 A）

- [ ] AI 能根据 `lottieSpec` 生成合法 JSON（通过 `json.loads`）
- [ ] 生成的 JSON 符合 Bodymovin Schema（通过 `lottie-validator`）
- [ ] `markers[]` 与故事板的 `cueId` 完全对齐
- [ ] 文件体积 < 500KB
- [ ] 无敏感字段（如 `shotInstruction` 等内部文案）

---

### 通道 B：自动收集（公开资源 API）

#### 3.2.1 收集流程

```
LottieSpec.semanticTags[]
  ↓
LottieCollector（收集器）
  ↓ 调用 LottieFiles API / 其他公开 API
  ↓ 筛选：CC 许可、体积 < 500KB、有 markers
  ↓
下载 + 本地镜像
  ↓
输出：/lottie/vendor/XXX.json
```

#### 3.2.2 LottieCollector 脚本

```python
# scripts/collect_lottie.py
import requests
import json
from pathlib import Path

LOTTIEFILES_API = "https://api.lottiefiles.com/v1"

def collect_lottie(spec: dict, registry: dict) -> str:
    """自动收集 Lottie 资产"""
    
    tags = spec["semanticTags"]
    query = " ".join(tags)
    
    # 1. 调用 LottieFiles API
    response = requests.get(
        f"{LOTTIEFILES_API}/search",
        params={"query": query, "limit": 5}
    )
    results = response.json()["data"]
    
    # 2. 筛选：许可、体积、markers
    for item in results:
        if not is_cc_licensed(item["license"]):
            continue
        if item["fileSize"] > 500 * 1024:
            continue
        if not has_markers(item):
            continue
        
        # 3. 下载 + 镜像
        local_path = download_and_mirror(item)
        
        # 4. 注册到 registry
        registry["entries"].append({
            "id": item["id"],
            "localMirror": local_path,
            "license": item["license"],
            "tags": tags
        })
        
        return local_path
    
    raise ValueError(f"未找到符合条件的 Lottie 资产: {query}")
```

#### 3.2.3 验收标准（通道 B）

- [ ] 能调用 LottieFiles API 并获取结果
- [ ] 能根据许可、体积、markers 筛选
- [ ] 下载的文件能本地镜像到 `public/lottie/vendor/`
- [ ] 注册表（`registry.json`）能正确更新
- [ ] 故事板能通过 `lottieAsset.uri` 引用收集的资产

---

## 四、DAG 节点设计

### 4.1 扩展现有 DAG

```
原有：STORYBOARD_READY → DESIGN → STITCH → BUILD

新增（二选一，由故事板 lottieSpec.source 决定）：
  STORYBOARD_READY
    ├─ lottieSpec.source == "generate"
    │   → LOTTIE_GENERATE（AI 生成）
    │   → LOTTIE_VALIDATE
    │   → STITCH
    │
    └─ lottieSpec.source == "collect"
        → LOTTIE_COLLECT（自动收集）
        → LOTTIE_VALIDATE
        → STITCH
```

### 4.2 新增节点详细

| 节点 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `LOTTIE_GENERATE` | `lottieSpec`（故事板） | `/lottie/Module_XX/pYY.json` | AI 生成 + LottieJSONBuilder |
| `LOTTIE_COLLECT` | `lottieSpec.semanticTags[]` | `/lottie/vendor/XXX.json` + `registry.json` | 调用 API + 下载镜像 |
| `LOTTIE_VALIDATE` | 生成的 JSON | 校验报告 + `build.validated` 字段 | Schema、体积、markers 对齐 |
| `LOTTIE_STITCH` | 校验通过的 JSON | `stitch-manifest.json` 更新 | 与音频/字幕同级别检查 |

---

## 五、验证脚本设计

### 5.1 `scripts/verify_course.py` 扩展

```python
def verify_lottie_assets(storyboard: dict, public_dir: Path):
    """验证 Lottie 资产（新增检查项）"""
    
    for slide in storyboard["slides"]:
        for cue in slide.get("motionCues", []):
            spec = cue.get("dynamicGuidance", {}).get("lottieSpec")
            if not spec:
                continue
            
            # 1. 检查文件存在
            asset_uri = spec.get("assetUri")
            if asset_uri:
                assert (public_dir / asset_uri).exists(), f"Lottie 文件不存在: {asset_uri}"
            
            # 2. 检查校验状态
            if spec["source"] == "generate":
                assert spec.get("build", {}).get("validated") == True
            
            # 3. 检查 markers 与 cueId 对齐
            markers = spec.get("markers", [])
            assert any(m["name"] == cue["cueId"] for m in markers)
            
            # 4. 检查体积
            if asset_uri:
                size = (public_dir / asset_uri).stat().st_size
                assert size < 500 * 1024, f"Lottie 文件过大: {size} bytes"
```

### 5.2 `scripts/validate_lottie.py`（独立验证脚本）

```python
"""Lottie JSON 专用验证脚本"""
import json
import sys

def validate_lottie_json(file_path: str):
    with open(file_path) as f:
        data = json.load(f)
    
    # 1. Schema 校验
    required = ["v", "fr", "op", "ip", "w", "h", "layers"]
    for field in required:
        if field not in data:
            raise ValueError(f"缺少字段: {field}")
    
    # 2. markers 校验
    if "markers" in data:
        for marker in data["markers"]:
            assert "name" in marker
            assert "time" in marker
    
    # 3. 图层校验
    for layer in data["layers"]:
        assert "ty" in layer
        assert "nm" in layer
    
    print(f"✅ {file_path} 验证通过")

if __name__ == "__main__":
    validate_lottie_json(sys.argv[1])
```

---

## 六、前端运行时设计

### 6.1 组件结构（无变更，复用现有）

```
CoursePlayer.vue（时间源）
  └─ SlideCanvas.vue
       ├─ CodeHighlight.vue（代码高亮）
       ├─ SubtitleTrack.vue（字幕）
       └─ LottieStage.vue（Lottie 容器，新增）
```

### 6.2 LottieStage.vue Props（简化）

```typescript
interface Props {
  uri: string;               // /lottie/...json
  currentTime: number;        // 来自 CoursePlayer
  activeCue: Cue | null;   // 当前激活的 cue
  markers: Marker[];         // 来自 Lottie JSON 的 markers
}
```

### 6.3 时间绑定（与现有逻辑一致）

```typescript
// LottieStage.vue
watch(() => props.currentTime, (time) => {
  if (!lottieInstance) return;
  
  // 方式 1：直接 seek（简单）
  const frame = Math.floor(time * frameRate);
  lottieInstance.goToAndStop(frame, true);
  
  // 方式 2：按 marker 切换（推荐，与故事板对齐）
  if (props.activeCue) {
    const markerName = props.activeCue.cueId;
    lottieInstance.playSegments([markerName], true);
  }
});
```

---

## 七、实施阶段（最小可验证）

### 阶段 0：故事板规格定义（P0）

**目标**：定义 `lottieSpec` 字段，让故事板能输出合法规格

**任务**：
1. ✅ 扩展 `storyboard-contract.json` schema，增加 `lottieSpec` 字段
2. ✅ 编写 `docs/LottieSpec_Schema.md`（字段详细说明）
3. ✅ 更新 `docs/Skill_Chain_DAG.md`，增加 Lottie 节点说明

**验收**：
- [ ] schema 文件存在且合法
- [ ] 文档详细说明每个字段的含义和映射规则
- [ ] DAG 文档更新完成

---

### 阶段 1：通道 B 先通（自动收集）（P1）

**目标**：先让"自动收集"通道跑通，验证整个管道

**任务**：
1. ✅ 实现 `scripts/collect_lottie.py`（调用 LottieFiles API）
2. ✅ 创建 `.agent/lottie-library/registry.json`（注册表）
3. ✅ 更新 `scripts/verify_course.py`（增加 Lottie 检查）
4. ✅ 故事板示例：写一个 `lottieSpec.source == "collect"` 的示例

**验收**：
- [ ] `collect_lottie.py` 能成功调用 API 并下载文件
- [ ] 下载的文件能本地镜像到 `public/lottie/vendor/`
- [ ] `registry.json` 能正确更新
- [ ] `verify_course.py` 能通过检查
- [ ] `npm run build` 通过

---

### 阶段 2：通道 A 生成（AI 生成）（P2）

**目标**：实现 AI 直接生成 Lottie JSON

**任务**：
1. ✅ 实现 `scripts/build_lottie_from_spec.py`（LottieJSONBuilder）
2. ✅ 设计 AI Prompt（结构化输入 → 合法 JSON）
3. ✅ 实现 `scripts/validate_lottie.py`（独立验证脚本）
4. ✅ 故事板示例：写一个 `lottieSpec.source == "generate"` 的示例

**验收**：
- [ ] AI 能根据 `lottieSpec` 生成合法 JSON
- [ ] `build_lottie_from_spec.py` 能正确拼装 JSON
- [ ] `validate_lottie.py` 能通过校验
- [ ] 生成的文件体积 < 500KB
- [ ] 浏览器手动验证：动画能正常播放

---

### 阶段 3：前端集成（P3）

**目标**：LottieStage.vue 组件实现，与时间轴绑定

**任务**：
1. ✅ 实现 `LottieStage.vue` 组件
2. ✅ 修改 `SlideCanvas.vue`，集成 LottieStage
3. ✅ 实现时间绑定逻辑（`currentTime` → Lottie 进度）
4. ✅ 实现 marker 切换逻辑（`activeCue` → `playSegments`）

**验收**：
- [ ] 组件能正确加载 Lottie JSON
- [ ] 播放器时间轴能驱动 Lottie 进度
- [ ] 切换 slide 时 Lottie 能正确重置
- [ ] 浏览器手动验证通过

---

### 阶段 4：全链路验证（P4）

**目标**：完整 DAG 跑通，从故事板到交付

**任务**：
1. ✅ 更新 `.agent/flow_engine.py`，增加 Lottie 节点
2. ✅ 完整验证：`verify_course.py` + `build` + 浏览器
3. ✅ 性能优化：懒加载、体积控制、`prefers-reduced-motion` 降级

**验收**：
- [ ] `python .agent/flow_engine.py --module Module_01` 能通过
- [ ] `npm run build` 通过
- [ ] 浏览器验证：播放、seek、切 slide 均无错误
- [ ] Lighthouse 性能分数不降低（对比无 Lottie 版本）

---

## 八、风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| AI 生成的 JSON 不合法 | 播放失败 | `LOTTIE_VALIDATE` 门闸 + Schema 强制校验 |
| API 收集失败（限流/付费） | 管道中断 | 本地缓存 + 重试逻辑 + 降级到通道 A |
| 生成的动画质量差 | 学习体验差 | 人工抽检 + 反馈循环（可选，不阻塞管道） |
| 体积过大 | 性能问题 | 强制 < 500KB + 懒加载 |
| markers 与 cueId 不对齐 | 时间轴不同步 | 验证脚本强制检查对齐 |

---

## 九、与之前方案的核心差异

| 维度 | 之前方案（Cursor 计划） | 本方案（优化版） |
|------|---------------------|----------------|
| **人工操作** | 允许 AE/设计制作 | ❌ 完全禁止 |
| **故事板角色** | 只写"意图" | ✅ 直接输出 `lottieSpec` |
| **生成方式** | AI + 工具链（复杂） | ✅ AI 直接生成 JSON（简单） |
| **收集方式** | 白名单（手动维护） | ✅ 自动收集（API 调用） |
| **复杂度** | 高（双通道并行） | 低（先 B 后 A，渐进） |

---

## 十、结论

**本方案完全符合您的要求**：
1. ✅ **故事板驱动**：`lottieSpec` 字段直接映射 to Lottie JSON
2. ✅ **全自动化**：AI 生成 或 自动收集，零人工制作
3. ✅ **禁止 AE/设计**：删除所有相关环节
4. ✅ **最小可验证**：每个阶段独立可验收

**推荐实施顺序**：
1. **P0**：故事板规格定义（让故事板能输出 `lottieSpec`）
2. **P1**：通道 B 先通（自动收集，验证管道）
3. **P2**：通道 A 生成（AI 生成，完善功能）
4. **P3**：前端集成（LottieStage 组件）
5. **P4**：全链路验证（DAG 跑通）

---

**下一步**：
请确认是否按此方案执行。如果确认，我将开始 **P0 阶段**（定义 `lottieSpec` schema + 更新文档）。

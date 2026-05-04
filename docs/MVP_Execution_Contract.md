# MVP Execution Contract

本文档定义“执行 MVP”的固定边界。后续执行不得依赖聊天上下文记忆，必须以 `.agent/mvp-execution-scope.json` 为机器可读依据。

## 生产物定义

MVP 可清理生产物只包括运行端可再生输出：

- `CourseApp/src`
- `CourseApp/public`
- `CourseApp/dist`
- `CourseApp` 下的前端入口与构建配置文件
- `CourseContent/Module_01`
- `scripts/generate_audio.py`
- `scripts/verify_course.py`

## 禁止清理

以下路径不是 MVP 清理目标：

- `.agent/**`
- `CourseApp/node_modules/**`
- `CourseApp/package-lock.json`
- `.git/**`
- `.env` 或任何环境密钥文件
- `docs/**`

## 执行规则

1. `MVPMCP.generate_products(...)` 必须先读取 `.agent/mvp-execution-scope.json`。
2. 配置缺失、JSON 非法、清理项命中 deny 规则时，必须拒绝执行。
3. MVP 入口不得删除、覆盖或重建 `.agent` 下的任何产物。
4. `node_modules` 是依赖缓存，不属于生产物，不得删除。
5. 需要变更清理边界时，先改配置和本文档，再执行。

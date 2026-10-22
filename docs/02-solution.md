# 方案
```mermaid
flowchart LR
  A[读取 JSON] --> B{字段有效?}
  B -->|缺失| C[返回 needs_input]
  B -->|有效| D[本地素材检索]
  D -->|失败| E[返回 tool_error]
  D -->|无结果| F[返回 insufficient_evidence]
  D -->|命中| G[确定性模板与时长估算]
  G --> H[输出 JSON 与 trace]
```

| 模块 | 实现 |
|---|---|
| CLI | src/main.py:main |
| 工作流 | src/main.py:run |
| 知识 | data/materials.json |
| 状态 | needs_input / tool_error / insufficient_evidence / duration_exceeded / completed |

选择标准库是为了让评审无需密钥和依赖即可复现。未使用多 Agent、向量库或记忆，因为本演示不需要它们。
真实候选人应按题目接入模型生成、检查器和必要工具；固定模板不能代替真实生成能力的证据。
时长按每秒四个字符粗估，仅用于演示边界检查，不是语音时长测量。

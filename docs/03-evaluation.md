# 测试与评估
本页只记录离线流程验证，未验证真实模型效果。运行记录见 [test-results](../examples/test-results.txt)。


| 用例 | 输入变化 | 预期 | 实测 |
|---|---|---|---|
| 正常 | normal.input.json | completed，来源 ID 一致，30 秒 | 通过 |
| 缺字段 | 缺 platform | needs_input，并列出 platform | 通过 |
| 无资料 | product_id=unknown | insufficient_evidence，无事实输出 | 通过 |
| 工具失败 | simulate_tool_failure=true | tool_error | 通过 |
| 时长非法 | 0、负数、超限、布尔和字符串 | ValueError | 通过 |
| 对象类型 | 数组输入 | ValueError | 通过 |
| 字段类型 | topic 为数组 | ValueError | 通过 |
| 输入保护 | 运行前后比较请求 | 输入不被修改 | 通过 |


三个 CLI 输入与实际输出见 examples/。自动化测试共 8 项，通过 8 项。


## 示例如何评判
| 观察项 | 证据 | 结论 |
|---|---|---|
| 目录、文档齐全 | README 和 docs | 满足目录规范 |
| 可复现 | 3 个 CLI 样例、test-results.txt | 已在当前 Python 环境验证 |
| Agent 生成质量 | src/main.py 使用固定模板 | 未验证，不可按真实模型生成评分 |
| 风险处理 | 缺字段、无资料、工具失败的显式状态 | 局部实现，有对应测试 |
| 生产可靠性 | 无持久化、无服务化 | 未实现；小影校招加分项而非默认底线 |


此示例不能仅因目录完整便被判定题目达标。个人理解、真实贡献和学习能力仍需后续核验；本仓库不对应实际候选人的录用评分。


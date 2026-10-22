# 应届生 Agent 项目交付示例

这是 GitHub 项目目录与材料组织的真实示例，采用题目一「短视频脚本生成」场景。
**代码是离线确定性 Mock，不调用大模型，不是完整参考答案；不得据此推断真实生成质量。**

## 快速运行
Python 3.10+，无第三方依赖，无需密钥。在仓库根目录执行：
```sh
python3 -m src.main --input examples/normal.input.json
python3 -m src.main --input examples/missing.input.json
python3 -m src.main --input examples/tool-failure.input.json
python3 -m unittest discover -s tests -v
```
程序成功输出 JSON；业务异常以 JSON 状态返回，格式错误返回非零退出码。界面可选，本示例使用 CLI。

## 项目目录
```text
.
├── README.md                     # 安装、运行、评审导航
├── requirements.txt              # 无第三方依赖的声明
├── .env.example                  # 不含真实密钥
├── .gitignore
├── docs/
│   ├── 01-requirements.md         # 用户、范围、指标
│   ├── 02-solution.md             # 流程、模块、取舍
│   ├── 03-evaluation.md           # 用例和实际测试记录
│   ├── 04-ai-usage.md             # AI 使用及验证
│   └── 05-retrospective.md        # 不足和迭代
├── src/
│   ├── __init__.py
│   └── main.py                   # CLI 和离线流程
├── tests/test_main.py            # 自动化测试
├── data/materials.json           # 合成素材与规则
└── examples/
    ├── normal.input.json
    ├── normal.output.json
    ├── missing.input.json
    ├── missing.output.json
    ├── tool-failure.input.json
    ├── tool-failure.output.json
    └── test-results.txt          # 实际执行记录
```

## 评审导航
| 检查项 | 入口 |
|---|---|
| 业务目标 | [需求](docs/01-requirements.md) |
| 流程与调用链 | [方案](docs/02-solution.md) |
| 测试、预期、结果 | [评估](docs/03-evaluation.md) |
| AI 辅助边界 | [AI 使用](docs/04-ai-usage.md) |
| 不足及改进 | [复盘](docs/05-retrospective.md) |

运行输出中的 trace 记录步骤；evidence 引用 data/materials.json 的素材 ID。
normal.output.json 等是离线 Mock 的实际结果，不是真实模型调用记录。

## 提交约定
所有代码、文档、示例数据和结果放在同一仓库。提交仓库 URL、题号和最终 commit SHA；README 标明入口。私有仓库需让指定评审账号能读取。不得提交密钥或真实业务/候选人数据。
目录采用 Python 示范；其他技术栈可以使用等价依赖清单，但仍须保留各类材料。
审核方应在隔离环境运行陌生代码，不向候选人仓库提供个人凭据。

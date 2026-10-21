# industry-report — 行业深度分析 Multi-Agent 框架

WorkBuddy Skill：一个指令驱动 10 个专业 Agent 协作，产出带图表的 HTML 行业深度研究报告。

> 框架版本 v2.4.3-r2（2026-10-19）

## 功能

输入"分析 XX 行业"，框架自动完成：

- **Leader 预研** → 数据底座（Agent8）→ 四路并行分析（需求/产业链/技术/市场估值）→ 周期分析（Agent9）→ 五路 QC → 统一口径基线仲裁 → 预期差公司筛选（Agent4）→ 终稿撰写（Agent5）→ **HTML 报告生成（Agent10）** → 终审交付
- 全程量化 QC 闸门、信源编号可回溯、核心数字 ≥2 源交叉验证（✅/⚠️/🔴 可信度标记）
- **最终交付 HTML 报告**：每页页眉品牌 + 结构性信息（产业链、成本利润池、技术路线、市场规模）ECharts 图表化

## 安装

方式一（推荐）：下载 `industry-report.skill`，将后缀改为 `.zip` 解压，把 `industry-report/` 文件夹放到：

```
用户级（所有项目可用）: ~/.workbuddy/skills/industry-report/
项目级（仅当前项目）:   <项目>/.workbuddy/skills/industry-report/
```

方式二：直接克隆本仓库，把 `industry-report/` 文件夹复制到上述路径。

重启会话后，对 WorkBuddy 说「用 industry-report 分析XX行业」即可触发。

## 前置条件（重要）

本框架的定性信息主源是**信息聚合知识星球**（付费订阅），未连接无法开工：

1. 在 WorkBuddy 中安装并连接**知识星球（zsxq）connector**
2. 确保当前账号已订阅「信息聚合」星球（group-id `15554514552822`）
3. Skill 启动时会自动探活检查；未通过将返回：
   `请连接信息聚合知识星球（group-id 15554514552822），订阅请微信联系ldlld1234`

可选增强：
- 自有 IMA 知识库（ima-mcp connector）：按 `_agent_templates/IMA_KB_API_GUIDE.md` 替换为自有库 kbId
- 行情/财务数据源：**无需配置**——框架自动使用已连接的行情 connector，缺省时自动安装 akshare（免费、免 token）取数

## 使用体验

门禁通过后**全自动运行**：不询问输出目录（默认当前工作区）、不询问数据源配置、不请求流程确认；中间过程只发简短进展，最终交付 `10-HTML报告/` 下的成套 HTML 报告。

## 目录结构

```
industry-report/
├── SKILL.md                      # 触发器入口（含数据源门禁）
└── _agent_templates/             # 全部模板（自包含，无外部依赖）
    ├── 00-leader-agent.md        # Leader 主模板
    ├── leader-scheduling.md      # 调度逻辑（阶段-1 门禁 ~ 阶段6 交付）
    ├── datasources.md            # 数据源政策（唯一事实源）
    ├── 01~09 各专业 Agent 模板    # 需求/产业链/技术/预期差/报告/QC/估值/数据/周期
    ├── 10-html-report-agent.md   # HTML 报告生成（页眉品牌+图表化）
    └── ...（关键词清单/信源列表模板、IMA 接口文档、CHANGELOG）
```

## 使用

| 说法 | 动作 |
|------|------|
| `用 industry-report 分析XX行业` | 全新全流程 r1 |
| `industry-report XX行业 r2` | 全新重跑（旧版归档） |
| `industry-report XX行业 续跑` | 断点续跑 |
| `industry-report XX行业 只跑A8/只QC` | 单环节执行 |

输出落在 `<工作区>/<行业名>/00~10 子目录`，最终报告在 `10-HTML报告/`。

## 免责声明

报告为 AI 辅助研究产物，核心数字虽已双源交叉验证，仍可能含误差；每份报告附《待核验清单》，精确数字请以公告/交易所原文终核。不构成投资建议。

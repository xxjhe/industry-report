# 统一数据接口层说明 v2.4

> **数据源政策唯一事实源为 [`datasources.md`](./datasources.md)。** 本文件仅定义接口封装与调用方式；凡涉及"数据源优先级、启用/停用"的表述，一律以 `datasources.md` 为准。

## 概述
Data Agent通过以下标准化接口访问数据，并负责将来源、查询、清洗、转换、口径和初验结果沉淀到数据账本。其他分析Agent优先引用Data Agent登记后的`data_id/source_id`，避免各Agent重复搜索、口径不一致和未登记数据进入最终报告。

数据层核心产物：
- `08-数据与图表附件/source_registry.csv`
- `08-数据与图表附件/data_ledger.csv`
- `08-数据与图表附件/data_validation_report.md`
- `08-数据与图表附件/conflict_log.md`
- `08-数据与图表附件/data_requirements_status.md`

## 数据源总览 v2.4

> 政策详见 `datasources.md`。下表仅为接口映射速查，优先级以 `datasources.md` 为准。

| 编号  | 数据源        | 连接方式                       | 数据类型             | 主要用途                          | 状态/优先级   |
| --- | ---------- | -------------------------- | ---------------- | ----------------------------- | ----- |
| DS5 | **信息聚合知识星球（门禁源）** | zsxq connector（group-id `15554514552822`） | 文本（研报/纪要/市场情绪/分歧/反方观点） | **行业定性信息唯一强制第一优先**（未连接不得开工） | ★★★★★ 第一优先 |
| DS1 | IMA知识库（使用者自有库，可选） | MCP `mcp__ima-mcp__*`（见 IMA_KB_API_GUIDE.md） | 文本（研报/纪要/专家交流/外资研报） | 定性信息可选增强（自有库 kbId） | ★★★ 可选 |
| DS4 | **WebSearch** | `WebSearch` tool | 文本（研报/政策/纪要/观点/新闻） | 近12个月动态 + IMA/星球未覆盖缺口 + **近6个月技术突破/订单/政策强制补搜** | ★★★ 补充 |
| DS0 | **结构化数据自动择源** | ①已连接行情 connector（westock-mcp/通达信/Tushare）②无则自动 pip 安装 **akshare**（免费、免 token） | 结构化（实时行情/估值/财务/宏观） | 股价/PE/PB/分位/市值/营收净利——**自动探测可用源，不作为门禁项，缺源自动补** | ★★★★★ 自动 |
| DS2 | 通达信        | MCP `mcp__tdx-connector__` | 结构化（行情/财务/板块/估值） | 行情/财务/板块/估值分位/技术指标——**备用，用前先测**      | ★★★★ 备用 |
| DS3 | Tushare    | Python API                 | 结构化（行情/财务/宏观）    | 补充财务数据、宏观经济指标（辅助）                 | ★★★ 辅助  |
| DS6 | Wind缓存长江指数 | 本地数据文件                     | 结构化（指数/行业）       | 行业指数历史数据（注意时效）                      | ★★★ 辅助  |

> **数据源使用顺序（以 datasources.md 为准）**：行业定性信息 → **信息聚合知识星球第一优先（自有 IMA 库可选增强）**，**WebSearch 补充**（近12个月动态/缺口 + 近6个月强制补搜）；股价/财务/估值结构化数字 → **自动择源**（已连接行情 connector 优先，缺省自动装 akshare），不作为门禁项。

## 接口函数定义 v2.4

### 1. 行业知识检索（定性信息，信息聚合知识星球第一优先，WebSearch 补充）
```
search_industry_knowledge(query, kb_ids=None, limit=10)
```
- 封装: **信息聚合知识星球 zsxq connector（第一优先·强制，group-id `15554514552822`）+ 自有 IMA 库 `mcp__ima-mcp__search_knowledge`（可选增强）**；**WebSearch 补充**（近12个月动态/缺口 + 近6个月强制补搜）；可辅以 `mcp__tdx-connector__wenda_report_query`（通达信用前先测）
- 用法: 按 datasources.md 检索纪律——先信息聚合知识星球 → （可选）自有 IMA 库 → 不足 WebSearch 补
- 示例: `search_industry_knowledge("固态电池")`（星球）

### 2. 行业板块数据
```
get_industry_sector(sector_name)
```
- 封装: `mcp__tdx-connector__tdx_quotes`
- 用法: 获取行业板块指数、成分股列表
- 示例: `get_industry_sector("储能")`

### 3. 股票财务数据
```
get_stock_financials(stock_codes, fields=None, periods=4)
```
- 封装: `mcp__tdx-connector__tdx_api_data`
- 用法: 获取公司营收、利润、ROE、毛利率等财务数据
- 示例: `get_stock_financials(["300750", "002594"], fields=["revenue", "net_profit", "roe", "gross_margin"])`

### 4. 股票行情数据
```
get_stock_quotes(stock_codes)
```
- 封装: `mcp__tdx-connector__tdx_quotes`
- 用法: 获取实时行情、涨跌幅、市值、PE/PB等
- 示例: `get_stock_quotes(["300750", "688390"])`

### 5. 股票K线数据
```
get_stock_kline(stock_code, period="day", count=250)
```
- 封装: `mcp__tdx-connector__tdx_kline`
- 用法: 获取历史K线数据，用于股价驱动因素分析和估值分位计算
- 示例: `get_stock_kline("300750", period="month", count=36)`

### 6. 行业/公司新闻
```
search_industry_news(keywords, days=30, limit=20)
```
- 封装: `WebSearch` + `mcp__tdx-connector__wenda_news_query`
- 用法: 搜索行业相关新闻和公司动态
- 示例: `search_industry_news(["储能", "钠电池"], days=180)`

### 7. 公司公告
```
get_company_notices(stock_codes, days=90)
```
- 封装: `mcp__tdx-connector__wenda_notice_query`
- 用法: 获取公司公告、业绩预告、重大事项
- 示例: `get_company_notices(["300750"], days=180)`

### 8. 条件筛选
```
screen_stocks(sector, conditions)
```
- 封装: `mcp__tdx-connector__tdx_screener`
- 用法: 按财务、估值、技术指标筛选股票
- 示例: `screen_stocks("储能", {"pe_max": 30, "roe_min": 15, "revenue_growth_min": 20})`

### 9. 宏观数据
```
get_macro_indicators(indicators=None)
```
- 封装: `mcp__tdx-connector__wenda_macro_query` + 本地`macro-turning-analysis` skill
- 用法: 获取GDP、PMI、利率等宏观指标
- 示例: `get_macro_indicators(["gdp", "pmi", "cpi"])`

### 10. 机构研报与评级（新增）
```
get_research_reports(keywords, days=180, limit=20)
```
- 封装: `mcp__tdx-connector__wenda_report_query`
- 用法: 获取机构研报摘要、评级和目标价，用于市场共识分析
- 示例: `get_research_reports("储能 行业", days=180)`

### 11. 技术指标数据（新增）
```
get_technical_indicators(stock_codes, indicators=None)
```
- 封装: `mcp__tdx-connector__tdx_indicator_select`
- 用法: 获取换手率、成交额、融资余额等技术指标
- 示例: `get_technical_indicators(["300750"], indicators=["turnover", "volume", "margin"])`

## Agent数据源使用矩阵 v2.0

| 数据需求 | Agent1 | Agent2 | Agent3 | Agent7 | Agent4 | Agent5 | Agent6 |
|----------|--------|--------|--------|--------|--------|--------|--------|
| search_industry_knowledge | ★★★ | ★★★ | ★★★ | ★★★ | ★★★ | ★★ | ★ |
| get_industry_sector | ★★ | ★★★ | ★ | ★★ | ★★★ | ★ | ★ |
| get_stock_financials | ★ | ★★ | ★ | ★★ | ★★★ | ★ | ★★★ |
| get_stock_quotes | ★ | ★★ | ★ | ★★★ | ★★★ | ★ | ★ |
| get_stock_kline | - | - | - | ★★★ | ★★ | - | ★ |
| search_industry_news | ★★ | ★★ | ★★★ | ★★ | ★★ | ★ | ★★★ |
| get_company_notices | ★ | ★ | ★★ | ★ | ★★★ | ★ | ★★ |
| screen_stocks | - | ★★ | ★ | ★ | ★★★ | - | ★ |
| get_macro_indicators | ★★★ | - | - | - | - | - | ★ |
| get_research_reports | ★ | ★ | ★ | ★★★ | ★★★ | ★ | ★★★ |
| get_technical_indicators | - | - | - | ★★★ | ★★ | - | ★ |

## v2.0 新增数据需求

### Agent7特有数据源
1. **卖方研报与评级**: 用于市场共识提炼，通过 `get_research_reports` 获取
2. **历史估值数据**: 用于估值分位分析，通过 `get_stock_kline` 和 `get_stock_quotes` 获取
3. **机构持仓数据**: 用于交易结构分析，通过通达信MCP和WebSearch获取
4. **融资融券数据**: 用于拥挤度判断，通过通达信MCP获取
5. **主题热度指数**: 用于情绪判断，通过WebSearch获取搜索指数

### Agent4新增数据依赖
1. **市场共识与分歧**: 来自Agent7输出（核心新增依赖）
2. **估值隐含预期**: 来自Agent7输出，用于估值预期差判断
3. **交易结构**: 来自Agent7输出，用于判断关注度和拥挤度风险

## 数据质量要求 v2.0

1. **来源标注**: 所有数据使用必须标注来源、统计口径和获取时间
2. **口径一致**: 同一指标在同一份报告中使用统一统计口径
3. **时效性检查**: Agent6核查时验证数据时间范围是否合理
4. **交叉验证**: 关键数据尽可能从多个来源交叉验证，优先使用一手来源
5. **估算标注**: 任何基于推算/估算的数据必须明确标注"估算"和测算方法

## 实际调用示例 v2.0

### Agent7 获取市场共识与估值数据
```python
# 1. 获取卖方研报
# 使用: mcp__tdx-connector__wenda_report_query({keyword: "储能 行业 2025 2026"})

# 2. 获取行业板块行情和估值
# 使用: mcp__tdx-connector__tdx_quotes({sector: "储能"})

# 3. 获取历史K线（计算估值分位）
# 使用: mcp__tdx-connector__tdx_kline({code: "300750", period: "month", count: 36})

# 4. 搜索市场观点和催化剂
# 使用: WebSearch({query: "储能行业 催化剂 2026 政策 订单"})
```

### Agent4 基于Agent7结论筛选预期差公司
```python
# 1. 读取Agent7的市场共识清单
# 2. 寻找市场共识假设可能错误的方向
# 3. 筛选估值隐含预期偏低的标的
# 4. 交叉验证基本面、产业链和技术面支撑
```

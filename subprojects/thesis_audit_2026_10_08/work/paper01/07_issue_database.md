# Issue Database

paper_id: paper01

共 14 条正式问题：必须修改 5 条（ISSUE-001/002/003/004/007），建议修改 6 条（ISSUE-005/006/008/009/010/014），格式修正 3 条（ISSUE-011/012/013）。

```text
### ISSUE-001: 摘要四阶段表述与正文分期时序矛盾

- severity: 严重
- priority: 必须修改
- certainty: 确认问题
- matrix_id: MX-001/MX-018
- object_ledger_id: OBJ-001
- claim_id: CLM-014
- method_id: M-01
- location: 行5（摘要）；对照行25（第二章第一小节）
- original_excerpt: "自2018年文化和旅游部组建以来，我国文旅融合政策经历了从分立管理、制度化推进、机构整合到深度融合发展与支柱产业定位的四个阶段"
- problem: 正文第一阶段为"分立管理时期的资源协作（1978—2008）"，早于2018年，摘要"自2018年……经历了……四个阶段"构成时序矛盾。
- basis: 论文前后文交叉核对（行5与行25）
- modification_requirement: 将摘要改为"自1978年以来特别是2018年文化和旅游部组建以来，我国文旅融合政策经历了……四个阶段"，或删去起始时间限定。
- factcheck_status: 不适用（内部一致性问题）

### ISSUE-002: "合计接近GDP的9%"直接加总未说明口径可加性

- severity: 严重
- priority: 必须修改
- certainty: 疑似问题
- matrix_id: MX-017/MX-019/MX-022/MX-023
- object_ledger_id: OBJ-019
- claim_id: CLM-003/CLM-015
- method_id: M-02
- location: 行91（四章一节）、行171（结论）
- original_excerpt: "两大产业合计贡献接近GDP的9%"；"文化旅游业增加值占GDP比重接近9%"
- problem: 4.61%+4.35%=8.96%的代入成立，但"文化及相关产业"与"旅游及相关产业"两套统计分类存在交叉（住宿、餐饮、娱乐等可能重复计入），两占比是否可直接相加构成方法前提，正文未作任何口径说明；该加总结论支撑"支柱产业地位初步确立"的核心判断。
- basis: Level 1 复算 + method_and_fact_audit.md 方法前提规则；国家统计局两套分类口径
- modification_requirement: 应补充两套统计口径的交叉重叠说明与加总依据，或改为分别表述"文化产业占4.61%、旅游业占4.35%"，并相应弱化"支柱产业地位初步确立"的确定性措辞。
- factcheck_status: partly_verified（两分项 verified，加总前提未获来源支撑）

### ISSUE-003: 参考文献[26]"综合整理"不可追溯且来源链接与内容不符

- severity: 严重
- priority: 必须修改
- certainty: 确认问题
- matrix_id: MX-007
- object_ledger_id: OBJ-011/OBJ-012
- claim_id: 无
- method_id: M-04
- location: 行227（著录）；行141、145、151、163（正文引用7处）；行255（Sources末条）
- original_excerpt: "[26] 文化和旅游领域国际比较研究相关文献与各国文化旅游政策法规 [R]. 综合整理."
- problem: 该条无作者、无年份、无具体文献，不可复核；Sources末条链接为《坚定走好独具特色的中国旅游发展之路》（ gov.cn 2024-05），与"国际比较研究"内容不符；第六章日/法/意/韩四国事实与第七章立法建议全部依赖该条，证据链断裂。
- basis: 学位论文问题汇总"引文出处不规范""正文引用了文献但无法定位"；核对 Sources 列表
- modification_requirement: 将[26]拆分为具体可查的国别政策文献（著录作者、题名、出处、年份），逐条替换正文引用；同时更正 Sources 末条与[26]不匹配的链接。
- factcheck_status: unsupported（公开渠道无法核验）

### ISSUE-004: 参考文献[10]缺期刊名称与卷期页码

- severity: 严重
- priority: 必须修改
- certainty: 确认问题
- matrix_id: MX-015
- object_ledger_id: OBJ-011
- claim_id: 无
- method_id: 无
- location: 行195
- original_excerpt: "[10] 崔凤军, 徐鹏, 陈旭峰. 文旅融合高质量发展研究——基于机构改革视角的分析 [J]. 2020(6)."
- problem: 标注[J]但未给出期刊名称、卷号、页码，文献不可检索；该条被正文引用7次并支撑基层体制机制问题诊断。
- basis: 学位论文问题汇总"参考文献格式不统一、字段不完整"
- modification_requirement: 补齐期刊名称、年份、卷期与页码，核对正式出版信息。
- factcheck_status: needs_author_source

### ISSUE-005: 四条参考文献的来源链接为平台转载页，与著录报刊名不一致

- severity: 重要
- priority: 建议修改
- certainty: 确认问题
- matrix_id: MX-016
- object_ledger_id: OBJ-012
- claim_id: CLM-010
- method_id: 无
- location: 行245（[16]）、行246（[17]）、行252（[23]）、行254（[25]）
- original_excerpt: "[双节文旅收官盘点：古韵山西破壁出圈](http://m.toutiao.com/group/7694190769397957170/)"
- problem: 著录来源为华夏时报、界面新闻、中国日报网、金融时报，但 Sources 给出的链接均为今日头条（m.toutiao.com）转载页；转载渠道与著录出处不一致，且平台页存在内容变更或失效风险，引用可追溯性与可靠性不足。
- basis: 学位论文问题汇总"引用来源不可靠""网页缺发布机构与访问日期"
- modification_requirement: 替换为原发媒体的正式页面链接，并补注访问日期；无法获得原发链接的，应在著录中如实标注转载渠道与访问日期。
- factcheck_status: confirmed（链接渠道与著录不一致可直接核对）

### ISSUE-006: 出游数据增速与文中基数不能互推

- severity: 重要
- priority: 建议修改
- certainty: 确认问题
- matrix_id: MX-021/MX-023
- object_ledger_id: OBJ-020
- claim_id: CLM-004
- method_id: M-02
- location: 行97
- original_excerpt: "2024年国内居民出游56.2亿人次，出游总花费5.8万亿元；2025年……65.22亿人次……6.30万亿元，同比分别增长16.2%和9.5%"
- problem: 按文中基数复算，人次增速为16.05%、花费增速为8.6%，与所引16.2%、9.5%不符；差异源于2024年基数为四舍五入约数（官方增速以精确基数计算，已外部核验属实），但正文未说明。
- basis: Level 1 公式代入复算 + 文旅部 2026-01-26 发布数据外部核验
- modification_requirement: 应注明"2024年数据为四舍五入约数，增速按官方口径计算"，或补注精确基数。
- factcheck_status: partly_verified

### ISSUE-007: 浮梁案例"旅游收入接近GDP四成"口径错配且数据与官方预计数不一致

- severity: 严重
- priority: 必须修改
- certainty: 确认问题
- matrix_id: MX-008/MX-022/MX-023
- object_ledger_id: OBJ-025
- claim_id: CLM-011
- method_id: M-03
- location: 行93
- original_excerpt: "江西浮梁县2025年接待游客773.70万人次、旅游综合收入80.53亿元，旅游收入体量已接近当地GDP的四成"
- problem: 其一，旅游综合收入为消费总流水，GDP为增加值，两口径不可直接相比；按浮梁县2025年统计公报GDP 191.31亿元代入得42.1%，数值虽接近但比较方法不成立。其二，浮梁县政府工作报告（2026-02）"预计"数为791.39万人次、74.59亿元，与文中数不一致，数据时点与来源口径未说明。
- basis: 浮梁县2025年统计公报与政府工作报告（外部核验）+ 方法前提规则
- modification_requirement: 应注明两项数据的具体来源与统计时点，说明"旅游综合收入"与GDP的口径差异，或改用可比口径（如旅游业增加值占GDP比重）重新表述。
- factcheck_status: partly_verified

### ISSUE-008: 摘要与导言段"研究发现"内容高度重复

- severity: 重要
- priority: 建议修改
- certainty: 确认问题
- matrix_id: MX-001
- object_ledger_id: OBJ-001/OBJ-002
- claim_id: 无
- method_id: 无
- location: 行5（摘要末段）与行9（导言末段）
- original_excerpt: 两处均以"研究发现："引出政策体系构成与问题诊断的同构表述
- problem: 摘要与导言均用整段概括研究框架与主要发现，内容重合度高，未体现二者功能分工。
- basis: 自检清单"摘要应聚焦学术工作，不能包含大篇幅背景或无关信息"；问题汇总"避免重复话语"
- modification_requirement: 摘要保留结论性陈述，导言段改为只述研究问题与章节安排，删去重复的发现概括。
- factcheck_status: 不适用

### ISSUE-009: "过境免签55国"未标注数据时点

- severity: 重要
- priority: 建议修改
- certainty: 确认问题
- matrix_id: MX-025
- object_ledger_id: OBJ-022
- claim_id: CLM-006
- method_id: M-01
- location: 行79
- original_excerpt: "过境免签覆盖范围达55个国家"
- problem: 所引[21]发布时间为2026-03-10，当时为55国；2026年9月新增吉尔吉斯斯坦、越南后已扩至57国。文章引用最新数据（[23]2026-10-08）却使用3月口径且未注明"截至"时点。
- basis: 外部事实核验（入境免签政策时点）
- modification_requirement: 注明"截至2026年3月"，或更新为57国并补充9月扩围的来源。
- factcheck_status: partly_verified

### ISSUE-010: 统计数据与党的文件表述主要引自二手媒体，部分历史数据无来源

- severity: 重要
- priority: 建议修改
- certainty: 确认问题
- matrix_id: MX-016
- object_ledger_id: OBJ-017
- claim_id: CLM-017
- method_id: M-01/M-02
- location: 行9、行17、行91、行97等（[13]共19处）；行27（2800万人次）
- original_excerpt: "2024年……占国内生产总值比重4.61%……[13]"；"当年国庆黄金周旅游接待人数达2800万人次"
- problem: 增加值、出游、景区等统计数据均以经济日报评论[13]为来源，党的二十大报告与二十届三中全会《决定》的表述亦引[13]；一手来源（国家统计局、文旅部统计公报、党的文件原文）未标注。行27"1999年国庆黄金周接待2800万人次"经公开检索未获确切口径来源。
- basis: 学位论文问题汇总"不要引用二手文献"；外部核验（FC-015）
- modification_requirement: 统计数据改引国家统计局/文旅部原始发布，党的文件改引报告与《决定》原文；"2800万人次"补注具体来源或删除该数字。
- factcheck_status: partly_verified（数据本体多已核验，来源层级需修正）

### ISSUE-011: 结论段句末合并引用，引用粒度不足

- severity: 一般
- priority: 格式修正
- certainty: 确认问题
- matrix_id: MX-014
- object_ledger_id: OBJ-010
- claim_id: CLM-018
- method_id: 无
- location: 行171
- original_excerpt: "2025年国内出游65.22亿人次……超1300亿美元……接近9%……[13][21]"
- problem: 同一句并列出游、入境、占比三组数据后合并标注[13][21]，读者无法判断各组数据分别对应哪一来源；行101多组案例数据共用[17]亦同。
- basis: 引用规范（对应性）
- modification_requirement: 将引用拆分至各自数据之后，或分句标注。
- factcheck_status: 不适用

### ISSUE-012: 参考文献著录字段不完整

- severity: 一般
- priority: 格式修正
- certainty: 确认问题
- matrix_id: MX-015
- object_ledger_id: OBJ-011
- claim_id: 无
- method_id: 无
- location: 行177（[1]仅2026）、行207-208（[16][17]仅2026-10）、行225（[25]仅2026）
- original_excerpt: "[16] 华夏时报. 双节文旅收官盘点：古韵山西破壁出圈 [N]. 2026-10."
- problem: 报纸文章缺出版日期（日），[1]缺具体日期，[25]仅著录年份，与同表其他条目精确到日的体例不统一。
- basis: 学位论文问题汇总"参考文献格式不统一"
- modification_requirement: 按统一体例补齐出版日期；无法确定的注明检索日期。
- factcheck_status: 不适用

### ISSUE-013: Sources链接列表未与参考文献编号对应

- severity: 一般
- priority: 格式修正
- certainty: 确认问题
- matrix_id: MX-016
- object_ledger_id: OBJ-012
- claim_id: 无
- method_id: 无
- location: 行229-255
- original_excerpt: "Sources: - [国务院关于落实全国人大常委会……](http://…)"
- problem: 26条链接按顺序排列但未标注对应编号，读者需自行推断对应关系；与ISSUE-003、ISSUE-005的链接问题叠加，进一步削弱可追溯性。
- basis: 引用规范（可追溯性）
- modification_requirement: 每条链接前加注对应编号，如"[1] 题名 — URL"。
- factcheck_status: 不适用

### ISSUE-014: 结论未交代研究局限与后续研究方向

- severity: 重要
- priority: 建议修改
- certainty: 确认问题
- matrix_id: MX-013
- object_ledger_id: OBJ-010
- claim_id: 无
- method_id: 无
- location: 行169-173
- original_excerpt: "展望未来，文旅融合政策的演进将呈现三条主线。"
- problem: 自检清单要求结论给出研究局限与未来研究方向；现结论只有政策展望，未说明本研究在数据时点、案例覆盖面、国际比较深度等方面的边界。
- basis: 学位论文自检清单第5部分"应给出研究局限以及未来研究方向或拓展"
- modification_requirement: 在结论中增加一段研究局限与后续研究方向（如数据截至时点、案例代表性、国别比较的文献基础）。
- factcheck_status: 不适用
```

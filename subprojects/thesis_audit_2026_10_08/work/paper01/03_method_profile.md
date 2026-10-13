# Method Profile

paper_id: paper01

| method_id | method_name | location | role | input_data | premises | outputs | supports_main_claim | public_or_internal_recheck | required_actions | status |
|---|---|---|---|---|---|---|---|---|---|---|
| M-01 | 政策文本分析 | 行5、21、23-85 | 核心方法：演进分期与体系结构 | 国务院/国办/文旅部政策文件、规划文本 | 引用政策文本真实存在且著录可追溯；分期标准一致 | 四阶段演进结论、"五位一体"工具结构 | 是（摘要与结论主干） | 文本可公开核对；引用编号已双向匹配 | internal_crosscheck + 外部抽查政策文号 | pass（分期与正文小节一致；四阶段/五位一体/五条路径三处内部一致） |
| M-02 | 统计数据实证观察 | 行17、75、79-81、91、93、97、105、171 | 核心证据：成效论证 | 国家统计局、文旅部、税务等统计口径数据 | 指标口径可比；占比可加性；增速基数一致 | 规模扩张、支柱产业判断 | 是（"支柱产业"核心判断） | Level 1 表内代入 + Level 2 公开数据复算 | minimal_recalculation + method_premise_check + external_factcheck | issue（ISSUE-002 加总口径、ISSUE-006 基数取整、ISSUE-007 县域口径） |
| M-03 | 典型案例考察 | 行93、101、110-118 | 辅助分析：模式归纳 | 浮梁、山西、敦煌、陶溪川等媒体报道 | 案例数据来源可追溯；案例与主题关联 | 四种融合模式、问题例证 | 部分（成效与问题章节） | 案例数据来自媒体二次来源 | external_factcheck + author_source_required | issue（浮梁数据官方预计数与文中数不一致，ISSUE-007） |
| M-04 | 国际比较研究 | 行141-145、151、163 | 辅助分析：镜鉴 | 日/法/意/韩政策实践 | 所引国别事实有可追溯文献支撑 | 三点政策启示 | 部分（第七章立法建议依赖） | 无具体来源，不可公开复核 | author_source_required | issue（[26]"综合整理"不可追溯，ISSUE-003） |

说明：本文为政策研究报告，不含计量模型、公式、问卷与实验，F 类"模型/公式/变量"检查项按体裁处理；作者自算结果限于比率与增量代入，已按 Level 0-2 复核。

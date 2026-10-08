# Hermes 飞书本地知识库 Skill

**开源协议：Apache License 2.0 · 允许商用。** 完整条款见 [LICENSE](LICENSE)，版权与归属声明见 [NOTICE](NOTICE)。

用于配置、核查和排障以下流程：

**飞书消息 → Hermes Gateway → 实际会话 Profile → 本地 Markdown 检索与读取 → 带来源回复。**

这是可复用的公开脱敏版本，包含操作指导与一个只读检索脚本。它不会自动创建飞书应用、修改 Hermes 配置或上传知识库。

## 文件

- [SKILL.md](SKILL.md)：技能入口、适用范围及验收标准。
- [飞书连接](references/feishu-connection.md)：权限、事件、启动与排障。
- [本地知识检索](references/local-knowledge.md)：Profile 可见性、分层检索和引用。
- [检索脚本](scripts/search_knowledge.py)：Python 标准库实现的 Markdown 固定字符串搜索。
- [Codex 界面信息](agents/openai.yaml)：技能名称与调用示例。

## 使用

将完整仓库目录放入运行工具实际支持的技能目录，目录名保持为 `hermes-feishu-local-knowledge`。Codex 可使用其用户技能目录；Hermes 应按当前版本的技能发现规则部署到实际处理飞书会话的 Profile。安装到 Codex 不会自动安装到 Hermes。

调用示例：

> 用 $hermes-feishu-local-knowledge 核查飞书与本地知识库链路，先做只读检查。

脚本需要 Python 3.9+，无需额外 Python 包。确认当前工作目录为仓库根目录，并把占位符替换为已授权的知识库目录：

```powershell
python -X utf8 scripts/search_knowledge.py --root '<AUTHORIZED_KNOWLEDGE_ROOT>' --query '示例主题' --limit 5
```

输出 JSON 包含文档相对路径、行号、匹配片段及读取错误。脚本不执行网络请求或写入知识库，跳过符号链接和目录联接。它是固定字符串检索，不是向量检索或数据库查询；匹配结果仍需读取正文核实。

## 脱敏与验证范围

公开文件不含个人目录、机器人昵称、真实模型配置、业务资料正文、凭证或历史部署日志。环境路径及账号标识均须由使用者在自己的部署环境配置。仓库公开不代表本地知识库应当公开。

发布前已验证 Skill 结构、相对文档链接、中文匹配、无匹配、缺失目录及读取错误处理，并对发布文件执行敏感信息模式扫描。飞书连接与完整消息闭环需在使用者实际环境中另行验收，本仓库不声称已在所有环境完成接入测试。

## 开源授权与商用说明

Copyright 2026 JediHzbot

除另有明确标注的第三方内容外，本仓库的原创 Skill 文档、配置示例和检索脚本均按 **Apache License, Version 2.0（Apache-2.0）** 授权。

### 允许的用途

- 个人使用、企业内部部署和商业使用。
- 复制、修改、分发，以及集成到收费产品或服务。
- 在遵守协议的前提下，以闭源方式分发衍生产品；协议不要求公开自己的修改。

**遵守 Apache-2.0 条款即可获得上述授权，无需另行申请商用许可，也无需支付本项目的许可费。** 第三方服务、模型或平台的费用及条款独立适用。

### 分发时的主要义务

- 随分发提供完整的 Apache-2.0 许可证副本。
- 在修改过的文件中显著说明已作修改。
- 在分发的衍生作品源文件中保留与所用部分相关的版权、专利、商标和归属声明。
- 本项目包含 [NOTICE](NOTICE)；分发衍生作品时，按协议第 4 条保留适用的归属声明。

### 授权范围与责任

协议包含第 3 条限定范围内的贡献者专利授权，并规定相应的专利诉讼终止条件；不授予商标使用权或官方背书。项目按现状提供，担保免责及责任限制以协议第 7、8 条和适用法律为准。

本授权不涵盖使用者的本地知识库、凭证、客户资料，也不替代 Hermes、飞书、模型或其他第三方组件自身的许可和服务条款。

以上中文说明仅便于理解，不增加、删减或替代协议条款；以仓库 [LICENSE](LICENSE) 中的英文全文为准。参考：[Apache 官方协议](https://www.apache.org/licenses/LICENSE-2.0)、[官方许可 FAQ](https://www.apache.org/foundation/license-faq.html)。

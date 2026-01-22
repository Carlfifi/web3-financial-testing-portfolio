# Web3金融业务测试实践作品集

## 项目简介
这是一个为系统化学习Web3金融业务（数字货币钱包、智能合约）测试而构建的实践项目。通过完整的动手操作，模拟了测试工程师在区块链领域的核心工作流程。

## 技术栈
- **区块链与工具**: Ethereum Sepolia测试网, MetaMask, Remix IDE, Etherscan
- **智能合约**: Solidity, OpenZeppelin标准库
- **测试开发**: Python, Web3.py
- **测试方法**: 手工测试、自动化脚本测试、业务场景分析

## 项目结构与内容
### 1. 钱包与链上交互 (`/1_wallet_and_onchain_interaction`)
- 创建并安全备份钱包，理解助记词、公私钥体系。
- 在Sepolia测试网进行转账、兑换等操作，熟悉Gas、区块浏览器。
- **我的测试网地址**: [0xAb34D44588e8aFf6DC1B67CB6F49448EFF27a324]
- **地址活动链接**: [https://sepolia.etherscan.io/address/0xAb34D44588e8aFf6DC1B67CB6F49448EFF27a324]

### 2. 智能合约测试 (`/2_smart_contract_testing`)
- 编写并部署了一个标准的ERC20代币合约 `MyTestToken`。
- **合约地址**: [0x7EB2956B16b8D1ab50f39c6e279Bd1181C0b3291]
- **部署交易**: [https://sepolia.etherscan.io/tx/0x26b29909ca9d1425420a5eab33708db79781af253405a4afb66d09b2786e63a1]
- 进行了手工功能测试与异常测试（如余额不足转账）。
- 使用Python + Web3.py编写自动化脚本，验证合约状态与异常行为。

### 3. 测试用例与文档 (`/3_test_cases_and_docs`)
- 设计了Web3钱包连接DApp的测试用例矩阵。
- 分析了中心化交易所充提币业务的核心流程与测试风险点。

### 4. 自动化脚本 (`/4_automation_scripts`)
- `automated_test.py`: 自动连接区块链、查询合约状态、模拟异常交易的脚本。
- `requirements.txt`: 项目Python依赖列表。
- 脚本成功运行截图：

(/4_automation_scripts/script_output.png)

## 如何运行自动化测试
1.  克隆本仓库: `git clone [你的仓库地址]`
2.  安装依赖: `pip install -r requirements.txt`
3.  在 `automated_test.py` 中配置你自己的Alchemy API URL。
4.  运行脚本: `python automated_test.py`

## 总结
通过本项目，我不仅实践了Web3测试的具体技术，更关键的是理解了在区块链**状态不可逆**特性下，**安全前置**和**异常测试**的极端重要性。这为我胜任金融业务测试工程师岗位打下了坚实的基础。

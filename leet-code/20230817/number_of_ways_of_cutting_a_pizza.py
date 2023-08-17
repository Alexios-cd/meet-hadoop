from typing import List
from unittest import TestCase
# https://leetcode.cn/problems/number-of-ways-of-cutting-a-pizza/
# 1444. 切披萨的方案数

class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        MOD = 10 ** 9 + 7
        m, n = len(pizza), len(pizza[0])
        s = [[0] * (n + 1) for _ in range(m + 1)]  # 二维后缀和
        f = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                s[i][j] = s[i][j + 1] + s[i + 1][j] - s[i + 1][j + 1] + (pizza[i][j] == 'A')
                if s[i][j]: f[i][j] = 1  # 初始值

        for _ in range(1, k):
            col_s = [0] * n  # col_s[j] 表示 f 第 j 列的后缀和
            for i in range(m - 1, -1, -1):
                row_s = 0  # f[i] 的后缀和
                for j in range(n - 1, -1, -1):
                    tmp = f[i][j]
                    if s[i][j] == s[i][j + 1]:  # 左边界没有苹果
                        f[i][j] = f[i][j + 1]
                    elif s[i][j] == s[i + 1][j]:  # 上边界没有苹果
                        f[i][j] = f[i + 1][j]
                    else:  # 左边界上边界都有苹果，那么无论怎么切都有苹果
                        f[i][j] = (row_s + col_s[j]) % MOD
                    row_s += tmp
                    col_s[j] += tmp
        return f[0][0]




class Test(TestCase):
    def test_01(self):
        pizza = ["A..","AAA","..."]
        k = 3
        ways = Solution().ways(pizza, k)
        self.assertEquals(ways, 3)


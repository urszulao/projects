class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        p = len(prices)
        
        profit = 0
        max_profit = 0
        
        i = 1 
        for i in range(1, p):
            profit += prices[i] - prices[i-1]
            if profit > 0:
                pass
            else:
                profit = 0
            max_profit = max(profit, max_profit)
        return max_profit

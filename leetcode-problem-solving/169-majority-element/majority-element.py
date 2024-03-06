class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        m = defaultdict(int)
        n = len(nums)

        for num in nums:
            m[num] += 1
        
        n = n//2

        for key, value in m.items():
            if value > n:
                return key 

        return 0 

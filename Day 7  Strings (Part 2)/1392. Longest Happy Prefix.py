class Solution:
    def longestPrefix(self, s: str) -> str:
        b = int((len(s) + 1) * -1)
        maxi = ""
        for i in range(len(s) - 1):
            for j in range(((i + 1) * -1), b, -1):
                if ((s[:i + 1]) == (s[j:])):
                    maxi = s[:i + 1]
                break
        if (maxi == ""):
            return ""
        return maxi

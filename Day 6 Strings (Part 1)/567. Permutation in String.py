class Solution:
    def checkInclusion(self, s1: str, s: str) -> bool:
        ws = len(s1)

        dih = {}
        dih1 = {}

        for c in s1:
            if c in dih:
                dih[c] += 1
            else:
                dih[c] = 1

        l = 0

        for r in range(len(s)):
            dih1[s[r]] = dih1.get(s[r], 0) + 1

            if r - l + 1 == ws:
                if dih1 == dih:
                    return True
                else:
                    dih1[s[l]] -= 1

                    if dih1[s[l]] == 0:
                        del dih1[s[l]]

                    l += 1

        return False
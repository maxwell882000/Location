def lengthOfLongestSubstring(self, s):
    check = {}
    length = len(s)
    starting_charachter = 0
    position = 0
    last = 0
    maxresult = 0
    for k in range(0, length):
        if s[k] in check and position < check[s[k]] + 1:
            position = check[s[k]] + 1
        check[s[k]] = k
        last = k
        if last - position + 1 > maxresult:
            maxresult = last - position + 1
    return maxresult


print(lengthOfLongestSubstring("", "abba"))

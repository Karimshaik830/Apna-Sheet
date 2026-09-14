def can_place(stalls, cows, distance):
    count = 1
    last = stalls[0]

    for i in range(1, len(stalls)):
        if stalls[i] - last >= distance:
            count += 1
            last = stalls[i]

            if count == cows:
                return True

    return False


def aggressive_cows(stalls, cows):
    stalls.sort()

    low = 0
    high = stalls[-1] - stalls[0]
    answer = 0

    while low <= high:
        mid = (low + high) // 2

        if can_place(stalls, cows, mid):
            answer = mid
            low = mid + 1
        else:
            high = mid - 1

    return answer


t = int(input())

for _ in range(t):
    n, c = map(int, input().split())
    stalls = [int(input()) for _ in range(n)]

    print(aggressive_cows(stalls, c))
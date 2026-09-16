import sys

# Increase recursion depth just in case, though we will use iterative DP
sys.setrecursionlimit(200000)


def solve():
    # Read n, l, r
    # Using sys.stdin.read to handle large input efficiently
    input_data = sys.stdin.read().split()

    if not input_data:
        return

    iterator = iter(input_data)

    try:
        n = int(next(iterator))
        l = int(next(iterator))
        r = int(next(iterator))

        a = []
        for _ in range(n):
            a.append(int(next(iterator)))
    except StopIteration:
        return

    MOD = 1000000007

    # Prefix sum array to calculate subarray sums in O(1)
    # prefix_sum[i] = sum(a[0]...a[i-1])
    # prefix_sum[0] = 0
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + a[i]

    # dp[i] = number of ways to paint the fence up to index i (first i blocks)
    # dp[0] = 1 (One way to paint 0 blocks: use 0 colors)
    dp = [0] * (n + 1)
    dp[0] = 1

    # We need to compute dp[i] using dp[j] where the sum of blocks from j to i-1 is in [l, r]
    # Sum(j to i-1) = prefix_sum[i] - prefix_sum[j]
    # Condition: l <= prefix_sum[i] - prefix_sum[j] <= r
    # Rearranging:
    # prefix_sum[i] - r <= prefix_sum[j] <= prefix_sum[i] - l

    # Since a[i] >= 1, prefix_sum is strictly increasing.
    # As i increases, the valid range for prefix_sum[j] shifts to the right.
    # We can maintain a sliding window / prefix sum of the dp array to optimize.
    # dp[i] = sum(dp[j]) for all valid j.

    # To do this efficiently (O(N) instead of O(N^2)), we maintain a running sum of valid dp values.
    # Let valid_j be the range of indices [left, right] such that:
    # 1. prefix_sum[i] - r <= prefix_sum[j]  => prefix_sum[j] >= prefix_sum[i] - r
    # 2. prefix_sum[i] - l >= prefix_sum[j]  => prefix_sum[j] <= prefix_sum[i] - l

    # Since prefix_sum is sorted, we can find the range of j using two pointers or binary search.
    # Let's use two pointers (left and right) to maintain the valid window of j.

    left = 0
    right = 0
    current_dp_sum = 0

    # We iterate i from 1 to n
    # For a given i, we need to find the range of j (0 <= j < i) such that:
    # L <= prefix_sum[i] - prefix_sum[j] <= R
    # => prefix_sum[i] - R <= prefix_sum[j] <= prefix_sum[i] - L

    for i in range(1, n + 1):
        target_min = prefix_sum[i] - r
        target_max = prefix_sum[i] - l

        # Adjust 'left' pointer: find the first index such that prefix_sum[left] >= target_min
        while left < i and prefix_sum[left] < target_min:
            left += 1

        # Adjust 'right' pointer: find the last index such that prefix_sum[right] <= target_max
        # We need right to be the largest index <= i-1 satisfying the condition.
        # We start right from where it was, but we must ensure right < i.
        # Actually, right should track the upper bound of valid j's.
        # As i increases, target_max increases, so right can only move forward.
        # However, right must be strictly less than i.

        # We want to include all j in [left, right] in our sum.
        # Initially, for i=1, left and right start at 0.

        # Expand right to include all j where prefix_sum[j] <= target_max
        # We need to be careful not to include j=i in the sum for dp[i]
        # So we check right < i

        # Let's refine the pointer logic:
        # We maintain a window [left, right] of valid j indices.
        # current_dp_sum holds sum(dp[k] for k in [left, right])

        # 1. Increase 'right' to include new valid j's (where prefix_sum[j] <= target_max)
        # We can check j = right + 1. If right + 1 < i and prefix_sum[right+1] <= target_max, we include it.
        # Note: right starts at -1 conceptually or we manage indices carefully.

        # Let's reset the logic for clarity:
        # We want sum(dp[j]) for j in [L_idx, R_idx]
        # L_idx is the smallest index such that prefix_sum[L_idx] >= prefix_sum[i] - r
        # R_idx is the largest index such that prefix_sum[R_idx] <= prefix_sum[i] - l

        # Since prefix_sum is increasing:
        # We can find L_idx using a pointer that only moves forward.
        # We can find R_idx using a pointer that only moves forward.

        # Let's use 'ptr_left' and 'ptr_right'
        # ptr_left: first index >= 0 such that prefix_sum[ptr_left] >= prefix_sum[i] - r
        # ptr_right: last index < i such that prefix_sum[ptr_right] <= prefix_sum[i] - l

        # To maintain sum efficiently:
        # We can maintain a window [ptr_left, ptr_right] and a running sum.

        # Initialize pointers before loop? No, they depend on i.
        # But since i increases, the required range shifts right.

        # Let's re-initialize logic inside loop but optimized.
        # We need to find the range [p1, p2] of j such that:
        # p1 = lower_bound(prefix_sum, prefix_sum[i] - r)
        # p2 = upper_bound(prefix_sum, prefix_sum[i] - l) - 1
        # And we only consider j < i.

        # Since we need O(N), we use two pointers.
        # Let's define:
        # low_idx: first valid index j
        # high_idx: last valid index j
        # We maintain a sum of dp[low_idx ... high_idx]

        # For current i:
        # 1. Find new low_idx: increment low_idx until prefix_sum[low_idx] >= prefix_sum[i] - r
        # 2. Find new high_idx: increment high_idx (up to i-1) while prefix_sum[high_idx+1] <= prefix_sum[i] - l
        #    Wait, high_idx is the upper bound. We want to include all j <= high_idx.
        #    So we increase high_idx as long as the next index satisfies the condition.

        # However, we must ensure high_idx < i.

        # Let's track the sum of dp values in the valid window.
        # When low_idx increases, we subtract dp[low_idx - 1].
        # When high_idx increases, we add dp[high_idx].

        # Initialization
        low_idx = 0
        high_idx = -1  # No valid indices yet
        current_sum = 0

        # We need to handle the window carefully.
        # Let's start high_idx such that it covers valid j's.
        # Actually, it's easier to just find the bounds [L, R] for each i and update the sum.
        # Since L and R only increase, we can maintain the sum.

        # Reset for the loop
        # We need to find the range of j in [0, i-1]

        # Let's restructure:
        # We maintain a window [l_ptr, r_ptr] of valid indices j.
        # current_sum = sum(dp[k] for k in [l_ptr, r_ptr])

        # For each i from 1 to n:
        #   1. Determine the valid range [L_bound, R_bound] based on prefix sums.
        #      L_bound: smallest j such that prefix_sum[j] >= prefix_sum[i] - r
        #      R_bound: largest j such that prefix_sum[j] <= prefix_sum[i] - l
        #   2. Adjust l_ptr to be at least L_bound. If l_ptr was < L_bound, subtract dp[l_ptr] and increment.
        #   3. Adjust r_ptr to be at least R_bound (but r_ptr must be < i).
        #      Actually, we want r_ptr to be exactly R_bound.
        #      If R_bound > r_ptr, we increment r_ptr and add dp[r_ptr] until r_ptr == R_bound.
        #      Wait, if R_bound < r_ptr, we must decrease r_ptr?
        #      Since prefix_sum[i] increases, R_bound = upper_bound(prefix_sum[i]-l) - 1.
        #      Since prefix_sum[i]-l increases, the upper bound index also increases or stays same.
        #      So r_ptr only moves forward.
        #      Similarly, L_bound increases.

        # So both pointers only move forward.

        # Initial state for i=1:
        # We haven't processed any j yet.
        # Let's set l_ptr = 0, r_ptr = -1, current_sum = 0.

        l_ptr = 0
        r_ptr = -1
        current_sum = 0

        for i in range(1, n + 1):
            val_min = prefix_sum[i] - r
            val_max = prefix_sum[i] - l

            # Find the new l_ptr
            # We need the first index >= 0 such that prefix_sum[index] >= val_min
            while l_ptr < i and prefix_sum[l_ptr] < val_min:
                # If we are moving l_ptr past the current window, we need to subtract from sum
                # But wait, the window is [l_ptr, r_ptr].
                # If l_ptr increases, we are removing dp[l_ptr] from the sum.
                # But we only subtract if l_ptr was <= r_ptr (i.e., it was in the window).
                if l_ptr <= r_ptr:
                    current_sum = (current_sum - dp[l_ptr] + MOD) % MOD
                l_ptr += 1

            # Find the new r_ptr
            # We need the largest index < i such that prefix_sum[index] <= val_max
            # We can increment r_ptr as long as r_ptr + 1 < i and prefix_sum[r_ptr+1] <= val_max
            # Note: r_ptr starts at -1.
            while r_ptr + 1 < i and prefix_sum[r_ptr + 1] <= val_max:
                r_ptr += 1
                if r_ptr >= l_ptr:
                    current_sum = (current_sum + dp[r_ptr]) % MOD

            # Now the valid range is [l_ptr, r_ptr]
            # If l_ptr > r_ptr, then current_sum is 0 (and dp[i] will be 0)
            dp[i] = current_sum

    print(dp[n])


if __name__ == "__main__":
    solve()
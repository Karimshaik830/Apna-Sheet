def countInversions(arr):
    def merge_sort(left, right):
        if right - left <= 1:
            return 0

        mid = (left + right) // 2

        inversions = merge_sort(left, mid)
        inversions += merge_sort(mid, right)

        temp = []
        i = left
        j = mid

        while i < mid and j < right:
            if arr[i] <= arr[j]:
                temp.append(arr[i])
                i += 1
            else:
                temp.append(arr[j])
                inversions += mid - i
                j += 1

        while i < mid:
            temp.append(arr[i])
            i += 1

        while j < right:
            temp.append(arr[j])
            j += 1

        arr[left:right] = temp

        return inversions

    return merge_sort(0, len(arr))
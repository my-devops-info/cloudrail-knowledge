from typing import Tuple, List

EMPTY_RANGE: Tuple[int, int] = (-1, -1)


def get_range_numbers_overlap(range1: Tuple[int, int], range2: Tuple[int, int]) -> Tuple[int, int]:
    low1, high1 = range1
    low2, high2 = range2
    if low2 <= low1 <= high2 or low1 <= low2 <= high1:
        low: int = low1 if low1 > low2 else low2
        high: int = high2 if high1 > high2 else high1
        return low, high
    else:
        return EMPTY_RANGE


def get_range_numbers_dis_overlap(range1: Tuple[int, int], range2: Tuple[int, int]) -> List[Tuple[int, int]]:
    low1, high1 = range1
    low2, high2 = range2
    overlap_range = get_range_numbers_overlap(range1, range2)

    if overlap_range != EMPTY_RANGE:
        overlap_low, overlap_high = overlap_range
        dis_overlap_list: List[Tuple[int, int]] = []
        if overlap_low > low1:
            dis_overlap_list.append((low1, overlap_low-1))
        elif overlap_low > low2:
            dis_overlap_list.append((low2, overlap_low-1))

        if overlap_high < high1:
            dis_overlap_list.append((overlap_high+1, high1))
        elif overlap_high < high2:
            dis_overlap_list.append((overlap_high+1, high2))

        return dis_overlap_list
    else:
        return [range1, range2]

import threading
import time

TOTAL_NUMBER = 10_000_000_000_000
TASK_COUNT = 4


def calculate_sum(start: int, end: int) -> int:
    count = end - start + 1
    return (start + end) * count // 2


def split_ranges(limit: int, parts: int) -> list[tuple[int, int]]:
    chunk_size = limit // parts
    ranges: list[tuple[int, int]] = []
    current_start = 1

    for index in range(parts):
        current_end = current_start + chunk_size - 1
        if index == parts - 1:
            current_end = limit
        ranges.append((current_start, current_end))
        current_start = current_end + 1

    return ranges


def worker(index: int, start: int, end: int, results: list[int]) -> None:
    results[index] = calculate_sum(start, end)


def main() -> None:
    ranges = split_ranges(TOTAL_NUMBER, TASK_COUNT)
    results = [0] * TASK_COUNT
    threads = []

    started_at = time.perf_counter()

    for index, (start, end) in enumerate(ranges):
        thread = threading.Thread(
            target=worker,
            args=(index, start, end, results),
            name=f"sum-thread-{index + 1}",
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(results)
    elapsed = time.perf_counter() - started_at

    print("Threading")
    print(f"Result: {total_sum}")
    print(f"Time: {elapsed:.6f} seconds")


if __name__ == "__main__":
    main()

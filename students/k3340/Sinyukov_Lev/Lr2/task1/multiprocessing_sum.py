import multiprocessing as mp
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


def worker(start: int, end: int, queue: mp.Queue) -> None:
    queue.put(calculate_sum(start, end))


def main() -> None:
    ranges = split_ranges(TOTAL_NUMBER, TASK_COUNT)
    queue: mp.Queue = mp.Queue()
    processes = []

    started_at = time.perf_counter()

    for start, end in ranges:
        process = mp.Process(target=worker, args=(start, end, queue))
        processes.append(process)
        process.start()

    partial_results = [queue.get() for _ in processes]

    for process in processes:
        process.join()

    total_sum = sum(partial_results)
    elapsed = time.perf_counter() - started_at

    print("Multiprocessing")
    print(f"Result: {total_sum}")
    print(f"Time: {elapsed:.6f} seconds")


if __name__ == "__main__":
    main()
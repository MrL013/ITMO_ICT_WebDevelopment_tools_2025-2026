import asyncio
import multiprocessing as mp
import time

from async_sum import calculate_sum as async_calculate_sum
from async_sum import split_ranges as async_split_ranges
from multiprocessing_sum import calculate_sum as process_calculate_sum
from multiprocessing_sum import split_ranges as process_split_ranges
from threading_sum import calculate_sum as thread_calculate_sum
from threading_sum import split_ranges as thread_split_ranges

TOTAL_NUMBER = 10_000_000_000_000
TASK_COUNT = 4


def run_threading() -> tuple[int, float]:
    import threading

    ranges = thread_split_ranges(TOTAL_NUMBER, TASK_COUNT)
    results = [0] * TASK_COUNT
    threads = []
    started_at = time.perf_counter()

    def worker(index: int, start: int, end: int) -> None:
        results[index] = thread_calculate_sum(start, end)

    for index, (start, end) in enumerate(ranges):
        thread = threading.Thread(target=worker, args=(index, start, end))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return sum(results), time.perf_counter() - started_at


def process_worker(start: int, end: int, queue: mp.Queue) -> None:
    queue.put(process_calculate_sum(start, end))


def run_multiprocessing() -> tuple[int, float]:
    ranges = process_split_ranges(TOTAL_NUMBER, TASK_COUNT)
    queue: mp.Queue = mp.Queue()
    processes = []
    started_at = time.perf_counter()

    for start, end in ranges:
        process = mp.Process(target=process_worker, args=(start, end, queue))
        processes.append(process)
        process.start()

    partial_results = [queue.get() for _ in processes]

    for process in processes:
        process.join()

    return sum(partial_results), time.perf_counter() - started_at


async def run_asyncio() -> tuple[int, float]:
    ranges = async_split_ranges(TOTAL_NUMBER, TASK_COUNT)
    started_at = time.perf_counter()
    tasks = [async_calculate_sum(start, end) for start, end in ranges]
    partial_results = await asyncio.gather(*tasks)
    return sum(partial_results), time.perf_counter() - started_at


def main() -> None:
    expected = (1 + TOTAL_NUMBER) * TOTAL_NUMBER // 2

    threading_result, threading_time = run_threading()
    multiprocessing_result, multiprocessing_time = run_multiprocessing()
    asyncio_result, asyncio_time = asyncio.run(run_asyncio())

    print(f"Expected result: {expected}")
    print()
    print("Comparison:")
    print(f"Threading        -> result: {threading_result}, time: {threading_time:.6f} seconds")
    print(f"Multiprocessing  -> result: {multiprocessing_result}, time: {multiprocessing_time:.6f} seconds")
    print(f"Asyncio          -> result: {asyncio_result}, time: {asyncio_time:.6f} seconds")


if __name__ == "__main__":
    main()

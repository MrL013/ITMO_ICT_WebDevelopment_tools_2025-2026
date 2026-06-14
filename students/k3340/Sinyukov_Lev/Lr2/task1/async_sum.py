import asyncio
import time

TOTAL_NUMBER = 10_000_000_000_000
TASK_COUNT = 4


async def calculate_sum(start: int, end: int) -> int:
    await asyncio.sleep(0)
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


async def main() -> None:
    ranges = split_ranges(TOTAL_NUMBER, TASK_COUNT)
    started_at = time.perf_counter()

    tasks = [calculate_sum(start, end) for start, end in ranges]
    partial_results = await asyncio.gather(*tasks)

    total_sum = sum(partial_results)
    elapsed = time.perf_counter() - started_at

    print("Asyncio")
    print(f"Result: {total_sum}")
    print(f"Time: {elapsed:.6f} seconds")


if __name__ == "__main__":
    asyncio.run(main())

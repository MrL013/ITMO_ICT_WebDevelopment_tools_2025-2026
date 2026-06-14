from __future__ import annotations

import multiprocessing as mp
import time

from common import URLS, fetch_title_sync, init_database, save_result, split_into_chunks

WORKER_COUNT = 3


def parse_and_save(url: str) -> None:
    title = fetch_title_sync(url)
    save_result(url, title, "multiprocessing")
    print(f"[multiprocessing] {url} -> {title}")


def worker(urls: list[str]) -> None:
    init_database()
    for url in urls:
        parse_and_save(url)


def run_multiprocessing() -> float:
    init_database()
    chunks = split_into_chunks(URLS, WORKER_COUNT)
    processes = []
    started_at = time.perf_counter()

    for chunk in chunks:
        process = mp.Process(target=worker, args=(chunk,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    return time.perf_counter() - started_at


def main() -> None:
    elapsed = run_multiprocessing()
    print(f"Multiprocessing completed in {elapsed:.6f} seconds")


if __name__ == "__main__":
    main()

from __future__ import annotations

import threading
import time

from common import URLS, fetch_title_sync, init_database, save_result, split_into_chunks

WORKER_COUNT = 3


def parse_and_save(url: str) -> None:
    title = fetch_title_sync(url)
    save_result(url, title, "threading")
    print(f"[threading] {url} -> {title}")


def worker(urls: list[str]) -> None:
    for url in urls:
        parse_and_save(url)


def run_threading() -> float:
    init_database()
    chunks = split_into_chunks(URLS, WORKER_COUNT)
    threads = []
    started_at = time.perf_counter()

    for index, chunk in enumerate(chunks, start=1):
        thread = threading.Thread(target=worker, args=(chunk,), name=f"parser-thread-{index}")
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return time.perf_counter() - started_at


def main() -> None:
    elapsed = run_threading()
    print(f"Threading completed in {elapsed:.6f} seconds")


if __name__ == "__main__":
    main()

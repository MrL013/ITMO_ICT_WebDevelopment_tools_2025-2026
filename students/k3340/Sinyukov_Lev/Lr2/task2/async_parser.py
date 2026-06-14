from __future__ import annotations

import asyncio
import time

import aiohttp

from common import URLS, REQUEST_TIMEOUT, extract_title, init_database, save_result, split_into_chunks

WORKER_COUNT = 3
_SESSION: aiohttp.ClientSession | None = None


async def fetch_title_async(url: str) -> str:
    if _SESSION is None:
        raise RuntimeError("HTTP session is not initialized")

    async with _SESSION.get(url, timeout=REQUEST_TIMEOUT, headers={"User-Agent": "Mozilla/5.0"}) as response:
        html = await response.text()
    return extract_title(html)


async def parse_and_save(url: str) -> None:
    title = await fetch_title_async(url)
    save_result(url, title, "asyncio")
    print(f"[asyncio] {url} -> {title}")


async def worker(urls: list[str]) -> None:
    for url in urls:
        await parse_and_save(url)


async def run_async() -> float:
    global _SESSION

    init_database()
    chunks = split_into_chunks(URLS, WORKER_COUNT)
    started_at = time.perf_counter()

    timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        _SESSION = session
        tasks = [worker(chunk) for chunk in chunks]
        await asyncio.gather(*tasks)
        _SESSION = None

    return time.perf_counter() - started_at


def main() -> None:
    elapsed = asyncio.run(run_async())
    print(f"Asyncio completed in {elapsed:.6f} seconds")


if __name__ == "__main__":
    main()

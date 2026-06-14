from __future__ import annotations

import asyncio

from async_parser import run_async
from multiprocessing_parser import run_multiprocessing
from threading_parser import run_threading


def main() -> None:
    threading_time = run_threading()
    multiprocessing_time = run_multiprocessing()
    asyncio_time = asyncio.run(run_async())

    print("Comparison:")
    print(f"Threading        -> time: {threading_time:.6f} seconds")
    print(f"Multiprocessing  -> time: {multiprocessing_time:.6f} seconds")
    print(f"Asyncio          -> time: {asyncio_time:.6f} seconds")


if __name__ == "__main__":
    main()
import asyncio


class AsyncWorkerPool:
    def __init__(self, concurrency=10):
        self.queue = asyncio.Queue()
        self.concurrency = concurrency

import multiprocessing
import threading
import asyncio
import time
import requests
from concurrent.futures import ThreadPoolExecutor


pool = ThreadPoolExecutor(multiprocessing.cpu_count()*10)

class StressTest:
    def run(self, thread_count=4, task_count=4, **kwargs):
        """
        :param thread_count: 执行并发任务的线程数
        :param task_count: 每个线程执行req请求的次数
        :return:
        """
        queue = asyncio.Queue(maxsize=thread_count*task_count)
        for _ in range(thread_count):
            p = threading.Thread(target=self._thread, args=(kwargs.get("api_url"),task_count, queue))
            p.start()

        while not queue.full():
            time.sleep(0.5)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._consumer(queue, thread_count*task_count))

    async def _consumer(self,queue,c):
        consumer = asyncio.ensure_future(self._consume(queue,c))
        await queue.join()
        consumer.cancel()

    @staticmethod
    async def _consume(queue,c):
        t = 0
        while not queue.empty():
            item = await queue.get()
            t += item
            queue.task_done()
        print(t/c)

    def _thread(self, url, task_count, queue):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._worker(url, loop, task_count, queue))

    async def _worker(self, url, loop, task_count, queue):
        tasks = [asyncio.ensure_future(self._req_one(url,loop,queue)) for _ in range(task_count)]
        result = await asyncio.gather(*tasks)
        return result

    @staticmethod
    async def _req_one(url, loop, queue):
        global pool
        start = time.time()
        await loop.run_in_executor(pool, requests.get, url)
        end = time.time()
        await queue.put((end-start))

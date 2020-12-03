import multiprocessing
import threading
import asyncio
import time
import requests
from concurrent.futures import ThreadPoolExecutor


class StressTest:
    def run(self, thread_count=10, task_count=100, **kwargs):
        """
        # ？TODO 其实不妨调个AB去做
        :param thread_count: 执行并发任务的线程数(建议为CPU核数)
        :param task_count: 每个线程执行req请求的次数
        :return:
        """
        self.pool = ThreadPoolExecutor(thread_count*task_count)  # 这个常量其实可以越大越好，反正都是IO密集，运行起来都是扔进池子wait。如果太小，反而会因为block耗时导致任务整体耗时变长
        queue = asyncio.Queue(maxsize=thread_count*task_count)
        for _ in range(thread_count):
            p = threading.Thread(target=self._thread, args=(kwargs.get("api_url"),task_count, queue))
            p.start()

        while not queue.full():
            time.sleep(0.1)

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
        s = requests.Session()
        tasks = [asyncio.ensure_future(self._req_one(url,loop,queue,s)) for _ in range(task_count)]
        result = await asyncio.gather(*tasks)
        return result

    async def _req_one(self, url, loop, queue,s):
        res = await loop.run_in_executor(self.pool, self._wrap_request, url,s)
        await queue.put(res)

    @staticmethod
    def _wrap_request(url, s):
        res = s.get(url)
        return res.elapsed.total_seconds()
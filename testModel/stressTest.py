import json
import threading
import asyncio
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from docOutput.textOutput import TextOutput
from utils.isNullCheck import is_null_check


class StressTest:
    def __init__(self, **kwargs):
        is_null_check(kwargs)
        self.api_url = kwargs.get("api_url")
        self.api_param = kwargs.get("api_param")
        self.api_methods = kwargs.get("api_methods")
        self.api_content_type = kwargs.get("api_content_type")
        self.docOutput = TextOutput(api_test_name="StressTest",**kwargs)

    def run(self, thread_count=4, task_count=10):
        """
        # 目前TPS值不太准确  更新：其实是准确的。服务处理多个user的请求时头几个是会比较慢。第一个接口的tps就是这么被拉下来的
        :param thread_count: 执行并发任务的线程数(建议为CPU核数)
        :param task_count: 每个线程执行req请求的次数
        :return:
        """
        self.pool = ThreadPoolExecutor(thread_count*task_count)  # 这个常量其实可以越大越好，反正都是IO密集，运行起来都是扔进池子wait。如果太小，反而会因为block耗时导致任务整体耗时变长
        queue = asyncio.Queue(maxsize=thread_count*task_count)
        for _ in range(thread_count):
            p = threading.Thread(target=self._thread, args=(task_count, queue))
            p.start()

        while not queue.full():
            time.sleep(0.1)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._consumer(queue, thread_count*task_count))

    async def _consumer(self,queue,c):
        asyncio.ensure_future(self._consume(queue,c))
        await queue.join()

    async def _consume(self, queue,c):
        t = 0
        while not queue.empty():
            item = await queue.get()
            t += item
            queue.task_done()
        self.docOutput.out_put(TPS=c/t, oth=0)

    def _thread(self, task_count, queue):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._worker(loop, task_count, queue))

    async def _worker(self, loop, task_count, queue):
        s = requests.Session()
        tasks = [asyncio.ensure_future(self._req_one(loop,queue,s)) for _ in range(task_count)]
        result = await asyncio.gather(*tasks)
        return result

    async def _req_one(self, loop, queue,s):
        res = await loop.run_in_executor(self.pool, self._wrap_request, s)
        await queue.put(res)

    def _wrap_request(self, s):
        if self.api_methods == "GET":
            res = s.get(self.api_url)
        else:
            res = s.post(self.api_url, data=json.dumps(self.api_param), headers={"Content-Type":self.api_content_type})
        return res.elapsed.total_seconds()
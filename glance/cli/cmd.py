import asyncio
import multiprocessing
import PIL
import signal
from glance.ocr import scan
from glance.util import output
from glance.util import paths


async def run_with_args(args):
    async def worker():
        while True:
            j = await tasks.get()

            try:
                await results.put((j, await loop.run_in_executor(None, scan.scan, j, args)))
            except Exception as e:
                await results.put((j, e))
            finally:
                tasks.task_done()

    async def displayer():
        while True:
            r = await results.get()

            try:
                if isinstance(r[1], Exception):
                    if isinstance(r[1], PIL.UnidentifiedImageError):
                        output.note("{0} is not an image".format(r[0]))
                    elif isinstance(r[1], OSError):
                        output.warn("{0} could not be opened".format(r[0]))
                    else:
                        raise r[1]
                else:
                    output.text(str(r[0]), r[1])
            finally:
                results.task_done()

    async def assigner():
        for path in paths.process(args.image, args):
            await tasks.put(path)

        await tasks.join()
        worker_pool.cancel()

        await results.join()
        displayer_task.cancel()

    if not args.jobs:
        pool_size = max(multiprocessing.cpu_count(), 2)
    else:
        pool_size = args.jobs

    loop = asyncio.get_event_loop()

    tasks = asyncio.Queue(pool_size)
    worker_pool = asyncio.gather(*list(asyncio.create_task(worker()) for _ in range(pool_size)))

    results = asyncio.Queue(pool_size)
    displayer_task = asyncio.create_task(displayer())

    task = asyncio.gather(assigner(), displayer_task, worker_pool)
    loop.add_signal_handler(signal.SIGINT, lambda: task.cancel())

    try:
        await task
    except asyncio.CancelledError:
        pass

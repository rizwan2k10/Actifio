#!/usr/bin/env python

# Author: rizwan
# Created: 7/3/18,12:31 PM
# filename: asyncio_stream

import sys
import logging
from logging import handlers as log_handle
import uuid
from threading import Thread
import asyncio
import requests
from tenacity import retry, retry_if_exception_type, stop_after_delay, wait_fixed

logger = None
log_file_name = '/tmp/dummmy_1'


IS_PY2 = sys.version_info < (3, 0)

if IS_PY2:
    from Queue import Queue
else:
    from queue import Queue


def setup_log():
    global logger
    logger = logging.getLogger(__file__)
    log_format = "%(asctime)s [%(levelname)s] (%(threadName)-5s) %(message)s"
    handler = log_handle.RotatingFileHandler(log_file_name, mode='a', maxBytes=83886080,
                                             backupCount=1, encoding=None, delay=0)
    handler.setFormatter(logging.Formatter(log_format))
    log_stream = logging.StreamHandler()
    log_stream.setFormatter(logging.Formatter(log_format))
    logger.addHandler(log_stream)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


async def _read_stream(stream, cb):
    while True:
        line = await stream.readline()
        if line:
            cb(line)
        else:
            break


async def _stream_subprocess(cmd, stdout_cb, stderr_cb):
    process = await asyncio.create_subprocess_exec(*cmd,
                                                   stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    await asyncio.wait([
        _read_stream(process.stdout, stdout_cb),
        _read_stream(process.stderr, stderr_cb)
    ])
    return await process.wait()


def execute(cmd, stdout_cb, stderr_cb):
    loop = asyncio.get_event_loop()
    rc = loop.run_until_complete(
        _stream_subprocess(
            cmd,
            stdout_cb,
            stderr_cb,
        ))
    loop.close()
    return rc


@retry(retry=retry_if_exception_type(RuntimeError), stop=stop_after_delay(60), wait=wait_fixed(0.5))
async def update_db(session_id, message):
    url_base = 'http://localhost:8000/update_log'
    param = {}
    param['message'] = message
    param['sessionid'] = session_id
    resp = requests.get(url_base, params=param)
    if resp.status_code != '200':
        raise RuntimeError
    return message


def process(cmd, session_id, user):

    rc = execute(
        cmd,
        lambda x: logger.info("STDOUT: %s" % update_db(session_id, x.strip().decode('utf-8'))),
        lambda x: logger.info("STDERR: %s" % update_db(session_id, x.strip().decode('utf-8'))),
    )
    update_db(session_id, "exit_code: " + str(rc))


class Worker(Thread):
    """ Thread executing tasks from a given tasks queue """
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                # An exception happened in this thread
                logger.error(e)
            finally:
                # Mark this task as done, whether an exception happened or not
                self.tasks.task_done()

    def stop(self):
        self.stop()


class ThreadPool:
    def __init__(self, num_threads):
        logger.debug(f"Initializing Threadpool with threads {num_threads}")
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """ Add a task to the queue """
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
        """ Add a list of tasks to the queue """
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        """ Wait for completion of all the tasks in the queue """
        self.tasks.join()

    # def kill_thread(self, ):
    #     self.tasks


if __name__ == '__main__':
    setup_log()
    pool = ThreadPool(5)
    session_id = 12345
    # Add the jobs in bulk to the thread pool. Alternatively you could use
    # `pool.add_task` to add single jobs. The code will block here, which
    # makes it possible to cancel the thread pool with an exception when
    # the currently running batch of workers is finished.
    pool.map()

    pool.wait_completion()
    # rc = execute(
    #     ["bash", "./test_run.sh"],
    #     lambda x: logger.info("STDOUT: %s" % x.strip().decode('utf-8')),
    #     lambda x: logger.info("STDERR: %s" % x.strip().decode('utf-8')),
    # )
    # logger.info("exit code: %s" % rc)

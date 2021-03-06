from __future__ import (
    absolute_import,
    unicode_literals,
)

import asyncio
import logging
import threading


class AsyncEventLoopThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.loop = asyncio.new_event_loop()
        self._done = threading.Event()
        self._logger = logging.getLogger('pysoa.async')

    def _loop_stop_callback(self):
        self._logger.info('Stopping async event loop thread')
        self.loop.stop()

    def run(self):
        self._logger.info('Starting async event loop thread')
        self._done.clear()
        asyncio.set_event_loop(self.loop)
        try:
            self._logger.info('Async event loop thread available and running')
            self.loop.run_forever()
        finally:
            try:
                pending_tasks = asyncio.Task.all_tasks(self.loop)
                if pending_tasks:
                    self._logger.info('Completing uncompleted async tasks')
                self.loop.run_until_complete(asyncio.gather(*pending_tasks))
            finally:
                self._logger.info('Closing async event loop')
                self.loop.close()
                asyncio.set_event_loop(None)
                self._done.set()

    def join(self, timeout=None):
        if self.loop.is_running():
            self._logger.info('Scheduling async event loop thread shutdown')
            self.loop.call_soon_threadsafe(self._loop_stop_callback)
            self._done.wait()
        else:
            self._logger.warning('Async event loop is already not running!')

        super().join(timeout)

    def run_coroutine(self, coroutine):
        return asyncio.run_coroutine_threadsafe(coroutine, self.loop)

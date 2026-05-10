from queue import Queue


class DownloadScheduler:
    def __init__(self):
        self.queue = Queue()

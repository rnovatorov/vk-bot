from threading import Thread


class Worker(Thread):

    def __init__(self, queue, func, **kwargs):
        super(Worker, self).__init__(**kwargs)
        self.queue = queue
        self.func = func


class Producer(Worker):

    def run(self):
        while True:
            for task in self.func():
                self.queue.put(task)


class Consumer(Worker):

    def run(self):
        while True:
            task = self.queue.get()
            if task is not None:
                self.func(task)
                self.queue.task_done()

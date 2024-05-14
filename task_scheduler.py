import time

class TaskScheduler:
    """
    Task Scheduler class to manage and execute tasks at specific intervals.
    """
    tasks = []
    last_ms = 0

    @classmethod
    def register(cls, task):
        """
        Register a new task to the scheduler.
        """
        cls.tasks.append(task)

    @classmethod
    def start(cls):
        """
        Start the scheduler to run registered tasks.
        """
        while True:
            current_ms = time.ticks_ms()
            if current_ms != cls.last_ms: # at least 1ms has elapsed
                cls.last_ms = current_ms
                for task in cls.tasks:
                    task.current_interval -= 1
                    if task.current_interval == 0:
                        task.current_interval = task.interval
                        task.loop()

class Task:
    """
    Base class for all tasks.
    """
    def __init__(self, interval=150): #ms
        self.interval = interval  # task execution interval
        self.current_interval = interval # ms

    def loop(self):
        """
        Method to be overridden by subclasses.
        """
        pass
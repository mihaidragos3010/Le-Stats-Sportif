from queue import Queue
from threading import Thread, Event, Semaphore, Lock
from app.tasks import Task
import os
import logging

# The implementation of a thread pool for tasks.
class ThreadPool:
    def __init__(self):
    
        self.nr_threads = self.get_num_of_threads()
        self.lock_task_queue = Lock()
        self.task_queue = Queue()
        self.isWorkingTime = Event()
        self.isWorkingTime.set()
        self.isTimeToStop = Event()
        self.isWorkingTime.clear()
        self.lock_running_tasks = Lock()
        self.running_tasks = set()
        
        self.threads = [TaskRunner(id, self.task_queue, self.lock_task_queue, self.running_tasks, 
                                   self.lock_running_tasks, self.isWorkingTime, self.isTimeToStop) 
                                   for id in range(self.nr_threads)]

    # The function sets the number of threads to be run based on the system's environment or architecture.
    def get_num_of_threads(self):
        num_of_threads = os.getenv('TP_NUM_OF_THREADS')
        if num_of_threads is not None:
            return int(num_of_threads)
        else:
            return os.cpu_count()
        
    # The function adds a task to be executed.
    def add(self, task: Task):
        self.task_queue.put(task)
        self.isWorkingTime.set()

        with self.lock_running_tasks:
            self.running_tasks.add(task.job_id)

    # The function activates the thread pool and all threads.
    def start(self):
        for thread in self.threads:
            thread.start()

    # The function notifies all threads to stop and waits for them to cease execution.
    def graceful_shutdown(self):
        self.isTimeToStop.set()
        self.isWorkingTime.set() 

        for thread in self.threads:
            thread.join()


    def deleteAllResultFiles(self, dir_path: str):
        try:
            if os.path.exists(dir_path):
                files = os.listdir(dir_path)
                for file_name in files:
                    file_path = os.path.join(dir_path, file_name)
                    os.remove(file_path)   

        except OSError as e:
            print(f"Error: {e}")

        finally:
            os.makedirs(dir_path, exist_ok=True)

    def isTaskDone(self, task_id: int):

        with self.lock_running_tasks:
            if task_id in self.running_tasks:
                return False
            else:
                return True


        


# The implementation of a thread.
class TaskRunner(Thread):
    def __init__(self, id: int, task_queue: list, lock_task_queue: Lock, running_tasks: set, lock_running_tasks: Lock, startEvent: Event, stopEvent: Event):

        Thread.__init__(self)
        self.id = id
        self.task_queue = task_queue
        self.lock_task_queue = lock_task_queue
        self.running_tasks = running_tasks
        self.lock_running_tasks = lock_running_tasks
        self.isWorkingTime = startEvent
        self.isTimeToStop = stopEvent

    # Each thread will run until it receives a notification from the thread pool and as long as there are tasks in the queue.
    def run(self):
        while True:

            if self.isTimeToStop.is_set() and self.task_queue.empty():
                break

            self.isWorkingTime.wait()

            with self.lock_task_queue:
                if not self.task_queue.empty():
                    task = self.task_queue.get(block=False)
                else:
                    task = None
                    self.isWorkingTime.clear()
            
            if task:
                task.execute()
                task.save_to_file()
                with self.lock_running_tasks:
                    self.running_tasks.remove(task.job_id)


                

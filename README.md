Nume: Mihai Dragos-Andrei

Grupă: 332CB

# Homework 1 ASC
      
  In implementing this college project, I had to implement a Thread pool within a backend server. When the server starts, threads are activated based on the machine on which the program is running. Using the Flask library, it listens for requests to interact with the server via REST API. A request is analyzed and, if it involves processing calculations, it will be added to the thread pool. Here, each thread is started and will process all tasks in the queue. After the server has been shut down, it will return an error message for future task requests.


# Implementation

  - __init__.py: Within this file, I initialize: a Thread pool, a Data Ingestor, a job counter, a Logging class, and the "isWorkingTime" variable. The Thread pool is started and activates a number of threads based on the environment variable "TP_NUM_OF_THREADS" or the number of system threads. The Data Ingestor is a class that reads the file "nutrition_activity_obesity_usa_subset.csv" with all the statistics and saves it in memory. The Logging class is used to initialize a logger that saves the program's traversal history based on a global date. This information is saved in a directory named "logger" in files with the name "webserver.log{index}". The "job_counter" variable counts the number of processed jobs. The "isWorkTime" variable indicates that the server has not been put into a shutdown state.

  - data_ingestor.py: Within this file, I save a data structure based on the statistics from "nutrition_activity_obesity_usa_subset.csv". The structure is represented by a list of dictionaries.

       ex:  [{"YearStart": 2017, "YearEnd": 2017, "LocationAbbr": "OH", "LocationDesc": "Ohio", ...}, ....]

  - loggin.py: Within this file, I have implemented a class that abstracts the implementation of a logger responsible for saving the program's purge history in a series of files within the "logger" directory named "webserver.log.{index}". This logger displays the time based on the global time zone. It checks if the file exists, creates it if it doesn't, and deletes all existing files from a previous session.
     
       ex: 2024-04-04 11:22:48 - website logger - INFO - A request has been posted to /api/mean_by_category

  - routes.py: Within this file, I have implemented the part responsible for listening to requests through a REST API.

  - task_runner.py: Within this file, I have implemented two classes: ThreadPool and TaskRunner. ThreadPool is responsible for starting threads, stopping threads, adding tasks to the queue, and providing responses for the completion of each task. TaskRunner is responsible for processing the data and saving the results in specific files. The synchronization part is implemented through:
     
      - "isWorkingTime" event informs the threads if there is a task in the queue. When the queue is empty, this event is set to false, and all threads will wait until a new task arrives.
     
      - "isTimeToStop" event informs the threads to execute all existing tasks in the queue and then shut down permanently.
     
      - "lock_task_queue" and "task_queue" are used to synchronize the threads during the addition and extraction of tasks from the queue.
     
      - "lock_running_tasks" and "running_tasks" Lock and Set of task IDs are used to track the state of the threads that are currently running. When a task is completed and its result is saved in a file, its ID is removed from the structure. This necessity arose when one thread writes the result file and the main thread tries to read from that file simultaneously.
    
  - tasks.py: In this file, I have implemented a Task class. This is a class that abstracts the dependencies and execution of each task individually. Child classes will specify the specific data required and the corresponding implementation.

# Tests

In this assignment, I received a checker from the university which I used. Additionally, I implemented three tests to cover all functionalities. The first test sends a GET request to shut down the server and sends a new request for "states_mean" to verify if an error message is received. The next two tests verify that the output from the "num_jobs" and "jobs" functions is consistent with the format required by the assignment.
During the testing process, I also used some scripts to send POST messages to the server at a specific URL.

# How to run

To prepare the environment, run the following commands:

      make create_venv
      source venv/bin/activate
      make install
      
To activate the server, run the command below and open the provided link in your browser:

      make run_server

To run the tests, execute one of the two commands:

      make run_tests
      make run_my_tests
     


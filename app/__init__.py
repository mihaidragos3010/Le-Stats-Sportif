from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from app.loggin import Loggin

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()

# A variable that sets the state of the server to accept or reject new tasks.
webserver.isWorkTime = True
webserver.path_dir_results = "./results"

# Create a directory named 'results jobs' and if it exists, delete all files within it.
webserver.tasks_runner.deleteAllResultFiles(webserver.path_dir_results)

# Create a Logger that presents information in a specific format and sets the date to the global date.
webserver.logger = Loggin("logger").get()

# The statistical data is read from the file.
webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

# The thread pool is started
webserver.tasks_runner.start()

# Index of the next job_id
webserver.job_counter = 1

from app import routes

Nume:
Grupă:

# Homework 1 ASC

   In implementing this college project, I had to implement a Thread pool within a backend server. When the server starts, threads are activated based on the machine on which the program is running. Using the Flask library, it listens for requests to interact with the server via REST API. A request is analyzed and, if it involves processing calculations, it will be added to the thread pool. Here, each thread is started and will process all tasks in the queue. After the server has been shut down, it will return an error message for future task requests.


# Implementation

  - __init__.py: Within this file, I initialize: a Thread pool, a Data Ingestor, a job counter, a Logging class, and the "isWorkingTime" event. The Thread pool is started and activates a number of threads based on the environment variable "TP_NUM_OF_THREADS" or the number of system threads. The Data Ingestor is a class that reads the file "nutrition_activity_obesity_usa_subset.csv" with all the statistics and saves it in memory. The Logging class is used to initialize a logger that saves the program's traversal history based on a global date. This information is saved in a directory named "logger" in files with the name "webserver.log{index}". The "job_counter" variable counts the number of processed jobs. The "isWorkTime" variable indicates that the server has not been put into a shutdown state.

  - data_ingestor.py: Within this file, I save a data structure based on the statistics from "nutrition_activity_obesity_usa_subset.csv". The structure is represented by a list of dictionaries in the form:
     [{"YearStart": 2017, "YearEnd": 2017, "LocationAbbr": "OH", "LocationDesc": "Ohio", ...}, ....]

Resurse utilizate
-

* Resurse utilizate - toate resursele publice de pe internet/cărți/code snippets, chiar dacă sunt laboratoare de ASC

Git
-
1. Link către repo-ul de git

Ce să **NU**
-
* Detalii de implementare despre fiecare funcție/fișier în parte
* Fraze lungi care să ocolească subiectul în cauză
* Răspunsuri și idei neargumentate
* Comentarii (din cod) și *TODO*-uri

Acest model de README a fost adaptat după [exemplul de README de la SO](https://github.com/systems-cs-pub-ro/so/blob/master/assignments/README.example.md).

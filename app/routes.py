import os
import json
import logging
from app.tasks import *
from app import webserver
from flask import request, jsonify

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405


# The POST method that stops the thread pool and prevents the server from accepting new tasks.
@webserver.route('/api/graceful_shutdown', methods=['GET'])
def get_graceful_shutdown():

    webserver.isWorkTime = False
    webserver.tasks_runner.graceful_shutdown()
    webserver.logger.info("Server is getting down")

    return jsonify({"status": "done"})


# A function that displays the number of running tasks.
@webserver.route('/api/num_jobs', methods=['GET'])
def get_num_jobs():

    try:
        files = os.listdir("results/")
        nr_result_files = len(files)
        return jsonify({"nr taks": webserver.job_counter - nr_result_files - 1})
    
    except FileNotFoundError:
        webserver.logger.error("Director 'results' not found!")
    except PermissionError:
        webserver.logger.error("Don't have permisions on 'results' directory!")
    except Exception as e:
        webserver.logger.error(e.args)


# A function that displays statistics for all tasks that are done and those that are running.
@webserver.route('/api/jobs', methods=['GET'])
def get_jobs():

    path_dir = webserver.path_dir_results
    data = []

    for i in range(1, webserver.job_counter):
        file_path = path_dir + '/' + f"result{i}.txt"
        if os.path.exists(file_path):
            data.append({f"job_id_{i}": "done"})
        else:
            data.append({f"job_id_{i}": "running"})

    return jsonify({"status": "done", "data": data})


# A function that displays the statistics of a task and waits until it finishes.
@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    print(f"JobID is {job_id}")

    job_id = int(job_id)
    if job_id <= 0 or job_id >= webserver.job_counter:
        return jsonify({"status": "error", "reason": "Invalid job_id"})
    
    tasks_runner = webserver.tasks_runner
    try:
        if tasks_runner.isTaskDone(job_id):
            with open(f"results/result{job_id}.txt", "r") as file:
                data = file.read()
                dir_data = json.loads(data)
                return jsonify({"status": "done", "data": dir_data})
        else:
            return jsonify({"status": "running"})

    except FileNotFoundError:
        return jsonify({"status": "running"})
    
    finally:
        logging.info("Finish '/api/get_results/<job_id>' request!")


@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():

    if not webserver.isWorkTime:
        return jsonify({"status": "error", "reason": "Server is down"})
    
    job_id = webserver.job_counter
    data = request.json
    data_ingestor = webserver.data_ingestor

    task = TaskStatesMean(job_id, data, data_ingestor)
    webserver.tasks_runner.add(task)

    webserver.job_counter += 1
    webserver.logger.info("A request has been posted to /api/states_mean")

    return jsonify({"job_id": job_id})


@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    
    if not webserver.isWorkTime:
        return jsonify({"status": "error", "reason": "Server is down"})
    
    job_id = webserver.job_counter
    data = request.json
    data_ingestor = webserver.data_ingestor

    task = TaskOneStateMean(job_id, data, data_ingestor)
    webserver.tasks_runner.add(task)

    webserver.job_counter += 1
    webserver.logger.info("A request has been posted to /api/state_mean")

    return jsonify({"job_id": job_id})


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    
    if not webserver.isWorkTime:
        return jsonify({"status": "error", "reason": "Server is down"})
    
    job_id = webserver.job_counter
    data = request.json
    data_ingestor = webserver.data_ingestor

    task = TaskBestFive(job_id, data, data_ingestor)
    webserver.tasks_runner.add(task)

    webserver.job_counter += 1
    webserver.logger.info("A request has been posted to /api/best5")

    return jsonify({"job_id": job_id})


@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():

    if not webserver.isWorkTime:
        return jsonify({"status": "error", "reason": "Server is down"})
    
    job_id = webserver.job_counter
    data = request.json
    data_ingestor = webserver.data_ingestor

    task = TaskWorstFive(job_id, data, data_ingestor)
    webserver.tasks_runner.add(task)

    webserver.job_counter += 1
    webserver.logger.info("A request has been posted to /api/worst5")

    return jsonify({"job_id": job_id})


@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():

    if not webserver.isWorkTime:
        return jsonify({"status": "error", "reason": "Server is down"})
    
    job_id = webserver.job_counter
    data = request.json
    data_ingestor = webserver.data_ingestor

    task = TaskGlobalMean(job_id, data, data_ingestor)
    webserver.tasks_runner.add(task)

    webserver.job_counter += 1
    webserver.logger.info("A request has been posted to /api/global_mean")

    return jsonify({"job_id": job_id})


@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():

    if not webserver.isWorkTime:
        return jsonify({"status": "error", "reason": "Server is down"})
    
    job_id = webserver.job_counter
    data = request.json
    data_ingestor = webserver.data_ingestor

    task = TaskDiffFromMean(job_id, data, data_ingestor)
    webserver.tasks_runner.add(task)

    webserver.job_counter += 1
    webserver.logger.info("A request has been posted to /api/diff_from_mean")

    return jsonify({"job_id": job_id})


@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():

    if not webserver.isWorkTime:
        return jsonify({"status": "error", "reason": "Server is down"})
    
    job_id = webserver.job_counter
    data = request.json
    data_ingestor = webserver.data_ingestor

    task = TaskStateDiffFromMean(job_id, data, data_ingestor)
    webserver.tasks_runner.add(task)

    webserver.job_counter += 1
    webserver.logger.info("A request has been posted to /api/state_diff_from_mean")

    return jsonify({"job_id": job_id})


@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
   
    if not webserver.isWorkTime:
        return jsonify({"status": "error", "reason": "Server is down"})
    
    job_id = webserver.job_counter
    data = request.json
    data_ingestor = webserver.data_ingestor

    task = TaskMeanByCategory(job_id, data, data_ingestor)
    webserver.tasks_runner.add(task)

    webserver.job_counter += 1
    webserver.logger.info("A request has been posted to /api/mean_by_category")

    return jsonify({"job_id": job_id})


@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
   
    if not webserver.isWorkTime:
        return jsonify({"status": "error", "reason": "Server is down"})
    
    job_id = webserver.job_counter
    data = request.json
    data_ingestor = webserver.data_ingestor

    task = TaskStateMeanByCategory(job_id, data, data_ingestor)
    webserver.tasks_runner.add(task)

    webserver.job_counter += 1
    webserver.logger.info("A request has been posted to /api/state_mean_by_category")

    return jsonify({"job_id": job_id})


# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg


def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes

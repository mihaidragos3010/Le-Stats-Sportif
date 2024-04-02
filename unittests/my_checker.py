import json
import unittest
import requests

class ServerInteraction(unittest.TestCase):

    # Set main website url for all tests
    def setUp(self):
        self.url = "http://127.0.0.1:5000"


    # The function tests the server shutdown function.
    def test_shutdown(self):

        shutdown_url = self.url + "/api/graceful_shutdown"
        response_1 = requests.get(shutdown_url)

        states_mean_url = self.url + "/api/states_mean"
        question = '{"question": "Percent of adults aged 18 years and older who have an overweight classification"}'
        response_2 = requests.post(states_mean_url, question)

        self.assertEqual(response_1.text, '{"status":"done"}\n')
        self.assertEqual(response_2.text, '{"reason":"Server is down","status":"error"}\n')


    # The function tests the functionality of displaying the remaining number of jobs to be executed.
    def test_num_jobs(self):

        num_jobs_url = self.url + "/api/num_jobs"
        response = requests.get(num_jobs_url)

        self.assertRegex(response.text, r'{"nr taks":\d+}\n')


    # The function tests if the job states are displayed in a correct format.
    def test_jobs(self):

        num_jobs_url = self.url + "/api/jobs"
        response = requests.get(num_jobs_url)

        self.assertRegex(response.text, r'{"data":\s*\[(?:{"job_id_\d+":\s*"done"},?\s*)*|(?:{"job_id_\d+":\s*"running"},?\s*)*],\s*"status":\s*"done"\s*}\n')



if __name__ == '__main__':
    unittest.main()
#!/bin/bash

curl -X POST -H "Content-Type: application/json" -d '{"question": "Percent of adults who report consuming vegetables less than one time daily", "state": "Virgin Islands"}' http://127.0.0.1:5000/api/state_diff_from_mean

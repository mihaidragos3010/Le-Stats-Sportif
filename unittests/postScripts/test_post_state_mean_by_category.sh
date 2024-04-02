#!/bin/bash

curl -X POST -H "Content-Type: application/json" -d '{"question": "Percent of adults aged 18 years and older who have an overweight classification", "state": "Oklahoma"}' http://127.0.0.1:5000/api/state_mean_by_category

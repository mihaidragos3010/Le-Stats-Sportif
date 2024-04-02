#!/bin/bash

curl -X POST -H "Content-Type: application/json" -d '{"question": "Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)"}' http://127.0.0.1:5000/api/best5

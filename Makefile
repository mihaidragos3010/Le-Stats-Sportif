IS_VENV_ACTIVE=false
ifdef VIRTUAL_ENV
	IS_VENV_ACTIVE=true
endif

enforce_venv:
ifeq ($(IS_VENV_ACTIVE), false)
	$(error "You must activate your virtual environment. Exiting...")
endif

create_venv:
	python3 -m venv venv
	#source venv/bin/activate

install: enforce_venv requirements.txt
	python3 -m pip install -r requirements.txt

run_server: enforce_venv
	flask run

run_tests: enforce_venv
	python3 checker/checker.py

run_my_tests: enforce_venv
	python3 -m unittest unittests/my_checker.py

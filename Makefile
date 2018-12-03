SHELL := /bin/bash

.PHONY: setup
setup:
	stat venv/bin/activate &> /dev/null || \
	virtualenv venv -p python3
	source venv/bin/activate; \
	pip install -r requirements.txt

.PHONY: setup_ci
setup_ci:
	pip install -r requirements.txt
	pip install -r requirements_test.txt

.PHONY: install
install:
	sudo sed "s|{{DIR}}|$(dirname $(realpath ./Makefile))|g" \
		dingdongditchcamera.service \
		> /lib/systemd/system/dingdongditchcamera.service
	sudo chmod 644 /lib/systemd/system/dingdongditchcamera.service
	sudo systemctl daemon-reload
	sudo systemctl enable dingdongditchcamera.service
	sudo systemctl start dingdongditchcamera
	sudo systemctl status dingdongditchcamera

.PHONY: uninstall
uninstall:
	sudo systemctl stop dingdongditchcamera
	sudo systemctl disable dingdongditchcamera.service
	sudo rm /lib/systemd/system/dingdongditchcamera.service
	sudo systemctl daemon-reload

.PHONY: test
test:
	source venv/bin/activate; \
	PYTHONPATH=.:./tests/mocks py.test --cov=dingdongditchcamera --cov-branch tests

.PHONY: lint
lint:
	source venv/bin/activate; \
	flake8 dingdongditchcamera

.PHONY: run
run:
	source venv/bin/activate; \
	source env.sh; \
	python run.py

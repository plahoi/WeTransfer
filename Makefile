ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

deploy:
	python3 -m pip install --upgrade pip
	python3 -m pip install -r $(ROOT_DIR)/requirements.txt
	cat $(ROOT_DIR)/crontab | crontab


run:
	streamlit run $(ROOT_DIR)/index.py

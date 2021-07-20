# Hi
Here is an application available to fetch data from different sources to gather it and produce csv and line graph.

## Docker Web app
It is built with the use of Streamlit framework https://streamlit.io/. Streamlit allows building DE/DS application very fast. Long story short, to run it you need to load docker image and run it.

To run the application you should do the following:
1. Install docker
2. `docker pull plaha/wetransfer_anton_poliakov`
3. `docker run -d -v $(pwd)/:/tmp/ -p 8501:8501 plaha/wetransfer_anton_poliakov:latest`
4. Head to http://localhost:8501/ to view graph and data
5. Wait for a minute to get the `wetransfer_out.csv` file into the working dir you run commands from.
6. Drink a glass of water
7. Have a good day :) 



URL: http://localhost:8501/ will allow you to get the data from all sources and to view the graph. You can also get csv file clicking the link 'Download csv file'.


## Standalone crontab script
The way we can keep csv file updated daily - is to put the script `load_coin_csv.py` into crontab by hand on a remote host (EC2 on aws for example). To do so - you should do the following steps:
1. Head to your working host
2. `git clone https://github.com/plahoi/WeTransfer.git`
3. `make deploy` copies the schedule from crontab file in repository to your local crontab

Additionally `make run` Starts streamlit webapp on http://localhost:8501/ address


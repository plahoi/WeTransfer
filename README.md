# Hi
Here is an application available to fetch data from different sources to gather it and produce csv and line graph.

It does not work as I expected, so I created several methods of deployment to support all requirements.

## Web app.
This is built with the use of framework Streamlit. Streamlit allows building DE/DS application very fast. Long story short, to run it you need to load docker image and run it.

`docker pull plaha/wetransfer_anton_poliakov`</br>
`docker run -d -p 8501:8501 plaha/wetransfer_anton_poliakov:latest`

URL: http://localhost:8501/ will allow you to get the data from all sources and to view the graph. You can also get csv file clicking the link 'Download csv file'.


*I tried to use cron in docker. However, I did not succeed and I decided not to waste time on that.*

## Standalone crontab script
The way we can keep csv file updated daily - is to put the script `load_coin_csv.py` into crontab by hand on a remote host (EC2 on aws for example). To do so - you should do the following steps:
1. Head to your working host
2. `git init` in the working directory
3. `git clone https://github.com/plahoi/WeTransfer.git`
4. `make deploy` copies the schedule from crontab file in repository to your local crontab

Additionally `make run` Starts streamlit webapp on http://localhost:8501/ address


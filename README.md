# NetworkReliabilityChecker
Python scripts that I can run in a docker container on my NAS that pings a server regularly and logs ping/packet loss.

Reason for this project was diagnosing whether my internet instability is due to dropouts from new 5G router vs a horrible WiFi/powerline setup in my house.

## Setup
### DOCKER
#### Build
```docker build -t network-reliability-checker .```

#### Run
``` docker run -dp 127.0.0.1:8000:8000 network-reliability-checker```

### Using virtual environment
#### Install dependencies
```pip install -r requirements.txt```
### Run
Create sqlite database

```python src/setup_database.py```

Run the script to continually ping, store in database and clear out old data from database

```python src/runner.py```

The ping operation needs administrator privileges to run and if you're running this in a virtual environment, you won't be able to run the commands with elevated privilege. We can, however, give Python elevated permissions to use RAW and PACKET sockets (allowing ping to function as normal) using the following command:

```sudo setcap cap_net_raw+ep $(readlink -f $(which python))```

Setup localhost server to view results in browser (to be run in separate shell to runner)

```python src/server.py```

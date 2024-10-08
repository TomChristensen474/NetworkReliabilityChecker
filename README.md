# NetworkReliabilityChecker
Python scripts that I can run in a docker container on my NAS that pings a server regularly and logs ping/packet loss.

Reason for this project was diagnosing whether my internet instability is due to dropouts from new 5G modem vs a horrible WiFi/powerline setup in my house.

Result

![Screenshot](images/screenshot.png)
Key:
RED - >50% packet loss,

ORANGE - >25% packet loss,

BLUE - no packet loss,

If there is packet loss ping is fixed at 200ms.


## Setup
### Using Docker - recommended
#### Build
```bash
docker build -t network-reliability-checker .
```

#### Run
```bash
docker run -dp 127.0.0.1:8000:8000 network-reliability-checker
```

#### Open
Open in browser to your [localhost url](http://127.0.0.1:8000/) at port 8000


### Using virtual environment
#### Install dependencies
```bash
pip install -r requirements.txt
```
### Run
Create sqlite database

```bash
python src/setup_database.py
```

Run the script to continually ping, store in database and clear out old data from database

```bash
python src/runner.py
```

The ping operation needs administrator privileges to run and if you're running this in a virtual environment, you won't be able to run the commands with elevated privilege. We can, however, give Python elevated permissions to use RAW and PACKET sockets (allowing ping to function as normal) using the following command:

```bash
sudo setcap cap_net_raw+ep $(readlink -f $(which python))
```

# NetworkReliabilityChecker
Simple python script for raspberry pi (or any device) that pings a server regularly and logs ping/packet loss.

Reason for this project was diagnosing 'true' speed of new 5G router vs a horrible WiFi setup in my house.

## Setup
#### Install dependencies
```pip install -r requirements.txt```
### Run
Create sqlite database

```python setup_database.py```

Run the script to continually ping, store in database and clear out old data from database

```python runner.py```

Setup localhost server to view results in browser (to be run in separate shell to runner)

```python server.py```

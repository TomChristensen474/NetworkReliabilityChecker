from pythonping import ping
from sqlite3 import Connection, Error
from time import localtime, strftime

# from datetime import datetime

import db_connector


def do_ping():
    try:
        return ping("8.8.8.8", interval=1, verbose=False)  # one ping every second
    except Exception as e:
        return False


def ping_and_record():
    connection = db_connector.create_connection("network_history.db")

    # ping_result = ""
    if connection:
        cursor = connection.cursor()

        ping_result = do_ping()
        datetime = strftime("%F %T", localtime())
        # datetime = datetime.now()
        print(datetime)

        if ping_result:
            print("Average ping time (ms): " + str(ping_result.rtt_avg_ms))
            print("Packet loss: " + str(ping_result.packet_loss))
            data = (datetime, ping_result.rtt_avg_ms, ping_result.packet_loss, False)
        else:
            print("Network down")
            data = (datetime, None, 1, True)

        cursor.execute("INSERT INTO network_history VALUES(NULL, ?, ?, ?, ?)", data)
        connection.commit()

        connection.close()


ping_and_record()

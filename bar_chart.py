import numpy as np
import pandas as pd
import sqlite3

from sqlite3 import Connection, Error

from bokeh.io import curdoc
from bokeh.models import DatetimeTickFormatter, ColumnDataSource
from bokeh.palettes import Bright6
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap

# from time import strptime
from datetime import datetime

def create_connection(path) -> Connection|None: 
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

connection = create_connection("networy_history.db")

# ping_result = ""
if connection:
    cursor = connection.cursor()

    result = cursor.execute("SELECT * FROM network_history ORDER BY id DESC LIMIT 20")
    
    # result = [(time, average_ping, packet_loss), ...]
    result = result.fetchall()
    # print(result)
    # df = pd.DataFrame(result,
    #                   columns=['id', 'time', 'average_ping', 'packet_loss', 'network_down'])
    # df.time = [(np.datetime64(datetime.strptime(i[1], "%d %b %Y %H:%M:%S"))) for i in result]
    # src = ColumnDataSource(df)
    # print(src)
    # source = ColumnDataSource([{
    #     'time': (np.datetime64(datetime.strptime(i[1], "%d %b %Y %H:%M:%S"))),
    #     'average_ping': i[2],
    #     'packet_loss': i[3],
    #     'network_down': i[4]}
    #     for i in result]
    # )

    # x = [i[1] for i in result]
    y = [i[2] for i in result]
    # print(y)
    datetimes = [(np.datetime64(datetime.strptime(i[1], "%d %b %Y %H:%M:%S"))) for i in result]
    # colour = [i[4] for i in result]
    # print(datetimes)
    # print(df.average_pint.to_list())

curdoc().theme = "dark_minimal"


p = figure(title="Network Status", sizing_mode="stretch_width", x_axis_type="datetime")

# p.vbar(x="time", top="time", width=0.1, legend_label="Packet loss", bottom=0,
#     fill_color=factor_cmap("network_down", factors=['false', 'true'], palette=["red", "green"]))
p.vbar(x=datetimes, top=y, width=0.1, legend_label="Packet loss", bottom=0)

p.toolbar_location = None # type: ignore
p.xaxis.formatter = DatetimeTickFormatter(hourmin="%H:%M", days="%d %b %Y")
p.yaxis.axis_label = "Average Ping (ms)"
p.xaxis.axis_label = "Time"

show(p)
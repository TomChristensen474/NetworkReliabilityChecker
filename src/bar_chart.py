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

def render_data():
    def create_connection(path) -> Connection|None: 
        connection = None
        try:
            connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        return connection

    ### converts packet loss to color for bar chart
    def packet_loss_to_color(packet_loss: float) -> str:
        if packet_loss < 0.25:
            return "#26AAE1"
        elif packet_loss < 0.5:
            return "orange"
        else:
            return "red"

    connection = create_connection("src/network_history.db")

    # ping_result = ""
    if connection:
        cursor = connection.cursor()

        result = cursor.execute("SELECT * FROM network_history WHERE `datetime` >= datetime('now', '-1 hour') AND network_down = 0 ORDER BY id")

        # result = [(time, average_ping, packet_loss), ...]
        result = result.fetchall()

        ping_no_loss = [i[2] for i in result]
        datetimes_no_loss = [np.datetime64(i[1]) for i in result]
        color = [packet_loss_to_color(i[3]) for i in result]

        # result = cursor.execute("SELECT * FROM network_history WHERE `datetime` >= datetime('now', '-1 hour') AND packet_loss >= 0.25 ORDER BY id")
        # result = result.fetchall()
        # ping_loss = [i[2] for i in result]
        # datetimes_loss = [np.datetime64(i[1]) for i in result]


    curdoc().theme = "dark_minimal"


    p = figure(title="Network Status", sizing_mode="stretch_width", x_axis_type="datetime")

    # p.vbar(x="time", top="time", width=0.1, legend_label="Packet loss", bottom=0,
    #     fill_color=factor_cmap("network_down", factors=['false', 'true'], palette=["red", "green"]))
    p.vbar(x=datetimes_no_loss, top=ping_no_loss, width=0.1, bottom=0, color=color)
    # p.vbar(x=datetimes_loss, top=ping_loss, width=0.1, legend_label="Packet loss", bottom=0, color="red")

    p.toolbar_location = None # type: ignore
    p.xaxis.formatter = DatetimeTickFormatter(hourmin="%H:%M", days="%d %b %Y")
    p.yaxis.axis_label = "Average Ping (ms)"
    p.xaxis.axis_label = "Time"

    show(p)

    print("Rendered bar_chart")

render_data()
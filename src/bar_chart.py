import numpy as np
import pandas as pd
import dataclasses

from bokeh.io import curdoc
from bokeh.models import DatetimeTickFormatter, ColumnDataSource
from bokeh.palettes import Bright6
from bokeh.plotting import figure, show, save
from bokeh.transform import factor_cmap
from datetime import datetime
from dataclasses import dataclass

import db_connector

@dataclass
class PingResult:
    ping: float
    datetime: np.datetime64
    packet_loss: float
    network_down: int

    def __post_init__(self):
        for (name, field_type) in self.__annotations__.items():
            if not isinstance(self.__dict__[name], field_type):
                current_type = type(self.__dict__[name])
                raise TypeError(f"The field `{name}` was assigned by `{current_type}` instead of `{field_type}`")

def packet_loss_to_color(packet_loss: float) -> str:
    if packet_loss < 0.25:
        return "#26AAE1"
    elif packet_loss < 0.5:
        return "orange"
    else:
        return "red"

def get_data_from_DB(timeframe_hours: int, connection):
    if connection:
        cursor = connection.cursor()

        result = cursor.execute("SELECT * FROM network_history WHERE `datetime` >= datetime('now', '-1 hour') AND network_down = 0 ORDER BY id")
        # result = [(time, average_ping, packet_loss), ...]
        result = result.fetchall()

        ping_results = []
        for i in result:
            ping_results.append(PingResult(
                ping=i[2],
                datetime=np.datetime64(i[1]),
                packet_loss=i[3],
                network_down=i[4]
            ))
    return ping_results

def render_data(data):
    curdoc().theme = "dark_minimal"

    p = figure(title="Network Status", sizing_mode="stretch_width", x_axis_type="datetime")

    ping_no_loss = []
    datetimes_no_loss = []
    color = []
    for i in data:
        if i.packet_loss == 0:
            ping_no_loss.append(i.ping)
            datetimes_no_loss.append(i.datetime)
            color.append(packet_loss_to_color(i.packet_loss))
        else:
            ping_no_loss.append(200) # placeholder to be able to show a bar when there is packet loss
            datetimes_no_loss.append(i.datetime)
            color.append(packet_loss_to_color(i.packet_loss))
    
    # p.vbar(x="time", top="time", width=0.1, legend_label="Packet loss", bottom=0,
    #     fill_color=factor_cmap("network_down", factors=['false', 'true'], palette=["red", "green"]))
    p.vbar(x=datetimes_no_loss, top=ping_no_loss, width=0.1, bottom=0, color=color)
    # p.vbar(x=datetimes_loss, top=ping_loss, width=0.1, legend_label="Packet loss", bottom=0, color="red")

    p.toolbar_location = None # type: ignore
    p.xaxis.formatter = DatetimeTickFormatter(hourmin="%H:%M", days="%d %b %Y")
    p.yaxis.axis_label = "Average Ping (ms)"
    p.xaxis.axis_label = "Time"

    save(p) # set to show(p) for debugging without server

    print("Rendered bar_chart")

def chart():
    connection = db_connector.create_connection("network_history.db")
    data = get_data_from_DB(1, connection)
    connection.close()

    render_data(data)
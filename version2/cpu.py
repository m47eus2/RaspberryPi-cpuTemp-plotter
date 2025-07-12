from bokeh.layouts import column
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, curdoc
import csv
import time
import pandas as pd

samples = 300
dataPath = "database.csv"

source = ColumnDataSource(data=dict(x=[], y=[]))

p=figure(title='CPU temp', x_axis_type="datetime")
p.line(x='x', y='y', source=source, color="red", line_width=2)
p.sizing_mode = "scale_width"
p.height=300

def update():
  data = pd.read_csv(dataPath)
  data = data.tail(samples)
  data['time'] = pd.to_datetime(data['time'])
  source.data = dict(x=data['time'], y=data['cpuTemp'])

curdoc().add_root(column(p, sizing_mode="scale_width"))
curdoc().add_periodic_callback(update, 1000)

#run with: bokeh serve cpu.py --port 5000 --allow-websocket-origin=192.168.x.x:5000
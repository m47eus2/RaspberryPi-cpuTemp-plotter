from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure, curdoc
import pandas as pd

dataPath = "database.csv"

sample_count = {'value':60}

source = ColumnDataSource(data=dict(x=[], y=[]))

p=figure(title='CPU temp', x_axis_type="datetime")
p.line(x='x', y='y', source=source, color="red", line_width=2)
p.sizing_mode = "scale_width"
p.height=300

select = Select(title='Zakres danych',value='60',
                options=[
                  ('60', '60 (1 min)'),
                  ('300', '300 (5 min)'),
                  ('600', '600 (10 min)'),
                  ('1800', '1.8k (30 min)')])

def updateSelect(attr, old, new):
  sample_count['value'] = int(new)

select.on_change('value', updateSelect)

def update():
  data = pd.read_csv(dataPath)
  data = data.tail(sample_count['value'])
  data['time'] = pd.to_datetime(data['time'])
  source.data = dict(x=data['time'], y=data['cpuTemp'])

curdoc().add_root(column(p, select, sizing_mode="scale_width"))
curdoc().add_periodic_callback(update, 1000)

#run with: bokeh serve cpu.py --port 5000 --allow-websocket-origin=192.168.x.x:5000
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure, curdoc
from datetime import datetime, timedelta
import pandas as pd

dataPath = "database.csv"

sample_count = {'value':60}

source = ColumnDataSource(data=dict(x=[], y=[]))

p=figure(title='CPU temp', x_axis_type="datetime", height=800)
p.line(x='x', y='y', source=source, color="red", line_width=2)
p.sizing_mode = "stretch_width"


select = Select(title='Zakres danych',value='60',
                options=[
                  ('60', '60 (1 min)'),
                  ('120', '120 (2min)'),
                  ('180', '180 (3min)'), 
                  ('300', '300 (5 min)'),
                  ('600', '600 (10 min)'),
                  ('1800', '1.8k (30 min)')])

def updateSelect(attr, old, new):
  sample_count['value'] = int(new)

select.on_change('value', updateSelect)

def update():
  data = pd.read_csv(dataPath)
  data['time'] = pd.to_datetime(data['time'], format="%Y-%m-%d %H:%M:%S")
  cuttof = datetime.now() - timedelta(seconds = sample_count['value'])
  data = data[data['time'] >= cuttof]
  source.data = dict(x=data['time'], y=data['cpuTemp'])

layout = column(p,select,sizing_mode='stretch_width')

curdoc().add_root(layout)
curdoc().add_periodic_callback(update, 1000)

#run with: bokeh serve cpu.py --port 5000 --allow-websocket-origin=192.168.x.x:5000
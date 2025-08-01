from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure, curdoc
from datetime import datetime, timedelta
import pandas as pd
from datetime import datetime

selectedTime = {'value':5}

source = ColumnDataSource(data=dict(x=[], y=[]))
p=figure(title='CPU temp', x_axis_type="datetime", height=800)
p.line(x='x', y='y', source=source, color="red", line_width=2)
p.sizing_mode = "stretch_width"


select = Select(title='Zakres danych',value='5',
                options=[
                  ('1', '1 min'),
                  ('2', '2 min'),
                  ('3', '3 min'),
                  ('5', '5 min'),
                  ('10', '10 min'),
                  ('20', '20 min'),
                  ('30', '30 min'),
                  ('60', '60 min'),
                  ('120', '2 h'),
                  ('240', '4 h'),
                  ('360', '6 h'),
                  ('480', '8 h'),
                  ('720', '12 h'),
                  ('1440', '24 h'),
                  ('2880', '48 h')])

def updateSelect(attr, old, new):
  selectedTime['value'] = int(new)

select.on_change('value', updateSelect)

def update():
  date = datetime.now().strftime("%Y-%m-%d")
  recentDataPATH = f"database/{date}-log.csv"
  agregatedDataPATH = "database/agrData.csv"

  recentData = pd.read_csv(recentDataPATH)
  agregatedData = pd.read_csv(agregatedDataPATH)
  data = pd.concat([agregatedData, recentData], ignore_index=True)
  #data = data.tail(86400)

  data['time'] = pd.to_datetime(data['time'], format="%Y-%m-%d %H:%M:%S")
  cuttof = datetime.now() - timedelta(minutes = selectedTime['value'])
  data = data[data['time'] >= cuttof]
  source.data = dict(x=data['time'], y=data['cpuTemp'])

layout = column(p,select,sizing_mode='stretch_width')

curdoc().add_root(layout)
curdoc().add_periodic_callback(update, 1000)

#run with: bokeh serve cpu.py --port 5000 --allow-websocket-origin=192.168.x.x:5000
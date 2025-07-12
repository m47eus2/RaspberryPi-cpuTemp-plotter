from bokeh.layouts import column
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, curdoc

source = ColumnDataSource(data=dict(x=[], y=[]))

p=figure(title='CPU temp')
p.line(x='x', y='y', source=source, color="red", line_width=2)
p.sizing_mode = "scale_width"
p.height=300

i = 0

def getCpuTemp():
  with open("/sys/class/thermal/thermal_zone0/temp") as file:
    temp = file.readline()
  return float(temp)/1000.0

def update():
  global i
  x=i
  y=getCpuTemp()
  source.stream(dict(x=[x], y=[y]), rollover=100)
  i += 1

curdoc().add_root(column(p, sizing_mode="scale_width"))
curdoc().add_periodic_callback(update, 500)
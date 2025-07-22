import csv
import time
import os
from datetime import datetime

def getTemp():
  with open('/sys/class/thermal/thermal_zone0/temp', mode='r') as file:
    temp = file.readline()
  return float(temp)/1000.0

def logTemp(now, temp):
  date = datetime.now().strftime("%Y-%m-%d")
  PATH = f"database/{date}-log.csv"
  fileExists = os.path.isfile(PATH)
  with open(PATH, mode='a', newline='') as file:
    writer = csv.writer(file)
    if not fileExists:
      writer.writerow(['time', 'cpuTemp'])
      print('First row created')
    writer.writerow([now, temp])
    print(f"Time logged -> {now},{temp}")

while True:
  temp = getTemp()
  now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  logTemp(now, temp)
  time.sleep(1)
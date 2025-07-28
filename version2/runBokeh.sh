#!/bin/bash
source ../venv/bin/activate
bokeh serve cpu.py --port 5000 --allow-websocket-origin=192.168.0.101:5000
#/bin/bash -c "exec nginx"

bokeh serve test.py --address 0.0.0.0 --port 5100 --allow-websocket-origin=sophia.stevencdang.com:5100 --allow-websocket-origin=sophia.stevencdang.com:4200
#bokeh serve test.py --address 0.0.0.0 --port 5100
#bokeh serve test.py --address 0.0.0.0 --port 5100 --allow-websocket-origin=127.0.0.1:5100

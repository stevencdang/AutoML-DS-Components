To test the server, you can run it using:

# Ensure to allow websockets from flask backend and angular frontend origins
bokeh serve test.py --address 0.0.0.0 --port 5100 --allow-websocket-origin=sophia.stevencdang.com:5100 --allow-websocket-origin=sophia.stevencdang.com:4200

import requests
import time

# Test Hello world for test service
r = requests.get('http://localhost:5000/test/Hello')
print(r.text)

# Ensure services are running
is_ready = False
count = 0
while not is_ready:
    r = requests.get('http://localhost:5000/test/isReady')
    print(r.text)
    print("count: %i" % count)
    # is_ready = r.text == "True"
    if count > 5:
        is_ready = True
    else:
        time.sleep(10)

    count = count + 1



import requests
import time

def test_connection():
    r = requests.get('http://localhost:5000/test/Hello')
    print(r.text)
    assert r.text == "Hello World"

def wait_ta3_ready():
    # Ensure services are running
    wait_ready = False
    count = 0
    while not wait_ready:
        r = requests.get('http://localhost:5000/test/isReady')
        print(r.text)
        print("count: %i" % count)
        is_ready = r.text == "True"
        if not is_ready:
            time.sleep(5)
        # Wait no longer than 5 minutes for all systems to be ready
        #if count > 60:
        if count > 1:
            wait_ready = True
        else:
            count = count + 1
    return is_ready

def test_is_ta3_ready():
    assert wait_ta3_ready()


def test_scanning_for_datasets():
    r = requests.get('http://localhost:5000/test/getDatasetList')
    assert r.text == "True"

def test_selecting_dataset():
    r = requests.get('http://localhost:5000/test/selectDataset')
    assert r.text == "True"

def test_get_default_problem():
    r = requests.get('http://localhost:5000/test/getDefaultProblem')
    assert r.text == "True"

def test_model_search_and_fit():
    r = requests.get('http://localhost:5000/test/modelSearch')
    assert r.text == "True"

def test_model_rank():
    r = requests.get('http://localhost:5000/test/modelRank')
    assert r.text == "True"

def test_model_export():
    r = requests.get('http://localhost:5000/test/modelExport')
    assert r.text == "True"



"""
Unit and functional tests for ElasticSearch PostProcessing Service
"""

import service
from webtest import TestApp as TApp  # Change alias so that pytest does not attempt to load this as a test case class
from werkzeug.debug import DebuggedApplication

debug_app = app = DebuggedApplication(service.app)
debug_app.catchall = False  # Now most exceptions are re-raised within bottle.
test_app = TApp(debug_app)


def test_service_initiated():
    """
    Assert root url returns a message showing the service is ready.
    """
    assert "ready" in service.index()


def test_no_data():
    """
    Assert correct error message is returned when no data is supplied to the unwind url.
    """
    response = test_app.post("/evaluate_goal", expect_errors=True)
    assert response.status == '400 Bad Request'
    assert "No data" in response.text


def test_valid_data():
    """
    Assert calculation returns valid results with valid input data.
    """

    with open('etc/test-attempts.json') as f:
        test_data = f.read()

    response = test_app.post("/evaluate_goal", params=test_data)
    assert response.status == '200 OK'
    assert len(response.json) == 1
    assert response.json[0]["error"]["code"] == 0
    assert response.json[0]["metGoal"] == True

def test_fewer_attempts():
    """
    Assert fewer (less than two) attempts result in met goal as false.
    """

    with open('etc/test-fewer-attempts.json') as f:
        test_data = f.read()

    response = test_app.post("/evaluate_goal", params=test_data)
    #print(response)
    assert response.status == '200 OK'
    assert len(response.json) == 1
    assert response.json[0]["error"]["code"] == 0
    assert response.json[0]["metGoal"] == False

def test_attempts_before_academicyear_start_are_ignored():
    """
    Assert attempts earlier than school academic year start are ignored.
    """

    with open('etc/test-attempts-before-academicyear-start.json') as f:
        test_data = f.read()

    response = test_app.post("/evaluate_goal", params=test_data)
    #print(response)
    assert response.status == '200 OK'
    assert len(response.json) == 1
    assert response.json[0]["error"]["code"] == 0
    assert response.json[0]["metGoal"] == False

def test_real_example():
    """
    Test a real example that was found to be failing and shouldn't be
    """

    with open('etc/real-example.json') as f:
        test_data = f.read()

    response = test_app.post("/evaluate_goal", params=test_data)
    #print(response)
    assert response.status == '200 OK'
    #assert len(response.json) == 1

    import json

    with open('/tmp/test.json', 'wb') as f:
        json.dump(response.json, f)
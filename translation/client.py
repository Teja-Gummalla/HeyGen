import requests

SERVER_URL = 'http://127.0.0.1:8080'

class StatusResponse:
    def __init__(self, status, retry_seconds=None, request_count=None):
        self.status = status
        self.retry_seconds = retry_seconds
        self.request_count = request_count

# we will have a backoff mechanism inspired wait time here
# based on the request count to suggest a wait time for the user
def get_suggested_backoff(request_count):
    if request_count < 3:
        return .25
    if request_count < 5:
        return .5
    if request_count < 7:
        return 1
    if request_count < 9:
        return 3
    return 5

def get_status(request_count=0):
    """
    Queries the translation server to fetch the status
    of the ongoing video translation
    Response(StatusResponse):
    - status: (string) one of the following status values: pending, error, completed
    - retry_seconds: (float) number of seconds to retry the request in, if status is pending
    - request_count: (int) the current request count, used to decided the suggested backoff
    """

    # if we have requested more than 20 times error out
    if request_count > 20:
        raise Exception("The processing is taking too long")

    status_url = SERVER_URL + '/status'
    try:
        response = requests.get(status_url).json()
        status = response['status']
    except Exception as e:
        raise ValueError('There was an error fetching the status: ' + str(e)) from e
    if status != 'pending':
        return StatusResponse(status)
    
    return StatusResponse(status, get_suggested_backoff(request_count), request_count+1)

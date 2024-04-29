import unittest
import time
from translation.client import get_status
from server.v1.status import app
import threading
from multiprocessing import Process, set_start_method

class TestCalculations(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_process = Process(target=app.run, kwargs={"port": 8080})
        self.app_process.start()
        time.sleep(2)

    def test_status(self):
        status = get_status()
        self.assertEqual(status.status, 'pending')
        self.assertEqual(status.retry_seconds, 0.25)
        self.assertEqual(status.request_count, 1)

        # first backoff
        retry_time = status.retry_seconds
        time.sleep(retry_time)

        # use the above returned request_count to pass into
        # the new request
        status = get_status(status.request_count)
        self.assertEqual(status.status, 'pending')
        self.assertEqual(status.retry_seconds, 0.25)
        self.assertEqual(status.request_count, 2)
        retry_time = status.retry_seconds
        time.sleep(retry_time)

        # send with request count 9
        status = get_status(9)
        # backoff should be 5 seconds and we should have status then
        self.assertEqual(status.status, 'pending')
        self.assertEqual(status.retry_seconds, 5)
        self.assertEqual(status.request_count, 10)
        retry_time = status.retry_seconds
        time.sleep(retry_time)

        status = get_status(status.request_count)
        self.assertIsNot(status.status, 'pending')
    
    def test_error_status(self):
        # request count > 20
        with self.assertRaises(Exception) as context:
            get_status(22)
        self.assertTrue('The processing is taking too long' in str(context.exception))

    def tearDown(self):
        self.app_process.terminate()
        self.app_process.join() 

if __name__ == '__main__':
    set_start_method("fork")
    unittest.main()
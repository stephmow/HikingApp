import server
import unittest

class route_tests(unittest.TestCase):

    def set_up(self):
        """Code to run before every test"""
        # Creating a test client similar to our server
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True


    def test_home(self):
        result = self.client.get('/')

        self.assertIn(b'Search for a hike', result.data)


    def test_login(self):
        result = self.client.post('/login', data={'user_email': 'stephaniemow@gmail.com', "user_password": "test"})

        self.assertIn(b'You are logged in', result.data)


if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()
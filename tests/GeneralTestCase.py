import unittest
import application

class GeneralTestCase(unittest.TestCase):
    def setUp(self):
        application.app.config['testing'] = True
        self.app = application.app.test_client()
        application.create_tables()

    def test_homepage(self):
        rv = self.app.get('/')
        self.assertTrue('Welcome to rayhaan.net.' in str(rv.data))

    def create_user(self, username, password):
        user = application.models.User()
        user.username = username
        user.set_password(password)
        application.db_session.add(user)
        return user

    def test_users(self):
        username = "test"
        password = "test"
        self.assertEqual(application.db_session.query(application.models.User).count(),
                         0, "Empty database does not have zero users!")
        new_user = self.create_user(username, password)
        self.assertTrue(new_user == application.db_session.query(application.models.User).first(),
                        "Could not add user to database.")
        login_correct = self.app.post('/login', data=dict(username="test", password="test"))
        self.assertTrue(login_correct.status_code, 302)

    def test_login_failure(self):
        login_incorrect = self.app.post('/login', data=dict(username="test", passowrd="wrongpassword"))
        self.assertTrue(login_incorrect.status_code, 403)

if __name__ == '__main__':
    unittest.main()

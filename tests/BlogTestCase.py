import application
import unittest
import json
__author__ = 'rayhaan'

class BlogTestCase(unittest.TestCase):

    def setUp(self):
        application.app.config['testing'] = True
        self.app = application.app.test_client()
        application.create_tables()

    def test_empty_blog_api(self):
        response = self.app.get('/api/blog')
        self.assertEqual(response.status_code, 200, "response code was " + str(response.status_code))
        json_data = json.loads(response.data.decode('utf-8'))
        self.assertEquals(json_data, dict(data=list()))

    def test_simple_blogpost_api(self):
        author = application.models.User()
        author.username = 'author'
        application.db_session.add(author)
        application.db_session.commit()
        self.assertTrue(author.id is not None)

        post = application.models.BlogPost("Title", author.id)
        application.db_session.add(post)

        response = self.app.get('/api/blog')
        json_data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_data['data'][0]['title'] == "Title")
        self.assertTrue(json_data['data'][0]['author']['username'] == "author")

if __name__ == '__main__':
    unittest.main()
import app

import unittest
import json

class ThisTestCase(unittest.TestCase):

    def test_get_all_director(self):
        '''Test Get All data Director'''
        client = app.connex_app.app.test_client()
        result = client.get('/api/director')
        # Make your assertions
        self.assertEqual(result.status_code, 200)

    def test_get_all_director_with_pagination(self):
        '''
            test Get all director with pagination current page = 80 and data per page = 25
            api : /api/director/{page}/{per_page}
        '''
        client = app.connex_app.app.test_client()
        result = client.get('/api/director/80/25')
        # Make your assertions
        self.assertEqual(result.status_code, 200,'page in director/page/per_page must not exceed max page or data in database')

    def test_get_one_director(self):
        '''
            test get one data director by director_id
            api: /api/director/{director_id}
        '''
        client = app.connex_app.app.test_client()
        result = client.get('/api/director/7111')
        # Make your assertions
        self.assertEqual(result.status_code, 200,'Director not found for Id inputted!')

    def test_create_director(self):
        '''
            test create data director
        '''
        client = app.connex_app.app.test_client()
        result = client.post('/api/director',json = {
                                                        "department": "man",
                                                        "gender": 0,
                                                        "name": "mandoo unit test",
                                                        "uid": 5})

        # Make your assertions
        self.assertEqual(result.status_code, 201,'Director failed to create! uid existed')
    
    def test_create_director_uid_existed(self):
        '''
            test create data director with existed uid
        '''
        client = app.connex_app.app.test_client()
        result = client.post('/api/director',json = {
                                                        "department": "man",
                                                        "gender": 0,
                                                        "name": "mandoo unit test",
                                                        "uid": 5})

        # Make your assertions
        self.assertEqual(result.status_code, 409,'Uid Not Exist, success created director')
        

if __name__ == '__main__':
    unittest.main()



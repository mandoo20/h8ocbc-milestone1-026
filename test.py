import app

import unittest
import director,movie

class ApiTestCase(unittest.TestCase):

    def test_get_all_director(self):
        '''Test Get All data Director'''
        client = app.connex_app.app.test_client()
        result = client.get('/api/director')
        # Make your assertions
        self.assertEqual(result.status_code, 200)

    def test_get_director_by_gender(self):
        '''
            Tesst Get director filtered by Gender
            /director/{gender}:
        '''
        client = app.connex_app.app.test_client()
        result = client.get('/api/director/gender/2')
        # Make your assertions
        self.assertEqual(result.status_code, 200,'gender input must exist')


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
        result = client.get('/api/director/7112')
        # Make your assertions
        self.assertEqual(result.status_code, 200,'Director not found for Id inputted!')

    # def test_create_director(self):
    #     '''
    #         test create data director
    #     '''
    #     client = app.connex_app.app.test_client()
    #     result = client.post('/api/director',json = {
    #                                                     "department": "man",
    #                                                     "gender": 0,
    #                                                     "name": "mandoo unit test",
    #                                                     "uid": 5})

    #     # Make your assertions
    #     self.assertEqual(result.status_code, 201,'if status code = 409 , Director failed to create Because UID already existed')
    
    # def test_update_director(self):
    #     '''
    #         test update data director
    #         api: /api/director/{director_id}
    #     '''
    #     client = app.connex_app.app.test_client()
    #     result = client.put('/api/director/7111',json = {
    #                                                     "department": "man",
    #                                                     "gender": 0,
    #                                                     "name": "mandoo unit test update",
    #                                                     "uid": 5})

    #     # Make your assertions
    #     self.assertEqual(result.status_code, 200,"director_id doesnt exist!")

    # def test_delete_director(self):
    #     '''
    #         test delete data director
    #         api: /api/director/{director_id}
    #     '''
    #     client = app.connex_app.app.test_client()
    #     result = client.delete('/api/director/7111')

    #     # Make your assertions
    #     self.assertEqual(result.status_code, 200,"director_id doesnt exist!")

    def test_get_all_movie(self):
        '''Test Get All data Movie'''
        client = app.connex_app.app.test_client()
        result = client.get('/api/movie')
        # Make your assertions
        self.assertEqual(result.status_code, 200)    

    def test_get_movie_by_popularity(self):
        '''Test Get data Movie sorted by popularity'''
        client = app.connex_app.app.test_client()
        result = client.get('/api/movie/popularity')
        # Make your assertions
        self.assertEqual(result.status_code, 200) 

    def test_get_movie_by_vote_average(self):
        '''Test Get data Movie sorted by vote average'''
        client = app.connex_app.app.test_client()
        result = client.get('/api/movie/vote_average')
        # Make your assertions
        self.assertEqual(result.status_code, 200) 

    def test_get_movie_with_star_end_release_dates(self):
        '''
            Test Get data Movie between start and end release dates
              /movie/dates/{start}/{end}
            params start:   start of release date want to view
            params end:     end of release date want to view
        '''
        client = app.connex_app.app.test_client()
        result = client.get('/api/movie/dates/2016-05-01/2016-05-20')
        # Make your assertions
        self.assertEqual(result.status_code, 200)

    def test_get_all_movie_with_pagination(self):
        '''
            test Get all movie with pagination current page = 80 and data per page = 25
            api : /api/movie/{page}/{per_page}
        '''
        client = app.connex_app.app.test_client()
        result = client.get('/api/movie/80/25')
        # Make your assertions
        self.assertEqual(result.status_code, 200,'current page must not exceed max page or data in database')

    def test_get_one_movie(self):
        '''
            test get one data movie by director_id and movie_id
            /director/{director_id}/movie/{movie_id}:

            params director_id:     id of director in movie assosiate with movie
            params movie_id:        id of movie
        '''
        client = app.connex_app.app.test_client()
        result = client.get('/api/director/4772/movie/43607')
        # Make your assertions
        self.assertEqual(result.status_code, 200,'Director not found for Id inputted!')

    
class TestDirector(unittest.TestCase):
    def test_read_all_director(self):
        '''test read all director function is return should be list type'''
        self.assertIs(type(director.read_all()),list)
    
    

class TestMovie(unittest.TestCase):
    def test_read_all_movie(self):
        '''test read all movie function is return should be list type'''
        self.assertIs(type(movie.read_all()),list)

if __name__ == '__main__':
    unittest.main()



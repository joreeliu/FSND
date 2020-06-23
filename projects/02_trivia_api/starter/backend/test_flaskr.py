import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:66252099@localhost:5432/trivia"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(len(data['categories']), 6)

    def test_get_questions(self):
        res = self.client().get('/questions')
        self.assertEqual(res.status_code, 200)

        res = self.client().get('/questions?page=10')
        self.assertEqual(res.status_code, 400)

    def test_delete_questions(self):
        res = self.client().delete('/questions/47')
        self.assertEqual(res.status_code, 200)

        res = self.client().delete('/questions/100')
        self.assertEqual(res.status_code, 400)

    def test_post_questions(self):
        res = self.client().post(
            '/question',
            json={
                "question": "how are you",
                "answer": "good",
                "difficulty": 1,
                "category": "2"})
        #data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        res = self.client().post('/question', json={})
        self.assertEqual(res.status_code, 400)

    def test_search_questions_by_term(self):
        res = self.client().post('/questions', json={'searchTerm': 'title'})
        data = json.loads(res.data)
        self.assertEqual(data['total_questions'], 1)

        res = self.client().post('/questions', json={'searchTerm': ''})
        self.assertEqual(res.status_code, 400)

    def test_search_questions_by_category(self):
        res = self.client().get('/categories/4/questions')
        data = json.loads(res.data)
        self.assertEqual(data['total_questions'], 3)

        res = self.client().get('/categories/400/questions')
        data = json.loads(res.data)
        self.assertEqual(data['total_questions'], 0)

    def test_next_question(self):
        res = self.client().post(
            '/quizzes',
            json={
                'quiz_category': {
                    'type': "Geography",
                    'id': "2"},
                'previous_questions': []})
        data = json.loads(res.data)
        self.assertTrue(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

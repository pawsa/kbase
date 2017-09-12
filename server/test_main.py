"""Test the main handler"""

import json
import unittest
import webapp2

# import the tested module.
import main
import questions


class TestQuestions(unittest.TestCase):
    def _deleteAll(self):
        for q in questions.db.read(None, 1, 1000000):
            questions.db.delete(q.id)

    def setUp(self):
        self._deleteAll()

    def tearDown(self):
        self._deleteAll()

    def test_get_empty(self):
        request = webapp2.Request.blank('/questions')
        response = request.get_response(main.app)

        self.assertEqual(response.status_int, 200)
        qst = json.loads(response.body)
        self.assertIn('questions', qst)

    def test_get_2(self):
        questions.db.add('Q1')
        questions.db.add('Q2', 'A2')
        request = webapp2.Request.blank('/questions')
        response = request.get_response(main.app)

        self.assertEqual(response.status_int, 200)
        qst = json.loads(response.body)
        self.assertIn('questions', qst)

    def test_get_single_existing(self):
        q1 = questions.db.add('Q1')
        request = webapp2.Request.blank('/questions/{}'.format(q1.id))
        response = request.get_response(main.app)

        self.assertEqual(response.status_int, 200)
        qst = json.loads(response.body)
        self.assertEqual(qst.get('q'), 'Q1')
        self.assertEqual(qst.get('id'), q1.id)

    def test_get_single_unexsiting(self):
        q1 = questions.db.add('Q1')
        request = webapp2.Request.blank('/questions/{}'.format(q1.id+1))
        response = request.get_response(main.app)

        self.assertEqual(response.status_int, 404)
        qst = json.loads(response.body)

if __name__ == '__main__':
    unittest.main()

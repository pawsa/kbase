#! /usr/bin/env python

"""Main Knowledge Base Handler. No persistency implemented yet"""

import json
import webapp2
import questions


class QuestionList(webapp2.RequestHandler):
    def get(self):
        self.response.content_type = 'application/json'
        query = self.request.get('q')
        retlist = questions.db.read(query)
        self.response.write(
            json.dumps({'questions': [j.todict() for j in retlist]}))

    def post(self):
        self.response.content_type = 'application/json'
        question = json.loads(self.request.body)
        if 'q' in question:
            self.response.write(json.dumps(
                {'questions': [
                 questions.db.add(question['q'], question.get('a'))
                    .todict()]}))
        else:
            self.response.status = 404
            self.response.write(json.dumps('q field is required'))


class Question(webapp2.RequestHandler):
    def get(self, qid):
        self.response.content_type = 'application/json'
        question = questions.db.readbyid(int(qid))
        if question is None:
            self.response.status = 404
            self.response.write(json.dumps('Not found'))
        else:
            self.response.write(json.dumps(question.todict()))

    def patch(self, qid):
        self.response.status = 501
        self.response.write('Please accept regrets')

app = webapp2.WSGIApplication([
    ('/questions', QuestionList),
    ('/questions/(.+)', Question),
], debug=True)


def main():
    from paste import httpserver
    from paste.urlparser import StaticURLParser
    from paste.cascade import Cascade
    static_server = StaticURLParser('client')
    testapp = Cascade([static_server, app])
    httpserver.serve(testapp, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()

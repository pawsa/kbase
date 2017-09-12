#! /usr/bin/env python3

"""This is the questions db model.  It supports adding, searching/reading,
updating, deleting questions.
"""

import re
import threading


class Question:
    def __init__(self, qid, question, answer=None):
        self.id = qid
        self.question = question
        self.answer = answer

    def __repr__(self):
        return '<Q:{}>'.format(re.sub(r'[^- a-zA-Z0-9]', '-', self.question))
    def todict(self):
        return {'id': self.id, 'q': self.question, 'a': self.answer}

class Db:
    """Question database"""
    def allocateId(self):
        with self.lock:
            retid = self.lastid
            self.lastid += 1
        return retid

    def __init__(self):
        self.questions = []
        self.lastid = 1
        self.lock = threading.Lock()

    def add(self, question, answer=None):
        qid = self.allocateId()
        question = Question(qid, question, answer)
        self.questions.append(question)
        return question

    def read(self, query=None, start=1, count=20):
        if query is None:
            resp = self.questions
        else:
            resp = [q for q in self.questions
                    if query in q.question or query in q.answer]
        return resp[(start-1):(start+count-1)]

    def readbyid(self, qid):
        for q in self.questions:
            if q.id == qid:
                return q
        return None

    def update(self, qid, updates):
        question = self.readbyid(qid)
        if question is None:
            return
        if 'question' in updates:
            question.question = updates['question']
        if 'answer' in updates:
            question.answer = updates['answer']

    def delete(self, qid):
        with _lock:
            for idx in range(0, len(self.questions)):
                if self.questions[idx].id == qid:
                    del self.questions[idx]
                    return True
        return False

db = Db()

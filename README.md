Knowledge base
==============

Very simple db operating in several modes:
- search (default): type some keywords and hope to find answers.
- ask question: creates a question entry, pass it to all recipients
  with mail, and a link to "add response".
- edit: allows to to edit the question/answer pair for clarity.

Client
======

The client has three controllers corresponding to the modes above. Components
are:
Researcher: Search box with a list of matches (question: summary)
AddQuery: simple add query box
ViewEquery/EditQuery

Server
======

Following endpoints are available:
- GET /questions?q=QUERY
- POST /questions
- GET /questions/ID    
- PATCH /questions/ID    
- DELETE /questions/ID

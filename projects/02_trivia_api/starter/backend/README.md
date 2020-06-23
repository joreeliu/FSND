# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## API Documentation

### Endpoints

**/categories** [GET]

- Get all available categories.
- Sample Response

```JSON
{
    "categories":["Science","Art","Geography","History","Entertainment","Sports"],
    "success":true,
    "total":6
}

```

---

**//questions?page=1** [GET]

- Get questions by page (10 questions per page). Each response includes a list of questions, number of total questions, current category, categories.
- Sample Response

```JSON
 {
     "categories":["Science","Art","Geography","History","Entertainment","Sports"],
     "current_category":["Science","Art","Geography","History","Entertainment","Sports"],
     "questions":[
         {
             "answer":"The Liver",
             "category":0,
             "difficulty":4,
             "id":20,
             "question":"What is the heaviest organ in the human body?"
        },
        ...],
    "success":true,
    "total_questions":39}
```

**/questions/\<int:question_id\>** [DELETE]

- Delete a question by question id
- Sample Response:

```JSON
{
    "success": true,
    "question_id": 1
}
```

**/question/** [POST]

- Add a new question which will require the question and answer text, category, and difficulty score
- Data: `{"question":"how are you", "answer": "good", "difficulty":1, "category"="2"}`
- Sample Response:

```JSON
{
  "success": true
}
```

**/questions/** [POST]

- get questions based on a search term. The response includes any questions for whom the search term is a substring of the question.
- Data: `{'searchTerm':'title'}`
- Sample Response:

```JSON
{
    "questions":[
        {
            "answer":"Edward Scissorhands",
            "category":4,
            "difficulty":3,
            "id":6,
            "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }],
    "success":true,
    "total_questions":1
}
```

**/categories/\<int:category_id\>/questions** [GET]

- Get questions based on category
- Sample Response:

```JSON
{
    "current_category":1,
    "questions":[
        {
            "answer":"Escher",
            "category":1,
            "difficulty":1,
            "id":16,
            "question":"Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
        },
        ...],
    "success":true,
    "total_questions":7
}
```

**/quizzes/** [POST]

- Get questions to play the quiz. The endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
- Data: `{'quiz_category': {'type': "Geography", 'id': "2"}, 'previous_questions': []}`
- Sample Response:

```JSON
{
  "question": {
    "answer": "Lake Victoria",
    "category": "2",
    "difficulty": 2,
    "id": 20,
    "question": "What is the largest lake in Africa?"
  },
  "success": true
}
```

## Testing

To run the tests, run

```

dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py

```

```

```

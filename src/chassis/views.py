from flask.ext import restful
from flask import request
from flask import render_template
from flask.ext.restful import fields, marshal_with
from flask.ext.cache import Cache
from chassis.models import Cat, Todo, db

api = restful.Api()
cache = Cache()

cat_fields = {
    'id': fields.String,
    'born_at': fields.Integer,
    'name': fields.String,
}

todo_fields = {
    'title': fields.String,
    'done': fields.Boolean,
    'order': fields.Integer,
}


def show_todos():
    return render_template("todo.html")

class TodoListAPI(restful.Resource):

    @marshal_with(todo_fields)
    def get(self):
        todos = Todo.query.all()
        return todos

    def post(self):
        todo_json = request.json
        todo = Todo.query.get(todo_json["title"])

        if todo is None:
            todo = Todo()

        todo.title = todo_json["title"]
        todo.done = todo_json["done"]
        todo.order = todo_json["order"]

        db.session.add(todo)
        db.session.commit()

class CatAPI(restful.Resource):

    @cache.cached(timeout=60)
    @marshal_with(cat_fields)
    def get(self, cat_id):
        """Get a :py:class:`~chassis.models.Cat` with the given cat ID.

        :param id: unique ID of the cat
        :type id: int
        :code 404: cat doesn't exist

        """

        q = Cat.query.get_or_404(cat_id)

        return q

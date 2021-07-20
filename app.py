from flask import Flask,jsonify
import datetime
from flask.wrappers import Request
from flask_restful import Resource,Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.exceptions import abort
from werkzeug.wrappers import request



app = Flask(__name__)

# Our configuration

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
db = SQLAlchemy(app)
Migrate(app,db)
api = Api(app)


# Our model
class Todo(db.Model):
    
    __tablename__ = 'todos'

    id = db.Column(db.Integer,primary_key=True)
    task = db.Column(db.String(150))
    create_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __init__(self,task):
        self.task = task

    def json(self):
        return {
            'id': self.id,
            'task': self.task,
            'create_at': self.create_at
        }


class TodoId(Resource):

    def get(self,id):

        todo = Todo.query.filter_by(id=id).first()

        if todo:
            return todo.json()
        else:
            return {"note": None},404

    def put(self,id):

        todo = Todo.query.filter_by(id=id).first()
        
        request_data = request.form['task']
        todo.task = request_data

        db.session.add(todo)
        db.session.commit()

        if not todo:
            abort(404, "todo not found")
        
        return todo.json

    def delete(self,id):

        todo = Todo.query.filter_by(id=id).first()

        db.session.delete(todo)
        db.session.commit()

        if todo:
            return todo.json()
        else:
            return {'note': 'not found'},404

class Todo(Resource):

    def post(self):

        todoname = Request.form['task']

        todo = Todo(task=todoname)
        db.session.add(todo)
        db.session.commit()

        return todo.json()


api.add_resource(TodoId,'api/v1/<int:id>')








if __name__ == '__main__':
    app.run(debug=True)

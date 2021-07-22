from flask import Flask
from datetime import datetime
from flask_restful import Resource,Api,reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.exceptions import abort



app = Flask(__name__)

# Our configuration

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)
api = Api(app)



# add argument for get and parse post on body request
parser = reqparse.RequestParser()
parser.add_argument('task')


# Our model
class Todo(db.Model):
    
    __tablename__ = 'todos'

    id = db.Column(db.Integer,primary_key=True)
    task = db.Column(db.String(150))
    create_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow())

    def __init__(self,task):
        self.task = task



    def json(self):
        return {
            'id': self.id,
            'task': self.task,
            'create_at': str(self.create_at)
        }




class TodoId(Resource):
    # ressource for get,delete and put todo

    def get(self,id):

        todo = Todo.query.filter_by(id=id).first()

        if not todo:
            abort(404,"todo not found")
        
        return todo.json()

    def put(self,id):

        todo = Todo.query.filter_by(id=id).first()
        
        if not todo:
            abort(404, "todo not found")

        args = parser.parse_args()
        _task= args["task"]

        todo.task = _task

        db.session.add(todo)
        db.session.commit()

        
        return todo.json()

    def delete(self,id):

        todo = Todo.query.filter_by(id=id).first()

        

        if todo:

            db.session.delete(todo)
            db.session.commit()

            return todo.json()
        else:
            abort(404, "todo not found")

class TodoA(Resource):
    # Ressource for add and list todos

    def get(self):
        todos = Todo.query.all()

        return [todo.json() for todo in todos]


    def post(self):

        args = parser.parse_args()
        _task= args["task"]

        new_task = Todo(task=_task)
        db.session.add(new_task)
        db.session.commit()

        return new_task.json()


api.add_resource(TodoId,'/api/v1/todo/<int:id>')
api.add_resource(TodoA,'/api/v1/todo')








if __name__ == '__main__':
    app.run()

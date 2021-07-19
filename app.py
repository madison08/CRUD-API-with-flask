from flask import Flask
import datetime
from flask_restful import Resource,Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



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









if __name__ == '__main__':
    app.run(debug=True)

from mongoengine import Document, StringField, IntField, BooleanField, ReferenceField, ValidationError, DateField
from mongoengine.errors import DoesNotExist
from .config import init_db
from datetime import date

init_db()

class User(Document):
    email = StringField(required=True)
    password = StringField(required=True)
    username = StringField(required=True)

    meta = {
        'collection': 'User'  
    }

    @classmethod
    def createUser(cls, email, password, username):
        user = cls(email=email, password=password, username=username)
        user.save()
        return user

class Task(Document):
    task = StringField(required=True)  # Asegúrate de usar 'task' aquí
    category = StringField(required=True)
    user = ReferenceField('User', required=True, reverse_delete_rule=3)
    completed = BooleanField(default=False)
    dueDate = DateField()

    meta = {
        'collection': 'Task'
    }

    @classmethod
    def create_task(cls, taskName, category, dueDate, user):
        task = cls(taskName=taskName, category=category, dueDate=dueDate, user=user)
        task.save()  # Asegúrate de que 'save' se complete sin errores
        return task
    
    @classmethod
    def get_tasks(cls, user):
        return cls.objects(user=user)

    @classmethod
    def delete_task(cls, task_id):
        try:
            task = cls.objects.get(id=task_id)  
            task.delete()
            return task
        except DoesNotExist:
            return None 

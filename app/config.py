from mongoengine import connect

def init_db():
    connect(
        db='Tasks', 
        host='mongodb+srv://citer:BunYnSec9tqRYq8Z@cluster0.nb7gd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
    )

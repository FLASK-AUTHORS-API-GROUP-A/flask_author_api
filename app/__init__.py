from flask import Flask 
from app.extensions import db,migrate ,jwt

#Application Factory Function
def create_app():
    
    app = Flask(__name__)
    app.config.from_object('config.Config')# we are registering our class Config in our AFF

    db.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)
    

    #Registering models
    from app.models.author_model import Author
    from app.models.book_model import Book
    from app.models.company_model import Company

 

    #index route
    @app.route('/')
    def home():
      return "Hello. This is OUR Flask Author API"
    

    return app
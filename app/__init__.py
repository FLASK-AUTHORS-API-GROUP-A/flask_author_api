from flask import Flask 
from app.extensions import db,migrate ,jwt
from app.controllers.auth.auth_controller import auth

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

    #registering blue prints
    app.register_blueprint(auth)

 

    #index route
    @app.route('/')
    def home():
      return "This is our Flask Author API"
    

    return app
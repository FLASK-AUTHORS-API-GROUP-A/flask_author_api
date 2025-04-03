from flask import Flask 
from app.extensions import db,migrate ,jwt , bcrypt
from app.controllers.auth.auth_controller import auth
from app.controllers.author.author_controller import author
from app.controllers.company.company_controller import companies
from app.controllers.book.book_controller import book

#Application Factory Function
def create_app():
    
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config.from_object('config.Config')# we are registering our class Config in our AFF


    db.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    

    #Registering models
    from app.models.author_model import Author
    from app.models.company_model import Company
    from app.models.book_model import Book
 
    #registering blue prints
    app.register_blueprint(auth)
    app.register_blueprint(author)
    app.register_blueprint(companies)
    app.register_blueprint(book)

 

    #index route
    @app.route('/')
    def home():
      return "This is our Flask Author API"
    

    return app
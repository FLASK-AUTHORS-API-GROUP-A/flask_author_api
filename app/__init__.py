from flask import Flask
from app.extensions import db, migrate, jwt,bcrypt
from app.controllers.auth.auth import auth
from app.controllers.author.author_controller import author
from app.controllers.company.company_controller import companies

def create_app():  
    app = Flask(__name__)#It gets its value depending on how we execute the containing script
    app.config.from_object("config.Config") #configuration comes in first
    
    db.init_app(app) # then the db
    migrate.init_app(app, db) #then we migrate 
    jwt.init_app(app) 
    bcrypt.init_app(app)

    # Registering models
    from app.models.author_model import Author
    from app.models.company_model import Company
    from app.models.book_model import Book

    #registering blue prints
    app.register_blueprint(auth)
    app.register_blueprint(author)
    app.register_blueprint(companies)

   #index route
    @app.route('/') 
    def index():
        return"hello"

    return app


 
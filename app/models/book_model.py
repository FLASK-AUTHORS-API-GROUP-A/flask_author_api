
from app.extensions import db
from datetime import datetime

class Book(db.Model):
    # you can also use  __bind_key__ = "books_db" 
     # the bind_ key tells SQLAlchemy which database a model should be associated with. 
     # Without it, all models would default to the primary database, making multiple database usage impossible.
     #while migrating my data after using SQLAlchemy_bind i will use the command flask db upgrade --bind books_db
     #it will apply migrations for my  specific database (books_db)
     __tablename__ = "books"
     book_id = db.Column(db.Integer, primary_key=True, nullable = False)
     title = db.Column(db.String(30), nullable = False)
     price = db.Column(db.Integer, nullable = False)
     description= db.Column(db.String(250), nullable = False)
     isbn = db.Column(db.String(30), nullable = False, unique = True)
     image = db.Column(db.String(255), nullable = True)
     no_of_pages = db.Column(db.String(5), nullable = False)
     price_unit= db.Column(db.String(20), nullable = False)
     author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'))
     company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'))
     author = db.relationship('Author', backref = 'books')
     company = db.relationship('Company', backref = 'books')
     publication_date = db.Column(db.Date, nullable = False)
     format= db.Column(db.String(50), nullable = False)
     genre= db.Column(db.String(50), nullable = False)
     language= db.Column(db.String(50), nullable = False)

     def __init__(self, book_id,title,price,description,isbn,image,no_of_pages,price_unit,publication_date,format, genre, language):
       super(Book, self).__init__()
       self.book_id = book_id
       self.title = title
       self.price = price
       self.description= description
       self.isbn = isbn
       self.image = image
       self.no_of_pages = no_of_pages
       self.price_unit= price_unit
       self.publication_date = publication_date
       self.format= format
       self.genre= genre
       self.language= language

     def __repr__(self) -> str:
         return f'{self.title} {self.description}'    

            
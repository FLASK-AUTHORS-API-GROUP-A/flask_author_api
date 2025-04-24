from app.extensions import db
from datetime import datetime

class Author(db.Model):
      __tablename__ = "authors" 
      author_id = db.Column(db.Integer, primary_key=True , nullable = False)
      first_name = db.Column(db.String(100) , nullable = False)
      last_name = db.Column(db.String(100) , nullable = False)
      contact = db.Column(db.String(10), nullable = False, unique = True)
      email = db.Column(db.String(30) , nullable = False, unique = True)
      password = db.Column(db.String(255), nullable = False)
      image = db.Column(db.String(255) , nullable = True)
      biography = db.Column(db.String(200), nullable = False)
      created_at = db.Column(db.DateTime, default = datetime.now())
      updated_at = db.Column(db.DateTime, onupdate = datetime.now())
      books = db.relationship('Book', backref='author', lazy=True)
      companies = db.relationship('Company', backref='author', lazy=True)

      def __init__(self, first_name, last_name, contact, email, password , image, biography):
        super(Author, self).__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.contact = contact
        self.email = email
        self.password = password
        self.image = image
        self.biography = biography

      def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
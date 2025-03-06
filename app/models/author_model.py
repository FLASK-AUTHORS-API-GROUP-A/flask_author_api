from app.extensions import db
from datetime import datetime

class Author(db.Model):
      __tablename__ = "authors" 
      id = db.Column(db.Integer, primary_key=True , nullable = False)
      first_name = db.Column(db.String(100) , nullable = False)
      last_name = db.Column(db.String(100) , nullable = False)
      contact = db.Column(db.String(10), nullable = False, unique = True)
      email = db.Column(db.String(30) , nullable = False, unique = True)
      password = db.Column(db.String(8), nullable = False)
      image = db.Column(db.String(255) , nullable = True)
      biography = db.Column(db.String(200), nullable = False)
      author_type = db.Column(db.String(20), default= "author")
      created_at = db.Column(db.DateTime, default = datetime.now())
      updated_at = db.Column(db.DateTime, onupdate = datetime.now())

      def __init__(self, id, first_name, last_name, contact, email, password , image, biography, author_type):
        super('Author', self).__init__()
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.contact = contact
        self.email = email
        self.password = password
        self.image = image
        self.biography = biography
        self.author_type = author_type

      def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
          
#add foreign keys
#craete a controllers folder and then within the controllers folder create 3 subfolders for
#author
#books
#company 
#for each subfolder create a controller file that will b used for CRUD for each entity. using blueprints within each controlleer file ensure
#that in the author controller u create a new other to login the author then in the company controller create all the CRUD functonality
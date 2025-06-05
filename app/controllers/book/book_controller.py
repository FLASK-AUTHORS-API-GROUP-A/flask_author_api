from flask import Blueprint, request, jsonify
from app.status_code import HTTP_400_BAD_REQUEST,HTTP_200_OK,HTTP_401_UNAUTHORIZED,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED,HTTP_404_NOT_FOUND
from app.models.book_model import Book
from app.extensions import db
from flask_jwt_extended import jwt_required,get_jwt_identity


#book blueprint
book = Blueprint('book', __name__, url_prefix='/api/v1/book')

#creating  a book   
@book.route('/create', methods=['POST'])
@jwt_required(get_jwt_identity)
def createBook():
    data = request.get_json()
    title = data.get("title")
    price = data.get('price')
    description = data.get('description')
    isbn = data.get('isbn')
    image = data.get('image')
    no_of_pages = data.get('no_of_pages')
    price_unit = data.get('price_unit')
    format = data.get('format')
    language = data.get('language')
    publication_date = data.get('publication_date')
    genre = data.get('genre')
    company_id = data.get('company_id')
    
    #validations of the incoming request
    if not title or not price or not description or not isbn or not image or not no_of_pages or not price_unit or not publication_date or not format or not genre or not language or not company_id:
        return jsonify({"error":"All fields are required"}),HTTP_400_BAD_REQUEST
    

    if Book.query.filter_by(title=title).first() is not None:
        return jsonify({"error":"Book title already exists."}),HTTP_409_CONFLICT
    
    try:
      

       #creating a new book
       new_book = Book(
            title=title,
            price=price, 
            description=description,
            isbn = isbn,
            image = image,
            no_of_pages= no_of_pages,
            price_unit= price_unit,
            publication_date= publication_date,
            format= format,
            genre= genre,
            language= language,
            company_id=company_id)
       db.session.add(new_book)
       db.session.commit()


       return jsonify({
           'message': title + " has been successfully created as an " ,
           'book':{
               'id':new_book.book_id,
               "name":new_book.title,
               "origin":new_book.price,
               "description": new_book.description,
               "genre" : new_book.genre,
               "language": new_book.language
           }
       }),HTTP_201_CREATED

    except Exception as e:   
        db.session.rollback() 
        return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    
 # getting book by id
@book.get('/book/<int:id>')
@jwt_required()
def getBook(book_id):
    try:

        book = Book.query.filter_by(book_id=book_id).first()
         
        if not Book: 
            return jsonify({"Error":"Book not found"}), HTTP_404_NOT_FOUND
        
        return jsonify({

            "message":"Book details retrieved successfully",
            "book":{
                    'id':book.id,
                    'title':book.title,
                    'price':book.price,
                    'price_unit':book.description,
                    'description':book.description,
                    'pages':book.pages,
                    'isbn':book.isbn,
                    'publication_date':book.publication_date, 
                    'craeted_at':book.created_at, 
                    'origin':book.origin, 
                'author':{
                        'first_name' : book.first_name,
                        'last_name' : book.last_name,
                        'email' : book.email,
                        'contact' : book.contact,
                        'biography' : book.biography,
                        'created_at' : book.created_at
            }
       }})
                    
    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
    
#Updating a Book  
@book.route('/update/<int:id>', methods=['PUT', 'PATCH'] ,  endpoint='update_book') # Defining a route for editing a book  
@jwt_required()
def updateBookdetails(book_id):
    
   try:
        
        current_book = get_jwt_identity() # returns the current book's id
        logged_in_user = Book.query.filter_by(book_id=current_book).first() # Querying the database for the book with the specified id
        
        
        book = Book.query.get(book_id) # Querying the database for the book with the specified id
        if not book:
            return jsonify({'message': 'Book is not found'}), HTTP_404_NOT_FOUND
        
        else:
        # store request data
               data = request.get_json
               title =data.get_json().get("title",book.name)
               price = data.get_json().get('price',book.price)
               description = data.get_json().get('description',book.description)
               isbn = data.get_json().get('isbn',book.isbn)
               image = data.get_json().get('image',book.image)
               no_of_pages = data.get_json().get('no_of_pages',book.no_of_pages)
               price_unit =  data.get_json().get('price_unit',book.price_unit)
               publication_date =  data.get_json().get('publication_date',book.publication_date)
               genre =  data.get_json().get('genre',book.genre)
               language = data.get_json().get('language', book.language)
               format = data.get_json().get('format', book.format)
               company_id =  data.get_json().get('company_id',book.company_id)

            
        if isbn != book.isbn and Book.query.filter_by(isbn=isbn).first():
               return jsonify({
                    "error": "ISBN already in use"
               }),HTTP_409_CONFLICT

        if title != book.title and Book.query.filter_by(title=title,user_id = logged_in_user).first():
               return jsonify({
                    "error": "title already in use"
               }),HTTP_409_CONFLICT
         
        book.title = title
        book.price= price
        book.price_unit= price_unit
        book.genre= genre
        book.description = description
        book.isbn= isbn
        book.publication_date= publication_date
        book.image= image
        book.language = language
        book.format = format
        book.no_of_pages= no_of_pages
        book.company_id= company_id
        
        db.session.commit()
              
        return jsonify({
            "book":{
                'message': title + ' has been updated successfully',
                'id':book.id,
                'title':book.title,
                'price':book.price,
                'price_unit':book.price_unit,
                'description':book.description,
                'no_of_pages':book.no_of_pages,
                'isbn':book.isbn,
                'genre':book.genre,
                'format':book.format,
                'language':book.language,
                'publication_date':book.publication_date,
                'image':book.image,
                'created_at':book.created_at,
                "company":{
                     'id':book.id,
                     'name':book.company.name,
                     'description':book.company.description,
                      }}})  
   except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR     
   
    #delete book

@book.route('/delete/<int:id>', methods=['DELETE']) 
@jwt_required()
def deletebook(id):
   try:
     current_user = get_jwt_identity()
     loggedInUser = current_user.query.filter(id=id).first
    # get book by id
     book = Book.query.filter_by(id=id).first()
     if not book:
            return jsonify({"error": "book not found"}),HTTP_404_NOT_FOUND
     
     elif loggedInUser.user_type != 'admin' and book.user_id!= current_user:
            return jsonify({"error": "you are not authorised to delete this book"}),HTTP_401_UNAUTHORIZED
     else:
 
            db.session.delete(book)
            db.session.commit()

            return jsonify({
                'message': 'book has been deleted successfully'
                }) , HTTP_200_OK
   except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
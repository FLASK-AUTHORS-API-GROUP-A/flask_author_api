from flask import Blueprint, request, jsonify
from app.status_code import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED
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
    publication_date = data.get('publication_date')
    genre = data.get('genre')
    format = data.get('format')
    language = data.get('language')
    company_id = data.get('company_id')
    


    #validations of the incoming request

    if not title or not price or not description or not isbn or not image or not no_of_pages or not price_unit or not publication_year or not genre or not specialisation or not company_id:
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
           genre= genre,
           format = format,
           language= language,
           company_id=company_id)

       db.session.add(new_book)
       db.session.commit()



       return jsonify({
           'message': title + " has been successfully created " ,
           'book':{
               "id" :new_book.id,
               "name" : new_book.title,
               "description" : new_book.description,
               "isbn" : new_book.isbn,
               "image" : new_book.image,
               "no_of_pages" : new_book.no_of_pages,
               "price_unit" : new_book.price_unit,
               "publication_date" : new_book.publication_date,
               "genre" : new_book.genre,
               "format" : new_book.format,
               "language" : new_book.language,
           }
       }),HTTP_201_CREATED

    except Exception as e:   
        db.session.rollback() 
        return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    
#Retrieving all books
@book.get('/')
@jwt_required()
def get_all_books():

      try:
        all_books = Book.query.all()

        book_data = []

        for book in all_books:
            book_info ={
              
        return jsonify({
            "message":"All companies retrieved successfully",
            "total_companies":len(companies_request),
            "companies":companies_request

        }), HTTP_200_OK
    
    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR

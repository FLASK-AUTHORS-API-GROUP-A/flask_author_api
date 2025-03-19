from flask import Blueprint, request, jsonify
from app.status_code import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED
import validators
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
    publication_year = data.get('publication_year')
    genre = data.get('genre')
    specialisation = data.get('specialisation')
    company_id = data.get('company_id')
    


    #validations of the incoming request

    if not title or not price or not description or not isbn or not image or not no_of_pages or not price_unit or not publication_year or not genre or not specialisation or not company_id:
        return jsonify({"error":"All fields are required"}),HTTP_400_BAD_REQUEST
    

    if Book.query.filter_by(title=title).first() is not None:
        return jsonify({"error":"Book title already exists."}),HTTP_409_CONFLICT
    
    
    try:
      

       #creating a new book
       new_book = Book(title=title,price=price, description=description, company_id=company_id)
       db.session.add(new_book)
       db.session.commit()



       return jsonify({
           'message': title + " has been successfully created as an " + new_book,
           'user':{
               'id':new_book.id,
               "name":new_book.title,
               "origin":new_book.price,
               "description": new_book.description
              
           }
       }),HTTP_201_CREATED

    except Exception as e:   
        db.session.rollback() 
        return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    
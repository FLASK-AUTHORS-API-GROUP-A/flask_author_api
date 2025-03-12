from flask import Blueprint, request, jsonify
from app.models.book_model import Book
from app.status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED,HTTP_404_NOT_FOUND,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR
from app.extensions import db, bcrypt
from flask_jwt_extended import create_accesss_token, create_refresh_token,jwt_required,get_jwt_identity

books_bp = Blueprint('books', __name__)

# Creating a new book
@books_bp.route('/create', methods=['POST'])
def create_abook():
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
    user_id = get_jwt_identity()


#validation of the incoming request data
    if not title or not isbn or not price or not description or not no_of_pages or not price_unit or not genre  or not specialisation:
     return jsonify ({"error":"All fields are required"}), HTTP_400_BAD_REQUEST
    
    if Book.querry.filter_by(title=title, user_id=user_id).first() is not None:
      return jsonify ({"error":"Book with this title and user id already exists"}),#HTTP_409_BAD_CONFLICT 
    
    if Book.querry.filter_by(isbn=isbn).first() is not None:
        return jsonify ({"error":"Book isbn is already in use"}),#HTTP_409_BAD_CONFLICT
    


    
   
      

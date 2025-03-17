from flask import Blueprint, request, jsonify
from app.status_code import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK,HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED 
from app.models.author_model import Author  
from flask_jwt_extended import jwt_required, get_jwt_identity 
from app.extensions import db, bcrypt  

# Creating an authors blueprint instance
author = Blueprint('author', __name__, url_prefix='/api/v1/author')  


# Getting all authors from the database
@author.get('authors') 
@jwt_required 
def get_all_authors():
    
    try:
        
        all_authors = Author.query.all() # Querying the database for all authors
        
        authors_data = [] # Creating an empty list to store the authors data 
        for author in all_authors:
            author_info = {
                'id' : author.author_id,
                'first_name' : author.first_name,
                'last_name' : author.last_name,
                'authorname': author.get_full_name(),
                'email' : author.email,
                'contact' : author.contact,
                'biography' : author.biography,
                'created_at' : author.created_at,
                'companies' : [],
                'books' : []       
            } # Creating a dictionary to store the author's data
            if hasattr(author,'books'):
                author_info['books'] = [{
                    'id' : book.book_id,
                    'title' : book.title,
                    'genre' : book.genre,
                    'price': book.price,
                    'description' : book.description,
                    'isbn' : book.isbn,
                    'image' : book.image,
                    'no_of_pages' : book.no_of_pages,
                    'price_unit' :book.price_unit,
                    'publication_date' :book.publication_date,
                    'format' : book.format
                } for book in author.books]
            if hasattr(author,'companies'):
                author_info['companies'] = [{
                    'company_id' : company.company_id,
                    'name' : company.name,
                    'origin' : company.origin,
                    'description' : company.description,
                    'email' : company.email,
                    'contact' : company.contact,
                } for company in author.companies]
            authors_data.append(author_info) # Appending the author's data to the authors_data list
        
        return jsonify({
            'message': 'All authors retrieved successfully',
            'authors': authors_data
        }) , HTTP_200_OK # Returning a response to the client which means data returned successfully
    

    except Exception as e:
        return jsonify({
            'error': str(e)
            }), HTTP_500_INTERNAL_SERVER_ERROR
        

#get author by id
@author.get('/author/<int:author_id>')  
@jwt_required()
def get_author(author_id):
    
    try:
        
        author = Author.query.filter_by(id = author_id).first # Querying the database for the author with the specified id
       
        books = []
        companies = []

        if hasattr(author,'books'):
                books = [{
                    'id' : book.book_id,
                    'title' : book.title,
                    'genre' : book.genre,
                    'price': book.price,
                    'description' : book.description,
                    'isbn' : book.isbn,
                    'image' : book.image,
                    'no_of_pages' : book.no_of_pages,
                    'price_unit' :book.price_unit,
                    'publication_date' :book.publication_date,
                    'format' : book.format
                } for book in books]
        
        if hasattr(author,'companies'):
                companies = [{
                    'company_id' : company.company_id,
                    'name' : company.name,
                    'origin' : company.origin,
                    'description' : company.description,
                    'email' : company.email,
                    'contact' : company.contact,
                } for company in companies]
    
        return jsonify({
            'message': 'Author details retrieved successfully',
            'author': {
                'author_id' : author.author_id,
                'first_name' : author.first_name,
                'last_name' : author.last_name,
                'email' : author.email,
                'contact' : author.contact,
                'biography' : author.biography,
                'created_at' : author.created_at,
                'companies' : companies,
                'books' : books
                }
        }) , HTTP_200_OK 

    except Exception as e:
        return jsonify({
            'error': str(e)
            }), HTTP_500_INTERNAL_SERVER_ERROR
        
        
    
@author.route('/edit/<int:id>', methods=['PUT', 'PATCH']) # Defining a route for editing an author  
@jwt_required()
def update_author_details(id):
    
    try:
        
        current_author = get_jwt_identity() # Getting the current author's id from the access token
        logged_in_author = Author.query.filter_by(id=current_author).first() # Querying the database for the author with the specified id
        
        
        author = Author.query.get(id) # Querying the database for the author with the specified id
    
        
        
        if not author:
            return jsonify({'message': 'Author does not exist'}), HTTP_404_NOT_FOUND
        
        elif logged_in_author.id != author.author_id:
            return jsonify({'message': 'You are not authorized to edit this author'}), HTTP_401_UNAUTHORIZED
        
        else:
            data = request.get_json() # Extracting the JSON data
            first_name = data.get('first_name', author.first_name) # Extracting the first name from the JSON data
            last_name = data.get('last_name', author.last_name) # Extracting the last name from the JSON data
            contact = data.get('contact', author.contact)
            email = data.get('email', author.email)
            biography = data.get('biography', author.biography)
            
            if "password" in request.json:
                password = request.json.get('password')
                hashed_password = bcrypt.generate_password_hash(password)
                author.password = hashed_password

            author.first_name = first_name
            author.last_name = last_name
            author.contact = contact
            author.email = email
            author.biography = biography
            
            db.session.commit() # Committing the changes to the database
            
            author_name = author.first_name + ' ' + author.last_name
            return jsonify({
                'message': author_name + ' has been updated successfully',
                'author': {
                    'first_name' : author.first_name,
                    'last_name' : author.last_name,
                    'email' : author.email,
                    'contact' : author.contact,
                    'biography' : author.biography,
                    'created_at' : author.created_at}
                }), HTTP_200_OK
            
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR








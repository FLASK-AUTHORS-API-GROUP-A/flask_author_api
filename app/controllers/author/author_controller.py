from flask import Blueprint, request, jsonify
from app.status_code import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK,HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED,HTTP_409_CONFLICT 
from app.models.author_model import Author  
from flask_jwt_extended import jwt_required, get_jwt_identity 
from app.extensions import db, bcrypt  

# Creating an authors blueprint instance
author= Blueprint('author', __name__, url_prefix='/api/v1/auth')  


# Getting all authors from the database
@author.get('/get_all', endpoint='get_all_authors') 
@jwt_required()
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
           print('Error:', e) 
           return jsonify({
            'error': str(e)
            }), HTTP_500_INTERNAL_SERVER_ERROR
        

#get author by id
@author.get('/author/<int:author_id>' ,  endpoint='get_author_by_id')  
@jwt_required()
def get_author_by_id(author_id):
    
    try:
        
        author = Author.query.filter_by(author_id = author_id).first() # Querying the database for the author with the specified id
       
        if not author:
            return jsonify({'message': 'Author does not exist'}), HTTP_404_NOT_FOUND
        
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
        
        
 #Updating an author   
@author.route('/update/<int:author_id>', methods=['PUT', 'PATCH'] ,  endpoint='update_author') # Defining a route for editing an author  
@jwt_required()
def update_author_details(author_id):
    
    try:
        
        current_author = get_jwt_identity() # returns the current author's id
        logged_in_author = Author.query.filter_by(author_id=current_author).first() # Querying the database for the author with the specified id
        
        
        author = Author.query.get(author_id) # Querying the database for the author with the specified id
    
        
        
        if not author:
            return jsonify({'message': 'Author does not exist'}), HTTP_404_NOT_FOUND
        
        elif logged_in_author.author_id != author.author_id:
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
            
            if email != author.email and Author.query.filter_by(email=email).first():
                  return jsonify({"Error":"Email is already in use."}),HTTP_409_CONFLICT
    
            if contact != author.contact and Author.query.filter_by(contact=contact).first():
                  return jsonify({"Error":"Contact is already in use."}),HTTP_409_CONFLICT
    
                 
            author.first_name = first_name
            author.last_name = last_name
            author.contact = contact
            author.email = email
            author.biography = biography
            
            db.session.commit() # Committing the changes to the database
            
            author_name = author.get_full_name()
            return jsonify({
                'message': author_name + ' has been updated successfully',
                'author': {
                    'first_name' : author.first_name,
                    'last_name' : author.last_name,
                    'email' : author.email,
                    'contact' : author.contact,
                    'biography' : author.biography,
                    'updated_at' : author.updated_at}
                }), HTTP_200_OK
            
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
#delete author
@author.route('/delete/<int:author_id>', methods=['DELETE'] ,  endpoint='delete_author') # Defining a route for deleting an author  
@jwt_required()
def delete_author(author_id):
    
    try:
        
        current_author = get_jwt_identity() # returns the current author's id
        logged_in_author = Author.query.filter_by(author_id=current_author).first() # Querying the database for the author with the specified id
        
        author = Author.query.get(author_id) 
        if not author:
            return jsonify({'message': 'Author does not exist'}), HTTP_404_NOT_FOUND
        
        elif logged_in_author.author_id != author.author_id:
            return jsonify({'message': 'You are not authorized to delete this author'}), HTTP_401_UNAUTHORIZED
        
        
        else:
        
            #delete associated companies
            for company in author.companies:
                  db.session.delete(company)
            
            #delete associated books
            for book in author.books:
                  db.session.delete(book)
            
            db.session.delete(author)
            db.session.commit()

            return jsonify({
                'message': 'Author has been deleted successfully'
                }) , HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
        
#search for an author
@author.get('/search', endpoint='search_authors') 
@jwt_required()
def search_authors():
     
     try:
          
          search_query = request.args.get('query', '')

          authors = Author.query.filter(
                                       (Author.first_name.ilike(f"%{search_query}%")) |
                                       (Author.last_name.ilike(f"%{search_query}%"))
                                       ).all()
          
          if not authors:
               return jsonify({
                'message': 'No results found.'
                }), HTTP_404_NOT_FOUND
          else:
              
            authors_data = [] # Creating an empty list to store the authors data 
          for author in authors:
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
            }   
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
                authors_data.append(author_info)
            
              return jsonify({
                            'message': f'Author with name {search_query} retrieved successfully',
                            'search_results': authors_data
                            }) , HTTP_200_OK 

     except Exception as e:
        return jsonify({
            'error': str(e)
            }), HTTP_500_INTERNAL_SERVER_ERROR
        






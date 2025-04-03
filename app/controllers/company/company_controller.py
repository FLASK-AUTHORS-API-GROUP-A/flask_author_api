from flask import Blueprint,request,jsonify 
from app.status_code import HTTP_201_CREATED,HTTP_400_BAD_REQUEST,HTTP_403_FORBIDDEN,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_404_NOT_FOUND,HTTP_200_OK
from app.models.company_model import Company
from app.models.author_model import Author
from app.extensions import db
from flask_jwt_extended import jwt_required,get_jwt_identity
from datetime import datetime

#company blueprint
companies = Blueprint('companies',__name__,url_prefix='/api/v1/companies')

#Creating companies
@companies.route('/create',methods=['POST'])
@jwt_required()
def createCompany():

  #storing request values
    data = request.json
    company_id = get_jwt_identity()
    name = data.get('name')
    origin = data.get('origin')
    description = data.get('description')
    contact = data.get('contact')
    email = data.get('email') 

  #validations of the incoming request to avoid request redandancy
    if not name or not origin or not description or not email or not contact:
        return jsonify({"error":"All fields are required"}), HTTP_400_BAD_REQUEST

    if Company.query.filter_by(name=name).first() is not None:
        return jsonify({"error":"Company name already exists"}),HTTP_409_CONFLICT
    
    if Company.query.filter_by(email=email).first() is not None:
        return jsonify({"error":"Email is already in use"}),HTTP_409_CONFLICT
    
    if Company.query.filter_by(contact=contact).first() is not None:
        return jsonify({"error":"Contact already in use"}),HTTP_409_CONFLICT

      # Using datetime for timestamps
    created_at = datetime.now()
    updated_at = datetime.now()

    try:
        #creating a new company
        new_company = Company(
            company_id=company_id,
            name=name,
            origin=origin,
            description=description,
            contact=contact,
            email=email,
            created_at=created_at,
            updated_at=updated_at) 
        
        db.session.add(new_company)
        db.session.commit()

        return jsonify({
             'message':name + "has been created successfully",
             'Company':{
                'company_id':new_company.company_id,
                'name':new_company.name,
                'origin':new_company.origin,
                'description':new_company.description,
                'email':new_company.email,
                'contact':new_company.contact,
                'created_at':new_company.created_at,
                'updated_at':new_company.updated_at,

            }
        }),HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify ({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    



#Retrieving all companies
@companies.get('/')
@jwt_required()
def get_all_companies():
    try:

        all_companies = Company.query.all()

        companies_request = []

        for company in all_companies:
            company_info ={
              'company_id':company.company_id,
                'name':company.name,
                'origin':company.origin,
                'description':company.description,
                'email':company.email,
                'contact':company.contact,
                'created_at':company.created_at,
                'updated_at':company.updated_at, 
                'author':{
                    'first_name' : company.first_name,
                    'last_name' : company.last_name,
                    'author_id' : company.authhor_id,
                    'email' : company.email,
                    'contact' : company.contact,
                    'biography' : company.biography,
                    'created_at' : company.created_at
                    } 
            }
            companies_request.append(company_info)

        return jsonify({
            "message":"All companies retrieved successfully",
            "total_companies":len(companies_request),
            "companies":companies_request

        }), HTTP_200_OK
    
    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
    


    
#Get company by id
@companies.get('/company/<int:id>')
@jwt_required()
def get_company(id):

    try:
        company = Company.query.filter_by(id=id).first()
        
        if not company:
            return jsonify({"error":"Company not found"}), HTTP_404_NOT_FOUND
        
        return jsonify({

            "message":"Company details retrieved successfully",

            "company":{
                    'company_id':company.company_id,
                    'name':company.name,
                    'origin':company.origin,
                    'description':company.description,
                    'email':company.email,
                    'contact':company.contact,
                    'created_at':company.created_at,
                    'updated_at':company.updated_at, 
                    'user':{
                        'first_name' : company.first_name,
                        'last_name' : company.last_name,
                        'author_id' : company.author_id,
                        'email' : company.email,
                        'contact' : company.contact,
                        'biography' : company.biography,
                        'created_at' : company.created_at
                    }}
        }),HTTP_200_OK
    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
    


    
#Update company details
@companies.route('/edit/<int:id>', methods=['PUT','PATCH'])
@jwt_required()
def update_company_details(id):

    try:
        
        current_author = get_jwt_identity() # returns the current author's id
        logged_in_author = Author.query.filter_by(author_id=current_author).first() # Querying the requestbase for the author with the specified id
        
        #get company by id
        company = Company.query.filter_by(id=id).first # Querying the requestbase for the company with the specified id
    
        
        if not company:
            return jsonify({'message': 'Company does not exist'}), HTTP_404_NOT_FOUND
        
        elif logged_in_author.author_id!= 'admin' and company.author_id!=current_author:
            return jsonify({'message': 'You are not authorized to edit this author'}), HTTP_403_FORBIDDEN
        
        else:
            name = request.get_json() # Extracting the JSON request
            origin = request.get('contact', company.contact)
            description = request.get('email', company.email)

            if name != company.name and Company.query.filter_by(name=name).first():
                return jsonify({"error":"Company already in use"}),HTTP_409_CONFLICT
            
        company.name = name
        company.origin = origin
        company.description = description

        db.session.commit()

         
        return jsonify({
                'message': name + ' has been updated successfully',
                 'company_id':company.company_id,
                    'name':company.name,
                    'origin':company.origin,
                    'description':company.description,
                    'email':company.email,
                    'contact':company.contact,
                    'created_at':company.created_at,
                    'updated_at':company.updated_at, 
                    'author':{
                        'first_name' : company.first_name,
                        'last_name' : company.last_name,
                        'author_id' : company.author_id,
                        'email' : company.email,
                        'contact' : company.contact,
                        'biography' : company.biography,
                        'created_at' : company.created_at}
                
                }), HTTP_200_OK
    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
        





#delete company details
@companies.route('/delete/<int:company_id>', methods=['DELETE'] ,  endpoint='delete_company') # Defining a route for deleting an author  
@jwt_required()
def delete_company(company_id):
    
    try:
        
        current_author = get_jwt_identity() # returns the current author's id
        logged_in_author = Author.query.filter_by(author_id=current_author).first() # Querying the database for the author with the specified id
        
        #get company by id
        company = Company.query.filter_by(id=id).first()
        if not company:
            return jsonify({'message': 'Company does not exist'}), HTTP_404_NOT_FOUND
        
        elif logged_in_author.author_id!= 'admin' and company.author_id!=current_author:
            return jsonify({'message': 'You are not authorized to delete this company'}), HTTP_403_FORBIDDEN
        
        
        else:
        
            #delete associated books
            for book in company.books:
                  db.session.delete(book)

            db.session.delete(company)
            db.session.commit()

            return jsonify({
                'message': 'Company has been deleted successfully'
                }) , HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
        

     
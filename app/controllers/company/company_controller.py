from flask import Blueprint,request,jsonify 
from app.status_code import HTTP_201_CREATED,HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR
from app.models.company_model import Company
from app.extensions import db
from flask_jwt_extended import jwt_required,get_jwt_identity

#company blueprint
companies = Blueprint('companies',__name__,url_prefix='/api/v1/company')

#Creating companies
@companies.route('/create',methods=['POST'])
@jwt_required()
def createCompany():

  #storing request values
    data = request.json
    company_id = get_jwt_identity()
    name = data.get('name')
    origin = data.get('origin')
    description =data.get('description')
    email = data.get('email')
    contact = data.get('contact') 
    created_at = data.get('created_at')
    updated_at = data.get('updated_at')

  #validations of the incoming request
    if not name or not origin or not description or not email or not contact:
        return jsonify({"error":"All fields are required"}), HTTP_400_BAD_REQUEST

    if Company.query.filter_by(name=name).first() is not None:
        return jsonify({"error":"Company name already exists"}),HTTP_409_CONFLICT
    
    if Company.query.filter_by(email=email).first() is not None:
        return jsonify({"error":"Email is already in use"}),HTTP_409_CONFLICT
    
    if Company.query.filter_by(contact=contact).first() is not None:
        return jsonify({"error":"Contact is already in use"}),HTTP_409_CONFLICT

    try:
        #creating a new company
        new_company = Company(
            company_id=company_id,
            name=name,
            origin=origin,
            description=description,
            email=email,
            contact=contact,
            created_at=created_at,
            updated_at=updated_at) 
        db.session.add(new_company)
        db.session.commit()

        return jsonify({
             'message':name + "has been created successfully",
             'user':{
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

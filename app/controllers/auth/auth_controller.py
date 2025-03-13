from flask import Blueprint, request, jsonify
from app.status_code import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED
import validators
from app.models.author_model import Author
from app.extensions import db,bcrypt

#auth blueprint
auth = Blueprint("auth", __name__, url_prefix='api/v1/auth')

#user registration

@auth.route('/register',methods = ['POST'])
def register_user(): 

    #storing request values
    data = request.json   #JSON is javascript 
    # network calls we work with json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact = data.get('contact')
    email = data.get('email')
    password = data.get('password')
    image = data.get('image')
    biography = data.get('biography')

     #validation of data
    if not first_name or not last_name or not contact or not password or not email:
        return jsonify({"Error":"All fields are required"}), HTTP_400_BAD_REQUEST
    
     #Ensuring password is less than 8
    if len(password) < 8:
        return jsonify({"Error":"Password is invalid"}), HTTP_400_BAD_REQUEST
    
    if not validators.email(email):
        return jsonify({"Error":"Email is not valid"}), HTTP_400_BAD_REQUEST
    
    #
    if Author.query.filter_by(email=email).first() is not None:
        return jsonify({"Error":"Email is already in use."}),HTTP_409_CONFLICT
    
    if Author.query.filter_by(contact=contact).first() is not None:
        return jsonify({"Error":"Contact is already in use."}),HTTP_409_CONFLICT
    
    try:
        #hashing the password to ensure that data is not stolen(security meaasures)
        hashed_password =  bcrypt.generate_password_hash(password)

        #creating a new author
        new_author = Author(
            first_name=first_name,
            last_name = last_name,
            password= hashed_password,
            contact=contact,
            biography= biography,
            email=email,
            image = image
        )
        db.session.add(new_author)
        db.session.commit()

        #author name
        authorname = new_author.get_full_name()

        return jsonify({
            "message": authorname + " has been successfully created as an",
            "user": {
                "author_id":new_author.id,
                "first_name":new_author.first_name,
                "last_name":new_author.last_name,
                "email":new_author.email,
                "contact":new_author.contact,
                "biography":new_author.biography,
                "image":new_author.image
            }
        }),HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({"Error":str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    
    


    


    








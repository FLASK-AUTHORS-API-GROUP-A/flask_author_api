from flask import Blueprint, request, jsonify
from app.status_code import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK
import validators
from app.models.author_model import Author
from app.extensions import db,bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

#auth blueprint
auth = Blueprint("auth", __name__, url_prefix='/api/v1/auth')

#user registration

@auth.route('/create',methods = ['POST'])
def register_user(): 

    #storing request values
    data = request.json
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
    
    if len(password) < 8:
        return jsonify({"Error":"Password is invalid"}), HTTP_400_BAD_REQUEST
    
    if not validators.email(email):
        return jsonify({"Error":"Email is not valid"}), HTTP_400_BAD_REQUEST
    
    if Author.query.filter_by(email=email).first() is not None:
        return jsonify({"Error":"Email is already in use."}),HTTP_409_CONFLICT
    
    if Author.query.filter_by(contact=contact).first() is not None:
        return jsonify({"Error":"Contact is already in use."}),HTTP_409_CONFLICT
    
    try:
        #hashing the password
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
            "message": authorname + " has been successfully created as an" ,
            "user": {
                "author_id":new_author.author_id,
                "first_name":new_author.first_name,
                "last_name":new_author.last_name,
                "email":new_author.email,
                "password":new_author.password,
                "contact":new_author.contact,
                "biography":new_author.biography,
                "image":new_author.image
            }
        }),HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({"Error":str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    

#author login
@auth.route("/login", methods=['POST'])
def login():
    
    email = request.json.get('email')
    password = request.json.get('password')

    try:
        if not email or not password:
            return jsonify({"Error":"Email and password are required"}), HTTP_400_BAD_REQUEST 
        
        author = Author.query.filter_by(email=email).first()

        if author:
            correct_password = bcrypt.check_password_hash(Author.password,password)

            if correct_password:
                access_token = create_access_token(identity=str(author.author_id))
                refresh_token = create_refresh_token(identity=author.author_id)


                return jsonify({
                    "author":{'author':author.author_id,
                              'authorname' : author. get_full_name(),
                              'email': author.email,
                              'access_token' : access_token,
                              'refresh_token' : refresh_token
                              }
                             }),HTTP_200_OK
            else:
                return jsonify({"Error":"Invalid password"}),HTTP_401_UNAUTHORIZED

        else:
            return jsonify({"Error":"Invalid email"}),HTTP_401_UNAUTHORIZED
        

    except Exception as e:
        return jsonify({"Error":str(e)})
    

    #refresh tokens
    # We are using the `refresh=True` options in jwt_required to only allow
    # refresh tokens to access this route.
@auth.route("token/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({"access_token" : access_token})
    
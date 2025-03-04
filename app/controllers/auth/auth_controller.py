from flask import Blueprint, request, jsonify

auth = Blueprint("auth", __name__, url_prefix='api/v1/auth')

#user registration

@auth.route('/register',methods = ['POST'])
def register_user(): 
    data = request.json
    author_id = data.get('author_id')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact = data.get('contact')
    email = data.get('email')
    password = data.get('password')
    image = data.get('image')
    bio = data.get('bio','')if type == "author" else ''
    created_at = data.get('created_at')
    updated_at = data.get('updated_at')

    if not first_name or last_name or not contact or not password or not email:
        return 







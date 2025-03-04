class Config:
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:@localhost/flask_author_api_db" 
    
#if we are going to migrate one by one table
#class Config:
#    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:@localhost/authors_db"    
#    SQLALCHEMY_BINDS = {
#         "books_db" : "mysql+pymysql://root:@localhost/books_db" , #my db for class Book
#       "companies_db" : "mysql+pymysql://root:@localhost/companies_db" #my db for class Company
#                    }
    
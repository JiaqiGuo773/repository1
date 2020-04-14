from sqlalchemy import create_engine

def get_db():
    URI ="127.0.0.1"
    PORT ="3306"
    DB="mydb"
    USER="root"
    PASSWORD = "abc963215"
    
    return create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER,PASSWORD,URI,PORT,DB),echo=True)

    
import sys
sys.path.append('App')

from app import app

if __name__ == '__main__':
    # app.config['db_path']='./database/results.db'
    app.run()
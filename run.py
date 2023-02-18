from app import create_app
import os
from config import config

app = create_app(os.environ.get('FLASK_ENV') or 'default')

if __name__ == '__main__':
    app.run()

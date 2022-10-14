from src.web import create_app
from waitress import serve

app = create_app()

if __name__ == '__main__':
    serve(app, listen='*:8080')
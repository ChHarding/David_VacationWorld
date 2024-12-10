'''This module initializes and runs the Flask web application.
The application is created using the `create_app` function from the `website` package.
It runs in debug mode when executed directly.
Attributes:
    app (Flask): The Flask application instance created by `create_app`.
Usage:
    To run the application, execute this script directly. The application will start
    in debug mode.
    Example:
        $ python main.py
'''
from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

"""
from socket import gethostname
if 'liveweb' not in gethostname(): # all pythonanywhere servers have liveweb in their name
    if __name__ == '__main__':
        with app.app_context():
            db.create_all()
    app.run(debug=True, port=8081)
"""
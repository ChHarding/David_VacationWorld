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
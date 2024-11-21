from flask import Flask
from views.user_view import user
from views.task_view import task

app = Flask(__name__)
app.register_blueprint(user)
app.register_blueprint(task)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Project Python</h1>"

if __name__ == '__main__':
    app.run(debug=True)
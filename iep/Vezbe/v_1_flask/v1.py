# Example 1, Minimal app



from flask import Flask
from v1blueprint import bp

app = Flask(__name__);

app.register_blueprint(bp);

@app.route('/')
def index():
    return 'Index Page';

# Create route 
@app.route('/hello')
def hello_world():
    return '<h1>Hello, World!</h1>'

@app.route('/projects/')
def projects():
    return "The projects page!";

@app.route('/about')
def about():
    return 'The about page!'


from markupsafe import escape

@app.route('/user/<forname>/<surname>')
def show_user_profile(forname, surname):
    return f"User {escape(forname)} {escape(surname)}"


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post: {post_id}'


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return f'Subpath: {escape(subpath)}';


if __name__ == '__main__':
    app.run(debug=True);

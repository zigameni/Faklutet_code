from flask import Flask, request, jsonify;
from flask_sqlalchemy import SQLAlchemy
import sqlite3

# initialize app 
app = Flask(__name__);
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db';
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;

db = SQLAlchemy(app);


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True);
    username = db.Column(db.String(80), unique=True, nullable=False);
    email = db.Column(db.String(120), unique=True, nullable=False);

    def __repr__(self):
        return f'<User {self.username}';


# temp route
@app.route('/')
def index():
    return 'Hello, World!';


# add user
@app.route("/add_user", methods=['POST'])
def add_user():
    username = request.json['username'];
    email = request.json['email'];
    new_user = User(username=username, email=email);
    db.session.add(new_user);
    db.session.commit();

    return jsonify({'message': "User added successfully!"}), 201


# Get all users:
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all();
    output = [];
    for user in users:
        user_data = {'id': user.id, 'username': user.username, 'email': user.email};
        output.append(user_data);

    return jsonify({'users': output});


# update user
@app.route('/update_user/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    username = request.json.get('username', user.username)
    email = request.json.get('email', user.email)
    user.username = username
    user.email = email
    db.session.commit()
    return jsonify({"message": "User updated successfully!"})

# @app.route('/update_user/<int:id>', methods=['PUT'])
# def update_user(id):
#     return jsonify({"message": f"User with ID {id} updated successfully!"})

# delete user
@app.route('/delete_user/<int:id>', methods=["DELETE"])
def delete_user(id):
    user = User.query.get_or_404(id);
    db.session.delete(user);
    db.session.commit();
    return jsonify({"message": "User deleted successfully!"})

def init_db():
    with sqlite3.connect('instance/example.db') as con:
        with open('init.sql', 'r') as f:
            con.executescript(f.read())

if __name__ == '__main__':
    with app.app_context():
        init_db();
        db.create_all();
    app.run(debug=True);

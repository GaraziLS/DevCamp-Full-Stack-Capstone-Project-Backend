
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Integer, Column, String, UnicodeText, PrimaryKeyConstraint
from flask_marshmallow import Marshmallow
import os



app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class user(db.Model):
    user_id = db.Column(db.Integer, autoincrement= True, primary_key=True)
    user_email = db.Column(db.String(50), unique=True)
    user_password = db.Column(db.String(20), unique=False)

    def __init__(self, user_email, user_password):
        self.user_email = user_email
        self.user_password = user_password
    
class userSchema(ma.Schema):
    class Meta:
        fields = ("user_email", "user_password")

user_schema = userSchema()
users_schema = userSchema(many=True)


class item(db.Model):
    item_id = db.Column(db.Integer, autoincrement= True, primary_key=True)
    item_title = db.Column(db.String(100), unique=False)
    item_content = db.Column(db.UnicodeText, unique=False)
    item_user_id = db.Column(db.Integer, ForeignKey(user.user_id))

    def __init__(self, item_title, item_content, item_user_id):
        self.item_title = item_title
        self.item_content = item_content
        self.item_user_id = item_user_id

class itemSchema(ma.Schema):
    class Meta:
        fields = ("item_title", "item_content", "item_user_id")

item_schema = itemSchema()
items_schema = itemSchema(many=True)

# Endpoint to create a new item

@app.route("/create", methods=['POST'])
def add_item():
    title = request.json["item_title"]
    content = request.json["item_content"]
    item_user_id = request.json["item_user_id"]

    new_item = item(title, content, item_user_id)

    db.session.add(new_item)
    db.session.commit()

    Item = item.query.get(new_item.item_id)

    return item_schema.jsonify(item)


if __name__ == '__main__':
    app.run(debug=True)
 
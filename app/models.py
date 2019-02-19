from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index =True)
    role_id =db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String)

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))

    def __repr__(self):
        return f'User {self.name}'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Blog('{self.title}', '{self.date_posted}')"

# class Comment(db.Model):
#     __tablename__ = 'comments'

#     id = db.Column(db.Integer,primary_key = True)
#     comment = db.Column(db.String(1000))
#     user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
#     blog = db.Column(db.Integer,db.ForeignKey("blogs.id"))

#     def save_comment(self):
#         db.session.add(self)
#         db.session.commit()

#     @classmethod
#     def get_comments(cls,blog):
#         comments = Comment.query.filter_by(blog_id=blog).all()
#         return comments

# class Blog(db.Model):
#     __tablename__ = 'blogs'

#     id = db.Column(db.Integer,primary_key = True)
#     blog_title = db.Column(db.String)
#     blog_content = db.Column(db.String(1000))
#     category = db.Column(db.String)
#     posted = db.Column(db.DateTime,default=datetime.utcnow)
#     user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
#     likes = db.Column(db.Integer)
#     dislikes = db.Column(db.Integer)

#     comments = db.relationship('Comment',backref =  'blog_id',lazy = "dynamic")

#     def save_blog(self):
#         db.session.add(self)
#         db.session.commit()

#     @classmethod
#     def get_blogs(cls,category):
#         blogs = Blog.query.filter_by(category=category).all()
#         return blogs
#     @classmethod
#     def count_blogs(cls,uname):
#         user = User.query.filter_by(username=uname).first()
#         blogs = Pitch.query.filter_by(user_id=user.id).all()

#         blogs_count = 0
#         for blog in blogs:
#             blogs_count += 1

#         return blogs_count
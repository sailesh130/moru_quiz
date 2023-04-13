from flask_bcrypt import generate_password_hash, check_password_hash
from flask_user import UserManager
from flask_user import UserMixin
from app import app, db

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    roles = db.relationship('Role', secondary='user_roles', backref='user_role')

    def __init__(self, **kwargs):
        self.username = kwargs.get("username")
        self.email = kwargs.get("email")
        self.password = kwargs.get("password")
        self.active = kwargs.get("active")
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode("utf8")

    def check_password(self, password):

        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f'<User {self.name}>'


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey(
        'roles.id', ondelete='CASCADE'))


class Category(db.Model):
    tablename__ = 'category'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    questions = db.relationship('Question', backref='q_choices')

    def update_to_db(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()

    def __repr__(self):
        return f'<User {self.name}>'


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer(), primary_key=True)
    category = db.Column(db.Integer(), db.ForeignKey(
        'category.id', ondelete='CASCADE'))
    question_text = db.Column(db.Text)
    marks = db.Column(db.Integer())
    choices = db.relationship('Choice', backref='c_questions', lazy='dynamic')

    def update_to_db(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()

    def __repr__(self):
        return f'<Question {self.question_text}>'


class Choice(db.Model):
    __tablename__ = 'choice'
    id = db.Column(db.Integer(), primary_key=True)
    choice_text = db.Column(db.Text)
    question = db.Column(db.Integer(), db.ForeignKey(
        'question.id', ondelete='CASCADE'))
    is_correct = db.Column(db.Boolean())

    def update_to_db(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()

    def __repr__(self):
        return f'<User {self.choice_text}>'


class QuizProfile(db.Model):
    __tablename__ = 'quiz_profile'
    id = db.Column(db.Integer(), primary_key=True)
    user = db.Column(db.Integer(), db.ForeignKey(
        'users.id', ondelete='CASCADE'))
    total_score = db.Column(db.Integer(), default=0)
    attempted_questions = db.relationship('AttemptedQuestion', backref='quiz', lazy='dynamic')


class AttemptedQuestion(db.Model):
    __tablename__ = 'attempted_question'
    id = db.Column(db.Integer(), primary_key=True)
    quiz_profile = db.Column(db.Integer(), db.ForeignKey(
        'quiz_profile.id', ondelete='CASCADE'))
    selected_choice = db.Column(
        db.Integer(), db.ForeignKey('choice.id', ondelete='CASCADE'))
    question = db.Column(db.Integer(), db.ForeignKey(
        'question.id', ondelete='CASCADE'))
    category = db.Column(db.Integer(), db.ForeignKey(
        'category.id', ondelete='CASCADE'))
    is_correct = db.Column(db.Boolean())
    marks_obtained = db.Column(db.Integer(), default=0)


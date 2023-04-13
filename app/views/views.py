from flask_restful import Resource
from flask import request
from app.serializer import CreateSignupInputSchema, CreateLoginInputSchema, ChoiceSchema, CategorySchema, QuestionSchema
from app.models import User, Category, Question, Choice, QuizProfile, AttemptedQuestion, Role
from app import db
from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from app.permission import is_admin
from app import jwt

# api for user registration
class SignUpApi(Resource):

    def post(self):
        input_data = request.get_json()
        user_data = input_data.get("user_data")
        admin = input_data.get("is_admin")
        create_validation_schema = CreateSignupInputSchema()
        if errors := create_validation_schema.validate(user_data):
            return jsonify(message=errors, success=False, status=400)

        check_username_exist = User.query.filter_by(
            username=user_data.get("username")
        ).first()
        check_email_exist = User.query.filter_by(
            email=user_data.get("email")).first()
        if check_username_exist:
            return jsonify(message="Username already exist", success=False, status=400)

        elif check_email_exist:
            return jsonify(message="Email  already taken", success=False, status=400)

        role_name = "Admin" if admin else "User"
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
        new_user = User(**user_data)
        new_user.hash_password()
        new_user.roles = [role]
        db.session.add(new_user)
        db.session.commit()
        return jsonify(message="User created", success=True, status=201)

# api to login user(generate token)
class LoginApi(Resource):

    def post(self):

        input_data = request.get_json()
        create_validation_schema = CreateLoginInputSchema()
        if errors := create_validation_schema.validate(input_data):
            return jsonify(message=errors, success=False, status=400)

        get_user = User.query.filter_by(email=input_data.get("email")).first()
        if get_user is None:
            return jsonify(message="User not found", success=False, status=404)

        if get_user.check_password(input_data.get("password")):

            access_token = create_access_token(identity=get_user.email)
            return jsonify(access_token=access_token, success=True ,status=201)
        else:
            return jsonify(message="Password is wrong", success=False, status=400)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(email=identity).one_or_none()

# api to create, update and delete category model
class CategoryApi(Resource):
    method_decorators = [is_admin, jwt_required()]

    def get(self, id):
        category = Category.query.get(id)
        if not category:
            return jsonify(message="Category not found", success=False, status=404)

        category_schema = CategorySchema().dumps(category)
        return jsonify(data=category_schema, Success=True, status=200)

    def post(self, id=None):
        input_data = request.get_json()
        name = input_data.get("name", None)
        if errors := CategorySchema().validate(input_data):
            return jsonify(message=errors, success=False, status=400)

        if category := Category.query.filter_by(name=name).first():
            return jsonify(message="Category already exists", success=False, status=400)

        new_category = Category(**input_data)
        db.session.add(new_category)
        db.session.commit()
        return jsonify(data=CategorySchema().dump(new_category), success=True, status=201)

    def patch(self, id):

        if not (category := Category.query.get(id)):
            return jsonify(message="Category not found", success=False, status=404)

        input_data = request.get_json()
        if error := CategorySchema(partial=True).validate(input_data):
            return jsonify(message=error, success=False, status=400)

        category.update_to_db(request.json)
        return jsonify(data=CategorySchema().dump(category), success=True, status=200)

    def delete(self, id):
        if category := Category.query.get(4):
            db.session.delete(category)
            db.session.commit()
            return jsonify(message="Category deletion successful", success=True, status=200)
        else:
            return jsonify(message="Category not found", success=False, status=404)
        

# api to create, update and delete question model
class QuestionApi(Resource):
    method_decorators = [is_admin, jwt_required()]

    def get(self, id):
        question = Question.query.get(id)
        if not question:
            return jsonify(message="Question not found", success=False, status=404)

        question_schema = QuestionSchema().dump(question)
        return jsonify(data=question_schema, success=True, status=200)

    def post(self):
        input_data = request.get_json()
        print(input_data)
        question_text = input_data.get("question_text")
        if errors := QuestionSchema().validate(input_data):
            return jsonify(message=errors, success=False, status=400)

        if question := Question.query.filter_by(question_text=question_text).first():
            return jsonify(message="Question already exists", success=False, status=400)

        new_question = Question(**input_data)
        db.session.add(new_question)
        db.session.commit()
        return jsonify(data=QuestionSchema().dump(new_question), success=True, status=201)

    def patch(self, id):
        input_data = request.get_json()
        if not (question := Question.query.get(id)):
            return jsonify(message="Question not found", success=False, status=404)
        if error := QuestionSchema(partial=True).validate(input_data):
            return jsonify(message=error, success=False, status=400)

        question.update_to_db(request.json)
        return jsonify(data=QuestionSchema().dump(question), success=True, status=200)

    def delete(self, id):
        if question := Question.query.get(id):
            db.session.delete(question)
            db.session.commit()
            return jsonify(message="question deletion successful", success=True, status=200)
        else:
            return jsonify(message="Question not found", success=False, status=400)


# api to create, update and delete choice model
class ChoiceApi(Resource):
    method_decorators = [is_admin, jwt_required()]

    def get(self, id):
        choice = Choice.query.get(id)
        if not choice:
            return jsonify(message="Choice not found", success=False, status=404)

        choice_schema = ChoiceSchema().dump(choice)
        print(choice_schema)
        return jsonify(data=choice_schema, success=True, status=200)

    def post(self):
        input_data = request.get_json()
        question_id = input_data.get("question")
        choice_text = input_data.get("choice_text")
        if errors := ChoiceSchema().validate(input_data):
            return jsonify(message=errors, success=False, status=400)

        question = Question.query.get(question_id)
        total_choice = len(question.choices) if question else 0
        if total_choice >= 4:
            return jsonify(message="Only four choice can be added", success=False, status=400)
        if choice := Choice.query.filter_by(choice_text=choice_text).first():
            return jsonify(message="Choice already exists", success=False, status=400)

        new_choice = Choice(**input_data)
        db.session.add(new_choice)
        db.session.commit()
        return jsonify(data=ChoiceSchema().dump(new_choice), success=True, status=201)

    def patch(self, id):
        input_data = request.get_json()
        if not (choice := Choice.query.get(id)):
            return jsonify(message="Choice not found", success=False, status=404)

        if error := ChoiceSchema(partial=True).validate(input_data):
            return jsonify(message=error, success=False, status=400)

        choice.update_to_db(request.json)
        return jsonify(data=ChoiceSchema().dump(choice), success=True, status=200)

    def delete(self, id):
        if choice := Choice.query.get(id):
            db.session.delete(choice)
            db.session.commit()

            return jsonify(message="question deletion successful", success=True, status=200)
        else:
            return jsonify(message="Choice not found", success=False, status=404)
        

# api to list question given category id
class ListCategoryQuestions(Resource):
    @jwt_required()
    def get(self, id):
        category = Category.query.get(id)
        if not category:
            return jsonify(message="Category not found", success=False, status=404)
        questions = category.questions
        questionschema = QuestionSchema(many=True).dump(questions)
        return jsonify(data=questionschema, success=True, status=200)
        

# api to play and view to attempt question given the categoty
class PlayQuiz(Resource):

    method_decorators = [jwt_required()]

    def _get_object(self):
        quiz_profile = QuizProfile.query.filter_by(
            user=current_user.id).one_or_none()
        if not quiz_profile:
            quiz_profile = QuizProfile(user=current_user.id)
            db.session.add(quiz_profile)
            db.session.commit()
        return quiz_profile

    def get(self, id):

        quiz_profile = self._get_object()

        attempted_questions = quiz_profile.attempted_questions.filter_by(
            category=id).all()
        pks = [question.question for question in attempted_questions]
        to_attempt = [q for q in Question.query.filter(
            Question.id.notin_(pks)) if len(list(q.choices)) == 4]
        questionschema = QuestionSchema(many=True).dump(to_attempt)
        return jsonify(data=questionschema, success=True, status=200)

    def post(self):
        quiz_profile = self._get_object()
        input_data = request.get_json()
        question_pk = input_data.get('question_pk')
        category_pk = input_data.get('category_pk')
        choice_pk = input_data.get('choice_pk')
        attempted_question = AttemptedQuestion.query.filter_by(
            question=question_pk).one_or_none()

        if attempted_question:
            return jsonify(message="Question already attempted", success=False, status=400)
        question = Question.query.get(question_pk)
        choice = question.choices.filter_by(is_correct=True).first()
        if not question or not choice:
            return jsonify(message="question_id or choice_id missing", success=False, status=400)
        marks_obtained = question.marks if choice.id == choice_pk else 0
        attempted_question = AttemptedQuestion(quiz_profile=quiz_profile.id, selected_choice=choice_pk,
                                               question=question_pk, category=category_pk, marks_obtained=marks_obtained, is_correct=choice.is_correct)
        db.session.add(attempted_question)
        quiz_profile.total_score += marks_obtained
        db.session.commit()

        return jsonify(message="Choice submitted", success=True, status=200)
    

# api to view score
class ViewScore(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        quiz_profile = QuizProfile.query.filter_by(
            user=current_user.id).first()
        if not quiz_profile:
            return jsonify(total_score=0, category_score=0)
        total_score = quiz_profile.total_score
        category_score = quiz_profile.attempted_questions.join(Category, AttemptedQuestion.category == Category.id).with_entities(
            Category.name, db.func.sum(AttemptedQuestion.marks_obtained).label("marks_obtained")).group_by(Category.name).all()
        category_score = {record[0]: record[1] for record in category_score}
        return jsonify(data={"total_score": total_score, "category_score": category_score}, success=True, status=200)

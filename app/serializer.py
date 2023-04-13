from marshmallow import Schema, fields, validate,post_dump
from flask_jwt_extended import current_user
class CreateSignupInputSchema(Schema):
 
    username = fields.Str(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    active = fields.Boolean(required=True)
    first_name = fields.Str(required=True, validate=validate.Length(min=3))
    last_name = fields.Str(required=True, validate=validate.Length(min=3))

class CreateLoginInputSchema(Schema):
  
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))



class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=4))
    questions = fields.Nested("QuestionSchema", only=("id", "question_text", "marks"), many=True,dump_only=True)

class QuestionSchema(Schema):
    id = fields.Int(dump_only=True)
    question_text = fields.Str(required=True, validate=validate.Length(min=3))
    category = fields.Int()
    marks = fields.Int(validate=validate.Range(min=1))
    choices = fields.Nested("ChoiceSchema", only=("id", "choice_text" ), many=True, dump_only=True)

class ChoiceSchema(Schema):
    id = fields.Int(dump_only=True)
    question = fields.Int(required=True)
    choice_text = fields.Str(required=True, validate=validate.Length(min=1))
    is_correct = fields.Boolean(required=True)

    @post_dump(pass_many=True)
    def wrap_with_envelope(self, data, many, **kwargs):
        if "Admin"  not in [role.name for role in current_user.roles]:
            del data["is_correct"]
        return data


        

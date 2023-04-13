from app import  api 
from app.views import LoginApi, SignUpApi, ListCategoryQuestions, ViewScore, CategoryApi, ChoiceApi, QuestionApi,PlayQuiz

api.add_resource(LoginApi, '/login')
api.add_resource(SignUpApi, '/signup')
api.add_resource(CategoryApi, '/category/<int:id>','/category' )
api.add_resource(QuestionApi, '/question/<int:id>','/question')
api.add_resource(ChoiceApi, '/choice/<int:id>','/choice')
api.add_resource(ListCategoryQuestions, '/list_questions/<int:id>')
api.add_resource(PlayQuiz, '/play/<int:id>','/play')
api.add_resource(ViewScore, '/score')
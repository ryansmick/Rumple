# Python file to interact with the database at a higher level than the django db implementation

from polls.models import Question, Option, Vote

class DBInterface:

    # Create a new poll in the database
    # question_text is a string containing the question
    # creator_id is an integer representing the user id of the poll creator
    # options is a list of strings for the options for the poll
    @staticmethod
    def create_poll(question_text, creator_id, options):
        # Create the question
        question = Question.objects.create(question_text=question_text, creator_id=creator_id)
        
        # Create all options and relate them to question
        for option in options:
            Option.objects.create(question=question, option_text=option)


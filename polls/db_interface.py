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

    # Add a new vote to a question
    @staticmethod
    def submit_vote(user_id, question_id, option_number):
        # Check if the user has already submitted a vote for the given question
        options = DBInterface.get_sorted_options_for_question(question_id)
        votes = DBInterface.get_all_votes_for_question(question_id)
        
        # Get previous vote if it exists
        previous_vote = None
        for vote in votes:
            if vote.voter_id == user_id:
                previous_vote = vote
                break

        # Identify chosen option
        chosen_option = options[option_number-1]

        # If the user previously voted on the question, update his vote
        if previous_vote:
            # Update vote
            previous_vote.option = chosen_option
            previous_vote.save()
        else:
            # Create a new vote
            Vote.objects.create(voter_id=user_id, option=chosen_option)

    # Return list containing all votes for a given question
    @staticmethod
    def get_all_votes_for_question(question_id):
        options = DBInterface.get_sorted_options_for_question(question_id)

        votes = []
        for option in options:
            votes += DBInterface.get_votes_for_option(option.id)

        return votes

    # Return the options for a given question in order by their id's
    @staticmethod
    def get_sorted_options_for_question(question_id):
        return Question.objects.get(id=question_id).option_set.order_by('id').all()

    # Return a list of votes for a given option
    @staticmethod
    def get_votes_for_option(option_id):
        return Option.objects.get(id=option_id).vote_set.all()

from django.test import TestCase
from polls.models import Question, Option, Vote
from polls.db_interface import DBInterface

# Create your tests here.

class TestDBInteraction(TestCase):
    
    # Test to ensure creating questions is functioning properly
    def test_question_creation(self):

        DBInterface.create_poll("How are you?", 4, ["Good", "Not so good", "Terrible"])
        
        self.assertEqual(len(Question.objects.all()), 1)
        self.assertEqual(Question.objects.first().question_text, "How are you?")
        self.assertEqual(len(Option.objects.all()), 3)
        self.assertEqual(len(Option.objects.filter(option_text="Good")), 1)

    # Test that multiple users can vote for the same option for a given question
    def test_multiple_votes_for_same_option(self):

        question = Question.objects.create(question_text="How are you?", creator_id=4)
        Option.objects.create(question=question, option_text="Good")
        Option.objects.create(question=question, option_text="Not so good")
        Option.objects.create(question=question, option_text="Terrible")
        question_id = question.id

        DBInterface.submit_vote(2, question_id, 3) # User id, question id, option number
        DBInterface.submit_vote(3, question_id, 3)

        self.assertEqual(len(Vote.objects.all()), 2)

    # Test that a user can only submit one vote per question
    def test_one_vote_per_user_per_question(self):
        
        question = Question.objects.create(question_text="How are you?", creator_id=4)
        Option.objects.create(question=question, option_text="Good")
        Option.objects.create(question=question, option_text="Not so good")
        Option.objects.create(question=question, option_text="Terrible")
        question_id = question.id

        DBInterface.submit_vote(2, question_id, 3)

        self.assertEqual(len(Vote.objects.all()), 1) 
        self.assertEqual(Vote.objects.first().option.option_text, "Terrible") 

        DBInterface.submit_vote(2, question_id, 2)

        self.assertEqual(len(Vote.objects.all()), 1) 
        self.assertEqual(Vote.objects.first().option.option_text, "Not so good") 

    # Test option ordering
    def test_options_sorted_by_id(self):
        question = Question.objects.create(question_text="How are you?", creator_id=4)
        option1 = Option.objects.create(question=question, option_text="Good")
        option2 = Option.objects.create(question=question, option_text="Not so good")
        option3 = Option.objects.create(question=question, option_text="Terrible")
        Vote.objects.create(option=option2, voter_id=1)
        Vote.objects.create(option=option3, voter_id=2)
        Vote.objects.create(option=option3, voter_id=3)
        question_id = question.id

        options = DBInterface.get_sorted_options_for_question(question_id)
        options = [option.option_text for option in options]

        self.assertEqual(options, ["Good", "Not so good", "Terrible"])

    # Test that all votes can be retrieved for a given question
    def test_get_all_votes_for_question(self):
        
        question = Question.objects.create(question_text="How are you?", creator_id=4)
        option1 = Option.objects.create(question=question, option_text="Good")
        option2 = Option.objects.create(question=question, option_text="Not so good")
        option3 = Option.objects.create(question=question, option_text="Terrible")
        Vote.objects.create(option=option2, voter_id=1)
        Vote.objects.create(option=option3, voter_id=2)
        Vote.objects.create(option=option3, voter_id=3)
        question_id = question.id

        votes = DBInterface.get_all_votes_for_question(question_id)

        self.assertEqual(len(votes), 3)
        self.assertTrue(type(votes[0]) is Vote)


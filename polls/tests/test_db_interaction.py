from django.test import TestCase
from polls.models import Question, Option, Vote
from polls.db_interface import DBInterface

# Create your tests here.

class TestDBInteraction(TestCase):
    
    # Test to ensure creating questions is functioning properly
    def test_question_creation(self):
        self.assertEqual(len(Question.objects.all()), 0)

        DBInterface.create_poll("How are you?", 4, ["Good", "Not so good", "Terrible"])
        
        self.assertEqual(len(Question.objects.all()), 1)
        self.assertEqual(Question.objects.first().question_text, "How are you?")
        self.assertEqual(len(Option.objects.all()), 3)
        self.assertEqual(len(Option.objects.filter(option_text="Good")), 1)



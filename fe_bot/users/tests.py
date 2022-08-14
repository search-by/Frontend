from django.test import TestCase


class TestCase1(TestCase):
    def setUp(self):
        print("Pre Test")
        pass

    def setUp1(self):
        print("Test")
        i = 434/0
        self.assertFalse(False)
        return "asda"
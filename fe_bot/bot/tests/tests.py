from __future__ import absolute_import
import random

import pytest

from bot.tests.test_commandhandler import TestCommandHandler
from telegram import Update
import unittest
from telegram.ext import Updater
from django_telegrambot.apps import DjangoTelegramBot
from fe_bot.settings import TOKEN
FIRST, SECONT, THIRD, FOURTH, PROPOSAL1, PROPOSAL2, PLATEGKA1, PLATEGKA2, LIQPAY = range(9)


bot = Updater(TOKEN)
dp = DjangoTelegramBot.dispatcher
f = TestCommandHandler()


class UpdateTestClass():
    def __init__(self, update: Update, id=False):
        self.update = update
        if id == False:
            self.id = random.randint(1111111111, 9999999999)
        else:
            self.id = id

    def chenge_update(self):
        self.update.message.chat.id = f"{self.id}"
        self.update.message.chat.username = f"{self.id}"
        self.update.message.chat.first_name = f"{self.id}"
        #self.update.message.username = f"{self.id}"
        #self.update.message.first_name = f"{self.id}"
        #self.update.message.last_name = f"{self.id}"
        self.update.message.from_user.id = f"{self.id}"
        #self.update.message.from_user.first_name = f"{self.id}"
        self.update.message.from_user.last_name = f"{self.id}"
        self.update.message.from_user.username = f"{self.id}"

    def set_comand(self, text):
        self.update.message.text = text
        self.update.message.entities[0].type = 'bot_command'
        self.update.message.entities[0].offset = 0
        self.update.message.entities[0].length = 6

    def get_update(self) -> Update:
        return self.update


@pytest.mark.usefixtures("TestCommandHandler")
class TestClass(unittest.TestCase):
    @pytest.mark.usefixtures("command")
    def setUp(self):
        pass

    def test_command(self):
        print("Method: test_one_plus_one_equals_two.")

        f.test_basic(dp=dp,command=self.CMD)
        self.assertEqual(f.test_basic(dp=dp,command='\start'), self.CMD)

    def test_make_command_update(self):
        print("a")
        #self.up = self.command_update(self.cm)
        #TestCommandHandler.test_basic(dp=dp, '\start')
        #self.b = TestCommandHandler()
        #self.b.test_basic(self, command=TestCommandHandler.command)
        #self.comand = TestCommandHandler.command
        #print(self.command_message())
        self.assertEqual(self.CMD, 1)




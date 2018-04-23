from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

# choose set to train from
path = './assets/train/data/'
training_set = 'training_data'

# create and train bot
bot = ChatBot(
    "Manual Bot",
    logic_adapters=[
        # "chatterbot.logic.MathematicalEvaluation",
        # "chatterbot.logic.TimeLogicAdapter",
        "chatterbot.logic.LowConfidenceAdapter",
        # "chatterbot.logic.SpecificResponseAdapter",
        "chatterbot.logic.BestMatch"
    ],
    database="./assets/bots/database/manual.db",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    input_adapter="chatterbot.input.TerminalAdapter",
    output_adapter="chatterbot.output.TerminalAdapter"
)

CONVERSATION_ID = bot.storage.create_conversation()


def get_feedback():
    from chatterbot.utils import input_function

    text = input_function()

    if 'y' in text.lower():
        return False
    elif 'n' in text.lower():
        return True
    else:
        print('Please type either "y" or "n"')
        return get_feedback()


print("Type something to begin...")

# The following loop will execute each time the user enters input
while True:
    try:
        print('Say something: ')

        input_statement = bot.input.process_input_statement()
        statement, response = bot.generate_response(input_statement, CONVERSATION_ID)

        bot.output.process_response(response)
        print('\n Is "{}" a coherent response to "{}"? \n'.format(response, input_statement))
        if get_feedback():
            # print('Update conversation?')
            # if get_feedback() == False:
            print("please input the correct response")
            response1 = bot.input.process_input_statement()
            bot.learn_response(response1, input_statement)
            bot.storage.add_to_conversation(CONVERSATION_ID, statement, response1)
            print("Responses added to bot!")

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break

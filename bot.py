import requests  
import os
from flask import Flask, Response, request

BOT_URL = f'https://api.telegram.org/bot{os.environ["BOT_KEY"]}/' # <--- add your telegram token as environment variable in your system


def get_chat_id(data):  
    """
    Method to extract chat id from telegram request.
    """
    chat_id = data['message']['chat']['id']

    return chat_id

def get_message(data):  
    """
    Method to extract message id from telegram request.
    """
    message_text = data['message']['text']

    return message_text

def send_message(prepared_data):  
    """
    Prepared data should be json which includes at least `chat_id` and `text`
    """ 
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=prepared_data)  # don't forget to make import requests lib

def change_text_message(text):  
    """
    To enable turning our message inside out
    """
    return text[::-1]

def prepare_data_for_answer(data):  
    answer = change_text_message(get_message(data))

    json_data = {
        "chat_id": get_chat_id(data),
        "text": answer,
    }

    return json_data


app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():  
    data = request.json
    # I recommend you to see this data in the debugger

    answer_data = prepare_data_for_answer(data)
    send_message(answer_data)

    return ''


if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

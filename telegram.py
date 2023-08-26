import os
import telebot
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import  service_pb2_grpc
from dotenv import load_dotenv
from langchain.llms import Clarifai
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import LLMChain

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import csv
from io import BytesIO
import spacy
from spacy.matcher import Matcher



load_dotenv()
nlp = spacy.load("en_core_web_sm")

# 
APP_ID = 'FINGU'
WORKFLOW_ID = 'workflow-ad5299'
# CLARIFAI_PAT = getpass()
llm = Clarifai(pat=PAT, user_id='clarifai', app_id='ml', model_id='llama2-7b-alternative-4k')
role_prompt = (
    "<s>\n"
    "<<SYS>> \n"
    "You are FINGU Financial Assistant.\n"
    "Your role is to provide useful and practical financial advice, and you can assist in creating financial plans.\n" 
    "You should respond within context only.\n"
    "Please consider the chat history provided as a reference to better understand the user's context and needs.\n"
    "Keep in mind that your responses should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Make sure your answers are socially unbiased and positive in nature.\n"
    "Feel free to ask clarifying questions if the user's query is unclear.\n"
    "If a question doesn't make sense or isn't factually coherent, explain why instead of providing incorrect information.\n"
    "Remember, the chat history is provided to assist you in giving relevant advice.\n"
    "The following lines will be the chat history in roles as 'AI:' and 'Human:' you will use those to take relevant information, the last 'Human:' line is the real prompt\n "
    "Stay within the 1040-character limit.\n"
    "If user asks to respond with csv file or needs something formatted as csv mention that he should use /csv command And always type any csv list formatted as csv \n "
    "You should respond normally without the Ai and Human roles i use, i will use them you shouldn't"
    "<</SYS>>\n"
    
    "[INST]\n"

)

prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            role_prompt
        ),
        # The `variable_name` here is what must align with memory
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ]
)
# memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=4000)
memory =  ConversationSummaryBufferMemory(memory_key="history", llm=llm , return_messages=True , max_token_limit=4000)


conversation = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory
)
# Set up the Telegram bot
bot = telebot.TeleBot(BOT_TOKEN)

# Set up the Clarifai channel
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)
metadata = (('authorization', 'Key ' + PAT),)
# Function to save the LLMChain response to a CSV file
def save_response_to_csv(response_text):
    lines = response_text.split('\n')

    # Initialize variables
    data = []
    header = None
    separator = None

    for line in lines:
        line = line.strip()
        if line.startswith('|') or line.startswith('.'):
            if separator is None:
                separator = '|' if '|' in line else '.'
            cells = [cell.strip() for cell in line.split(separator)]
            if len(cells) >= 2:
                if header is None:
                    header = cells[1]
                data.append(cells[1:])  # Extract all cells

    if header is not None:
        with open('response.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([header])  # Write header
            csvwriter.writerows(data)  # Write data


@bot.message_handler(commands=['csv'])
def save_response_as_csv(message):
    if message.reply_to_message and message.reply_to_message.text:
        input_prompt = message.reply_to_message.text
        response = generate_response_llmchain(input_prompt)
        
        save_response_to_csv(response)
        
        # Send the CSV file with the LLMChain response
        with open('response.csv', 'rb') as csv_file:
            bot.send_document(message.chat.id, csv_file)

# Handle start and hello commands
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    welcome_message = (
        "Welcome to FINGU Financial Assistant!\n"
        "I'm here to help you with financial queries.\n"
        "If you have any financial questions or problems, feel free to ask."
    )
    bot.reply_to(message, welcome_message)

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    if message.text:
        input_text = message.text
        response = generate_response_llmchain(input_text)
        bot.reply_to(message, response)



def generate_response_llmchain(prompt):
    memory.load_memory_variables({})

    input_prompt = 'Dont start with Ai or Human,now here is my prompt:' +prompt + " [/INST]"

    ans = conversation.predict(input=input_prompt)
    response = ans  # You can process or modify the response here if needed
    return response
# Start the bot's polling loop
bot.infinity_polling()

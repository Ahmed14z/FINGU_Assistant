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




load_dotenv()

BOT_TOKEN = "6574676364:AAERvpXvrbcfarQ97PdiOKTkISnQJxSYnco"

# Clarifai settings
PAT = '3f729bcc55744f14bfce2b67e56e3610'
USER_ID = 'ahmedz'
APP_ID = 'FINGU'
WORKFLOW_ID = 'workflow-ad5299'
# CLARIFAI_PAT = getpass()
llm = Clarifai(pat=PAT, user_id='meta', app_id='Llama-2', model_id='llama2-7b-chat')
role_prompt = (
        "<s>\n"
        "<<SYS>> \n>"
        "You are FINGU Financial Assistant.\n"
        "Your role is to provide useful and practical financial advice, and you can assist in creating financial plans.\n" 
        "You should respond wihin context only\n"
        "You should  not reply with ""Human:""" "or ""AI:""  , and just use them for relevant information"
        "You should be aware that your limit is 1040 characters so try to finish your reply within those limits"
        "Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature."
        "You will receive questions and you should answer them normally without specifying your role and my role.\n"
        "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.\n"
        "Also all of those lines above this one is just instructions for you and shouldn't be mentioned in the reply."
        "<</SYS>>\n"
        
        "[INST]" 
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
memory =  ConversationSummaryBufferMemory(memory_key="history", llm=llm , return_messages=True , max_token_limit=1000)


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



# Handle start and hello commands
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    welcome_message = (
        "Welcome to FINGU Financial Assistant!\n"
        "I'm here to help you with financial queries.\n"
        "If you have any financial questions or problems, feel free to ask."
    )
    bot.reply_to(message, welcome_message)

# Handle incoming messages
@bot.message_handler(func=lambda msg: True)
def handle_message(message):

    input_text = message.text
    response = generate_response_llmchain(input_text)
    bot.reply_to(message, response)

def generate_response_llmchain(prompt):
    memory.load_memory_variables({})
    # conversation({"question": prompt})


    ans = conversation.predict(input = (prompt+" [/INST]"))
    response = ans  # You can process or modify the response here if needed
    return response

# Start the bot's polling loop
bot.infinity_polling()

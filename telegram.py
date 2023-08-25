import os
import telebot
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

# Telegram bot token
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Clarifai settings
PAT = 'PAT'
USER_ID = 'ID'
APP_ID = 'APP'
WORKFLOW_ID = 'workflow'

# Set up the Telegram bot
bot = telebot.TeleBot(BOT_TOKEN)

# Set up the Clarifai channel
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)
metadata = (('authorization', 'Key ' + PAT),)

# Function to generate response using Clarifai
def generate_response_clarifai(prompt):
    # Define the role and purpose of the model in the prompt
   role_prompt = (
        "<s>[INST] <<SYS> \n>"
        "You are FINGU Financial Assistant.\n"
        "Your role is to provide useful and practical financial advice, and you can assist in creating financial plans.\n" 
        "You should respond wihin context only\n"
        "Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature."
        # "You will receive questions and you should answer them normally without specifying your role and my role.\n"
        "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.\n"
        "<</SYS>>" + prompt + " [/INST]"
    )

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    response = ""  # save response from the model

    post_workflow_results_response = stub.PostWorkflowResults(
        service_pb2.PostWorkflowResultsRequest(
            user_app_id=userDataObject,
            workflow_id=WORKFLOW_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw=role_prompt  # Use the modified prompt
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )

    if post_workflow_results_response.status.code != status_code_pb2.SUCCESS:
        print(post_workflow_results_response.status)
        return response

    results = post_workflow_results_response.results[0]

    for output in results.outputs:
        model = output.model
        response += output.data.text.raw + "\n"

    return response


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
    # Generate response using Clarifai
    asyncio.run(handle_clarifai_response(bot, message, input_text))

async def handle_clarifai_response(bot, message, input_text):
    response = await asyncio.to_thread(generate_response_clarifai, input_text)
    bot.reply_to(message, response)

# Start the bot's polling loop
bot.infinity_polling()

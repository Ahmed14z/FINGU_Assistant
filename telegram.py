import os
import io
import telebot
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import pandas as pd
from dotenv import load_dotenv
import asyncio  # For asynchronous processing (if supported by telebot)

# Load environment variables
load_dotenv()

# Telegram bot token
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Clarifai settings
PAT = PAT
USER_ID = USERID
APP_ID = APPID
WORKFLOW_ID = 'workflow-ad5299'

# Set up the Telegram bot
bot = telebot.TeleBot(BOT_TOKEN)

# Set up the Clarifai channel
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)
metadata = (('authorization', 'Key ' + PAT),)

# Function to generate response using Clarifai
def generate_response_clarifai(prompt):
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
                            raw=prompt
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

    if "upload" in input_text.lower():
        bot.reply_to(message, "Sure! Please upload your CSV file.")
    else:
        # Generate response using Clarifai
        asyncio.run(handle_clarifai_response(bot, message, input_text))

async def handle_clarifai_response(bot, message, input_text):
    response = await asyncio.to_thread(generate_response_clarifai, input_text)
    bot.reply_to(message, response)

# Function to generate advice based on CSV data
def generate_advice(df):
    # Here you can implement your logic to analyze the CSV data
    # and generate meaningful advice
    advice = "Based on the data in the CSV file:\n"
    advice += "I suggest that you analyze the data and consider the following factors for your financial decisions."
    return advice

# Handle document uploads
@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_extension = message.document.file_name.split('.')[-1]

    if file_extension == 'csv':
        try:
            # Convert the downloaded bytes into a file-like object
            file_obj = io.BytesIO(downloaded_file)
            
            # Load the CSV data into a pandas DataFrame
            df = pd.read_csv(file_obj)
            
            # Generate advice based on the CSV data
            advice = generate_advice(df)
            
            bot.reply_to(message, advice)

        except Exception as e:
            bot.reply_to(message, f"An error occurred while processing the CSV file: {e}")

    else:
        bot.reply_to(message, "I'm sorry, I can only handle CSV files at the moment.")

# Start the bot's polling loop
bot.infinity_polling()

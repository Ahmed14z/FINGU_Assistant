# FINGU Financial Assistant Telegram Bot

This Telegram bot serves as a Financial Assistant, designed to provide financial advice and support to users. It is powered by the Llama 2 language model using Clarifai's technology. The bot is optimized to generate more useful and contextually relevant responses, and it offers special features like CSV file interaction and multi-user memory management.

## Features

1. **Enhanced Financial Advice:** The bot leverages the power of the Llama 2 language model, integrated with Clarifai, to provide improved financial advice and support.

2. **CSV Interaction:** The bot can interact with CSV files. You can upload a CSV file, and the bot will engage in a conversation based on the content of the file. Similarly, you can request the bot to generate a CSV file as a response.

3. **Memory Management:** The bot utilizes LangChain memory to maintain separate conversation memories for different users. It helps the bot retain context and provide personalized responses.

4. **Clear Memory:** The `/newchat` command allows users to clear their conversation memory and start a new chat session with the bot.

## Algorithm and Pipeline

The bot's functionality is orchestrated using the following steps:

1. **User Interaction:** The bot interacts with users through Telegram messages. It listens for commands, prompts, and uploads.

2. **Llama 2 Model with Clarifai:** To generate meaningful financial advice, the bot employs the Llama 2 language model with Clarifai's technology. It understands user inputs and generates contextually relevant responses.

3. **Role Prompt Optimization:** The bot starts each conversation with a carefully designed role prompt that helps guide the bot's behavior. This role prompt is optimized to provide useful responses, eliminating excessive randomness.

4. **CSV Interaction:** Users can upload CSV files, and the bot processes the content of the file using regular expressions to remove date and time formats. It then uses this processed content to formulate a conversation with the user.

5. **Memory Management:** LangChain's memory management allows the bot to maintain separate conversation histories for each user. This enables the bot to recall past interactions and provide more personalized advice.

6. **Clear Memory Command:** The `/newchat` command allows users to clear their conversation memory. This is especially useful when users want to start a fresh chat session.

## Usage

1. Start a chat with the bot using `/start` or `hello` command.

2. Engage in financial conversations with the bot. It provides advice and answers related to personal finance.

3. Upload a CSV file to chat. The bot will process the content and engage in a conversation based on the file's data.

4. Use the `/csv` command in reply to the desired chat or prompt to generate a CSV file as a response.

5. Utilize the `/newchat` command to clear your current conversation memory and start a new chat session.

## Installation and Setup

1. Clone this repository.

2. Install the required packages using `pip install -r requirements.txt`.

3. Run python -m spacy download en_core_web_sm

4. Set up a Telegram bot and obtain the API token.

5. Set up Clarifai and obtain the necessary credentials.

6. Replace the placeholders for Clarifai credentials and Telegram bot token in the code.

7. Run the bot script using `python telegram.py`.

## Conclusion

The Financial Assistant Telegram Bot offers an enhanced way to interact with financial advice using natural language. With CSV interaction, personalized memory management, and optimized role prompts, the bot provides a comprehensive and helpful experience for users seeking financial guidance.

import telebot
from huggingface_hub import InferenceClient
from PIL import Image


# Telegram Bot Token
BOT_TOKEN = "7143865123:AAGAgu57BIpDpMbwM7Y9nL4kFMLJLuMJYHE"

# Hugging Face API Token and Model
HUGGINGFACE_API_TOKEN = "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"
MODEL_NAME = "stabilityai/stable-diffusion-3.5-large"

# Initialize Hugging Face Inference Client
client = InferenceClient(token=HUGGINGFACE_API_TOKEN)

# Initialize Telegram Bot
bot = telebot.TeleBot(BOT_TOKEN)

# Function to generate an image from text
def generate_image(prompt):
    try:
        # Generate image from text prompt
        image = client.text_to_image(prompt, model=MODEL_NAME)
        return image  # Returns PIL.Image object
    except Exception as e:
        return str(e)

# Start command handler
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Welcome to the AI Bot! Send me a prompt, and I'll generate an image for you using Stable Diffusion.",
    )

# Handle text messages to generate images
@bot.message_handler(func=lambda message: True, content_types=["text"])
def handle_prompt(message):
    prompt = message.text
    bot.send_message(message.chat.id, "Generating your image... Please wait.")
    try:
        # Generate image
        image = generate_image(prompt)
        if isinstance(image, str):  # Error occurred
            bot.send_message(message.chat.id, f"Error: {image}")
        else:
            # Save and send the image
            image_path = f"{message.chat.id}_generated_image.png"
            image.save(image_path)
            with open(image_path, "rb") as img:
                bot.send_photo(message.chat.id, img)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {e}")

# Run the bot
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling()

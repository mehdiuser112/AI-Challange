import os
import telebot
from huggingface_hub import InferenceClient
from PIL import Image
import sqlite3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Securely load tokens from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
MODEL_NAME = "stabilityai/stable-diffusion-3.5-large"

# Initialize Hugging Face Inference Client
client = InferenceClient(token=HUGGINGFACE_API_TOKEN)

# Initialize Telegram Bot
bot = telebot.TeleBot(BOT_TOKEN)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        telegram_id INTEGER UNIQUE)''')
    conn.commit()
    conn.close()

def add_user(username, telegram_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (username, telegram_id) VALUES (?, ?)", (username, telegram_id))
    conn.commit()
    conn.close()

# Function to generate images from text prompt
def generate_image(prompt, num_images=1):
    try:
        images = []
        for _ in range(num_images):
            image = client.text_to_image(prompt, model=MODEL_NAME)
            images.append(image)
        return images  # List of PIL.Image objects
    except Exception as e:
        return str(e)

# Start command handler
@bot.message_handler(commands=["start"])
def send_welcome(message):
    username = message.chat.username
    telegram_id = message.chat.id
    add_user(username, telegram_id)
    bot.send_message(
        message.chat.id,
        "Welcome to the AI Bot! Send me a prompt, and I'll generate images for you using Stable Diffusion.\n\n" +
        "To generate multiple images, use the format: <prompt>;<number of images>."
    )

# Handle text messages to generate images
@bot.message_handler(func=lambda message: True, content_types=["text"])
def handle_prompt(message):
    bot.send_chat_action(message.chat.id, "typing")
    parts = message.text.split(";")
    prompt = parts[0]
    num_images = int(parts[1]) if len(parts) > 1 else 1

    if num_images > 5:
        bot.send_message(message.chat.id, "Please limit the number of images to 5.")
        return

    bot.send_message(message.chat.id, "Generating your images... Please wait.")

    try:
        images = generate_image(prompt, num_images=num_images)
        if isinstance(images, str):  # Error occurred
            bot.send_message(message.chat.id, f"Error: {images}")
        else:
            for idx, image in enumerate(images):
                image_path = f"{message.chat.id}_generated_image_{idx}.png"
                image.save(image_path)
                with open(image_path, "rb") as img:
                    bot.send_photo(message.chat.id, img)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {e}")

# Main function to start the bot
if __name__ == "__main__":
    print("Bot is running...")
    init_db()
    bot.polling()


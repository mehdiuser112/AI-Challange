from telebot import TeleBot
from huggingface_hub import InferenceClient
from PIL import Image
import sqlite3
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Securely load tokens from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
MODEL_NAME = "stabilityai/stable-diffusion-3.5-large"

# Initialize Hugging Face Inference Client
client = InferenceClient(token=HUGGINGFACE_API_TOKEN)

# Initialize Telegram Bot
bot = TeleBot(BOT_TOKEN)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("gallery.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS images (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        prompt TEXT,
                        image_path TEXT)''')
    conn.commit()
    conn.close()

def add_image_to_gallery(user_id, prompt, image_path):
    conn = sqlite3.connect("gallery.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO images (user_id, prompt, image_path) VALUES (?, ?, ?)", (user_id, prompt, image_path))
    conn.commit()
    conn.close()

def get_user_gallery(user_id):
    conn = sqlite3.connect("gallery.db")
    cursor = conn.cursor()
    cursor.execute("SELECT prompt, image_path FROM images WHERE user_id = ?", (user_id,))
    results = cursor.fetchall()
    conn.close()
    return results

# Function to generate images with customization
def generate_image(prompt, resolution="512x512", style=None):
    try:
        full_prompt = prompt
        if style:
            full_prompt += f", {style}"
        image = client.text_to_image(full_prompt, model=MODEL_NAME, width=int(resolution.split("x")[0]), height=int(resolution.split("x")[1]))
        return image  # Returns PIL.Image object
    except Exception as e:
        return str(e)

# Start command handler
@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.chat.id
    bot.send_message(
        message.chat.id,
        """🌟 *Welcome to the AI Image Creator Bot!* 🎨\n\nHi there! I'm here to bring your imagination to life with stunning AI-generated images. Just tell me what you'd like to see, and I'll create it for you in seconds using the power of Stable Diffusion.\n\n✨ *Commands You Can Use:*\n- */gallery* - Browse your personal gallery of previously generated images. 🖼️\n- *Custom Image Generation* - Want something unique? Use this format:\n  `<prompt>;<resolution>;<style>`\n  Example: _"A breathtaking mountain sunset;1024x1024;oil painting style"_\n\nReady to create something amazing? 🚀 Let's get started! 🎉""",
        parse_mode="Markdown",
    )

# Handle the /gallery command
@bot.message_handler(commands=["gallery"])
def view_gallery(message):
    user_id = message.chat.id
    gallery = get_user_gallery(user_id)
    if not gallery:
        bot.send_message(user_id, "Your gallery is empty! Generate some images to see them here.")
        return
    for prompt, image_path in gallery:
        bot.send_message(user_id, f"Prompt: {prompt}")
        with open(image_path, "rb") as img:
            bot.send_photo(user_id, img)

# Handle text messages for image generation
@bot.message_handler(func=lambda message: True, content_types=["text"])
def handle_prompt(message):
    bot.send_chat_action(message.chat.id, "typing")
    parts = message.text.split(";")
    prompt = parts[0]
    resolution = parts[1] if len(parts) > 1 else "512x512"
    style = parts[2] if len(parts) > 2 else None

    bot.send_message(message.chat.id, "Generating your image... Please wait.")

    try:
        image = generate_image(prompt, resolution, style)
        if isinstance(image, str):  # Error occurred
            bot.send_message(message.chat.id, f"Error: {image}")
        else:
            # Save the image and add it to the gallery
            image_path = f"{message.chat.id}_{prompt.replace(' ', '_')}.png"
            image.save(image_path)
            add_image_to_gallery(message.chat.id, prompt, image_path)

            with open(image_path, "rb") as img:
                bot.send_photo(message.chat.id, img)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {e}")

# Main function to start the bot
if __name__ == "__main__":
    print("Bot is running...")
    init_db()
    bot.polling()


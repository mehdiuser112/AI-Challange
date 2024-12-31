# Telegram AI Image Bot

Generate AI-powered images through Telegram using Stable Diffusion 3.5. This bot creates custom images from text prompts, manages user galleries, and runs 24/7 on Railway.

## Key Features

- Text-to-image generation using Stable Diffusion 3.5
- Customizable image resolution and artistic styles
- Personal image gallery for each user
- Automatic user registration and management
- Continuous deployment on Railway
- Local image and data storage with SQLite

## Usage

### Commands
- `/start` - Register and get started
- `/gallery` - View your generated images
- Generate images using format:
  ```
  <prompt>;<resolution>;<style>
  ```
  Example: `A serene mountain lake;1024x1024;oil painting`

### Supported Customizations
- **Resolutions**: 512x512, 768x768, 1024x1024
- **Styles**: watercolor, oil painting, digital art, abstract, photorealistic
- **Default Settings**: 512x512 resolution, no specific style

## Technical Stack

### Core Technologies
- Python 3.11+
- Stable Diffusion 3.5 via Hugging Face
- SQLite Database
- Railway Platform

### Dependencies
- pyTelegramBotAPI 4.12.0
- huggingface_hub 0.27.0
- Pillow 9.5.0
- python-dotenv 1.0.0

## Development Setup

### Prerequisites
```bash
# Clone repository
git clone <repository-url>
cd <repository-name>

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Configuration
Create `.env` file:
```plaintext
BOT_TOKEN=your_telegram_bot_token
HUGGINGFACE_API_TOKEN=your_huggingface_api_token
```

### Database Schema
```sql
CREATE TABLE images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    prompt TEXT,
    image_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Deployment

### Railway Deployment
1. Fork this repository
2. Connect your Railway account
3. Add environment variables in Railway dashboard
4. Deploy from main branch

### Local Deployment
```bash
python3 model.py
```

### Docker Deployment
```bash
docker build -t telegram-ai-bot .
docker run -d --env-file .env telegram-ai-bot
```

## Project Structure
```
.
├── model.py              # Main application
├── requirements.txt      # Python dependencies
├── Dockerfile           # Container configuration
├── .env                 # Environment variables
├── .gitignore          # Git ignore rules
├── runtime.txt         # Python version specification
├── README.md           # Documentation
└── database/           # SQLite database files
    ├── gallery.db      # Image and user data
    └── backup/         # Database backups
```

## Error Handling

### Common Issues
1. **Image Generation Fails**
   - Check Hugging Face API token
   - Verify prompt length (max 500 characters)
   - Ensure valid resolution format

2. **Database Errors**
   - Check write permissions
   - Verify database file existence
   - Monitor storage space

3. **Bot Unresponsive**
   - Validate Telegram token
   - Check Railway logs
   - Verify internet connectivity

## API Rate Limits
- Hugging Face API: 30,000 requests/month (free tier)
- Telegram Bot API: 30 messages/second

## Security Measures
- Environment variable protection
- Database backup system
- Input sanitization
- Error logging

## Contributing
1. Fork repository
2. Create feature branch
3. Submit pull request
4. Follow coding standards

## Support
- Email: mmprofessional112@gmail.com
- Telegram: 

## License
This project is licensed under the MIT License.

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    ContextTypes, ConversationHandler, MessageHandler, filters
)
from card_generator import CardGenerator
from constants import (
    BOT_TOKEN, WELCOME_MESSAGE, ERROR_MESSAGE, COMMANDS,
    COLORS, BORDER_COLORS, NAME_COLORS, BG_COLORS, CONTENT_PROMPT,
    NAME_COLOR_PROMPT, COLOR_PROMPT, BORDER_COLOR_PROMPT, BG_COLOR_PROMPT
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
CHOOSE_NAME_COLOR, CHOOSE_COLOR, CHOOSE_BORDER, CHOOSE_BG = range(4)

class CardGeneratorBot:
    def __init__(self):
        try:
            self.card_generator = CardGenerator()
            logger.info("CardGenerator initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing CardGenerator: {str(e)}")
            raise

    def create_colored_button(self, text: str, color_code: str, callback_data: str) -> InlineKeyboardButton:
        """Create a button with color indicator and emoji"""
        color_name = text.title()
        if color_code.lower() == "#ffffff":
            return InlineKeyboardButton(f"âšª {color_name}", callback_data=callback_data)
        elif color_code.lower() == "#000000":
            return InlineKeyboardButton(f"âš« {color_name}", callback_data=callback_data)
        elif color_code.lower() == "#1da1f2":
            return InlineKeyboardButton(f"ðŸ”µ {color_name}", callback_data=callback_data)
        elif color_code.lower() == "#ff0000":
            return InlineKeyboardButton(f"ðŸ”´ {color_name}", callback_data=callback_data)
        elif color_code.lower() == "#00ff00":
            return InlineKeyboardButton(f"ðŸ’š {color_name}", callback_data=callback_data)
        elif color_code.lower() == "#833ab4":
            return InlineKeyboardButton(f"ðŸ’œ {color_name}", callback_data=callback_data)
        elif color_code.lower() == "#ffd700":
            return InlineKeyboardButton(f"ðŸ’› {color_name}", callback_data=callback_data)
        else:
            return InlineKeyboardButton(f"ðŸŽ¨ {color_name}", callback_data=callback_data)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for /start command"""
        logger.info(f"Start command received from user {update.effective_user.id}")
        await update.message.reply_text(WELCOME_MESSAGE)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle any message in private chat"""
        try:
            # Ignore commands
            if not update.message or update.message.text.startswith('/'):
                return

            # Store the message content
            context.user_data['content'] = update.message.text
            await update.message.reply_text("ðŸŽ¨ Starting card generation...")

            # Create name color selection buttons
            keyboard = []
            for color_name, color_code in NAME_COLORS.items():
                keyboard.append([self.create_colored_button(color_name, color_code, f"name_{color_code}")])

            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(NAME_COLOR_PROMPT, reply_markup=reply_markup)
            return CHOOSE_NAME_COLOR

        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
            await update.message.reply_text(ERROR_MESSAGE)
            return ConversationHandler.END

    async def gen_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for /gen command in groups"""
        try:
            if not update.message.reply_to_message:
                await update.message.reply_text("Please reply to a message to generate a card from it.")
                return ConversationHandler.END

            context.user_data['content'] = update.message.reply_to_message.text
            await update.message.reply_text("ðŸŽ¨ Starting card generation...")

            # Create name color selection buttons
            keyboard = []
            for color_name, color_code in NAME_COLORS.items():
                keyboard.append([self.create_colored_button(color_name, color_code, f"name_{color_code}")])

            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(NAME_COLOR_PROMPT, reply_markup=reply_markup)
            return CHOOSE_NAME_COLOR

        except Exception as e:
            logger.error(f"Error in gen command: {str(e)}")
            await update.message.reply_text(ERROR_MESSAGE)
            return ConversationHandler.END

    async def name_color_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle name color selection"""
        try:
            query = update.callback_query
            await query.answer()

            color_code = query.data.replace("name_", "")
            context.user_data['name_color'] = color_code
            await query.message.edit_text("âœ… Name color selected!")

            # Create text color selection buttons
            keyboard = []
            for color_name, color_code in COLORS.items():
                keyboard.append([self.create_colored_button(color_name, color_code, f"color_{color_code}")])

            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(COLOR_PROMPT, reply_markup=reply_markup)
            return CHOOSE_COLOR

        except Exception as e:
            logger.error(f"Error handling name color selection: {str(e)}")
            await update.callback_query.message.reply_text(ERROR_MESSAGE)
            return ConversationHandler.END

    async def color_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text color selection"""
        try:
            query = update.callback_query
            await query.answer()

            color_code = query.data.replace("color_", "")
            context.user_data['text_color'] = color_code
            await query.message.edit_text("âœ… Text color selected!")

            # Create border color selection buttons
            keyboard = []
            for color_name, color_code in BORDER_COLORS.items():
                keyboard.append([self.create_colored_button(color_name, color_code, f"border_{color_code}")])

            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(BORDER_COLOR_PROMPT, reply_markup=reply_markup)
            return CHOOSE_BORDER

        except Exception as e:
            logger.error(f"Error handling text color selection: {str(e)}")
            await update.callback_query.message.reply_text(ERROR_MESSAGE)
            return ConversationHandler.END

    async def border_color_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle border color selection"""
        try:
            query = update.callback_query
            await query.answer()

            color_code = query.data.replace("border_", "")
            context.user_data['border_color'] = color_code
            await query.message.edit_text("âœ… Border color selected!")

            # Create background color selection buttons
            keyboard = []
            for color_name, color_code in BG_COLORS.items():
                keyboard.append([self.create_colored_button(color_name, color_code, f"bg_{color_code}")])

            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(BG_COLOR_PROMPT, reply_markup=reply_markup)
            return CHOOSE_BG

        except Exception as e:
            logger.error(f"Error handling border color selection: {str(e)}")
            await update.callback_query.message.reply_text(ERROR_MESSAGE)
            return ConversationHandler.END

    async def bg_color_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle background color selection and generate card"""
        try:
            query = update.callback_query
            await query.answer()

            color_code = query.data.replace("bg_", "")
            context.user_data['bg_color'] = color_code
            await query.message.edit_text("âœ… Background color selected!")

            # Send status message
            status_message = await query.message.reply_text("ðŸŽ¨ Generating your social card...")

            # Get user information
            user = update.effective_user
            name = user.first_name
            username = user.username or "user"

            # Get profile photo
            profile_photos = await user.get_profile_photos()
            profile_pic_url = None
            if profile_photos and profile_photos.photos:
                photo = profile_photos.photos[0][-1]
                file = await photo.get_file()
                profile_pic_url = file.file_path
                logger.info("Retrieved profile picture")

            # Generate card
            await status_message.edit_text("âœ¨ Adding special effects...")
            card_image = self.card_generator.generate_card(
                name=name,
                username=username,
                content=context.user_data['content'],
                text_color=context.user_data['text_color'],
                name_color=context.user_data['name_color'],
                border_color=context.user_data['border_color'],
                bg_color=context.user_data['bg_color'],
                profile_pic_url=profile_pic_url
            )
            logger.info("Card generated successfully")

            # Send card
            await status_message.edit_text("ðŸ“¤ Uploading your masterpiece...")
            await status_message.reply_photo(card_image)
            await status_message.edit_text("âœ¨ Your beautiful card is ready!")
            return ConversationHandler.END

        except Exception as e:
            logger.error(f"Error handling background color selection: {str(e)}")
            await update.callback_query.message.reply_text(ERROR_MESSAGE)
            return ConversationHandler.END

def main():
    """Main function to run the bot"""
    try:
        # Create bot instance
        bot = CardGeneratorBot()
        logger.info("Bot instance created")

        # Initialize application
        application = Application.builder().token(BOT_TOKEN).build()
        logger.info("Application initialized")

        # Create conversation handler
        conv_handler = ConversationHandler(
            entry_points=[
                CommandHandler('gen', bot.gen_command),
                MessageHandler(filters.ChatType.PRIVATE & ~filters.COMMAND, bot.handle_message)
            ],
            states={
                CHOOSE_NAME_COLOR: [
                    CallbackQueryHandler(bot.name_color_selected, pattern='^name_')
                ],
                CHOOSE_COLOR: [
                    CallbackQueryHandler(bot.color_selected, pattern='^color_')
                ],
                CHOOSE_BORDER: [
                    CallbackQueryHandler(bot.border_color_selected, pattern='^border_')
                ],
                CHOOSE_BG: [
                    CallbackQueryHandler(bot.bg_color_selected, pattern='^bg_')
                ],
            },
            fallbacks=[
                CommandHandler('start', bot.start_command),
                MessageHandler(filters.COMMAND, bot.start_command)
            ],
            allow_reentry=True,
            name="card_creator"
        )

        # Add handlers
        application.add_handler(CommandHandler("start", bot.start_command))
        application.add_handler(conv_handler)
        logger.info("Handlers added")

        # Start the bot
        logger.info("Starting bot polling...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        logger.error(f"Critical error starting bot: {str(e)}")
        raise

if __name__ == "__main__":
    main()
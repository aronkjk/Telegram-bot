import logging
import imdb
import emoji

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

moviesDB = imdb.IMDb()
print(dir(moviesDB))

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

 
def echo(update: Update, context: CallbackContext) -> None:
    amime_name = update.message.new_chat_title
    context.bot.delete_message(chat_id = update.message.chat_id, message_id = update.message.message_id)
    message_text = amime_name + '\n'
    movies = moviesDB.search_movie(amime_name)
    id = movies[0].getID()
    for movie in movies:

        print(movie['title'], movie['year'])

    movie = moviesDB.get_movie(id)
    genres = movie['genres']
    emoji_genre = ''

    if genres[0] != "Animation":
        update.message.reply_text("No concidence with an anime")
        return

    for genre in genres:
        if genre != "Animation":
            if genre == "Action":
                emoji_genre = emoji_genre + '🔥'
            if genre == "Adult":
                emoji_genre = emoji_genre + '🔞'
            if genre == "Adventure":
                emoji_genre = emoji_genre + '⛰️'
            if genre == "Biography":
                emoji_genre = emoji_genre + '👵'
            if genre == "Comedy":
                emoji_genre = emoji_genre + '🤣'
            if genre == "Documentary":
                emoji_genre = emoji_genre + '💯'
            if genre == "Drama":
                emoji_genre = emoji_genre + '🎭'
            if genre == "Family":
                emoji_genre = emoji_genre + '👪'
            if genre == "Fantasy":
                emoji_genre = emoji_genre + '🦄'
            if genre == "Film-Noir":
                emoji_genre = emoji_genre + '⚫'
            if genre == "Game-Show":
                emoji_genre = emoji_genre + '🎮'
            if genre == "History":
                emoji_genre = emoji_genre + '⛩️'
            if genre == "Horror":
                emoji_genre = emoji_genre + '👹'
            if genre == "Musical":
                emoji_genre = emoji_genre + '👨‍🎤'
            if genre == "Music":
                emoji_genre = emoji_genre + '🎼'
            if genre == "Mystery":
                emoji_genre = emoji_genre + '⁉️'
            if genre == "News":
                emoji_genre = emoji_genre + '📰'
            if genre == "Reality-TV":
                emoji_genre = emoji_genre + '📺'
            if genre == "Romance":
                emoji_genre = emoji_genre + '👩‍❤️‍👩'
            if genre == "Sci-Fi":
                emoji_genre = emoji_genre + '🌌'
            if genre == "Short":
                emoji_genre = emoji_genre + '✂️'
            if genre == "Sport":
                emoji_genre = emoji_genre + '🏅'
            if genre == "Talk-Show":
                emoji_genre = emoji_genre + '💱'
            if genre == "Thriller":
                emoji_genre = emoji_genre + '🔪'
            if genre == "War":
                emoji_genre = emoji_genre + '⚔️'
            if genre == "Western":
                emoji_genre = emoji_genre + '🤠'
 
    message_text = message_text + str(movie['year']) + ' A. D.\n' 
    message_text = message_text + str(movie['rating']) + '/10\n'
    message_text = message_text + 'Genres: ' + emoji.emojize(emoji_genre)
    message_text = message_text + movie['cover'] + '\n'
    update.message.reply_text(message_text)

def delete_message(self, update: Update, context: CallbackContext) -> None:
    context.bot.delete_message(chat_id = message.chat_id, message_id = message.message_id)



def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1525820634:AAGYw3aewXXw6LHvDixOuMidUGOtenvreMo", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
#    dispatcher.add_handler(CommandHandler("name", name))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

    delete_message()        


if __name__ == '__main__':
    main()
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
# print(dir(moviesDB))

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('-Si el anime que busca es una saga o tiene partes en las que comparte titulo, puede incuir una _ al final de la busqueda para obtener un mejor resultado. \n-Si no se encuentra el anime que desea pruebe a escibirlo mejor.')
 
def echoAnime(update: Update, context: CallbackContext) -> None:
    if update.channel_post:
        anime_name = update.channel_post.text
        context.bot.delete_message(chat_id = update.channel_post.chat_id, message_id = update.channel_post.message_id)
    
    else:
        anime_name = update.message.text
        context.bot.delete_message(chat_id = update.message.chat_id, message_id = update.message.message_id)

    movies = moviesDB.search_movie(anime_name)

    try:
        id = movies[0].getID()
    except:
        context.bot.send_message(update.channel_post.chat_id, "No concidence with an anime")

    for uf_movie in movies:
        try:
            id = uf_movie.getID()
            movie = moviesDB.get_movie(id)
            title = movie['title']
            year = str(movie['year'])
            genres = movie['genres']  
            print(title, year)
            
            if genres[0] == 'Animation':
                print('ANIME')
                break

        except:
            print('Error')

    movie = moviesDB.get_movie(id)
    genres = movie['genres']

    if genres[0] != "Animation":
        update.message.reply_text("No concidence with an anime")
        return

    message_text = createMessage(movie['title'], str(movie['year']), str(movie['rating']), movie['full-size cover url'], genres)

    if update.channel_post:
        context.bot.send_message(update.channel_post.chat_id, message_text)
    else:
        update.message.reply_text(message_text)

    createPoll(update, context, movie['title'])
   
def genreToEmoji(genres) -> str:
    emoji_genre = ''
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

    return emoji_genre

def createMessage(title, year, rating, cover, genres) -> str:
    message_text = title + '\n'
    message_text = message_text + year + ' A. D.\n'
    try:
        message_text = message_text + rating + '/10\n'
    except:
        message_text = message_text + 'No rated\n'
    try:
        message_text = message_text + cover + '\n'
    except:
        message_text = message_text + 'No cover\n'
    message_text = message_text + 'Genres: ' + emoji.emojize(genreToEmoji(genres))

    return message_text

def createPoll(update: Update, context: CallbackContext, anime) -> None:
    """Sends a predefined poll"""
    questions = ["👍",'😐', "👎"]
    message = context.bot.send_poll(
        update.effective_chat.id,
        "Te ha gustado " + anime + '?',
        questions,
        is_anonymous=True,
        allows_multiple_answers=True,
    )
    # Save some info about the poll the bot_data for later use in receive_poll_answer
    payload = {
        message.poll.id: {
            "questions": questions,
            "message_id": message.message_id,
            "chat_id": update.effective_chat.id,
            "answers": 0,
        }
    }
    context.bot_data.update(payload)

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

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echoAnime))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle() 

if __name__ == '__main__':
    main()
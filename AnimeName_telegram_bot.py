import logging
import imdb
import emoji
import time

import psycopg2
from psycopg2 import Error

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
moviesDB = imdb.IMDb()
sticker_L = 'CAACAgUAAxkBAAEBw91f_xpABQABvmb1qV278Ny9XuM7NIMAAs4AA8aZ-iD-CmEQhSPB7x4E'

def connect_db():
    try:
        connection = psycopg2.connect(user="anime_bot",
                                    password="ewq",
                                    host="127.0.0.1",
                                    port="5432",
                                    database="animes")
        return connection
                                    
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL: ", error)

        return null

def close_db(connection):
    if (connection):
        connection.cursor().close()
        connection.close()
        print("Connection DB is closed")

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hi!')

def help_command(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('-Si el anime que busca es una saga o tiene partes en las que comparte titulo, puede incuir una _ al final de la busqueda para obtener un mejor resultado. \n-Si no se encuentra el anime que desea pruebe a escibirlo mejor.')

def echoAnime(update: Update, context: CallbackContext):
    if update.channel_post:
        anime_name = update.channel_post.text
        chat_id = update.channel_post.chat_id
        message_id = update.channel_post.message_id
        
    else:
        anime_name = update.message.text
        chat_id = update.message.chat_id
        message_id = update.message.message_id

    context.bot.delete_message(chat_id = chat_id, message_id = message_id)
    sticker_id = context.bot.send_sticker(chat_id = chat_id, sticker = sticker_L).message_id
    movies = moviesDB.search_movie(anime_name)

    try:
        id = movies[0].getID()

    except:
        context.bot.delete_message(chat_id = chat_id, message_id = sticker_id)
        return

    for uf_movie in movies:
        id = uf_movie.getID()

        movie = moviesDB.get_movie(id)

        try:
            genres = movie['genres']

        except:
            context.bot.delete_message(chat_id = chat_id, message_id = sticker_id)
            return

        if genres[0] == 'Animation':
            print('ANIME')
            break

    movie = moviesDB.get_movie(id)
    genres = movie['genres']

    if genres[0] != "Animation":
        context.bot.delete_message(chat_id = chat_id, message_id = sticker_id)
        return

    try:
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("SELECT name FROM message_id where name = %s and chat_id = %s", (movie['title'], chat_id))
        record = cursor.fetchall()

        if len(record) > 0:  
            a = record[0][0]

            context.bot.delete_message(chat_id = chat_id, message_id = sticker_id)

            close_db(connection)
            
            try:
                context.bot.send_message(chat_id=chat_id, reply_to_message_id=a, text="🔝")
                print("Closed DB because the object is repeat")
                return
            
            except:
                print('The message was deleted, creating a new tuple, delete old tuple in the future')

    except (Exception, Error) as error:
        print("Error while connecting to DB, err: ", error)

    finally:
        close_db(connection)    

    if movie['kind'] == 'tv series':
        year = movie['series years']
        aka = '📺'
        duration = ' mins/ep'
        if len(year) < 7:
            airing = '🔴  ON AIR'
        
        else:
            airing = '✅  ENDED'

    else:
        year = movie['year']
        aka = '🎞'
        duration = ' mins'
        airing = ''

    message_text = createMessage(movie['title'], str(year), str(movie['rating']), movie['full-size cover url'], genres, movie['runtimes'][0], airing, aka, duration)

    context.bot.delete_message(chat_id = chat_id, message_id = sticker_id)
    
    if update.channel_post:
        anime_id = context.bot.send_message(chat_id, message_text).message_id

    else:
        anime_id = update.message.reply_text(message_text).message_id

    try:
        connection = connect_db()
        cursor = connection.cursor()
        insert_query = """ INSERT INTO animes (name, message_id, chat_id) VALUES (%s, %s, %s);"""
        item_tuple = (movie['title'], anime_id, chat_id)
        cursor.execute(insert_query, item_tuple)
        connection.commit()
    
    except (Exception, Error) as error:
        print('Error while writting in DB, err: ', error)

    finally:
        close_db(connection)

    createPoll(update, context, movie['title'])

def genreToEmoji(genres):
    emoji_genre = ''
    for genre in genres:
        if genre != "Animation":
            if genre == "Action":
                emoji_genre = emoji_genre + ' 🔥'
            if genre == "Adult":
                emoji_genre = emoji_genre + ' 🔞'
            if genre == "Adventure":
                emoji_genre = emoji_genre + ' ⛰️'
            if genre == "Biography":
                emoji_genre = emoji_genre + ' 👵'
            if genre == "Comedy":
                emoji_genre = emoji_genre + ' 🤣'
            if genre == "Documentary":
                emoji_genre = emoji_genre + ' 💯'
            if genre == "Drama":
                emoji_genre = emoji_genre + ' 🎭'
            if genre == "Family":
                emoji_genre = emoji_genre + ' 👪'
            if genre == "Fantasy":
                emoji_genre = emoji_genre + ' 🦄'
            if genre == "Film-Noir":
                emoji_genre = emoji_genre + ' ⚫'
            if genre == "Game-Show":
                emoji_genre = emoji_genre + ' 🎮'
            if genre == "History":
                emoji_genre = emoji_genre + ' ⛩️'
            if genre == "Horror":
                emoji_genre = emoji_genre + ' 👹'
            if genre == "Musical":
                emoji_genre = emoji_genre + ' 👨‍🎤'
            if genre == "Music":
                emoji_genre = emoji_genre + ' 🎼'
            if genre == "Mystery":
                emoji_genre = emoji_genre + ' ⁉️'
            if genre == "News":
                emoji_genre = emoji_genre + ' 📰'
            if genre == "Reality-TV":
                emoji_genre = emoji_genre + ' 📺'
            if genre == "Romance":
                emoji_genre = emoji_genre + ' 👩‍❤️‍👩'
            if genre == "Sci-Fi":
                emoji_genre = emoji_genre + ' 🌌'
            if genre == "Short":
                emoji_genre = emoji_genre + ' ✂️'
            if genre == "Sport":
                emoji_genre = emoji_genre + ' 🏅'
            if genre == "Talk-Show":
                emoji_genre = emoji_genre + ' 💱'
            if genre == "Thriller":
                emoji_genre = emoji_genre + ' 🔪'
            if genre == "War":
                emoji_genre = emoji_genre + ' ⚔️'
            if genre == "Western":
                emoji_genre = emoji_genre + ' 🤠'

    return emoji_genre

def createMessage(title, year, rating, cover, genres, runtimes, airing, aka, duration):
    message_text = title + '    ' + aka + '\n'
    message_text = message_text + year + airing +'\n'

    try:
        message_text = message_text + rating + '    '
    except:
        message_text = message_text + 'No rated    '

    message_text = message_text + emoji.emojize(genreToEmoji(genres)) + '\n'

    try:
        message_text = message_text + runtimes + duration + ' \n'

    except:
        message_text = message_text + 'No runtimes data\n'

    try:
        message_text = message_text + cover + '\n'

    except:
        message_text = message_text + 'No cover'

    return message_text

def createPoll(update: Update, context: CallbackContext, anime):
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

def cancel_search_command():
    global cancel_search
    cancel_search = True

def main():
    updater = Updater("1525820634:AAGYw3aewXXw6LHvDixOuMidUGOtenvreMo", use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echoAnime))

    updater.start_polling()

    updater.idle() 

if __name__ == '__main__':
    main()

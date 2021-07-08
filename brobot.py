#hello

# bot.py
import os
import logging
import discord
from dotenv import load_dotenv

#DB connection
import psycopg2
from config import config


load_dotenv('/env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


# logging shiz
# https://discordpy.readthedocs.io/en/stable/logging.html
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(Levelname)s: %(message)s'))
logger.addHandler(handler)


# #DB stuff
# def connect():
#     """ Connect to the PostgreSQL database server """
#     conn = None
#     try:
#         # read connection parameters
#         params = config()

#         # connect to the PostgreSQL server
#         print('Connecting to the PostgreSQL database...')
#         conn = psycopg2.connect(**params)
		
#         # create a cursor
#         cur = conn.cursor()
        
# 	# execute a statement
#         print('PostgreSQL database version:')
#         cur.execute('SELECT version()')

#         # display the PostgreSQL database server version
#         db_version = cur.fetchone()
#         print(db_version)
       
# 	# close the communication with the PostgreSQL
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()
#             print('Database connection closed.')


def insert_quote(cory_quotes):
    """ insert a new quote into the vendors table """
    sql = """INSERT INTO quote(cory_quotes)
             VALUES(%s) RETURNING quote;"""
    conn = None
    quote = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (cory_quotes,))
        # get the generated id back
        quote = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return quote


client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
@client.event
async def on_message(message):

    # bot ignores messages fromt self
    if message.author == client.user:
        return

    msg = message.content

    if message.content.startswith('$hello'):
        await message.channel.send('Hello')
        return

    if msg.startswith("$new"):
        cory_quote = msg.split("$new ",1)[1]
        insert_quote(cory_quote)
        await message.channel.send("New Cory Quote added.")
  
    if msg.startswith("$list"):
        cory_quote = []
        
client.run(TOKEN)
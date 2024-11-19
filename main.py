import threading
import asyncio
from typing import Final
import os

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv, find_dotenv

from Scripts.User import is_member, register_active_user, contains_link, contains_embeded_link, is_forwarded, delete_bot_message, generate_random_varchar, is_admin, get_chat_admins
from Scripts.Log import log, log_user_message, fetch_user_message, deletion_wave_log, to_delete_id
from Scripts.functions import json_loader, update_holidays, send_comment, change_meta_data, show_meta_data ,download_file


# --Get Private Files From .env file
try:
    load_dotenv(find_dotenv('Private/.env'))
    BOT_TOKEN: Final = os.getenv('BOT_TOKEN')
except Exception as e:
    print("Load Enviroment Error: ", e)

BOT_USERNAME: Final = '@habtemaryam26bot'
CHANNEL_CHAT_ID: Final = '-1001446571420'
phone_number: int = None

# --A function that will run the DeleteBotMessage
def between_func(sec, update, context, chat_id, message_id):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(delete_bot_message(sec, update, context, chat_id, message_id))
    loop.close()


#######################################TELEGRAM#################################
#Command Functions
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_chat_action('typing')

        chat_id: int = update.message.chat.id
        user_name: str = update.message.from_user.username
        first_name: str = update.message.from_user.first_name
        last_name: str = update.message.from_user.last_name
        full_name: str = update.message.from_user.full_name
        user_id: int = update.message.from_user.id
        text: str = update.message.text
        message_type: str = update.message.chat.type

        #Register User Information
        registration = register_active_user(user_id, user_name, first_name, last_name, full_name, chat_id)

        # Log
        if registration:
            log('Start Command', 'Registered User', f'{full_name}({user_name})')
        elif not registration:
            log('Start Command', 'Registered User', f'{full_name}({user_name})  Already Exists', log_level='WARNING')
        else:
            log('Start Command', 'Unknown', f'{full_name}({user_name})' + f'Unknown return Value: {registration}', log_level='ERROR')

        if await is_member(update, context): # Check if user is in the Channel
            try:
                if message_type == 'private':
                    await update.message.reply_text(json_loader("start"))
                    log('Start Command', 'Sent user Private start message', f'To: {full_name}({user_name} user_text: {text})')
                else:
                    if BOT_USERNAME not in text:
                        return None
                    await update.message.reply_text(json_loader('private_start'))
                    log('Start Command', 'Sent user Public start message', f'To: {full_name}({user_name} user_text: {text})')

            except Exception as e:
                print(e)
                log("Start Command", e, None, log_level="ERROR")
        else:
            pass # Send Them a Message to Go and Join the Main Channel
    except Exception as e:
        print(e)
        log("Start Command", e, None, log_level="CRITICAL")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_chat_action('typing')

        text: str = update.message.text
        message_type: str = update.message.chat.type
        full_name: str = update.message.from_user.full_name
        user_name: str = update.message.from_user.username

        if message_type != 'private':
            if BOT_USERNAME not in text:
                return
            await update.message.reply_text(json_loader("help"))
            log("Help Command", f'Sent Message to {full_name}({user_name})', 'For Public Chat', log_level="INFO")
        if message_type == 'private':
            await update.message.reply_text(json_loader("help"))
            log("Help Command", f'Sent Message to {full_name}({user_name})', 'For Private Chat', log_level="INFO")

    except Exception as e:
        print(e)
        log("Help Command", e, None, log_level="CRITICAL")


async def holidays_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_chat_action('typing')
        
        text: str = update.message.text
        message_type: str = update.message.chat.type
        chat_id = update.message.chat_id
        full_name: str = update.message.from_user.full_name
        user_name: str = update.message.from_user.username

        if message_type != 'private':
            if BOT_USERNAME not in text:
                return
        await context.bot.forwardMessage(chat_id, CHANNEL_CHAT_ID, json_loader('holidays'))
        log("Holidays Command", f'Sent Message to{full_name}({user_name})', 'For Private Chat', log_level="INFO")

    except Exception as e:
        print(e)
        log("Holiday Command", e, None, log_level="CRITICAL")


async def comment_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_chat_action('typing')

        text: str = update.message.text
        message_type: str = update.message.chat.type
        chat_id: int = update.message.chat_id
        full_name: str = update.message.from_user.full_name
        user_name: str = update.message.from_user.username
        processed: str = text.lower().replace('/comment ', '')
        
        if message_type != 'private':
            if BOT_USERNAME not in text:
                return
            
        comment = f'Message From: {full_name}(@{user_name}), \nSays: {processed}'
        if processed == "/comment":
            await update.message.reply_text("Please send the Comment You want to send the <a href='https://t.me/ElChapo_ET'>Administrator</a>: ", parse_mode='html')
            log_user_message(processed)
            
        else:
            await send_comment(update, context, comment, full_name, user_name)
            await context.bot.send_message(chat_id, 'Successfully Sent Comment to Administrator, They will contact you in 48 hours!')

    except Exception as e:
        print(e)
        log("Comment Command", e, None, log_level="CRITICAL")


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_chat_action('typing')


    except Exception as e:
        print(e)
        log("About Command", e, None, log_level="CRITICAL")


async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id: int = update.message.chat_id
    try:
        await update.message.reply_chat_action('typing')

    except Exception as e:
        print(e)
        log("Ping Command", e, None, log_level="CRITICAL")


async def update_holidays_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_chat_action('typing')

        text: str = update.message.text
        processed: str = text.lower().replace('/update_holidays ', '')
        full_name: str = update.message.from_user.full_name
        user_name: str = update.message.from_user.username
        message_type: str = update.message.chat.type
        
        if message_type != 'private':
            if BOT_USERNAME not in text:
                return
        if processed != '/update_holidays':
            update_holidays(log, processed, full_name, user_name)
            await update.message.reply_text(f'Successfully Updated The message to https://t.me/habtemaryam26/{processed.split("/")[-1]}')
        else:
            log_user_message(text)
            await update.message.reply_text("Please send the Message id or Message link", parse_mode='html')
        
        log('UpdateHolidays Command', 'Updated the Holiday Message', f'Updated By: {user_name}')

    except Exception as e:
        print(e)
        log("UpdateHolidays Command", e, None, log_level="CRITICAL")
        await update.message.reply_text("UpdateHolidays Command", e, f"Currunt holiday message{json_loader('holidays')}", log_level="ERROR")


async def change_metadata_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_chat_action('typing')

        text: str = update.message.text
        processed: str = text.lower().replace('/change_metadata ', '')
        message_type: str = update.message.chat.type
        chat_id: int = update.message.chat.id

        if message_type != 'private':
            return

        log_user_message(text)
        await update.message.reply_text("Please send the SONG with the Caption as the Title and i will send back the updated version", parse_mode='html')

    except Exception as e:
        print(e)
        log("ChangeMetaData Command", e, None, log_level="CRITICAL")
        await update.message.reply_text("ChangeMetaData Command: ", e)

async def policy_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    full_name: str = update.message.from_user.full_name
    user_name: str = update.message.from_user.username
    text: str = update.message.text

    message_id = 123  # Replace with the actual message ID

    message = await context.bot.get_updates(offset=1)
    print(message)
    try:
        await update.message.reply_chat_action('typing')
        await update.message.reply_text(json_loader('GroupPolicy'), parse_mode='html')
        log('Policy Command', 'Sent user Group Policy', f'To: {full_name}({user_name} user_text: {text})')
    except Exception as e:
        print(e)
        log("Policy Command", e, None, log_level="CRITICAL")












# Message Handlers
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE): # Activeted when ever their is no command in the message
    #Log Every Actions
    text: str = update.message.text
    text_html: str = update.message.text_html
    full_name: str = update.message.from_user.full_name
    user_name: str = update.message.from_user.username
    chat_id: int = update.message.chat_id
    message_id: int = update.message.id
    message_type: str = update.message.chat.type
    forward_from: str = update.message.forward_from
    forward_from_chat: str = update.message.forward_from_chat
    is_admin: bool = False
    try:
        if message_type != 'private':
            administrators = await context.bot.get_chat_administrators(chat_id)
    except Exception as e:
        administrators = ''
        log('Handle Message', "Couldn't find any admins", e, log_level='WARNING')
    admins = get_chat_admins(administrators)
    Group_Anonumous_Bot = 1087968824
    user_id = update.message.from_user.id
    print(update.channel_post)

    # Check if the user is from the main group and is admin or Anonimous bot of that group

    last_message: str = fetch_user_message()
    log_user_message(text)

    if message_type != 'private': # cHECK IF THE RECIEVED MESSAGE WASN'T PRIVATE
        for id in admins:
            if str(user_id) == str(id) or str(user_id) == str(Group_Anonumous_Bot): #Check if Admin...
                is_admin = True
            if not is_admin and str(user_id) != '777000':
                if contains_embeded_link(text_html) or contains_link(text) or list(is_forwarded(forward_from, forward_from_chat))[1] == 'Chat':
                    # Log Chat
                    # Delete Chat
                    try:
                        await context.bot.delete_message(chat_id, message_id)
                    except Exception as e:
                        print(e)
                    # Send User warning
                    rand_varchar: str = generate_random_varchar(16)
                    deletion_wave_log(rand_varchar + '\n')

                    if user_name == None:
                        message_: str = f'Dear User({full_name}), Your Message was deleted because it Violates the Group Policies, Visit @habtemaryam26bot to see Group Policeis\n\nViolation: Forwarding Messages'
                    else:
                        message_: str = f'Dear @{user_name}, Your Message was deleted because it Violates the Group Policies, Visit @habtemaryam26bot to see Group Policeis\n\nViolation: Forwarding Messages'
                    
                    return await context.bot.send_message(chat_id, message_, parse_mode='html')
        if BOT_USERNAME not in text:
                return
    #waves: list = deletion_wave_log('', parameter='GET').split('\n')
#
    #for wave in waves:
    #    if wave in str(text):
    #        waves.remove(wave)
    #        to_delete_id(message_id, parameter='POST')
#
    #deletion_wave_log('\n'.join(waves), parameter='CLEAR')
#
    #message_ids: str = to_delete_id('', parameter='GET').split('\n')
#
    #for id in message_ids:
    #    try:
    #        await context.bot.delete_message(chat_id, id)
    #    except:
    #        pass
#
    #    print('Deleted: ' + id)
    #    
    #to_delete_id('', parameter='CLEAR')

    if message_type == 'private':
        comment: str = f'Message From: {full_name}(@{user_name}), \nSays: {text}'
        if last_message[0].lower() == '/update_holidays':
            update_holidays(log, text, full_name, user_name)
            await context.bot.send_message(chat_id, f'Holiday\'s Message Successfully Updated to {text}')
            return
        
        elif last_message[0].lower() == '/comment':
            last_message: str = fetch_user_message()

            await send_comment(update, context, comment, full_name, user_name)
            await context.bot.send_message(chat_id, 'Successfully Sent Comment to Administrator, They will contact you in 48 hours!')
            log('Handle Message', 'Successfully Sent message Anonimously', f'from ChatID: {chat_id}')
            return
        
        await update.message.reply_text("I don't Understand what you are saying click on /help")



async def handle_all_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    caption_text: str = update.message.caption
    caption_html: str = update.message.caption_html
    forward_from: str = update.message.forward_from
    forward_from_chat: str = update.message.forward_from_chat
    chat_id: int = update.message.chat_id
    message_id: int = update.message.message_id
    full_name: str = update.message.from_user.full_name
    user_name:str = update.message.from_user.username
    threaded: bool = False # Down
    message_type: str = update.message.chat.type
    last_message: str = fetch_user_message()
    is_admin: bool = False
    try:
        administrators = await context.bot.get_chat_administrators(chat_id)
    except Exception as e:
        administrators = ''
        log('handle_all_message', "Couldn't find any admins", e, log_level='WARNING')
    admins = get_chat_admins(administrators)
    Group_Anonumous_Bot = 1087968824
    user_id = update.message.from_user.id
    try:
        file_id: str = update.message.audio.file_id
    except Exception as e:
        log('handle_all_message', e, 'No File ID', log_level='WARNING')

    # Auto Delete Bot Message (where bot message == bot message)
    #if not threaded:
    #    threading.Thread(target=between_func, args=(10, update, context, chat_id, message_id)).start()
    #    threaded: bool = True
    if message_type == 'private':
        if last_message[0].lower() == '/change_metadata':
            try:
                file_song: tuple = await context.bot.get_file(file_id)
            except Exception as e:
                log('Handle_All_Messages', e, 'No File Id Found', log_level='WARNING')

            await update.message.reply_text('processing...')
            download_file(str(file_song.file_path))
            change_meta_data('✝️ደቂቀ ሐብተማርያም✝️',
                        '✝️ደቂቀ ሐብተማርያም✝️', 
                        ['✝️ደቂቀ ሐብተማርያም✝️'], 
                        caption_text,
                        art= f"Images/cover.jpg"
                        )
            try:
                meta_data: list = show_meta_data()
                metaData_message: str = f"""album : {meta_data[0]}
    albumartist: {meta_data[1]}
    artist: {meta_data[2]}
    audio_offset: {meta_data[3]}
    bitdepth: {meta_data[4]}
    bitrate: {meta_data[5]}
    comment: {meta_data[6]}
    composer: {meta_data[7]}
    disc: {meta_data[8]}
    disc_total: {meta_data[9]}
    duration: {meta_data[10]}
    filesize: {meta_data[11]}
    genre: {meta_data[12]}
    samplerate: {meta_data[13]}
    title: {meta_data[14]}
    track: {meta_data[15]}
    track_total: {meta_data[16]}
    year: {meta_data[17]}
    extra: {meta_data[18]}
    """
                await context.bot.edit_message_text(f'New Metadata Set:\n\n{metaData_message}', chat_id, message_id + 1)
            except Exception as e:
                print(e)
                pass

            await update.message.reply_chat_action('upload_audio')
            await context.bot.send_audio(chat_id,
                                        f"Audio/audio_file.mp3",
                                        caption = f'<b>✝️<a href="https://t.me/habtemaryam26">{caption_text}</a>✝️</b>',
                                        parse_mode='html',
                                        write_timeout=60,
                                        connect_timeout=60,
                                        pool_timeout=60,
                                        read_timeout=60)
    if message_type != 'private':
        for id in admins:
            if str(user_id) == str(id) or str(user_id) == str(Group_Anonumous_Bot): #Check if Admin...
                is_admin = True
            if not is_admin and str(user_id) != '777000':
                if contains_embeded_link(caption_html) or contains_link(caption_text) or list(is_forwarded(forward_from, forward_from_chat))[1] == 'Chat':
                    # Log Chat
                    # Delete Chat
                    try:
                        await context.bot.delete_message(chat_id, message_id)
                    except Exception as e:
                        print(e)
                    # Send User warning
                    rand_varchar: str = generate_random_varchar(16)
                    deletion_wave_log(rand_varchar + '\n')

                    if user_name == None:
                        message_: str = f'Dear User({full_name}), Your Message was deleted because it Violates the Group Policies, Visit @habtemaryam26bot to see Group Policeis\n\nViolation: Forwarding Messages'
                    else:
                        message_: str = f'Dear @{user_name}, Your Message was deleted because it Violates the Group Policies, Visit @habtemaryam26bot to see Group Policeis\n\nViolation: Forwarding Messages'
                    
                    return await context.bot.send_message(chat_id, message_, parse_mode='html')
                # Log Bot Response

#Error Handlers
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE): # Activated when ever an error occurs
    print(context.error)
    log('Error Handler', context.error, None, log_level="ERROR")

#######################################TELEGRAM#################################

if __name__ == '__main__':
    print('Starting Program ...')

    app: Application = Application.builder().token(BOT_TOKEN).build()    
    #commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('holidays', holidays_command))
    app.add_handler(CommandHandler('comment', comment_command))
    app.add_handler(CommandHandler('about', about_command))
    app.add_handler(CommandHandler('ping', ping_command))
    app.add_handler(CommandHandler('update_holidays', update_holidays_command))
    app.add_handler(CommandHandler('change_metadata', change_metadata_command))
    app.add_handler(CommandHandler('policy', policy_command))
    #MEssages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.ALL, handle_all_message))
    #Errors
    app.add_error_handler(error)    
    #Polling
    print('Polling ...')
    app.run_polling(poll_interval=1)
import json
import random
import time
import re

CHANNEL_CHAT_ID: int = -1001658864142


async def is_member(update, context) -> bool:
    user_id = update.message.from_user.id
    accepted_user_status = ['creator','administrator', 'member']
    state = await context.bot.get_chat_member(CHANNEL_CHAT_ID, user_id)

    if str(state.status) in accepted_user_status:
        return True
    else:
        print(f'User status: {state.status}')
        await context.bot.send_message(update.message.chat_id, 'Please Join the Main <a href = "https://t.me/habtemaryam26">Channel</a> and try again! @habtemaryam26 ', parse_mode='html')
        return False


def register_active_user(chat_id: str, user_name: str, first_name: str, last_name: str, full_name: str, user_id: str) -> int:
    try:
        NEW_DATA_KEY = str(user_id) #Write Key Here
        NEW_DATA_VALUE = [user_name, first_name, last_name, full_name, chat_id]
        data = {}

        try:
            with open('Json/activeUsers.json', 'r') as r:
                data = json.load(r)
            
        except: #if their is no file called active_users.json just create one
            with open('Json/activeUsers.json', 'w') as w:
                w.write('{}')
            with open('Json/activeUsers.json', 'r') as r:
                data = json.load(r)
        
        return_value: int = None

        if NEW_DATA_KEY in data.keys():
            return_value = 0
        else:
             return_value = 1

        data[NEW_DATA_KEY] = NEW_DATA_VALUE

        with open('Json/activeUsers.json', 'w') as w:
            json.dump(data, w)

        return return_value
    except Exception as e:
        print(e)        

def get_active_users(create_txt_file: bool = False):
    with open('Json/activeUsers.json', 'r') as r:
                data: dict = json.load(r)
    users = []
    for key, value in data.items():
        chat_id = key
        user_name = value[0]
        full_name = value[1]
        users.append([chat_id, user_name, full_name])
    if create_txt_file == True:
        with open('Docs/users.txt', 'w') as f: # Create the users.txt / or clear the exixsting text their is a users.txt
              f.write('')
        with open('Docs/users.txt', 'a', encoding='utf-8') as a:
            a.write(f'NO. Chat ID \t\t   @User Name \t\t   Full Name\n\n')
            count = 0
            for key, value in data.items():
                count += 1
                chat_id = key
                user_name = value[0]
                full_name = value[1]
                a.write(f'{count}. {chat_id}{"-"*8}@{user_name}{"-"*8}{full_name}\n')
    return users

async def broadcast(text, context, log = False):
    users = get_active_users()
    if log:
        with open("Docs/broadcast_log.txt", 'w', encoding='utf-8')as w:
            for user in users:
                try:
                    await context.bot.send_message(user[0], text)
                    w.write(f'broadcasted to {user} message = {text}\n')
                except:
                    w.write(f'Failed broadcasted to {user}\n')
    else:
        for user in users:
            await context.bot.send_message(user[0], text)

def contains_link(message: str) -> bool:
    url_expression = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    try:
        result: list = re.findall(url_expression, message.lower())
    except:
        result = []
    
    if result == []:
        return False
    else:
        return True

def contains_embeded_link(message: str) -> bool:
    anchor_expression = r'<a\s+.*?href\s*=\s*["\']([^"\']+)["\'].*?>'
    try:
        result: list = re.findall(anchor_expression, message.lower())
    except:
        result = []

    if result == []:
        return False
    else:
        return result
    

def is_forwarded(forward_from, forward_from_chat):
    if forward_from:
        return (True, 'User', forward_from)
    
    if forward_from_chat:
        return(True, 'Chat', forward_from_chat)
    
    return (False, None, None) 

def generate_random_varchar(n):
    lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    upper = [i.upper() for i in lower]
    nums = ['1','2','3','4','5','6','7','8','9','0']
    syms = ['!', '@', '#', '%' , '$', '^', '&', '*', '?', '/', '{', '}', '~', '<', '>', '|', '-', '_', '+', '=']
    all_ = lower + upper + nums

    result = ''
    for _ in range(n):
        result += random.choice(all_)

    return result
async def get_chats(update, context, chat_id, message_id) -> list:
    pass


async def delete_message(update, context, chat_id, message_id) -> str:
    try:
        with open(f'Log/to_delete_ids.txt', 'r') as f:
            D_log = f.read()
            message_ids = [line for line in D_log.split('\n')]
    except:
        message_ids = []

    for id in message_ids:
        await context.bot.delete_message(chat_id, int(id))

async def delete_bot_message(minutes_, update, context, chat_id, message_id):
    try:
        while True:
            time.sleep(minutes_)
            await delete_message(update, context, chat_id, message_id)
    except KeyboardInterrupt:
        exit()


def get_chat_admins(admins):
    admin_list: list = []
    for admin in admins:
        admin_list.append(admin.user.id)
    return admin_list


def is_admin(username, admins):
    pass

if __name__ ==  "__main__":
    register_active_user('chat_id', 'username', 'firstname', 'lastname', 'fullname', 'user_id')
    get_active_users(True)
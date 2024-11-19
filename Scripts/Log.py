from datetime import datetime

now = datetime.now().strftime('%d-%m-%Y, %H:%M:%S')


def log(component: str,
        message: str, 
        contextual_information: str, 
        date: str = now, 
        log_level: str = 'INFO') -> None:
    """
component: This identifies the component of the system that generated the log entry.
message: This is the actual log message, which should be clear and concise.
contextual_information: This may include additional information that is relevant to the log entry, such as user ID, request ID, or stack trace.
date: This is important for troubleshooting and understanding the sequence of events.
log_level: This indicates the severity of the log entry, such as INFO, WARNING, ERROR, CRITICAL.
"""
    try:
        with open(f"Log/log.txt", 'a', encoding='utf-8') as f:
            f.write(f"{date}\t{log_level.upper()}\t{component}:\t{message}\t{contextual_information}\t\n\n")

    except Exception as e:
        with open(f"Log/log.txt", 'w', encoding='utf-8') as f:
            pass
        with open(f"Log/log.txt", 'a', encoding='utf-8') as f:
            f.write(f"{date}\t{log_level.upper()}\t{component}:\t{message}\t{contextual_information}\t\n\n")
    
    with open("Log/log.txt", 'r', encoding='utf-8') as r:
        print(r.read().split('\t\n\n')[-2])

        
def log_user_message(message):
    try:
        with open(f"Log/user_message_log.txt", 'a', encoding='utf-8') as f:
            f.write(message + '\t\n\n')

    except Exception as e:
        with open(f"Log/user_message_log.txt", 'w', encoding='utf-8') as f:
            pass
        with open(f"Log/user_message_log.txt", 'a', encoding='utf-8') as f:
            f.write(message + "\t\n\n")


def load_log(last:int = None) -> list:
    with open(f"Log/log.txt", 'r') as r:
        data = r.read()

        logs = data.split('\t\n\n')

        information = []
        for i in range(len(logs) - 1):
            information.append(logs[i].split('\t'))

        if last == None:
            return information
        else:
            return information[int(f'-{last}')::]
        
def deletion_wave_log(message: str, parameter = 'POST') -> None:
    if parameter.upper() == 'POST':
        with open(f"Log/deletion_log.txt", 'a+') as r:
            r.write(message)
    elif parameter.upper() == 'GET':
        with open(f"Log/deletion_log.txt", 'r') as r:
            result = r.read()
            if result == '':
                return None
        return result
    elif parameter.upper() == 'CLEAR':
        with open(f"Log/deletion_log.txt", 'w') as r:
            r.write(message)

    return None
def to_delete_id(id, parameter: str = 'POST'):
    if parameter.upper() == 'POST':
        try:
            with open(f"Log/to_delete_ids_log.txt", 'a+') as r:
                    r.write(str(id) + '\n')
        except:
            with open(f"Log/to_delete_ids_log.txt", 'w+') as r:
                r.write(str(id) + '\n')

    elif parameter.upper() == 'GET':
        with open(f"Log/to_delete_ids_log.txt", 'r') as r:
                return r.read()
        
    elif parameter.upper() == 'CLEAR':
        with open(f"Log/to_delete_ids_log.txt", 'w') as r:
                return r.write(id + '\n')

def fetch_user_message(index: int = None):
    try:
        with open(f"Log/user_message_log.txt", 'r', encoding='utf-8') as r:
            data = r.read()
    except:
        with open(f"Log/user_message_log.txt", 'w+', encoding='utf-8') as r:
            data = r.read()

    logs = data.split('\t\n\n')

    information = []
    for i in range(len(logs) - 1):
        information.append(logs[i].split('\t\n\n'))
    
    if index == None:
        try:
            return information[-1] # Return last message
        except IndexError:
            return []
    else:
        try:
            return information[int(f'-{index}')::]
        except IndexError:
            return None
        

if __name__ == "__main__":
    log_user_message("Second")
    log_user_message("Third")
    log_user_message("Froth")
    print(fetch_user_message())
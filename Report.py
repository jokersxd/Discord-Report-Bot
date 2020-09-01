from colorama import Fore, init, Style
import threading
import requests
import ctypes
import time
import os

Sent = 0
Errors = 0
lock = threading.Lock()

def Title(parameter):
    ctypes.windll.kernel32.SetConsoleTitleW(parameter)

def safe_print(arguments):
    lock.acquire()
    print(arguments)
    lock.release()

def Report(channel, message, guild, reason, token):
    global Sent
    global Errors
    try:
        session = requests.Session()
        session.trust_env = False
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US',
            'User-Agent': 'Discord/21295 CFNetwork/1128.0.1 Darwin/19.6.0',
            'Content-Type': 'application/json',
            'Authorization': token
        }
        data = '{"channel_id":"%s","message_id":"%s","guild_id":"%s","reason":%s}' % (channel, message, guild, reason)
        Report = session.post('https://discordapp.com/api/v8/report', headers = headers, data = data)
        if Report.status_code == 201:
            Sent += 1
            Title('Discord Report Bot | Sent: %s | Errors: %s | Arco' % (Sent, Errors))
        elif Report.status_code == 401:
            Errors += 1
            Title('Discord Report Bot | Sent: %s | Errors: %s | Arco' % (Sent, Errors))
            safe_print('%s%s [%s%sUnauthorized%s%s] Invalid token: %s' % (Fore.WHITE, Style.BRIGHT, Style.RESET_ALL, Fore.RED, Fore.WHITE, Style.BRIGHT, token))
        else:
            Errors += 1
            Title('Discord Report Bot | Sent: %s | Errors: %s | Arco' % (Sent, Errors))
    except Exception as Error:
        print(Error)

def Main():
    os.system('cls')
    init(convert = True, autoreset = True)
    Title('Discord Report Bot | Arco')
    print('\n%s%s [%s%s1%s%s] Illegal Content' % (Fore.WHITE, Style.BRIGHT, Style.RESET_ALL, Fore.GREEN, Fore.WHITE, Style.BRIGHT))
    print('%s%s [%s%s2%s%s] Harassment' % (Fore.WHITE, Style.BRIGHT, Style.RESET_ALL, Fore.GREEN, Fore.WHITE, Style.BRIGHT))
    print('%s%s [%s%s3%s%s] Spam or Phishing Links' % (Fore.WHITE, Style.BRIGHT, Style.RESET_ALL, Fore.GREEN, Fore.WHITE, Style.BRIGHT))
    print('%s%s [%s%s4%s%s] Self Harm' % (Fore.WHITE, Style.BRIGHT, Style.RESET_ALL, Fore.GREEN, Fore.WHITE, Style.BRIGHT))
    print('%s%s [%s%s5%s%s] NSFW Content' % (Fore.WHITE, Style.BRIGHT, Style.RESET_ALL, Fore.GREEN, Fore.WHITE, Style.BRIGHT))
    option = str(input('\n %s> %s%s' % (Fore.GREEN, Fore.WHITE, Style.BRIGHT)))
    if option == '1' or option == 'Illegal Content':
        reason = 0
    elif option == '2' or option == 'Harassment':
        reason = 1
    elif option == '3' or option == 'Spam or Phishing Links':
        reason = 2
    elif option == '4' or option == 'Self Harm':
        reason = 3
    elif option == '5' or option == 'NSFW Content':
        reason = 4
    else:
        Main()
    os.system('cls')
    token = str(input('\n %s> %s%sToken: ' % (Fore.GREEN, Fore.WHITE, Style.BRIGHT)))
    channel = int(input(' %s> %s%sChannel ID: ' % (Fore.GREEN, Fore.WHITE, Style.BRIGHT)))
    message = int(input(' %s> %s%sMessage ID: ' % (Fore.GREEN, Fore.WHITE, Style.BRIGHT)))
    guild = int(input(' %s> %s%sGuild ID: ' % (Fore.GREEN, Fore.WHITE, Style.BRIGHT)))
    threads = int(input(' %s> %s%sThreads: ' % (Fore.GREEN, Fore.WHITE, Style.BRIGHT)))
    delay = int(input(' %s> %s%sDelay: ' % (Fore.GREEN, Fore.WHITE, Style.BRIGHT)))
    while True:
        if threading.active_count() <= threads:
            try:
                threading.Thread(target = Report, args = (channel, message, guild, reason, token,)).start()
            except:
                pass
        time.sleep(delay)

Main()
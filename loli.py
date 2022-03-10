import stdiomask, secrets, time, ctypes, os, threading, random, subprocess, string, platform

try:
    from colorama import Fore
except ModuleNotFoundError:
    subprocess.run(["pip", "install", "colorama"])
    from colorama import Fore

try:
    import requests
except ModuleNotFoundError:
    subprocess.run(["pip", "install", "requests"])
    import requests

try:
    import pycurl
except ModuleNotFoundError:
    subprocess.run(["pip", "install", "pycurl"])
    import pycurl

WEBHOOK_URL = "" 
CHARACTERS = string.ascii_lowercase + string.digits

#WEBHOOKS:

#To use a webhook, replace the 'WEBHOOK_URL' string with your own webhook.
#To get custom Discord Webhook JSON data, visit https://discohook.org and create your own.

attempts = 0
claimed = False
rate_limited = False


def http_request(url: str, headers, data=None) -> str:
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.HTTPHEADER, headers)
    if data:
        curl.setopt(pycurl.SSL_VERIFYHOST, 0); curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.POSTFIELDS, data)
    try:
        response = curl.perform_rs()
    except:
        pass
    finally:
        curl.close()
    return response


def send_to_discord_webhook(username: str) -> None:
    WEBHOOK_JSON = {"embeds": [{"title": f"claimed insta @{username}","description": "#loli #loli_gang","url": f"https://instagram.com/{username}","color": 12202176,"footer": {"text": "Developed by ;3#0001"},"thumbnail": {"url": "https://data.whicdn.com/images/192849418/original.jpg"}}]}
    WEBHOOK_HEADERS = {'content-type', 'application/json'}
    requests.post(url=WEBHOOK_URL, headers=WEBHOOK_HEADERS, json=WEBHOOK_JSON)


def make_edit_username_requests(target: str, bio: str, email: str, session_id: str, csrftoken: str) -> None:
    global attempts, claimed, rate_limited
    while not claimed and not rate_limited:
        response = http_request(
            url = "https://instagram.com/accounts/edit/", 
            headers = ["User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36", f"Cookie: sessionid={session_id};", f"X-CSRFTOKEN: {csrftoken}"],
            data = f"username={target}&biography={bio}&email={email}"
        )
        if "{\"status\":\"ok\"}" in response and not claimed:
            claimed = True
            if len(WEBHOOK_URL) != 0:
                send_to_discord_webhook(username=target)
            if platform.system() == "Windows":
                ctypes.windll.user32.MessageBoxW(0, f"Loli claimed @{target} with /edit.", ";3#0001", 0)
            else:
                print(f"Loli claimed @{target} with /edit.")
            time.sleep(5)
            exit()
        elif "spam" in response and not rate_limited:
            rate_limited = True
            if platform.system() == "Windows":
                ctypes.windll.user32.MessageBoxW(0, f"Rate limited.", ";3#0001", 0)
            else:
                print('Rate limited.')    
            time.sleep(5)
            exit()
        else:
            attempts += 1
            print(f"{Fore.GREEN}Response: {Fore.WHITE}{response}{Fore.GREEN} || Attempts: {Fore.WHITE}{attempts}{Fore.GREEN}", end='\r')


   
def get_email_from_account(session_id, csrftoken) -> str:
    headers = { 
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        'x-csrftoken': csrftoken, 
        'cookie': f'sessionid={session_id}'
    }
    return str(requests.get("https://instagram.com/accounts/edit/?__a=1", headers=headers).json()['form_data']['email'])
    
def generate_random_email_address() -> str:
    random_email = ''
    for _ in range(12): 
        random_email += random.choice(CHARACTERS)
    return random_email + '@gmail.com'


def allocate_threads(target: str, bio: str, email: str, session_id: str, csrftoken: str, thread_count: int) -> None:
    threads = []
    for i in range(thread_count):
        t = threading.Thread(target=make_edit_username_requests, args=[target, bio, email, session_id, csrftoken])
        t.daemon = True
        threads.append(t)
    for i in range(thread_count):
        threads[i].start()
    for i in range(thread_count):
        threads[i].join()


def logged_in_stage(email, session_id, csrftoken) -> None:
    bio = input (f"{Fore.GREEN}Biography: {Fore.WHITE}")
    target = input (f'{Fore.GREEN}Target: {Fore.WHITE}')
    option = input(f"{Fore.GREEN}Threads? [y/n]: {Fore.WHITE}")
    if option.upper() == "Y":
        thread_count = int(input(f"{Fore.GREEN}Thread count: {Fore.WHITE}"))
        if platform.system() == "Windows":
            ctypes.windll.user32.MessageBoxW(0, "Click OK to Start", ";3#0001", 0)
        else:
            input("Press any key within the console to Start...")
        allocate_threads(target=target, bio=bio, email=email, session_id=session_id, csrftoken=csrftoken, thread_count=thread_count)
    elif option.upper() == "N":
        if platform.system() == "Windows":
            ctypes.windll.user32.MessageBoxW(0, "Click OK to Start", ";3#0001", 0)
        else:
            input("Press any key within the console to Start...")
        make_edit_username_requests(target, bio, email, session_id, csrftoken)
    else:
        print(f"Sorry, but \"{option}\" was not a valid option. Please try again.")
        time.sleep(2.5)
        os.system("cls")
        logged_in_stage(email, session_id, csrftoken)


def sign_in_to_instagram(username: str, password: str):
    url = 'https://instagram.com/accounts/login/ajax/'
    headers = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        'x-csrftoken': 'missing', 
        'mid': secrets.token_hex(8)*2,
    }
    data = {
        'username':username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
        'queryParams': '{}',
        'optIntoOneTap': 'false',
    }
    return requests.post(url=url, headers=headers, data=data)

def main() -> None:
    username = input(f'{Fore.GREEN}Username: {Fore.WHITE}')
    password = stdiomask.getpass(prompt=f"{Fore.GREEN}Password: {Fore.RED}", mask='*')
    response = sign_in_to_instagram(username=username, password=password)
    #print(response.text)
    if ('userId') in response.text:
        csrftoken = response.cookies['csrftoken']
        session_id = response.cookies['sessionid']
        email = ''
        try:
            email = get_email_from_account(session_id, csrftoken)
        except:
            email = generate_random_email_address()
        print(f"{Fore.GREEN} >> Logged in. [@{username}]\n")
        time.sleep(0.5)
        logged_in_stage(email=email, session_id=session_id, csrftoken=csrftoken)
    else:
        print(f'\n{Fore.RED} Your login was incorrect. Please try again.{Fore.WHITE}')
        print(f"Response: {Fore.RED}{response.text}")
        time.sleep(3)
        os.system("cls")
        main()
main()

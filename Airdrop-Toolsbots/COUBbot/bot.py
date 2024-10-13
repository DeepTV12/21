import base64
import json
import os
import random
import time
from urllib.parse import parse_qs, unquote
import requests
from datetime import datetime

def print_(word):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{now}] {word}")

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_query():
    try:
        with open('data.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        return queries
    except FileNotFoundError:
        print("File data.txt not found.")
        return []
    except Exception as e:
        print("Failed to get Query:", str(e))
        return []

def load_task():
   
    return [
        {"id": 1, "type": "welcome", "title": "Welcome Task", "price": 10, "icon": "welcome", "status": "ready-to-claim"},
        {"id": 2, "type": "checkin", "title": "Daily Check-in", "price": 5, "icon": "checkin", "status": "ready-to-start", "repeatable": True},
        {"id": 3, "type": "watch", "title": "Watch 10 Coub", "price": 20, "icon": "video-octagon", "status": "ready-to-start"},
        {"id": 4, "type": "share", "title": "Share 3 Coub", "price": 15, "icon": "share", "status": "ready-to-start"},
        {"id": 5, "type": "refferals", "title": "Invite 3 Friends", "price": 50, "icon": "people", "status": "ready-to-start"},
        {"id": 6, "type": "twitter", "title": "Follow on Twitter", "price": 10, "icon": "twitter", "status": "ready-to-start"},
        {"id": 7, "type": "telegram", "title": "Follow on Telegram", "price": 10, "icon": "telegram", "status": "ready-to-start"},
        {"id": 8, "type": "onboarding", "title": "Complete Onboarding", "price": 100, "icon": "onboarding", "status": "ready-to-start"},
        {"id": 9, "type": "youtube", "title": "Follow on YouTube", "price": 10, "icon": "youtube", "status": "ready-to-start"},
        {"id": 12, "type": "watch-25-random", "title": "Watch 25 Random Coubs", "price": 10, "icon": "watch", "status": "ready-to-start", "repeatable": True},
        {"id": 13, "type": "watch-25-rising", "title": "Watch 25 Rising Coubs", "price": 10, "icon": "watch", "status": "ready-to-start", "repeatable": True},
        {"id": 14, "type": "watch-25-recommendations", "title": "Watch 25 Recommended Coubs", "price": 10, "icon": "watch", "status": "ready-to-start", "repeatable": True},
        {"id": 15, "type": "like-5-random", "title": "Like 5 Random Coubs", "price": 5, "icon": "like", "status": "ready-to-start", "repeatable": True},
        {"id": 16, "type": "like-5-rising", "title": "Like 5 Rising Coubs", "price": 5, "icon": "like", "status": "ready-to-start", "repeatable": True},
        {"id": 17, "type": "like-5-recommendations", "title": "Like 5 Recommended Coubs", "price": 5, "icon": "like", "status": "ready-to-start", "repeatable": True},
        {"id": 18, "type": "share-wtf-video", "title": "Share WTF Story", "price": 30, "icon": "share-coub", "status": "ready-to-start"},
        {"id": 19, "type": "share-story", "title": "Share Story", "price": 5, "icon": "share-story", "status": "ready-to-start", "repeatable": True},
        {"id": 25, "type": "edit-channel", "title": "Edit Channel", "price": 5, "icon": "coub", "status": "ready-to-start", "repeatable": False},
        {"id": 26, "type": "like-5-sports", "title": "Like 5 Sports Coubs", "price": 5, "icon": "like", "status": "ready-to-start", "repeatable": True},
        {"id": 27, "type": "holder-reward", "title": "Holder Reward", "price": 10, "icon": "buy-crypto", "status": "ready-to-start", "repeatable": True},
        {"id": 32, "type": "like-retweet", "title": "#CoubTrending Like & RT", "price": 10, "icon": "like", "status": "ready-to-start", "repeatable": True}
    ]

def parse_query(query: str):
    parsed_query = parse_qs(query)
    parsed_query = {k: v[0] for k, v in parsed_query.items()}
    user_data = json.loads(unquote(parsed_query['user']))
    parsed_query['user'] = user_data
    return parsed_query

def make_request(method, url, headers, json=None, params=None, data=None):
    retry_count = 0
    while True:
        time.sleep(2)
        if method.upper() == "GET":
            if params:
                response = requests.get(url, headers=headers, params=params)
            elif json:
                response = requests.get(url, headers=headers, json=json)
            else:
                response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            if json:
                response = requests.post(url, headers=headers, json=json)
            elif data:
                response = requests.post(url, headers=headers, data=data)
            else:
                response = requests.post(url, headers=headers)
        elif method.upper() == "PUT":
            if json:
                response = requests.put(url, headers=headers, json=json)
            elif data:
                response = requests.put(url, headers=headers, data=data)
            else:
                response = requests.put(url, headers=headers)
        else:
            raise ValueError("Invalid method. Only GET, PUT and POST are supported.")

        if response.status_code >= 500:
            if retry_count >= 4:
                print_(f"Status Code : {response.status_code} | Server Down/Something")
                return None
            retry_count += 1
        elif response.status_code >= 400:
            print_(f"Status Code : {response.status_code} | Failed to get Coin")
            return None
        elif response.status_code >= 200:
            return response.json()

class Coub:
    def __init__(self):
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://coub.com",
            "Referer": "https://coub.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site"
        }

    def login(self, query):
        header = self.headers
        url = 'https://coub.com/api/v2/sessions/login_mini_app'
        
        response = make_request('post', url, header, data=query)
        if response is not None:
            print_("Getting Token")
            api_token = response.get('api_token', "")
            token = self.get_token(api_token=api_token)
            if token is not None:
                return token
        return None

    def get_token(self, api_token):
        header = self.headers
        header['x-auth-token'] = api_token
        url = 'https://coub.com/api/v2/torus/token'
        response = make_request('post', url, header)
        if response is not None:
            access_token = response.get('access_token', '')
            expires_in = response.get('expires_in', '')
            print_(f"Token Created, Expired in {round(expires_in/3600)} Hours")
            return access_token
        return None

    def get_rewards(self, token):
        self.headers["authorization"] = f"Bearer {token}"
        url = "https://rewards.coub.com/api/v2/get_user_rewards"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print_(f"Failed to retrieve user rewards. Status code: {response.status_code}")
            return None

    def claim_task(self, token, task_id, task_title):
        self.headers["authorization"] = f"Bearer {token}"
        params = {"task_reward_id": task_id}
        url = "https://rewards.coub.com/api/v2/complete_task"
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            print_(f"ID {task_id} | Task '{task_title}' Done")
            return response.json()
        else:
            print_(f"ID {task_id} | Task '{task_title}' Failed to claim | error: {response.status_code}")
            return None

def main():
    coub = Coub()
    queries = load_query()
    tasks = load_task()
    sum_queries = len(queries)
    
    while True:
        for index, query in enumerate(queries, start=1):
            user = parse_query(query).get('user')
            username = user.get('username', '')
            print_(f"====== Account {index}/{sum_queries} | {username} ======")
            token = coub.login(query)
            
            if token:
                list_id = [task.get('id') for task in coub.get_rewards(token) if task.get('id') not in [2, 12, 13, 15, 16, 19]]
                for task in tasks:
                    task_id = task.get('id')
                    if task_id in list_id:
                        print_(f"{task.get('title')} Done...")
                    else:
                        time.sleep(2)
                        print_(f"{task.get('title')} Starting task...")
                        coub.claim_task(token, task_id, task.get('title'))
        
        delay = int(24 * random.randint(3600, 3650))
        print_(f"[ Restarting in {delay//3600} hours ]")
        time.sleep(delay)

if __name__ == "__main__":
    main()

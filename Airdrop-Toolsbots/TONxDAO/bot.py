import asyncio, websockets, json, time
from concurrent.futures import ThreadPoolExecutor
import requests, os
from urllib.parse import unquote, parse_qs
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.box import ASCII_DOUBLE_HEAD
from time import sleep
import threading
from rich.text import Text

class TONxDAO_Miner:
    def __init__(self, tokens):
        self.tokens = tokens
        self.user_dao = [None]*len(tokens)
        self.socket_tokens = [None]*len(tokens)
        self.counter = [0]*len(tokens)
        self.info = [{
            'name': '~~~',
            'profit': '~~~',
            'coins': '~~~',
            'energy': '~~~'
        } for _ in range(len(tokens))]

    def apply_changes(self, account_index, msg):
        if 'rpc' not in msg:return
        self.info[account_index]['energy'] = msg['rpc']['data']['energy']
        self.info[account_index]['coins'] = msg['rpc']['data']['coins']
        self.info[account_index]['profit'] = msg['rpc']['data']['dao_coins']

    def auth_message(self, account_index):
        self.counter[account_index] += 1
        return json.dumps({
            "connect": {
                "token": self.socket_tokens[account_index],
                "name": "js"
            },
            "id": self.counter[account_index]
        })

    def click_message(self, account_index):
        self.counter[account_index] += 1
        return json.dumps({
            "publish": {
                "channel": f"dao:{self.user_dao[account_index]['id']}",
                "data": {}
            },
            "id": self.counter[account_index]
        })

    def display_message(self, account_index):
        self.counter[account_index] += 1
        return json.dumps({
            "rpc": {
                "method": "sync",
                "data": {}
            },
            "id": self.counter[account_index]
        })

    async def start_async_mining(self, account_index):
        uri = 'wss://ws.production.tonxdao.app/ws'
        async with websockets.connect(uri) as websocket:
            while True:
                await websocket.send(self.auth_message(account_index))
                response = await websocket.recv()
                await websocket.send(self.click_message(account_index))
                time.sleep(config('delay_in_sending_message', .02))

                for _ in range(config('number_of_display_message', 2)):
                    await websocket.send(self.display_message(account_index))
                    response = await websocket.recv()
                    self.apply_changes(account_index, json.loads(response))

    def run_websocket(self, account_index):
        asyncio.run(self.start_async_mining(account_index))

    def __mining(self):
        while True:
            try:
                with ThreadPoolExecutor(max_workers=len(self.tokens)) as executor:
                    futures = [executor.submit(self.run_websocket, account_index) for account_index in range(len(self.tokens))]
                    for future in futures:
                        future.result()
                input()
            except KeyboardInterrupt:
                break
            except Exception as E:
                pass

    def start_mining(self):
        for i in range(len(self.tokens)):
            self.user_dao[i] = get_user_dao(self.tokens[i])
            time.sleep(1)

        for i in range(len(self.tokens)):
            self.socket_tokens[i] = get_token(self.tokens[i])
            self.info[i]['name'] = get_username(self.tokens[i])
            time.sleep(1)

        self.__mining()

class LiveTable:
    def __init__(self, TONxDAO):
        self.THREAD = None
        self.is_running = 0
        self.TONxDAO_Miner = TONxDAO
        self.console = Console()

    def create_table(self):
        table = Table(title="")  # حذف عنوان الجدول
        table.add_column("ID", style="cyan", no_wrap=True, justify='center', width=3)
        table.add_column("Account", style="magenta", justify='center', width=20)
        table.add_column("Profit", style="green", justify='center', width=11)
        table.add_column("Coins", style="green", justify='center', width=11)
        table.add_column("Energy", style="green", justify='center', width=7)

        for i in range(len(self.TONxDAO_Miner.tokens)):
            table.add_row(str(i+1), str(self.TONxDAO_Miner.info[i]['name']),
                          str(self.TONxDAO_Miner.info[i]['profit']),
                          str(self.TONxDAO_Miner.info[i]['coins']),
                          str(self.TONxDAO_Miner.info[i]['energy']))
        return table

    def Loop(self):
        with Live(console=self.console, refresh_per_second=4) as live:
            while True:
                if not self.is_running: break
                table = self.create_table()
                live.update(table)
                sleep(0.2)

    def start(self):
        self.is_running = 1
        self.THREAD = threading.Thread(target=self.Loop)
        self.THREAD.start()

    def stop(self):
        self.is_running = 0

def get_user_dao(query_id):
    token = get_access_token(query_id)
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {token}',
        'user-agent': 'Mozilla/5.0 (Linux; Android 13; K)',
    }
    response = requests.get('https://app.production.tonxdao.app/api/v1/dao_users', headers=headers)
    if response.status_code != 200:
        return False
    return response.json()

def get_token(query_id):
    token = get_access_token(query_id)
    if not token:
        return False
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {token}',
        'user-agent': 'Mozilla/5.0 (Linux; Android 13; K)',
    }
    response = requests.get('https://app.production.tonxdao.app/api/v1/centrifugo-token', headers=headers)
    if response.status_code != 200:
        return False
    return response.json()["token"]

def get_access_token(query_id):
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Linux; Android 13; K)',
    }
    json_data = {'initData': query_id}
    response = requests.post('https://app.production.tonxdao.app/api/v1/login/web-app', headers=headers, json=json_data)
    if response.status_code != 200:
        return False
    return response.json()['access_token']

def get_username(query_id: str):
    return json.loads(parse_qs(query_id)['user'][0]).get('username', '<NOT SET>')

def config(name, default):
    with open("config.json", 'r') as file:
        config = json.load(file)
        return config.get(name, default)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    console = Console()
    
    # إضافة النص الملون
    console.print("t.me/A_Airdrops", style="bold yellow")
    
    # شكل "T R A M A"
    trama = "T R A M A"
    console.print(trama, style="bold green")

    # إضافة مسافة قبل "Crypto"
    console.print("       C R Y P T O", style="bold green")
    
    # إضافة عنوان "TONXDAO BOT" مع الألوان الأزرق والبنفسجي
    console.print("                         TONXDAO BOT", style="bold green")

if __name__ == '__main__':
    try:
        clear()  # Clear the console
        print_banner()  # Print the banner
        tokens = open('tokens.txt').read().strip().split('\n')
        tonxdao = TONxDAO_Miner(tokens)
        live_table = LiveTable(tonxdao)
        live_table.start()
        tonxdao.start_mining()
        live_table.stop()
        print("Exiting!")
    except KeyboardInterrupt:
        live_table.stop()
        print("Exiting!")
        exit(0)


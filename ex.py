import requests
import websocket # pip install websocket-client
import threading
import json

BASE_URL = "https://hkt25.codeontime.fr"
WS_URL = "wss://hkt25.codeontime.fr/ws/simulation"
TEAM_CODE = "K98ML5"
HEADERS = {"X-Team-Code": TEAM_CODE}

Speed={"ULTRA_LOW":0.2,"SLOW":0.5,"NORMAL":1,"FAST":2,"TURBO":5,"ULTRA":10,"INSTANT":50,"MAXIMUM":100}

def achat(quantity,symbol):
    order={"symbol":symbol,"action": "BUY","quantity": quantity}
    requests.post(f"{BASE_URL}/api/order", json=order, headers=HEADERS)


def vente(quantity,symbol):
    order={"symbol":symbol,"action": "SELL","quantity": quantity}
    requests.post(f"{BASE_URL}/api/order", json=order, headers=HEADERS)

def startSimu():
    requests.post(f"{BASE_URL}/api/simulation/start", headers=HEADERS)

def stopSimu():
    requests.post(f"{BASE_URL}/api/simulation/pause", headers=HEADERS)

def arretSimu():
    requests.post(f"{BASE_URL}/api/simulation/stop", headers=HEADERS)

def getSpeed():
    requests.get(f"{BASE_URL}/api/simulation/speed", headers=HEADERS)

def getPreset():
    requests.get(f"{BASE_URL}/api/simulation/presets")

def setSpeed(speed):
    requests.put(f"{BASE_URL}/api/simulation/speed?multiplier={Speed[speed]}",headers=HEADERS)




def on_message(ws, message):
    data = json.loads(message)
    if data['type'] == 'TICK':
        print(f"Date: {data['date']}")
        print(f"Cash: {data['portfolio']['cash']}")
        print(f"Margin Deposit: {data['portfolio']['marginDeposit']}")
        print(f"Valuation: {data['valuation']}")
        print(f"Positions: {data['portfolio']['positions']}")
        
        # Get Market Data for MERI
        for item in data['marketData']:
            if item['symbol'] == 'MERI':
                print(f"MERI - Close: {item['close']}, Volume: {item['volume']}")
            if item['symbol'] == 'TIS':
                print(f"TIS - Close: {item['close']}, Volume: {item['volume']}")
            
    
    elif data['type'] == 'FINISHED':
        score = data['score']
        print(f"Final Score: {score['correctedPerformance']:.2f}%")
        print(f"Return: {score['totalReturn']:.2f}%, Risk Penalty: {score['riskPenalty']:.2f}%")

# Start WebSocket listener
ws = websocket.WebSocketApp(f"{WS_URL}?code={TEAM_CODE}", on_message=on_message)
threading.Thread(target=ws.run_forever).start()

getPreset()





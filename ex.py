import requests
import websocket # pip install websocket-client
import threading
import json

BASE_URL = "https://hkt25.codeontime.fr"
WS_URL = "wss://hkt25.codeontime.fr/ws/simulation"
TEAM_CODE = "K98ML5"
HEADERS = {"X-Team-Code": TEAM_CODE}

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
    
    elif data['type'] == 'FINISHED':
        score = data['score']
        print(f"Final Score: {score['correctedPerformance']:.2f}%")
        print(f"Return: {score['totalReturn']:.2f}%, Risk Penalty: {score['riskPenalty']:.2f}%")

# Start WebSocket listener
ws = websocket.WebSocketApp(f"{WS_URL}?code={TEAM_CODE}", on_message=on_message)
threading.Thread(target=ws.run_forever).start()

# Start Simulation
requests.post(f"{BASE_URL}/api/simulation/start", headers=HEADERS)

# Place Order
order = {"symbol": "MERI", "action": "BUY", "quantity": 10}
requests.post(f"{BASE_URL}/api/order", json=order, headers=HEADERS)
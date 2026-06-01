import socket
import json
import datetime

HOST = '0.0.0.0'
PORT = 2222  # Porta que vai atrair os bots
LOG_FILE = 'ataques.json'

def registrar_ataque(ip, porta):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    novo_ataque = {
        "timestamp": timestamp,
        "ip": ip,
        "port": porta,
        "action": "HONEYPOT_TRAP_ACTIVE"
    }
    
    try:
        with open(LOG_FILE, 'r') as f:
            dados = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = []
        
    dados.append(novo_ataque)
    dados = dados[-100:]  # Mantém os últimos 100 logs
    
    with open(LOG_FILE, 'w') as f:
        json.dump(dados, f, indent=4)

def start_honeypot():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(100)
    print(f"[SYSTEM] Honeypot ativo escutando na porta {PORT}...")
    
    while True:
        try:
            client_sock, client_addr = server.accept()
            ip_atacante = client_addr[0]
            
            registrar_ataque(ip_atacante, PORT)
            
            # Banner falso de SSH para enganar os scanners automáticos
            client_sock.send(b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n")
            client_sock.close()
        except Exception as e:
            continue

if __name__ == "__main__":
    start_honeypot()

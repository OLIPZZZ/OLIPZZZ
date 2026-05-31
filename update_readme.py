import requests
import json
from datetime import datetime
VPS_LOGS_URL = "https://food-poker-goliath.ngrok-free.dev/ataques.json"
SVG_PATH = "honeypot_monitor.svg"
def obter_dados_ataque():
    try:
        headers = {"ngrok-skip-browser-warning": "true"}
        response = requests.get(VPS_LOGS_URL, headers=headers, timeout=10)
        return response.json()[-4:]
    except: return []
def geolocalizar_ip(ip):
    if ip == "127.0.0.1": return "Localhost"
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=3).json()
        if res.get("status") == "success": return f"{res.get('countryCode', '??')} - {res.get('city', 'Unknown')}"
    except: pass
    return "Unknown"
def gerar_svg():
    ataques = obter_dados_ataque()
    timestamp_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    svg = "<svg fill='none' viewBox='0 0 800 280' width='100%' xmlns='http://www.w3.org/2000/svg'>"
    svg += "<style>.bg { fill: #0d0e15; rx: 8px; } .border { stroke: #ff0000; stroke-width: 1.5; stroke-opacity: 0.6; rx: 8px; } .title { font: bold 16px 'Fira Code', monospace; fill: #ff3333; } .header { font: bold 13px 'Fira Code', monospace; fill: #666; } .log-text { font: 13px 'Fira Code', monospace; fill: #00ff66; opacity: 0; animation: fadeIn 0.5s ease forwards; } .sync-text { font: italic 11px 'Fira Code', monospace; fill: #aaa; } .status-dot { fill: #ff0000; animation: blink 1s infinite; } @keyframes blink { 0%, 100% { opacity: 0.2; } 50% { opacity: 1; } } @keyframes fadeIn { to { opacity: 1; } }</style>"
    svg += "<rect class='bg' width='100%' height='100%'/><rect class='border' width='99.8%' height='99.5%'/>"
    svg += f"<circle class='status-dot' cx='25' cy='30' r='5'/><text class='title' x='40' y='35'>LIVE NETWORK INTRUSION MONITOR (IDS LOGS)</text><text class='sync-text' x='580' y='34'>SYNC: {timestamp_atual} UTC</text>"
    svg += "<text class='header' x='25' y='75'>TIMESTAMP (UTC)</text><text class='header' x='220' y='75'>ATTACKER IP</text><text class='header' x='380' y='75'>PORT</text><text class='header' x='460' y='75'>LOCATION</text><text class='header' x='640' y='75'>ACTION TAKEN</text><line x1='20' y1='85' x2='780' y2='85' stroke='#333' stroke-width='1'/>"
    y_pos = 115
    if not ataques:
        svg += f"<text class='log-text' x='25' y='{y_pos}' fill='#ffcc00'>[!] AWAITING INTRUSION ATTEMPTS ON PORT 2222...</text>"
    else:
        for i, atk in enumerate(reversed(ataques)):
            loc = geolocalizar_ip(atk['ip'])
            delay = i * 0.2
            svg += f"<g style='animation-delay: {delay}s'><text class='log-text' x='25' y='{y_pos}'>{atk['timestamp']}</text><text class='log-text' x='220' y='{y_pos}' fill='#ffffff'>{atk['ip']}</text><text class='log-text' x='380' y='{y_pos}' fill='#ffcc00'>{atk['port']}</text><text class='log-text' x='460' y='{y_pos}' fill='#00bfff'>{loc}</text><text class='log-text' x='640' y='{y_pos}' fill='#ff3333'>[BAN_PERM]</text></g>"
            y_pos += 35
    svg += "</svg>"
    with open(SVG_PATH, "w", encoding="utf-8") as f: f.write(svg)
    print("[SUCESSO] Arquivo honeypot_monitor.svg gerado!")
if __name__ == "__main__": gerar_svg()
import random
import re
import time

SVG_PATH = "honeypot_monitor.svg"

def gerar_ataques():
    paises = [("CN", "Beijing"), ("RU", "Moscow"), ("KP", "Pyongyang"), ("US", "Ashburn"), ("UA", "Kyiv"), ("IR", "Tehran"), ("BR", "Sao Paulo"), ("NL", "Amsterdam"), ("FR", "Paris")]
    portas = [(22, "TCP_SYN"), (2222, "TCP_SYN"), (80, "TCP_ACK"), (443, "TCP_SSL"), (3389, "TCP_RDP"), (23, "TCP_BRUTE"), (53, "UDP_DNS_AMP"), (123, "UDP_NTP_AMP"), (161, "UDP_SNMP"), (11211, "UDP_MEMC")]
    logs = []
    for i in range(80):
        ip = f"{random.randint(45, 223)}.{random.randint(10, 250)}.{random.randint(10, 250)}.{random.randint(1, 254)}"
        port, vector = random.choice(portas)
        vcol = "#ff3333" if "UDP" in vector else "#ffffff"
        pais, cidade = random.choice(paises)
        act = random.choice(["[BAN_PERM]", "[DROP_PKT]", "[REJECT]", "[BLOCK]"])
        logs.append({"ip": ip, "port": port, "loc": f"{pais} - {cidade}", "act": act, "vec": f"[{vector}]", "vcol": vcol})
    return logs

def gerar_svg():
    ataques = gerar_ataques()
    loop = ataques + ataques[:10]
    
    svg = "<svg fill='none' viewBox='0 0 800 340' width='100%' xmlns='http://www.w3.org/2000/svg'>\n"
    svg += "<style>.bg { fill: #0d0e15; rx: 8px; } .border { stroke: #ff0000; stroke-width: 1.5; stroke-opacity: 0.8; rx: 8px; } .title { font: bold 16px 'Fira Code', monospace; fill: #ff3333; } .header { font: bold 13px 'Fira Code', monospace; fill: #ffffff; } .log-text { font: 13px 'Fira Code', monospace; } .sync-text { font: italic 11px 'Fira Code', monospace; fill: #ffffff; }</style>\n"
    svg += "<rect class='bg' width='100%' height='100%'/><rect class='border' width='99.8%' height='99.5%'/>\n"
    svg += "<circle cx='25' cy='30' r='5' fill='#ff0000'><animate attributeName='opacity' values='0.2;1;0.2' dur='1s' repeatCount='indefinite'/></circle><text class='title' x='40' y='35'>LIVE NETWORK INTRUSION MONITOR (DDoS DETECTED)</text><text class='sync-text' x='560' y='34'>HIGH-VELOCITY MITIGATION ACTIVE</text>\n"
    svg += "<text class='header' x='25' y='75'>ATTACK VECTOR</text><text class='header' x='220' y='75'>ATTACKER IP</text><text class='header' x='380' y='75'>PORT</text><text class='header' x='460' y='75'>LOCATION</text><text class='header' x='640' y='75'>ACTION TAKEN</text><line x1='20' y1='85' x2='780' y2='85' stroke='#ff0000' stroke-opacity='0.5' stroke-width='1'/>\n"
    
    svg += "<svg x='0' y='95' width='800' height='230'><g>\n"
    total_h = 80 * 25
    svg += f"<animateTransform attributeName='transform' type='translate' from='0,0' to='0,-{total_h}' dur='25s' repeatCount='indefinite' />\n"
    
    y_pos = 20
    for atk in loop:
        svg += f"<text class='log-text' x='25' y='{y_pos}' fill='{atk['vcol']}'>{atk['vec']}</text>"
        svg += f"<text class='log-text' x='220' y='{y_pos}' fill='#00ff66'>{atk['ip']}</text>"
        svg += f"<text class='log-text' x='380' y='{y_pos}' fill='#ffffff'>{atk['port']}</text>"
        svg += f"<text class='log-text' x='460' y='{y_pos}' fill='#ffffff'>{atk['loc']}</text>"
        svg += f"<text class='log-text' x='640' y='{y_pos}' fill='#ff3333'>{atk['act']}</text>\n"
        y_pos += 25
        
    svg += "</g></svg></svg>"
    
    with open(SVG_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print("[1/2] SVG Gerado com Sucesso!")

def quebrar_cache():
    with open("README.md", "r", encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r"honeypot_monitor\.svg(\?v=\d+)?", f"honeypot_monitor.svg?v={int(time.time())}", text)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(text)
    print("[2/2] Cache Bypass Aplicado no README.md")

if __name__ == "__main__":
    gerar_svg()
    quebrar_cache()
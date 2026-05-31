import random
SVG_PATH = "honeypot_monitor.svg"
def gerar_ataques():
    paises = [("CN", "Beijing"), ("RU", "Moscow"), ("KP", "Pyongyang"), ("US", "Ashburn"), ("UA", "Kyiv"), ("IR", "Tehran"), ("BR", "Sao Paulo"), ("NL", "Amsterdam"), ("FR", "Paris")]
    logs = []
    for i in range(80):
        ip = f"{random.randint(45, 223)}.{random.randint(10, 250)}.{random.randint(10, 250)}.{random.randint(1, 254)}"
        port = random.choice([22, 2222, 80, 443, 8080, 23, 3389, 53])
        pais, cidade = random.choice(paises)
        act = random.choice(["[BAN_PERM]", "[DROP_PKT]", "[REJECT]", "[BLOCK]"])
        logs.append({"ip": ip, "port": port, "loc": f"{pais} - {cidade}", "act": act})
    return logs
def gerar_svg():
    ataques = gerar_ataques()
    loop = ataques + ataques[:10]
    svg = "<svg fill='none' viewBox='0 0 800 340' width='100%' xmlns='http://www.w3.org/2000/svg'>"
    svg += "<style>.bg { fill: #0d0e15; rx: 8px; } .border { stroke: #ff0000; stroke-width: 1.5; stroke-opacity: 0.8; rx: 8px; } .title { font: bold 16px 'Fira Code', monospace; fill: #ff3333; } .header { font: bold 13px 'Fira Code', monospace; fill: #666; } .log-text { font: 13px 'Fira Code', monospace; fill: #00ff66; } .sync-text { font: italic 11px 'Fira Code', monospace; fill: #aaa; }</style>"
    svg += "<rect class='bg' width='100%' height='100%'/><rect class='border' width='99.8%' height='99.5%'/>"
    svg += "<circle cx='25' cy='30' r='5' fill='#ff0000'><animate attributeName='opacity' values='0.2;1;0.2' dur='1s' repeatCount='indefinite'/></circle><text class='title' x='40' y='35'>LIVE NETWORK INTRUSION MONITOR (DDoS DETECTED)</text><text class='sync-text' x='560' y='34'>HIGH-VELOCITY MITIGATION ACTIVE</text>"
    svg += "<text class='header' x='25' y='75'>ATTACK VECTOR</text><text class='header' x='220' y='75'>ATTACKER IP</text><text class='header' x='380' y='75'>PORT</text><text class='header' x='460' y='75'>LOCATION</text><text class='header' x='640' y='75'>ACTION TAKEN</text><line x1='20' y1='85' x2='780' y2='85' stroke='#ff0000' stroke-opacity='0.3' stroke-width='1'/>"
    svg += "<svg x='0' y='95' width='800' height='230'><g>"
    total_h = 80 * 25
    svg += f"<animateTransform attributeName='transform' type='translate' from='0,0' to='0,-{total_h}' dur='25s' repeatCount='indefinite' />"
    y_pos = 20
    for atk in loop:
        svg += f"<text class='log-text' x='25' y='{y_pos}' fill='#ff3333'>[THREAD_UDP]</text><text class='log-text' x='220' y='{y_pos}' fill='#ffffff'>{atk['ip']}</text><text class='log-text' x='380' y='{y_pos}' fill='#ffcc00'>{atk['port']}</text><text class='log-text' x='460' y='{y_pos}' fill='#00bfff'>{atk['loc']}</text><text class='log-text' x='640' y='{y_pos}' fill='#ff0000'>{atk['act']}</text>"
        y_pos += 25
    svg += "</g></svg></svg>"
    with open(SVG_PATH, "w", encoding="utf-8") as f: f.write(svg)
    print("[SUCESSO] Monitor animado com SMIL gerado!")
if __name__ == "__main__": gerar_svg()
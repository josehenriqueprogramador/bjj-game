from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import random

app = FastAPI()

# Banco de dados em memória
game_state = {
    "p1": {"nome": "Henrique", "pontos": 0, "vantagens": 0, "stamina": 100, "posicao": "Em pé"},
    "p2": {"nome": "Oponente", "pontos": 0, "vantagens": 0, "stamina": 100, "posicao": "Em pé"},
    "logs": ["O árbitro central autoriza a luta! Combate iniciado."],
    "turno": 1
}

def processar_logica(move: str):
    p1 = game_state["p1"]
    sucesso = random.randint(1, 6)
    
    if move == "queda":
        if sucesso > 3:
            p1["pontos"] += 2
            p1["posicao"] = "Por cima (Meia-guarda)"
            game_state["logs"].append(f"Round {game_state['turno']}: {p1['nome']} aplicou uma queda! +2 pts.")
        else:
            p1["vantagens"] += 1
            game_state["logs"].append(f"Round {game_state['turno']}: Tentativa de queda. +1 vantagem.")
            
    elif move == "passar":
        if sucesso > 4:
            p1["pontos"] += 3
            p1["posicao"] = "Cem Quilos (Estabilizado)"
            game_state["logs"].append(f"Round {game_state['turno']}: Passagem de guarda! +3 pts.")
        else:
            game_state["logs"].append(f"Round {game_state['turno']}: Oponente travou a passagem.")
            
    elif move == "costas":
        if sucesso == 6:
            p1["pontos"] += 4
            p1["posicao"] = "Costas (Ganchos colocados)"
            game_state["logs"].append(f"Round {game_state['turno']}: PEGOU AS COSTAS! +4 pts.")
        else:
            game_state["logs"].append(f"Round {game_state['turno']}: Quase pegou as costas, mas oponente escapou.")

    p1["stamina"] -= 5
    game_state["turno"] += 1

@app.get("/", response_class=HTMLResponse)
async def home():
    log_html = "".join([f"<p style='margin:5px; border-bottom: 1px solid #222;'> {log}</p>" for log in game_state["logs"][-5:]])
    
    html_content = f"""
    <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>BJJ Retro Manager</title>
            <style>
                body {{ background: #000; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; padding: 10px; }}
                .container {{ border: 2px solid #00ff00; display: inline-block; padding: 15px; width: 90%; max-width: 400px; }}
                .stats {{ display: flex; justify-content: space-around; font-size: 0.9em; }}
                .btn {{ background: #00ff00; color: #000; padding: 12px; border: none; cursor: pointer; font-weight: bold; margin: 5px; width: 80%; border-radius: 5px; }}
                .log-box {{ background: #111; border: 1px solid #333; height: 160px; overflow: hidden; text-align: left; padding: 10px; font-size: 0.85em; margin: 10px 0; }}
                .pos {{ color: #fff; font-weight: bold; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2 style="margin-top:0;">BJJ SIMULATOR</h2>
                <div class="stats">
                    <div>
                        <strong>{game_state['p1']['nome']}</strong><br>
                        PTS: {game_state['p1']['pontos']} | V: {game_state['p1']['vantagens']}<br>
                        STM: {game_state['p1']['stamina']}%
                    </div>
                    <div style="color: #888;">
                        <strong>Oponente</strong><br>
                        PTS: {game_state['p2']['pontos']} | V: {game_state['p2']['vantagens']}<br>
                        STM: {game_state['p2']['stamina']}%
                    </div>
                </div>
                <div class="log-box">
                    {log_html}
                </div>
                <div class="pos">📍 {game_state['p1']['posicao']}</div>
                <hr style="border: 0; border-top: 1px solid #333;">
                <button class="btn" onclick="location.href='/action/queda'">TENTAR QUEDA (2 PTS)</button>
                <button class="btn" onclick="location.href='/action/passar'">PASSAR GUARDA (3 PTS)</button>
                <button class="btn" onclick="location.href='/action/costas'">PEGAR COSTAS (4 PTS)</button>
                <button class="btn" onclick="location.href='/reset'" style="background:#500; color:#fff; margin-top:15px; width: 40%;">RESET</button>
            </div>
        </body>
    </html>
    """
    return html_content

@app.get("/action/queda")
async def route_queda():
    processar_logica("queda")
    return HTMLResponse("<script>window.location.href='/'</script>")

@app.get("/action/passar")
async def route_passar():
    processar_logica("passar")
    return HTMLResponse("<script>window.location.href='/'</script>")

@app.get("/action/costas")
async def route_costas():
    processar_logica("costas")
    return HTMLResponse("<script>window.location.href='/'</script>")

@app.get("/reset")
async def reset():
    game_state["p1"] = {"nome": "Henrique", "pontos": 0, "vantagens": 0, "stamina": 100, "posicao": "Em pé"}
    game_state["logs"] = ["Luta resetada. Combate iniciado!"]
    game_state["turno"] = 1
    return HTMLResponse("<script>window.location.href='/'</script>")

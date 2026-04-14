from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import random

app = FastAPI()

# Banco de dados simples em memória
game_state = {
    "p1": {"nome": "Henrique", "pontos": 0, "vantagens": 0, "stamina": 100, "posicao": "Em pé"},
    "p2": {"nome": "Oponente", "pontos": 0, "vantagens": 0, "stamina": 100, "posicao": "Em pé"},
    "logs": ["O árbitro central autoriza a luta! Combate iniciado."],
    "turno": 1
}

@app.get("/", response_class=HTMLResponse)
async def home():
    log_html = "".join([f"<p style='margin:5px; font-family: monospace;'> {log}</p>" for log in game_state["logs"][-5:]])
    
    html_content = f"""
    <html>
        <head>
            <title>BJJ Retro Manager</title>
            <style>
                body {{ background: #000; color: #00ff00; font-family: 'Courier New', Courier, monospace; text-align: center; }}
                .container {{ border: 2px solid #00ff00; display: inline-block; padding: 20px; margin-top: 50px; }}
                .stats {{ display: flex; justify-content: space-around; margin-bottom: 20px; }}
                .btn {{ background: #00ff00; color: #000; padding: 10px; border: none; cursor: pointer; font-weight: bold; margin: 5px; }}
                .log-box {{ background: #111; border: 1px solid #333; height: 150px; overflow: hidden; text-align: left; padding: 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>BJJ RETRO SIMULATOR</h1>
                <div class="stats">
                    <div>
                        <h3>{game_state['p1']['nome']}</h3>
                        <p>PONTOS: {game_state['p1']['pontos']} | V: {game_state['p1']['vantagens']}</p>
                        <p>STAMINA: {game_state['p1']['stamina']}%</p>
                    </div>
                    <div>
                        <h3>{game_state['p2']['nome']}</h3>
                        <p>PONTOS: {game_state['p2']['pontos']} | V: {game_state['p2']['vantagens']}</p>
                        <p>STAMINA: {game_state['p2']['stamina']}%</p>
                    </div>
                </div>
                <div class="log-box">
                    {log_html}
                </div>
                <hr>
                <p>Posição Atual: <strong>{game_state['p1']['posicao']}</strong></p>
                <div id="controls">
                    <button class="btn" onclick="location.href='/action/queda'">Tentar Queda (2 pts)</button>
                    <button class="btn" onclick="location.href='/action/passar'">Passar Guarda (3 pts)</button>
                    <button class="btn" onclick="location.href='/action/costas'">Pegar Costas (4 pts)</button>
                    <button class="btn" onclick="location.href='/reset'" style="background:red; color:white;">Reset</button>
                </div>
            </div>
        </body>
    </html>
    """
    return html_content

@app.get("/action/{{move}}")
async def action(move: str):
    p1 = game_state["p1"]
    p2 = game_state["p2"]
    sucesso = random.randint(1, 6)
    
    if move == "queda":
        if sucesso > 3:
            p1["pontos"] += 2
            p1["posicao"] = "Por cima (Meia-guarda)"
            game_state["logs"].append(f"Round {game_state['turno']}: {p1['nome']} aplicou uma queda linda! +2 pontos.")
        else:
            p1["vantagens"] += 1
            game_state["logs"].append(f"Round {game_state['turno']}: Quase derrubou! Ganhou uma vantagem.")
            
    elif move == "passar":
        if sucesso > 4:
            p1["pontos"] += 3
            p1["posicao"] = "Cem Quilos (Estabilizado)"
            game_state["logs"].append(f"Round {game_state['turno']}: Passagem de guarda técnica! +3 pontos.")
        else:
            game_state["logs"].append(f"Round {game_state['turno']}: Oponente repôs a guarda.")
            
    elif move == "costas":
        if sucesso == 6:
            p1["pontos"] += 4
            p1["posicao"] = "Costas (Ganchos colocados)"
            game_state["logs"].append(f"Round {game_state['turno']}: PEGOU AS COSTAS! Domínio máximo. +4 pontos.")
        else:
            game_state["logs"].append(f"Round {game_state['turno']}: Tentou as costas mas escorregou.")

    p1["stamina"] -= 5
    game_state["turno"] += 1
    return HTMLResponse("<script>window.location.href='/'</script>")

@app.get("/reset")
async def reset():
    game_state["p1"] = {"nome": "Henrique", "pontos": 0, "vantagens": 0, "stamina": 100, "posicao": "Em pé"}
    game_state["p2"] = {"nome": "Oponente", "pontos": 0, "vantagens": 0, "stamina": 100, "posicao": "Em pé"}
    game_state["logs"] = ["Luta resetada. Combate iniciado!"]
    game_state["turno"] = 1
    return HTMLResponse("<script>window.location.href='/'</script>")

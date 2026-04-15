from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import random

app = FastAPI()

# Estado Global do Jogo
game_state = {
    "p1": {"nome": None, "pontos": 0, "vantagens": 0, "stamina": 100, "posicao": "Em pé"},
    "p2": {"nome": "IA Oponente", "pontos": 0, "vantagens": 0, "stamina": 100},
    "logs": ["Aguardando lutadores..."],
    "turno": 1,
    "vitoria": False,
    "vencedor": None,
    "cor_posicao": "#00ff00"
}

def processar_combate(acao):
    if game_state["vitoria"] or not game_state["p1"]["nome"]: return
    p1, ia = game_state["p1"], game_state["p2"]
    dado, dado_ia = random.randint(1, 6), random.randint(1, 6)
    msg = ""
    
    # Sistema de Cansaço
    mod = 0 if p1["stamina"] > 25 else -2

    if acao == "queda":
        if dado + mod >= 4:
            p1["pontos"] += 2
            p1["posicao"] = "Por cima (Meia-Guarda)"
            game_state["cor_posicao"] = "#0088ff"
            msg = f"{p1['nome']} aplicou uma queda linda!"
        else:
            ia["pontos"] += 2
            p1["posicao"] = "Por baixo (Guarda)"
            game_state["cor_posicao"] = "#ff4444"
            msg = "A IA antecipou e te derrubou no contra-golpe!"

    elif acao == "passar":
        if p1["posicao"] == "Em pé":
            msg = "Você não pode passar guarda estando em pé!"
        elif dado + mod >= 5:
            p1["pontos"] += 3
            p1["posicao"] = "Cem Quilos"
            game_state["cor_posicao"] = "#ffcc00"
            msg = f"{p1['nome']} passou a guarda com pressão!"
        else:
            ia["vantagens"] += 1
            msg = "IA travou a passagem e ganhou vantagem."

    elif acao == "finalizar":
        if dado >= 5:
            game_state["vitoria"], game_state["vencedor"] = True, p1["nome"]
            msg = f"PEGOOU! {p1['nome']} finalizou a luta!"
        elif dado_ia == 6:
            game_state["vitoria"], game_state["vencedor"] = True, "IA Oponente"
            msg = "Bobeou! A IA te pegou em um triângulo!"

    p1["stamina"] = max(0, p1["stamina"] - 12)
    game_state["logs"].append(f"R{game_state['turno']}: {msg}")
    game_state["turno"] += 1

@app.get("/", response_class=HTMLResponse)
async def home():
    # Se não tem nome, mostra tela de entrada
    if not game_state["p1"]["nome"]:
        return """
        <html>
            <head><meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { background: #111; color: #0f0; font-family: monospace; text-align: center; padding: 50px 20px; }
                input { background: #000; border: 1px solid #0f0; color: #0f0; padding: 10px; width: 80%; margin: 20px 0; }
                button { background: #0f0; border: none; padding: 15px 30px; font-weight: bold; cursor: pointer; }
            </style></head>
            <body>
                <h1>BJJ MANAGER</h1>
                <p>DIGITE SEU NOME PARA ENTRAR NO TATAME:</p>
                <form action="/start" method="post">
                    <input type="text" name="nome" placeholder="NOME DO LUTADOR" required>
                    <br><button type="submit">ENTRAR NA LUTA</button>
                </form>
            </body>
        </html>
        """

    log_html = "".join([f"<p style='margin:3px; border-bottom: 1px solid #222;'>• {log}</p>" for log in game_state["logs"][-4:]])
    st_width = game_state["p1"]["stamina"]
    
    return f"""
    <html>
        <head><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ background: #111; color: #eee; font-family: monospace; text-align: center; padding: 10px; }}
            .card {{ border: 3px solid {game_state['cor_posicao']}; display: inline-block; padding: 15px; width: 95%; max-width: 400px; background: #000; }}
            .scoreboard {{ display: flex; justify-content: space-around; background: #222; padding: 10px; margin-bottom: 10px; }}
            .st-bar {{ background: #333; height: 10px; width: 100%; margin: 10px 0; }}
            .st-fill {{ background: #0f0; height: 100%; width: {st_width}%; transition: 0.5s; }}
            .btn {{ background: #222; color: {game_state['cor_posicao']}; border: 1px solid {game_state['cor_posicao']}; padding: 12px; margin: 5px 0; width: 100%; display: block; text-decoration: none; }}
            .log-box {{ background: #050505; color: #888; height: 110px; text-align: left; padding: 10px; font-size: 0.75em; border-left: 2px solid {game_state['cor_posicao']}; }}
        </style></head>
        <body>
            <div class="card">
                <div class="scoreboard">
                    <div><strong>{game_state['p1']['nome']}</strong><br><span style="font-size:1.5em">{game_state['p1']['pontos']}</span></div>
                    <div style="color:#666">VS</div>
                    <div><strong>IA</strong><br><span style="font-size:1.5em">{game_state['p2']['pontos']}</span></div>
                </div>
                <div class="st-bar"><div class="st-fill"></div></div>
                <div class="log-box">{log_html}</div>
                <p>📍 {game_state['p1']['posicao']}</p>
                
                {"<h2>VENCEDOR: " + game_state['vencedor'] + "</h2><a href='/reset' class='btn'>NOVA LUTA</a>" if game_state['vitoria'] else '''
                <a href="/queda" class="btn">TENTAR QUEDA (+2)</a>
                <a href="/passar" class="btn">PASSAR GUARDA (+3)</a>
                <a href="/finalizar" class="btn" style="color:#f0f; border-color:#f0f;">FINALIZAR</a>
                <a href="/reset" style="color:#444; text-decoration:none; font-size:0.7em; display:block; margin-top:10px;">SAIR/RESET</a>
                '''}
            </div>
        </body>
    </html>
    """

@app.post("/start")
async def start_game(nome: str = Form(...)):
    game_state["p1"]["nome"] = nome
    game_state["logs"] = [f"Lutador {nome} entrou no tatame!"]
    return RedirectResponse(url="/", status_code=303)

@app.get("/{action}")
async def r_action(action: str):
    if action in ["queda", "passar", "finalizar"]:
        processar_combate(action)
    elif action == "reset":
        game_state["p1"] = {"nome": None, "pontos": 0, "vantagens": 0, "stamina": 100, "posicao": "Em pé"}
        game_state["p2"] = {"nome": "IA Oponente", "pontos": 0, "vantagens": 0, "stamina": 100}
        game_state["vitoria"] = False
        game_state["turno"] = 1
    return RedirectResponse(url="/", status_code=303)

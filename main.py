from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import random

app = FastAPI()

# Estado inicial do jogo
def get_initial_state():
    return {
        "p1": {"nome": "Henrique", "pontos": 0, "vantagens": 0, "stamina": 100, "posicao": "Em pé", "classe": "Franzino Tático"},
        "p2": {"nome": "IA Oponente", "pontos": 0, "vantagens": 0, "stamina": 100, "posicao": "Em pé"},
        "logs": ["Tatame pronto. Árbitro: 'COMBATE!'"],
        "turno": 1,
        "cor_posicao": "#00ff00"
    }

game_state = get_initial_state()

def processar_combate(acao_jogador):
    p1 = game_state["p1"]
    
    reacoes_ia = ["Travar", "Antecipar", "Explodir"]
    defesa_ia = random.choice(reacoes_ia)
    
    # Modificador de fadiga
    modificador = 1 if p1["stamina"] > 30 else -1
    dado = random.randint(1, 6) + modificador
    
    msg = ""
    custo_stamina = 0

    if acao_jogador == "queda":
        custo_stamina = 15
        if dado >= 4:
            p1["pontos"] += 2
            p1["posicao"] = "Por cima (Meia-Guarda)"
            game_state["cor_posicao"] = "#0088ff"
            msg = "QUEDA! Você fintou a IA e derrubou."
        else:
            p1["vantagens"] += 1
            msg = "Tentativa de queda frustrada, mas ganhou vantagem."

    elif acao_jogador == "passar":
        custo_stamina = 20
        if p1["posicao"] == "Em pé":
            msg = "Impossível passar: você ainda está em pé!"
            custo_stamina = 0
        elif dado >= 5:
            p1["pontos"] += 3
            p1["posicao"] = "Cem Quilos (Dominado)"
            game_state["cor_posicao"] = "#ffcc00"
            msg = "PASSAGEM! Você estabilizou o controle lateral."
        else:
            msg = "A IA travou sua passagem com uma reposição."

    elif acao_jogador == "costas":
        custo_stamina = 25
        if p1["posicao"] == "Em pé":
            msg = "Tente derrubar primeiro!"
            custo_stamina = 0
        elif dado >= 5:
            p1["pontos"] += 4
            p1["posicao"] = "COSTAS (Mochilado)"
            game_state["cor_posicao"] = "#ff0000"
            msg = "PEGOU AS COSTAS! Domínio absoluto."
        else:
            msg = "Você tentou os ganchos, mas a IA se encolheu."

    p1["stamina"] = max(0, p1["stamina"] - custo_stamina)
    game_state["logs"].append(f"R{game_state['turno']}: {msg}")
    game_state["turno"] += 1

@app.get("/", response_class=HTMLResponse)
async def home():
    log_html = "".join([f"<p style='margin:3px; border-bottom: 1px solid #222;'>• {log}</p>" for log in game_state["logs"][-4:]])
    st_width = game_state["p1"]["stamina"]
    
    return f"""
    <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ background: #111; color: #eee; font-family: sans-serif; text-align: center; }}
                .card {{ border: 2px solid {game_state['cor_posicao']}; display: inline-block; padding: 20px; width: 90%; max-width: 400px; border-radius: 15px; background: #000; margin-top: 20px; }}
                .st-bar {{ background: #333; height: 10px; width: 100%; border-radius: 5px; margin: 10px 0; }}
                .st-fill {{ background: #00ff00; height: 100%; width: {st_width}%; border-radius: 5px; transition: 0.5s; }}
                .btn {{ background: {game_state['cor_posicao']}; color: #000; padding: 15px; border: none; cursor: pointer; font-weight: bold; margin: 5px 0; width: 100%; border-radius: 8px; text-decoration: none; display: block; }}
                .log-box {{ background: #050505; color: #aaa; height: 120px; text-align: left; padding: 10px; font-size: 0.8em; margin: 15px 0; border-left: 3px solid {game_state['cor_posicao']}; }}
                .pos-label {{ font-size: 1.2em; color: {game_state['cor_posicao']}; font-weight: bold; margin-bottom: 15px; }}
            </style>
        </head>
        <body>
            <div class="card">
                <div style="font-size: 0.7em; color: #888; text-transform: uppercase;">{game_state['p1']['classe']}</div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h2 style="margin: 0;">{game_state['p1']['nome']}</h2>
                    <div style="font-size: 1.5em;">{game_state['p1']['pontos']} <small style="font-size: 0.5em;">PTS</small></div>
                </div>
                <div class="st-bar"><div class="st-fill"></div></div>
                <div class="log-box">{log_html}</div>
                <div class="pos-label">📍 {game_state['p1']['posicao']}</div>
                
                <a href="/action/queda" class="btn">Tentar Queda</a>
                <a href="/action/passar" class="btn">Passar Guarda</a>
                <a href="/action/costas" class="btn">Pegar Costas</a>
                
                <a href="/reset" style="color: #444; text-decoration: none; font-size: 0.8em; display: block; margin-top: 20px;">REINICIAR LUTA</a>
            </div>
        </body>
    </html>
    """

@app.get("/action/queda")
async def action_queda():
    processar_combate("queda")
    return HTMLResponse("<script>window.location.href='/'</script>")

@app.get("/action/passar")
async def action_passar():
    processar_combate("passar")
    return HTMLResponse("<script>window.location.href='/'</script>")

@app.get("/action/costas")
async def action_costas():
    processar_combate("costas")
    return HTMLResponse("<script>window.location.href='/'</script>")

@app.get("/reset")
async def reset():
    global game_state
    game_state = get_initial_state()
    return HTMLResponse("<script>window.location.href='/'</script>")

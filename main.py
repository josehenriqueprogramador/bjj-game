from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import random

app = FastAPI()

def get_initial_state():
    return {
        "p1": {"nome": "Henrique", "pontos": 0, "vantagens": 0, "stamina": 100, "posicao": "Em pé"},
        "p2": {"nome": "IA Oponente", "pontos": 0, "vantagens": 0, "stamina": 100},
        "logs": ["O árbitro autoriza! 'COMBATE!'"],
        "turno": 1,
        "vitoria": False,
        "vencedor": None,
        "cor_posicao": "#00ff00"
    }

game_state = get_initial_state()

def processar_combate(acao):
    if game_state["vitoria"]: return
    p1 = game_state["p1"]
    ia = game_state["p2"]
    dado = random.randint(1, 6)
    dado_ia = random.randint(1, 6)
    msg = ""
    
    modificador = 0 if p1["stamina"] > 25 else -2

    # LÓGICA DE ATAQUE DO HENRIQUE
    if acao == "queda":
        if dado + modificador >= 4:
            p1["pontos"] += 2
            p1["posicao"] = "Por cima (Meia-Guarda)"
            game_state["cor_posicao"] = "#0088ff"
            msg = "QUEDA! Você derrubou a IA."
        else:
            ia["pontos"] += 2
            p1["posicao"] = "Por baixo (Guarda)"
            game_state["cor_posicao"] = "#ff4444"
            msg = "CONTRA-GOLPE! A IA te deu um balão e caiu por cima."
            
    elif acao == "passar":
        if p1["posicao"] == "Em pé":
            msg = "Derrube primeiro para passar!"
        elif dado + modificador >= 5:
            p1["pontos"] += 3
            p1["posicao"] = "Cem Quilos"
            game_state["cor_posicao"] = "#ffcc00"
            msg = "PASSAGEM! Você estabilizou o controle."
        else:
            ia["vantagens"] += 1
            msg = "A IA travou o quadril e ganhou uma vantagem na defesa."

    elif acao == "costas":
        if dado + modificador >= 5:
            p1["pontos"] += 4
            p1["posicao"] = "COSTAS"
            game_state["cor_posicao"] = "#ff4400"
            msg = "PEGOU AS COSTAS! Domínio total."
        else:
            msg = "A IA escapou do gancho."

    elif acao == "finalizar":
        if dado >= 5:
            game_state["vitoria"] = True
            game_state["vencedor"] = p1["nome"]
            msg = "ESTALOU! Você finalizou a IA!"
        elif dado_ia == 6: # IA contra-ataca com finalização!
            game_state["vitoria"] = True
            game_state["vencedor"] = "IA Oponente"
            msg = "PERIGO! A IA pegou seu braço no contra-ataque!"

    p1["stamina"] = max(0, p1["stamina"] - 10)
    game_state["logs"].append(f"R{game_state['turno']}: {msg}")
    game_state["turno"] += 1

@app.get("/", response_class=HTMLResponse)
async def home():
    log_html = "".join([f"<p style='margin:3px; border-bottom: 1px solid #222;'>• {log}</p>" for log in game_state["logs"][-4:]])
    
    return f"""
    <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ background: #111; color: #eee; font-family: monospace; text-align: center; padding: 10px; }}
                .card {{ border: 3px solid {game_state['cor_posicao']}; display: inline-block; padding: 15px; width: 95%; max-width: 400px; background: #000; }}
                .scoreboard {{ display: flex; justify-content: space-around; background: #222; padding: 10px; margin-bottom: 10px; border-radius: 5px; }}
                .btn {{ background: #222; color: {game_state['cor_posicao']}; border: 1px solid {game_state['cor_posicao']}; padding: 12px; margin: 5px 0; width: 100%; display: block; text-decoration: none; }}
                .log-box {{ background: #050505; color: #888; height: 110px; text-align: left; padding: 10px; font-size: 0.75em; border-left: 2px solid {game_state['cor_posicao']}; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h3>BJJ MANAGER MVP</h3>
                <div class="scoreboard">
                    <div><strong>{game_state['p1']['nome']}</strong><br><span style="font-size:1.5em">{game_state['p1']['pontos']}</span></div>
                    <div style="color:#666">VS</div>
                    <div><strong>IA</strong><br><span style="font-size:1.5em">{game_state['p2']['pontos']}</span></div>
                </div>
                
                <div class="log-box">{log_html}</div>
                
                {"<h2>VENCEDOR: " + game_state['vencedor'] + "</h2><a href='/reset' class='btn'>NOVA LUTA</a>" if game_state['vitoria'] else '''
                <a href="/queda" class="btn">TENTAR QUEDA</a>
                <a href="/passar" class="btn">PASSAR GUARDA</a>
                <a href="/costas" class="btn">PEGAR COSTAS</a>
                <a href="/finalizar" class="btn" style="color:#f0f; border-color:#f0f;">FINALIZAR</a>
                '''}
            </div>
        </body>
    </html>
    """

# (Mantenha as rotas @app.get("/queda"), /passar, etc., como no código anterior)
@app.get("/queda")
async def r_queda():
    processar_combate("queda")
    return HTMLResponse("<script>window.location.href='/'</script>")

@app.get("/passar")
async def r_passar():
    processar_combate("passar")
    return HTMLResponse("<script>window.location.href='/'</script>")

@app.get("/costas")
async def r_costas():
    processar_combate("costas")
    return HTMLResponse("<script>window.location.href='/'</script>")

@app.get("/finalizar")
async def r_finalizar():
    processar_combate("finalizar")
    return HTMLResponse("<script>window.location.href='/'</script>")

@app.get("/reset")
async def r_reset():
    global game_state
    game_state = get_initial_state()
    return HTMLResponse("<script>window.location.href='/'</script>")


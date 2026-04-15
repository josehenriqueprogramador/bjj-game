from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import random

app = FastAPI()

# Função para resetar o estado inicial
def get_initial_state():
    return {
        "p1": {"nome": "Henrique", "pontos": 0, "vantagens": 0, "stamina": 100, "posicao": "Em pé", "status": "Vivo"},
        "p2": {"nome": "IA Oponente", "pontos": 0, "stamina": 100},
        "logs": ["O árbitro central autoriza a luta! 'COMBATE!'"],
        "turno": 1,
        "vitoria": False,
        "cor_posicao": "#00ff00"
    }

game_state = get_initial_state()

def processar_combate(acao):
    if game_state["vitoria"]: return
    
    p1 = game_state["p1"]
    dado = random.randint(1, 6)
    msg = ""
    custo_stamina = 10
    
    # Bônus de Stamina: Cansado luta pior
    modificador = 0 if p1["stamina"] > 25 else -2

    if acao == "queda":
        if dado + modificador >= 4:
            p1["pontos"] += 2
            p1["posicao"] = "Por cima (Meia-Guarda)"
            game_state["cor_posicao"] = "#0088ff"
            msg = "QUEDA! Você fintou a IA e derrubou com autoridade."
        else:
            p1["vantagens"] += 1
            msg = "A IA fez o sprawl. Você ganhou apenas uma vantagem."
            
    elif acao == "passar":
        if p1["posicao"] == "Em pé":
            msg = "Erro: Você precisa derrubar antes de tentar passar."
            custo_stamina = 0
        elif dado + modificador >= 5:
            p1["pontos"] += 3
            p1["posicao"] = "Cem Quilos (Estabilizado)"
            game_state["cor_posicao"] = "#ffcc00"
            msg = "PASSAGEM! Pressão total e guarda superada."
        else:
            msg = "A IA travou o quadril e repôs a guarda."

    elif acao == "costas":
        if p1["posicao"] == "Em pé":
            msg = "Não dá para ir para as costas direto de pé!"
            custo_stamina = 0
        elif dado + modificador >= 5:
            p1["pontos"] += 4
            p1["posicao"] = "COSTAS (Mochilado)"
            game_state["cor_posicao"] = "#ff4400"
            msg = "PEGOU AS COSTAS! Ganchos no lugar e domínio total."
        else:
            msg = "A IA se encolheu e você perdeu o tempo do gancho."

    elif acao == "finalizar":
        custo_stamina = 30
        if p1["posicao"] == "Em pé":
            msg = "Tentou um bote voador desesperado e caiu de costas!"
            p1["posicao"] = "Por baixo (Guarda)"
            game_state["cor_posicao"] = "#555"
        elif dado >= 5: # Chance de 33% (5 ou 6)
            game_state["vitoria"] = True
            p1["status"] = "VENCEDOR"
            p1["posicao"] = "FINALIZAÇÃO (Tap-out!)"
            game_state["cor_posicao"] = "#ffffff"
            msg = "ESTALOU! Finalização perfeita. A IA deu o tapinha!"
        else:
            p1["posicao"] = "Em pé (Perdeu o ajuste)"
            game_state["cor_posicao"] = "#00ff00"
            msg = "Perdeu o braço! A IA escapou e a luta voltou de pé."

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
                body {{ background: #111; color: #eee; font-family: 'Courier New', monospace; text-align: center; margin: 0; padding: 10px; }}
                .card {{ border: 3px solid {game_state['cor_posicao']}; display: inline-block; padding: 15px; width: 95%; max-width: 400px; border-radius: 10px; background: #000; box-shadow: 0 0 15px {game_state['cor_posicao']}44; }}
                .st-bar {{ background: #333; height: 12px; width: 100%; border-radius: 6px; margin: 10px 0; overflow: hidden; }}
                .st-fill {{ background: #00ff00; height: 100%; width: {st_width}%; transition: 0.5s; }}
                .btn {{ background: #222; color: {game_state['cor_posicao']}; border: 1px solid {game_state['cor_posicao']}; padding: 12px; font-weight: bold; margin: 5px 0; width: 100%; display: block; text-decoration: none; border-radius: 5px; font-size: 0.9em; }}
                .btn:active {{ background: {game_state['cor_posicao']}; color: #000; }}
                .finish-btn {{ background: #505; color: #f0f; border-color: #f0f; margin-top: 10px; }}
                .log-box {{ background: #050505; color: #888; height: 110px; text-align: left; padding: 10px; font-size: 0.75em; margin: 10px 0; border-left: 2px solid {game_state['cor_posicao']}; overflow: hidden; }}
                .pos-label {{ font-size: 1.1em; color: {game_state['cor_posicao']}; font-weight: bold; padding: 10px; border: 1px dashed {game_state['cor_posicao']}; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h3 style="margin: 0; color: {game_state['cor_posicao']};">BJJ RETRO MANAGER</h3>
                <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                    <div style="text-align: left;"><strong>{game_state['p1']['nome']}</strong><br><small>PTS: {game_state['p1']['pontos']}</small></div>
                    <div style="text-align: right; color: #666;"><strong>IA OPONENTE</strong><br><small>PTS: 0</small></div>
                </div>
                <div class="st-bar"><div class="st-fill" style="background: {'#ff0000' if st_width < 30 else '#00ff00'}"></div></div>
                <div class="log-box">{log_html}</div>
                <div class="pos-label">📍 {game_state['p1']['posicao']}</div>
                
                {"<h2 style='color:#fff'>FIM DE LUTA</h2>" if game_state['vitoria'] else f'''
                <a href="/action/queda" class="btn">TENTAR QUEDA (+2)</a>
                <a href="/action/passar" class="btn">PASSAR GUARDA (+3)</a>
                <a href="/action/costas" class="btn">PEGAR COSTAS (+4)</a>
                <a href="/action/finalizar" class="btn finish-btn">FINALIZAR (RISCO ALTO)</a>
                '''}
                
                <a href="/reset" style="color: #444; text-decoration: none; font-size: 0.7em; display: block; margin-top: 20px;">REINICIAR TATAME</a>
            </div>
        </body>
    </html>
    """

@app.get("/action/{{move}}")
async def action(move: str):
    processar_combate(move)
    return HTMLResponse("<script>window.location.href='/'</script>")

@app.get("/reset")
async def reset():
    global game_state
    game_state = get_initial_state()
    return HTMLResponse("<script>window.location.href='/'</script>")

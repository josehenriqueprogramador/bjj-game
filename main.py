from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import random

app = FastAPI()

# Estado do Jogo com Atributos de RPG
game_state = {
    "p1": {"nome": "Henrique", "pontos": 0, "vantagens": 0, "stamina": 100, "posicao": "Em pé", "classe": "Franzino Tático"},
    "p2": {"nome": "IA Oponente", "pontos": 0, "vantagens": 0, "stamina": 100, "posicao": "Em pé"},
    "logs": ["Tatame pronto. Árbitro: 'COMBATE!'"],
    "turno": 1,
    "cor_posicao": "#00ff00" # Verde para Neutro/Vantagem
}

def processar_combate(acao_jogador):
    p1 = game_state["p1"]
    p2 = game_state["p2"]
    
    # IA decide uma reação (Simulando uma mente defensiva)
    reacoes_ia = ["Travar", "Antecipar", "Explodir"]
    defesa_ia = random.choice(reacoes_ia)
    
    # Sorteio base influenciado pela Stamina
    modificador = 1 if p1["stamina"] > 30 else -1
    dado = random.randint(1, 6) + modificador
    
    sucesso = False
    msg = ""

    if acao_jogador == "queda":
        coste_stamina = 15
        if defesa_ia == "Explodir" and dado < 4:
            msg = f"IA deu um sprawl violento! Você gastou energia à toa."
        elif dado >= 4:
            p1["pontos"] += 2
            p1["posicao"] = "Por cima (Meia-Guarda)"
            game_state["cor_posicao"] = "#0088ff" # Azul para Domínio
            sucesso = True
            msg = f"QUEDA! Você fintou a IA e derrubou."

    elif acao_jogador == "passar":
        coste_stamina = 20
        if p1["posicao"] == "Em pé":
            msg = "Você precisa derrubar antes de tentar passar!"
            coste_stamina = 0
        elif dado >= 5:
            p1["pontos"] += 3
            p1["posicao"] = "Cem Quilos (Estabilizado)"
            game_state["cor_posicao"] = "#ffcc00" # Amarelo para Pressão
            sucesso = True
            msg = "PASSAGEM! Você amassou e chegou no lado."
        else:
            p1["vantagens"] += 1
            msg = "A IA repôs a guarda, mas você ganhou uma vantagem."

    elif acao_jogador == "costas":
        coste_stamina = 25
        if dado == 6:
            p1["pontos"] += 4
            p1["posicao"] = "COSTAS (Mochilado)"
            game_state["cor_posicao"] = "#ff0000" # Vermelho para Perigo Total
            sucesso = True
            msg = "PEGOU AS COSTAS! Oponente em perigo real."
        else:
            msg = "A IA fechou o cotovelo e você não conseguiu o gancho."

    p1["stamina"] = max(0, p1["stamina"] - coste_stamina)
    game_state["logs"].append(f"T{game_state['turno']}: {msg}")
    game_state["turno"] += 1

@app.get("/", response_class=HTMLResponse)
async def home():
    log_html = "".join([f"<p style='margin:3px; border-bottom: 1px solid #222;'>• {log}</p>" for log in game_state["logs"][-4:]])
    
    # Determina a largura da barra de stamina
    stamina_width = game_state["p1"]["stamina"]
    
    return f"""
    <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ background: #111; color: #eee; font-family: sans-serif; text-align: center; }}
                .card {{ border: 2px solid {game_state['cor_posicao']}; display: inline-block; padding: 20px; width: 90%; max-width: 400px; border-radius: 15px; background: #000; }}
                .stamina-bar {{ background: #333; height: 10px; width: 100%; border-radius: 5px; margin: 10px 0; }}
                .stamina-fill {{ background: #00ff00; height: 100%; width: {stamina_width}%; border-radius: 5px; transition: 0.5s; }}
                .btn {{ background: {game_state['cor_posicao']}; color: #000; padding: 15px; border: none; cursor: pointer; font-weight: bold; margin: 5px; width: 100%; border-radius: 8px; text-transform: uppercase; }}
                .log-box {{ background: #050505; color: #aaa; height: 120px; text-align: left; padding: 10px; font-size: 0.8em; margin: 15px 0; border-left: 3px solid {game_state['cor_posicao']}; }}
                .pos-label {{ font-size: 1.2em; color: {game_state['cor_posicao']}; font-weight: bold; margin-bottom: 15px; }}
            </style>
        </head>
        <body>
            <div class="card">
                <div style="font-size: 0.8em; color: #888;">{game_state['p1']['classe']}</div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h2 style="margin: 0;">{game_state['p1']['nome']}</h2>
                    <div style="font-size: 1.5em;">{game_state['p1']['pontos']} <span style="font-size: 0.5em;">PTS</span></div>
                </div>
                
                <div class="stamina-bar"><div class="stamina-fill"></div></div>
                
                <div class="log-box">{log_html}</div>
                
                <div class="pos-label">📍 {game_state['p1']['posicao']}</div>
                
                <button class="btn" onclick="location.href='/action/queda'">Tentar Queda</button>
                <button class="btn" onclick="location.href='/action/passar'">Passar Guarda</button>
                <button class="btn" onclick="location.href='/action/costas'">Pegar Costas</button>
                
                <a href="/reset" style="color: #444; text-decoration: none; font-size: 0.7em; display: block; margin-top: 15px;">REINICIAR LUTA</a>
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
    game_state = {{
        "p1": {{"nome": "Henrique", "pontos": 0, "vantagens": 0, "stamina": 100, "posicao": "Em pé", "classe": "Franzino Tático"}},
        "p2": {{"nome": "IA Oponente", "pontos": 0, "vantagens": 0, "stamina": 100, "posicao": "Em pé"}},
        "logs": ["Luta reiniciada!"],
        "turno": 1,
        "cor_posicao": "#00ff00"
    }}
    return HTMLResponse("<script>window.location.href='/'</script>")

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import random

app = FastAPI()

def get_initial_state():
    return {
        "p1": {"nome": None, "pontos": 0, "vantagens": 0, "stamina": 100, "posicao": "Em pé"},
        "p2": {"nome": "IA Oponente", "pontos": 0, "vantagens": 0, "stamina": 100},
        "logs": ["Tatame limpo. Aguardando lutadores..."],
        "turno": 1,
        "vitoria": False,
        "vencedor": None,
        "cor_posicao": "#00ff00"
    }

game_state = get_initial_state()

def processar_combate(acao):
    if game_state["vitoria"] or not game_state["p1"]["nome"]: return
    p1, ia = game_state["p1"], game_state["p2"]
    dado = random.randint(1, 6)
    msg = ""
    
    # Sistema de Fadiga (Biotipo Franzino ganha bônus de agilidade se tiver stamina)
    mod = 1 if p1["stamina"] > 40 else -2

    # --- LÓGICA DE GOLPES EXPANDIDA ---
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
            msg = "Não dá para passar guarda em pé! Derrube primeiro."
        elif dado + mod >= 5:
            p1["pontos"] += 3
            p1["posicao"] = "Cem Quilos (Dominado)"
            game_state["cor_posicao"] = "#ffcc00"
            msg = "PASSAGEM! Você superou a guarda da IA."
        else:
            ia["vantagens"] += 1
            msg = "IA travou a passagem e ganhou vantagem na defesa."

    elif acao == "raspar":
        if "Por baixo" in p1["posicao"] or "Guarda" in p1["posicao"]:
            if dado + mod >= 4:
                p1["pontos"] += 2
                p1["posicao"] = "Por cima (Meia-Guarda)"
                game_state["cor_posicao"] = "#0088ff"
                msg = "RASPAGEM! Você inverteu a posição com técnica."
            else:
                msg = "Tentou raspar, mas a IA pesou o quadril."
        else:
            msg = "Você já está por cima! Tente passar ou pegar as costas."

    elif acao == "costas":
        if p1["posicao"] == "Em pé":
            msg = "Tente derrubar ou puxar para a guarda antes."
        elif dado + mod >= 5:
            p1["pontos"] += 4
            p1["posicao"] = "COSTAS (Mochilado)"
            game_state["cor_posicao"] = "#ff4400"
            msg = "PEGOU AS COSTAS! Domínio absoluto."
        else:
            msg = "IA se encolheu e evitou os ganchos."

    elif acao == "finalizar":
        # Finalização é mais fácil se estiver nas costas
        alvo = 5 if "COSTAS" in p1["posicao"] else 6
        if dado >= alvo:
            game_state["vitoria"], game_state["vencedor"] = True, p1["nome"]
            msg = f"ESTALOU! {p1['nome']} finalizou a luta!"
        else:
            p1["posicao"] = "Em pé (Perdeu o ajuste)"
            game_state["cor_posicao"] = "#00ff00"
            msg = "Você perdeu o braço! A luta volta de pé."

    p1["stamina"] = max(0, p1["stamina"] - 12)
    game_state["logs"].append(f"R{game_state['turno']}: {msg}")
    game_state["turno"] += 1

@app.get("/", response_class=HTMLResponse)
async def home():
    if not game_state["p1"]["nome"]:
        return """
        <html>
            <head><meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { background: #111; color: #0f0; font-family: monospace; text-align: center; padding: 50px 20px; }
                input { background: #000; border: 1px solid #0f0; color: #0f0; padding: 12px; width: 80%; margin: 20px 0; font-family: monospace; }
                button { background: #0f0; border: none; padding: 15px 30px; font-weight: bold; cursor: pointer; border-radius: 5px; }
            </style></head>
            <body>
                <h1>BJJ MANAGER MVP</h1>
                <p>NOME DO LUTADOR:</p>
                <form action="/start" method="post">
                    <input type="text" name="nome" placeholder="EX: HENRIQUE" required>
                    <br><button type="submit">ENTRAR NO TATAME</button>
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
            body {{ background: #111; color: #eee; font-family: monospace; text-align: center; padding: 10px; margin: 0; }}
            .card {{ border: 3px solid {game_state['cor_posicao']}; display: inline-block; padding: 15px; width: 95%; max-width: 400px; background: #000; box-shadow: 0 0 10px {game_state['cor_posicao']}55; }}
            .scoreboard {{ display: flex; justify-content: space-around; background: #222; padding: 10px; margin-bottom: 10px; border-radius: 5px; }}
            .st-bar {{ background: #333; height: 10px; width: 100%; margin: 10px 0; border-radius: 5px; overflow: hidden; }}
            .st-fill {{ background: #0f0; height: 100%; width: {st_width}%; transition: 0.5s; }}
            .btn {{ background: #222; color: {game_state['cor_posicao']}; border: 1px solid {game_state['cor_posicao']}; padding: 12px; margin: 5px 0; width: 100%; display: block; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 0.85em; }}
            .log-box {{ background: #050505; color: #888; height: 110px; text-align: left; padding: 10px; font-size: 0.75em; border-left: 2px solid {game_state['cor_posicao']}; margin-bottom: 10px; }}
        </style></head>
        <body>
            <div class="card">
                <div class="scoreboard">
                    <div><strong>{game_state['p1']['nome']}</strong><br><span style="font-size:1.5em">{game_state['p1']['pontos']}</span><br><small>V: {game_state['p1']['vantagens']}</small></div>
                    <div style="color:#666; align-self: center;">VS</div>
                    <div><strong>IA</strong><br><span style="font-size:1.5em">{game_state['p2']['pontos']}</span><br><small>V: {game_state['p2']['vantagens']}</small></div>
                </div>
                <div class="st-bar"><div class="st-fill"></div></div>
                <div class="log-box">{log_html}</div>
                <p style="color:{game_state['cor_posicao']}">📍 {game_state['p1']['posicao']}</p>
                
                {"<h2>VENCEDOR: " + game_state['vencedor'] + "</h2><a href='/reset' class='btn'>NOVA LUTA</a>" if game_state['vitoria'] else f'''
                <a href="/queda" class="btn">TENTAR QUEDA (+2)</a>
                <a href="/raspar" class="btn">RASPAR / INVERTER (+2)</a>
                <a href="/passar" class="btn">PASSAR GUARDA (+3)</a>
                <a href="/costas" class="btn">PEGAR COSTAS (+4)</a>
                <a href="/finalizar" class="btn" style="color:#f0f; border-color:#f0f; margin-top:10px;">FINALIZAR (SUBMISSION)</a>
                <a href="/reset" style="color:#444; text-decoration:none; font-size:0.75em; display:block; margin-top:15px;">SAIR DO TATAME</a>
                '''}
            </div>
        </body>
    </html>
    """

@app.post("/start")
async def start_game(nome: str = Form(...)):
    game_state.update(get_initial_state())
    game_state["p1"]["nome"] = nome.upper()
    game_state["logs"] = [f"Lutador {nome.upper()} entrou no tatame!"]
    return RedirectResponse(url="/", status_code=303)

@app.get("/{action}")
async def r_action(action: str):
    if action in ["queda", "passar", "finalizar", "raspar", "costas"]:
        processar_combate(action)
    elif action == "reset":
        game_state["p1"]["nome"] = None
    return RedirectResponse(url="/", status_code=303)

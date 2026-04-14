# 🥋 BJJ Retro Manager - MVP

Um simulador tático de Jiu-Jitsu brasileiro em estilo retro, desenvolvido com **Python** e **FastAPI**. O projeto transforma a estratégia do tatame em lógica de programação, simulando a gestão de posições, stamina e pontuações oficiais da IBJJF.



## 🚀 Sobre o Projeto

O **BJJ Retro Manager** não é apenas um sorteio de resultados. Ele é um motor de combate que exige que o jogador tome decisões baseadas na posição atual e no nível de energia do atleta. 

### Funcionalidades Principais:
- **Lógica de Posição:** O sistema reconhece onde a luta está (Em pé, Meia-Guarda, Cem Quilos, Costas) e só permite movimentos válidos para cada situação.
- **Gestão de Stamina:** Cada tentativa de ataque consome energia. Atacar com stamina baixa reduz drasticamente as chances de sucesso.
- **IA Defensiva:** O oponente reage de forma aleatória entre "Travar", "Explodir" ou "Antecipar", criando um desafio dinâmico.
- **Regras Oficiais:** Sistema de pontuação fiel à realidade (Quedas: 2, Passagens: 3, Costas: 4).

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.x
- **Framework Web:** FastAPI (Assíncrono)
- **Servidor ASGI:** Uvicorn
- **Interface:** HTML5/CSS3 com design responsivo focado em Mobile.
- **Deploy & Infra:** Git, GitHub e Render.

## 📁 Estrutura do Repositório

- `main.py`: Contém todo o motor de regras, as rotas da aplicação e a interface front-end.
- `requirements.txt`: Lista de dependências para o ambiente de produção.

## 🎮 Como Jogar

1. **Início:** A luta começa em pé.
2. **Estratégia:** Tente a queda para progredir. Uma vez no solo, você deve decidir entre tentar passar a guarda ou arriscar ir direto para as costas.
3. **Atenção:** Observe a barra de Stamina. Se ela chegar a zero, seus movimentos raramente terão sucesso.
4. **Feedback:** A interface muda de cor conforme o seu domínio na luta aumenta (Verde -> Azul -> Amarelo -> Vermelho).

## 👷 Como Rodar Localmente (Termux ou PC)

```bash
# Clone o repositório
git clone [https://github.com/josehenriqueprogramador/bjj-game.git](https://github.com/josehenriqueprogramador/bjj-game.git)

# Entre na pasta
cd bjj-game

# Instale as dependências
pip install -r requirements.txt

# Inicie o servidor
uvicorn main:app --reload

# 🥋 BJJ Manager MVP - Edição Customizada

Um simulador tático de Jiu-Jitsu Brasileiro (BJJ) desenvolvido com **Python** e **FastAPI**. Esta versão evoluiu de um simples simulador de texto para um jogo de estratégia interativo com gestão de nome, stamina e placar completo para ambos os lutadores.

## 🌟 O que há de novo?

- **Sistema de Identificação:** Tela de entrada para registro do nome do lutador, tornando a experiência personalizada.
- **Mecânicas Técnicas Expandidas:** Inclusão de **Raspagens/Inversões**, permitindo jogar estrategicamente por baixo (guarda).
- **Placar Real da IA:** Oponente reativo que agora pontua e aplica contra-ataques caso você falhe nos movimentos.
- **Contagem de Vantagens:** Sistema de desempate fiel às regras da IBJJF (V: 0).
- **Morte Súbita (Submission):** Opção de finalização com bônus de precisão se você estiver nas costas.

## 🛠️ Tecnologias e Conceitos Aplicados

- **Back-end:** FastAPI com rotas dinâmicas e manipulação de formulários (`python-multipart`).
- **Frontend:** HTML5/CSS3 responsivo com interface que altera o brilho e cores conforme o domínio da luta (Feedback Visual).
- **Lógica de Dados:** Gestão de estado global para persistência da stamina e pontuação durante o round.
- **Deploy:** Configurado para **Render** com integração contínua via GitHub.

## 🎮 Como Funciona a Luta

1. **Entrada:** Digite seu nome para subir no tatame.
2. **Estratégia de Posição:**
   - **Em Pé:** Foque em **Quedas** (+2 pts).
   - **Por Baixo:** Use **Raspagens** (+2 pts) para inverter e chegar por cima.
   - **Por Cima:** Tente **Passar a Guarda** (+3 pts) ou **Pegar as Costas** (+4 pts).
3. **Gestão de Energia:** Cada movimento consome Stamina. Se sua energia estiver abaixo de 40%, suas chances de sucesso diminuem drasticamente.
4. **Finalização:** Tentar encerrar a luta a qualquer momento. Se falhar, você perde a posição e a luta volta em pé.

## 🚀 Instalação e Uso

### Pré-requisitos
Certifique-se de ter o arquivo `requirements.txt` com as seguintes bibliotecas:
- `fastapi`
- `uvicorn`
- `python-multipart`

### Rodando Localmente (Termux ou PC)
```bash
# Clone o projeto
git clone [https://github.com/josehenriqueprogramador/bjj-game.git](https://github.com/josehenriqueprogramador/bjj-game.git)

# Instale as dependências
pip install -r requirements.txt

# Inicie o servidor
uvicorn main:app --host 0.0.0.0 --port 8000

# 🐍 Fuga nas Cobras

Um jogo feito em **Python + Pygame**, onde o jogador precisa sobreviver às cobras e derrotar chefões a cada 10 fases.

---

## 🎮 Como jogar

- **W A S D** → mover o jogador  
- **Objetivo**:
  - Sobreviver por **30 segundos** em cada fase
  - A cada 10 fases aparece um **BOSS**
  - Pegue as **anticobras** para causar dano no boss
- Cada boss tem **150 de vida**
- Cada anticobra causa **5 de dano**
- O boss se move para cima e para baixo e dispara mísseis retos

---

## 👾 Mecânicas do jogo

- Cobras seguem o jogador
- As cobras ficam mais rápidas conforme o tempo
- Fases normais e fases de boss
- Música diferente para:
  - Fases normais (`musica1.ogg`)
  - Fases de boss (`musica2.ogg`)
- Sistema de fases automáticas (30 segundos cada)

---

## 🖼️ Imagens usadas

- `inicio.png` – tela inicial
- `player.png` – jogador
- `cobra.png` – cobra normal
- `boss.png` – boss
- `missil.png` – míssil do boss
- `anticobra.png` – item de dano no boss

---

## 🔊 Sons e músicas

- `musica1.ogg` – música normal
- `musica2.ogg` – música do boss
- `som_anticobra.ogg` – som ao pegar anticobra

---

## 🛠️ Tecnologias

- Python 3.12
- Pygame 2.6
- PyInstaller (para gerar o `.exe`)

---

## 👨‍💻 Autor

Projeto desenvolvido por **Miguel**  

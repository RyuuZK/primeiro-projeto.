# primeiro-projeto.

# ⚡ Pokemon TD (Tower Defense)

Este é o meu **primeiro projeto de programação**! Trata-se de um jogo no estilo *Tower Defense* desenvolvido em Python com a biblioteca **Pyxel** (uma engine focada em jogos retro de 8 bits). O projeto mistura a temática de Pokémon com a mecânica clássica de defesa de caminhos de Bloons TD.

O projeto conta com mecânicas de economia, loja, ondas progressivas de inimigos, trilha sonora em tempo real sintetizada via código e até algoritmos de predição física para os tiros das torres!

---

## 🎮 Como Jogar

O objetivo é defender o caminho impedindo que os Pokémons inimigos alcancem o final da rota. Você perde vidas para cada inimigo que escapar.

### Controles:
* **Mouse (Clique Esquerdo):** Interage com a loja na parte inferior para selecionar torres (Blastoise, Venusaur ou Charizard) e posicioná-las no mapa.
* **Botão "Cancel":** Cancela a seleção atual da torre.
* **Tecla P:** Pausa e despausa o jogo (também pausa a música de fundo).

### Recursos Disponíveis:
* **Money (Dinheiro):** Usado para comprar novas torres. Cada eliminação concede $+ \$10$.
* **Lives (Vidas):** Você começa com 20 vidas. O jogo termina se chegar a 0.
* **Horde (Hordas):** Sobreviva a 10 hordas de Pokémons que ficam progressivamente mais fortes e rápidos.

---

## 🧠 Desafios Técnicos Superados (Destaques do Código)

Como meu primeiro contato com código, apliquei conceitos lógicos e matemáticos desafiadores:

* **Predição de Trajetória do Projétil:** Em vez de atirar onde o inimigo *está*, o código calcula uma estimativa baseada na velocidade do projétil e do alvo (`time_to_hit`), fazendo com que as torres atirem um pouco à frente (onde o inimigo *estará*).
* **Matriz de Rotação Trigonométrica:** Para torres com disparos múltiplos (como o Blastoise, que atira em três direções), utilizei cálculos de radianos com `pyxel.cos` e `pyxel.sin` para rotacionar os vetores de velocidade dos projéteis em ângulos de $10^{\circ}$ ou $15^{\circ}$.
* **Áudio Gerado por Código:** Toda a música de fundo e os efeitos sonoros de tiro e impacto foram sintetizados puramente via strings de notas musicais (`C3 E3 G3 C4...`) interpretadas nativamente pela engine de som do Pyxel.
* **Máquina de Estados e Spawns Dinâmicos:** Controle de tempo de recarga (*cooldown*) individual por torre e geração randômica ponderada de inimigos com base no número da horda atual.

---

## 🛠️ Como Executar o Projeto

Você precisará do **Python 3** e da biblioteca **Pyxel** instalados.

1. Instale a biblioteca do Pyxel:
   ```bash
   pip install pyxel
   
2. Certifique-se de ter os seguintes arquivos de imagem na mesma pasta do código:mapa.png (Cenário de fundo)blastoise.png, venusaur.png, charizard.png (Sprites das torres)rattata.png, raticate.png, articuno.png, mew.png (Sprites dos inimigos)

3. Rode o script principal:jogo.py

📁 Estrutura das Torres e InimigosUnidadeTipo / ComportamentoCustoDano / AtributoBlastoiseTorre Inicial (Disparo Triplo em Leque)$\$60$Dano: 2 | Alcance: 60VenusaurTorre Intermediária (Disparo Duplo)$\$90$Dano: 3 | Alcance: 85CharizardTorre Avançada (Disparo Único Pesado)$\$120$Dano: 4 | Alcance: 110InimigosRattata, Raticate, Articuno e Mew-HP e Velocidade escalam por tipo

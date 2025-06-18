import sys
import os
import pygame
import random
import pyttsx3
import speech_recognition as sr
sys.path.append(os.path.join(os.path.dirname(__file__), "Recursos"))
from Recursos.funcoes import salvar, carregar_historico
from Recursos.funcoes import mostrar_mensagem_central
from Recursos.dica import mostrar_dica

pygame.init()

largura, altura = 1000, 700
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Brainrot Dodge")

VERDE_ESCURO = (0, 102, 0)
MARROM = (139, 69, 19)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AMARELO = (255, 223, 0)
LARANJA = (255, 165, 0)

fonte = pygame.font.Font('Recursos/letra.TTF', 28)
fonte_grande = pygame.font.Font('Recursos/letra.ttf', 48)

nome = ""
relogio = pygame.time.Clock()
pontuacao = 0
velocidade = 5

sprite_jogador = pygame.image.load("Recursos/personagem.png").convert_alpha()
sprite_jogador = pygame.transform.scale(sprite_jogador, (100, 120))
jogador_rect = sprite_jogador.get_rect(midtop=(largura // 2, altura - 150))

sprite_inimigo = pygame.image.load("Recursos/inimigo.png").convert_alpha()
sprite_inimigo = pygame.transform.scale(sprite_inimigo, (120, 120))
inimigo_rect = sprite_inimigo.get_rect(midtop=(largura // 2, 80))
velocidade_inimigo = 3

def falar_boas_vindas(nome_jogador):
    engine = pyttsx3.init()
    engine.say(f"Bem-vindo, {nome_jogador}")
    engine.runAndWait()

def escutar_comando():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("🎙️ Diga 'iniciar' para começar o jogo...")
            audio = r.listen(source, timeout=5)
            comando = r.recognize_google(audio, language="pt-BR")
            print("Você disse:", comando)
            if "iniciar" in comando.lower():
                return True
        except:
            pass
    return False

def desenhar_caixa_texto(nome_digitado):
    tela.fill(VERDE_ESCURO)
    instrucao = fonte.render("Digite seu nome e pressione Enter", True, PRETO)
    tela.blit(instrucao, (largura // 2 - instrucao.get_width() // 2, 200))
    pygame.draw.rect(tela, PRETO, (largura // 2 - 200, 300, 400, 50), 2)
    texto_nome = fonte.render(nome_digitado, True, PRETO)
    tela.blit(texto_nome, (largura // 2 - 190, 310))
    pygame.display.flip()

def tela_boas_vindas_com_fundo(nome_jogador):
    fundo = pygame.image.load("Recursos/Boas-Vindas.png")
    fundo = pygame.transform.scale(fundo, (largura, altura))
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                return
        tela.blit(fundo, (0, 0))
        texto1 = fonte_grande.render("Boas-vindas", True, MARROM)
        texto2 = fonte_grande.render(f"{nome_jogador}!", True, MARROM)
        tela.blit(texto1, (largura // 2 - texto1.get_width() // 2, 180))
        tela.blit(texto2, (largura // 2 - texto2.get_width() // 2, 250))
        pygame.display.update()
        relogio.tick(30)

def tela_mecanica_jogo():
    botao_largura, botao_altura = 200, 60
    botao_x = largura // 2 - botao_largura // 2
    botao_y = 500
    explicacao = [
        " Mecânica do jogo:",
        "- Desvie dos ataques do Capuccino Assassino.",
        "- Use as setas para se mover.",
        "- Pressione 'Espaço' para pausar.",
        "",
        "Clique no botão, pressione Enter ou diga 'iniciar' para começar."
    ]
    fonte_temp = pygame.font.SysFont(None, 36)

    renderizou = False

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                return
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_x <= evento.pos[0] <= botao_x + botao_largura and botao_y <= evento.pos[1] <= botao_y + botao_altura:
                    return

        tela.fill(VERDE_ESCURO)
        for i, linha in enumerate(explicacao):
            texto = fonte_temp.render(linha, True, BRANCO)
            tela.blit(texto, (largura // 2 - texto.get_width() // 2, 150 + i * 40))
        pygame.draw.rect(tela, MARROM, (botao_x, botao_y, botao_largura, botao_altura))
        texto_botao = fonte_temp.render("Iniciar", True, BRANCO)
        tela.blit(texto_botao, (botao_x + botao_largura // 2 - texto_botao.get_width() // 2,
                                botao_y + botao_altura // 2 - texto_botao.get_height() // 2))
        pygame.display.flip()
        relogio.tick(30)

        if not renderizou:
            pygame.time.wait(1000)
            renderizou = True
        else:
            if escutar_comando():
                return

        tela.fill(VERDE_ESCURO)
        for i, linha in enumerate(explicacao):
            texto = fonte_temp.render(linha, True, BRANCO)
            tela.blit(texto, (largura // 2 - texto.get_width() // 2, 150 + i * 40))
        pygame.draw.rect(tela, MARROM, (botao_x, botao_y, botao_largura, botao_altura))
        texto_botao = fonte_temp.render("Iniciar", True, BRANCO)
        tela.blit(texto_botao, (botao_x + botao_largura // 2 - texto_botao.get_width() // 2,
                                botao_y + botao_altura // 2 - texto_botao.get_height() // 2))
        pygame.display.flip()
        relogio.tick(30)

def game_over(nome_jogador):
    salvar(nome_jogador, pontuacao)
    historico = carregar_historico()
    tela.fill(PRETO)

    texto_morte = fonte_grande.render("morreu!", True, VERMELHO)
    texto_nome = fonte.render(f"Jogador: {nome_jogador}", True, BRANCO)
    texto_pontuacao = fonte.render(f"Pontos: {pontuacao}", True, BRANCO)

    tela.blit(texto_morte, (largura // 2 - texto_morte.get_width() // 2, 100))
    tela.blit(texto_nome, (largura // 2 - texto_nome.get_width() // 2, 160))
    tela.blit(texto_pontuacao, (largura // 2 - texto_pontuacao.get_width() // 2, 200))

    y_inicio = 260
    titulo_hist = fonte.render("Últimas 5 tentativas:", True, BRANCO)
    tela.blit(titulo_hist, (largura // 2 - titulo_hist.get_width() // 2, y_inicio))

    for i, (nome_hist, pontos_hist, hora_hist) in enumerate(historico):
        texto_hist = fonte.render(f"{i+1}. {nome_hist} - {pontos_hist} pts - {hora_hist}", True, BRANCO)
        tela.blit(texto_hist, (largura // 2 - texto_hist.get_width() // 2, y_inicio + 30 + i * 30))

    pygame.display.flip()
    pygame.time.wait(3000)

def jogo(nome_jogador):
    global pontuacao, jogador_rect, inimigo_rect, velocidade_inimigo
    pausado = False
    espadas = []
    tempo_inicio_ataque = pygame.time.get_ticks()
    intervalo_espada = 2000
    vidas = 3
    invulneravel = False
    tempo_invulneravel = 1000  
    ultimo_dano = 0 

    sprite_espada = pygame.image.load("Recursos/katana.png").convert_alpha()
    sprite_espada = pygame.transform.scale(sprite_espada, (60, 60))
    fundo = pygame.image.load("Recursos/TelaPrincipal.jpg")
    fundo = pygame.transform.scale(fundo, (largura, altura))
    sprite_folha = pygame.image.load("Recursos/folha.png").convert_alpha()
    sprite_folha = pygame.transform.scale(sprite_folha, (40, 40))

    folhas = []
    for _ in range(5):
        folha_rect = sprite_folha.get_rect(midtop=(random.randint(0, largura), random.randint(0, altura)))
        folhas.append({"rect": folha_rect, "vx": random.choice([-2, -1, 1, 2]), "vy": random.choice([-1, 0, 1])})

    raio_base = 30
    raio_atual = raio_base
    delta_raio = 0.3
    max_raio = 40
    min_raio = 25
    raio_direcao = 1

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pausado = not pausado

        if not pausado:
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT] and jogador_rect.left > 0:
                jogador_rect.x -= velocidade
            if teclas[pygame.K_RIGHT] and jogador_rect.right < largura:
                jogador_rect.x += velocidade

            pontuacao += 1
            inimigo_rect.x += velocidade_inimigo
            if inimigo_rect.right >= largura or inimigo_rect.left <= 0:
                velocidade_inimigo *= -1

            tempo_atual = pygame.time.get_ticks()
            tempo_decorrido = (tempo_atual - tempo_inicio_ataque) // 4000
            intervalo_espada = max(300, 2000 - tempo_decorrido * 150)

            if tempo_atual % intervalo_espada < 60:
                espadas.append(sprite_espada.get_rect(midtop=(inimigo_rect.centerx, inimigo_rect.bottom)))

            for espada in espadas[:]:
                espada.y += 10
                if espada.top > altura:
                    espadas.remove(espada)
                elif espada.colliderect(jogador_rect):
                    if not invulneravel:
                        vidas -= 1
                        ultimo_dano = tempo_atual
                        invulneravel = True
                        if vidas <= 0:
                            game_over(nome_jogador)
                            return
                    espadas.remove(espada)

            if invulneravel and tempo_atual - ultimo_dano > tempo_invulneravel:
                invulneravel = False

            for folha in folhas:
                folha["rect"].x += folha["vx"]
                folha["rect"].y += folha["vy"]
                if folha["rect"].right < 0 or folha["rect"].left > largura:
                    folha["rect"].x = random.randint(0, largura)
                    folha["rect"].y = random.randint(0, altura)

            raio_atual += delta_raio * raio_direcao
            if raio_atual >= max_raio or raio_atual <= min_raio:
                raio_direcao *= -1

        tela.blit(fundo, (0, 0))
        pygame.draw.circle(tela, AMARELO, (largura - 70, 70), int(raio_atual))
        pygame.draw.circle(tela, LARANJA, (largura - 70, 70), int(raio_atual), 4)

        for folha in folhas:
            tela.blit(sprite_folha, folha["rect"])

        tela.blit(sprite_jogador, jogador_rect)
        tela.blit(sprite_inimigo, inimigo_rect)
        for espada in espadas:
            tela.blit(sprite_espada, espada)

        texto_pontos = fonte.render(f"Pontos: {pontuacao}", True, PRETO)
        texto_pausa = fonte.render("Pressione Espaco para Pausar", True, PRETO)
        texto_vidas = fonte.render(f"Vidas: {vidas}", True, VERMELHO)
        tela.blit(texto_pontos, (10, 10))
        tela.blit(texto_pausa, (10, 40))
        tela.blit(texto_vidas, (10, 70))

        if pausado:
            mostrar_mensagem_central(tela, "PAUSADO", fonte_grande, BRANCO, largura, altura)

        mostrar_dica(tela, largura, altura)

        pygame.display.update()
        relogio.tick(60)


digitando_nome = True
nome = ""
while digitando_nome:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN and nome.strip() != "":
                digitando_nome = False
            elif evento.key == pygame.K_BACKSPACE:
                nome = nome[:-1]
            else:
                if len(nome) < 20 and evento.unicode.isprintable():
                    nome += evento.unicode
    desenhar_caixa_texto(nome)
    relogio.tick(30)

tela_boas_vindas_com_fundo(nome)
falar_boas_vindas(nome)
tela_mecanica_jogo()
jogo(nome)

from datetime import datetime
import pygame

def salvar(nome, pontos):
    linha = f"{nome},{pontos},{datetime.now().strftime('%H:%M:%S')}\n"
    with open("recursos/historico.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)


def carregar_historico():
    try:
        with open("recursos/historico.txt", "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
            ultimas = linhas[-5:]  
            return [linha.strip().split(",") for linha in ultimas]
    except FileNotFoundError:
        return []

def mostrar_mensagem_central(tela, texto, fonte, cor, largura, altura):
    """Exibe uma mensagem centralizada na tela."""
    mensagem = fonte.render(texto, True, cor)
    tela.blit(mensagem, (largura // 2 - mensagem.get_width() // 2,
                         altura // 2 - mensagem.get_height() // 2))



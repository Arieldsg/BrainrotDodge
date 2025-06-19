import pygame


def mostrar_dica(tela, largura, altura):
    fonte_menor = pygame.font.Font("Recursos/letra.ttf", 20)
    mensagem = "Dica: Mantenha-se em movimento para sobreviver!"
    texto = fonte_menor.render(mensagem, True, (255, 255, 0))  
    tela.blit(texto, (largura // 2 - texto.get_width() // 2, altura - 40))


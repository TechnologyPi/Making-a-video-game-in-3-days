import pygame

def Text(text, color,x=10, y=10, size=20):
    display = pygame.display.get_surface()
    font = pygame.font.SysFont("../assets/fonts/Comic Sans MS.ttf", size)
    text_colour = color
    text_surface = font.render(text, True, text_colour)
    display.blit(text_surface, (x, y))
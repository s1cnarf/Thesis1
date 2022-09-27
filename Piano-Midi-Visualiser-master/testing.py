import pygame
pygame.init()

res = (600,600)
screen = pygame.display.set_mode(res)
pygame.display.set_caption("Tic Tac Toe")

background = (255,150,150)
color_light = (170,170,170)
color_dark = (100,100,100)
hover_color = (255, 204, 203)
width = screen.get_width()
height = screen.get_height()

def draw_line():

    pygame.draw.rect(screen, line_color, (190,10,10,580))
    pygame.draw.rect(screen, line_color, (390, 10, 10, 580))
    pygame.draw.rect(screen, line_color, (10, 200, 580, 10))
    pygame.draw.rect(screen, line_color, (10, 390, 580, 10))

rect_list = [
    pygame.Rect(10, 10, 180, 190),
    pygame.Rect(200, 10, 180, 190),
    pygame.Rect(400, 10, 180, 190),
    pygame.Rect(10, 210, 180, 190),
    pygame.Rect(200, 210, 180, 190),
    pygame.Rect(400, 210, 180, 190),
    pygame.Rect(10, 400, 180, 190),
    pygame.Rect(200, 400, 180, 190),
    pygame.Rect(400, 400, 180, 190)]
clicked_list = [0 for _ in rect_list]

def highlight():
    for rect in rect_list:
        if rect.collidepoint(mouse):
            pygame.draw.rect(screen, hover_color, rect)

while True:
    mouse = pygame.mouse.get_pos()
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
        if ev.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(rect_list):
                if rect.collidepoint(ev.pos):
                    clicked_list[i] = 1
    
    line_color = (212, 212, 255)
    screen.fill(background)
    draw_line()
    highlight()
    for i, rect in enumerate(rect_list):
        if clicked_list[i] == 1:
            pygame.draw.rect(screen,(255,255,255),(200, 210, 180, 190))
    pygame.display.update()
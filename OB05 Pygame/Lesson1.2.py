import pygame
import time

pygame.init()

window_size = (1200, 800)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Тестовый проект')

image = pygame.image.load('owl.png')
image_rect = image.get_rect()
image2 = pygame.image.load('jack.png')
image2_rect = image2.get_rect()


run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEMOTION:
            x, y = pygame.mouse.get_pos()
            image_rect.x = x - 100
            image_rect.y = y - 100

    if image_rect.colliderect(image2_rect):
        print('Произошло столкновение')
        time.sleep(1)


    screen.fill((89, 155, 214))
    screen.blit(image, image_rect)
    screen.blit(image2, image2_rect)
    pygame.display.flip()

pygame.quit()


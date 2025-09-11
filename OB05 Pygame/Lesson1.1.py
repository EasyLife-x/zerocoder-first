import pygame

pygame.init()

window_size = (1200, 800)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Тестовый проект')

image = pygame.image.load('owl.png')
image_rect = image.get_rect()
speed = 1

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        image_rect.x -= speed
    if keys[pygame.K_d]:
        image_rect.x += speed
    if keys[pygame.K_w]:
        image_rect.y -= speed
    if keys[pygame.K_s]:
        image_rect.y += speed


    screen.fill((89, 155, 214))
    screen.blit(image, image_rect)
    pygame.display.flip()

pygame.quit()


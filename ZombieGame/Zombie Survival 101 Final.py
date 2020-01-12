#Import and Initialize
import pygame, pyZombies, random
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1600, 900))

def game():
    #Display
    pygame.display.set_caption("Zombie Survival 101") 
    
    #Entities
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0)) 
    
    #Create Sprites
    player = pyZombies.Player(screen)
    zombie = pyZombies.Zombie(screen)
    zombies = pygame.sprite.Group(zombie)
    devils = pygame.sprite.Group()
    runners = pygame.sprite.Group()
    score = pyZombies.Score()
    gameover = pygame.image.load("game-over.gif")
    gameover = gameover.convert()
    bullets = pygame.sprite.Group()
    fireballs = pygame.sprite.Group()
    healthpowerup = pyZombies.Healthpowerup(screen)
    armorpowerup = pyZombies.Armorpowerup(screen)
    player_hit = pygame.mixer.Sound("Pain.wav")
    player_hit.set_volume(0.4)    
    devil_spawn = pygame.mixer.Sound("Zombie Demon Spawn.wav")
    devil_spawn.set_volume(0.4)  
    fireball_shoot = pygame.mixer.Sound("Fireball.wav")
    fireball_shoot.set_volume(0.4)  
    shooting = pygame.mixer.Sound("Gun Sound.wav")
    shooting.set_volume(0.4)  
    allSprites = pygame.sprite.OrderedUpdates(bullets, fireballs, player, score, healthpowerup, armorpowerup, runners, devils, zombies)
    
    #Action
    
    #Assign
    keepGoing = True
    clock = pygame.time.Clock()
    time = 0
    not_spawned = True
    health_powerup_show = False
    armor_powerup_show = False
    armor_on = False
    quitting = False
    
    # Loop
    while keepGoing:
      
        # Time
        clock.tick(60)   
        time += 1
        
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True
                keepGoing = False   
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = pyZombies.Bullet(player.player_posx(), player.player_posy(), player.get_direction_facing(), screen)
                    bullets.add(bullet)
                    shooting.play()
                    allSprites = pygame.sprite.OrderedUpdates(bullets, fireballs, player, healthpowerup, armorpowerup, runners, devils, zombies, score)
                    
        keydown = pygame.key.get_pressed()
        if keydown[pygame.K_UP]:
            player.go_up()
        elif keydown[pygame.K_DOWN]:
            player.go_down()         
        elif keydown[pygame.K_LEFT]:
            player.go_left()        
        elif keydown[pygame.K_RIGHT]:
            player.go_right()  
            
        for zombie in zombies:
            if zombie.rect.colliderect(player):
                if time % 40 == 0:
                    if armor_on:
                        score.lose_armor(20)
                        zombie.stop()  
                    else:
                        score.lose_health(10)
                        player_hit.play()
                        zombie.stop()                                                
            else:
                zombie.move_to_player(player.player_posx(), player.player_posy())
                
        for runner in runners:
            if runner.rect.colliderect(player):
                if time % 40 == 0:
                    if armor_on:
                        score.lose_armor(40)
                        runner.stop()  
                    else:
                        score.lose_health(20) 
                        player_hit.play()
                        runner.stop()                                                
            else:
                runner.move_to_player(player.player_posx(), player.player_posy())        
                
        for devil in devils:
            if random.randrange(55) == 7:
                fireball = pyZombies.Fireball(player.player_posx(), \
                                              player.player_posy(), \
                                              devil.devil_posx(), \
                                              devil.devil_posy(), screen)
                fireballs.add(fireball)  
                fireball_shoot.play()
                allSprites = pygame.sprite.OrderedUpdates(bullets, fireballs, player, healthpowerup, armorpowerup, runners, devils, zombies, score)
                
            if devil.rect.colliderect(player):
                if time % 40 == 0:
                    if armor_on:
                        score.lose_armor(10)
                        devil.stop()  
                    else:
                        score.lose_health(50) 
                        player_hit.play()
                        devil.stop()                                                
            else:
                devil.move_to_player(player.player_posx(), player.player_posy())        
            
        for bullet in bullets:
            shotZombie = pygame.sprite.spritecollide(bullet, zombies, False)
            if shotZombie:
                for zombie in shotZombie:
                    score.player_scored(100)
                    score.add_zombies_killed()
                    bullet.kill()
                    zombie.reset()
                    
            shotDevil = pygame.sprite.spritecollide(bullet, devils, False)
            if shotDevil:
                for devil in shotDevil:
                    bullet.kill()
                    devil.lose_devil_health() 
                    if devil.get_devil_health() == 0:
                        score.player_scored(200)
                        score.add_zombies_killed()
                        devil.kill()
                        
            shotRunner = pygame.sprite.spritecollide(bullet, runners, False)
            if shotRunner:
                for runner in shotRunner:
                    bullet.kill()
                    score.player_scored(150)
                    score.add_zombies_killed()
                    runner.kill()            
                                    
        for fireball in fireballs:
            if fireball.rect.colliderect(player):
                if armor_on:
                    score.lose_armor(50)
                    zombie.stop()  
                else:
                    score.lose_health(25) 
                    player_hit.play() 
                fireball.kill()
                
        if score.get_zombies_killed()%5 == 0:
            if not_spawned:
                zombie = pyZombies.Zombie(screen)
                zombies.add(zombie)
                allSprites = pygame.sprite.OrderedUpdates(bullets, fireballs, player, score, healthpowerup, armorpowerup, runners, devils, zombies, score)
                not_spawned = False              
        else:
            not_spawned = True        
        
        #health powerup      
        if random.randrange(2000) == 12:
            if health_powerup_show == False:
                healthpowerup.show()
                health_powerup_show = True
        
        #armor powerup        
        if random.randrange(1500) == 18:
            if armor_powerup_show == False:
                armorpowerup.show()
                armor_powerup_show = True 
                
        #devil spawn
        if random.randrange(1000) == 66:
            devil = pyZombies.Devil(screen)
            devils.add(devil)
            devil_spawn.play()
            allSprites = pygame.sprite.OrderedUpdates(bullets, fireballs, player, healthpowerup, armorpowerup, runners, devils, zombies, score)          
            
        #runner spawn
        if random.randrange(700) == 69:
            runner = pyZombies.Runner(screen)
            runners.add(runner)
            allSprites = pygame.sprite.OrderedUpdates(bullets, fireballs, player, healthpowerup, armorpowerup, runners, devils, zombies, score)                  
        
        if player.rect.colliderect(healthpowerup):  
            score.restore_health()
            healthpowerup.hide()
            health_powerup_show = False  
            
        if player.rect.colliderect(armorpowerup):
            score.restore_armor()
            armorpowerup.hide()
            armor_on = True
            armor_powerup_show = False
                        
        if score.get_health() <= 0:
            keepGoing = False
            
        if score.get_armor() <= 0:
            armor_on = False
        
        # Refresh screen
  
        screen.blit(background, (0, 0))         
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
           
        pygame.display.flip() 
        
    #Closes game window    
    screen.blit(gameover, (200, 100))
    pygame.display.flip() 
    pygame.time.delay(2000)

    return quitting
    
def menu():
    '''This function defines the 'mainline logic' for our game.'''
      
    # Display
    pygame.display.set_caption("Menu")
     
    # Entities
    background = pygame.Surface(screen.get_size())
    background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    menu_play = pyZombies.Label("Play", (800,500))
    menu_instructions = pyZombies.Label("How to Play", (790,600))
    menu_exit = pyZombies.Label("Exit", (800,700))
    allSprites = pygame.sprite.Group(menu_play, menu_instructions, menu_exit)
     
    # ACTION
     
    # Assign 
    clock = pygame.time.Clock()
    keepGoing = True
    quitting = False
    instructions_display = False  
 
    # Loop
    while keepGoing:
        # Time
        clock.tick(30)
     
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True
                keepGoing = False
                
        if menu_play.rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN:
                game()
                
        if menu_instructions.rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN:
                instructions_display = True
                keepGoing = False
                                 
        if menu_exit.rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN:
                quitting = True
                keepGoing = False
                
        keydown = pygame.key.get_pressed()
        if instructions_display:
            if keydown[pygame.K_ESCAPE]:
                instructions_display = False        
                      
        # Refresh screen    
        screen.blit(background, (0, 0))
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
         
        pygame.display.flip()  
      
    return (quitting, instructions_display)

def instructions():
    '''This function defines the 'mainline logic' for our game.'''
      
    # Display
    pygame.display.set_caption("Instructions")
     
    # Entities
    background = pygame.Surface(screen.get_size())
    background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    instructions = pygame.image.load("Instructions.png")
    instructions.convert()
     
    # ACTION
     
    # Assign 
    clock = pygame.time.Clock()
    keepGoing = True
    quitting = False
    instructions_display = True  
 
    # Loop
    while keepGoing:
        # Time
        clock.tick(30)
     
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True
                keepGoing = False
                
        keydown = pygame.key.get_pressed()
        if instructions_display:
            if keydown[pygame.K_ESCAPE]:
                instructions_display = False  
                keepGoing = False
                      
        # Refresh screen    
        screen.blit(instructions, (0, 0))
        pygame.display.flip()  
      
    return (quitting, instructions_display)
    
def main():
    keepGoing = True
    while keepGoing:
        quitting, instructions_display = menu()
        if quitting:
            keepGoing = False
            break
        elif instructions_display:
            instructions()
        if game() == True:
            keepGoing = False
            break
        
    pygame.quit()
            
# Call the main function
main()            
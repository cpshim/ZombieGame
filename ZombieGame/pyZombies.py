import pygame, math, random

class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.player_left = pygame.image.load("Player Sprite Left.gif")
        self.player_right = pygame.image.load("Player Sprite Right.gif")
        self.player_up = pygame.image.load("Player Sprite Up.gif")
        self.player_down = pygame.image.load("Player Sprite Down.gif")
        self.image = self.player_right
        self.__direction = (1,0)
        self.__screen = screen
        self.rect = self.image.get_rect()
        self.rect.x = screen.get_width()/2
        self.rect.y = screen.get_height()/2
        self.__dx = 5
        self.__dy = 5
        
    def go_right(self):
        self.image = self.player_right
        self.__direction = (1,0)
        self.rect.x += self.__dx
    
    def go_left(self):
        self.image = self.player_left
        self.__direction = (-1,0)
        self.rect.x -= self.__dx
        
    def go_up(self):
        self.image = self.player_up
        self.__direction = (0,1)
        self.rect.y -= self.__dx    

    def go_down(self):
        self.image = self.player_down
        self.__direction = (0,-1)
        self.rect.y += self.__dx
        
    def get_direction_facing(self):
        return self.__direction
        
    def player_posx(self):
        return self.rect.x
                
    def player_posy(self):
        return self.rect.y
    
    def update(self):
        if self.rect.right > self.__screen.get_width():
            self.rect.right = self.__screen.get_width()
        if self.rect.x < 0:
            self.rect.x = 0    
        if self.rect.bottom > self.__screen.get_height():
            self.rect.bottom = self.__screen.get_height()
        if self.rect.top < 0:
            self.rect.top = 0
    
class Zombie(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.__screen = screen
        self.screen_side = random.randrange(4)
        self.zombie_left = pygame.image.load("Zombie Sprite Left.gif")
        self.zombie_right = pygame.image.load("Zombie Sprite Right.gif")
        self.zombie_up = pygame.image.load("Zombie Sprite Up.gif")
        self.zombie_down = pygame.image.load("Zombie Sprite Down.gif")  
        self.zombie_NE = pygame.image.load("Zombie Sprite NE.gif")
        self.zombie_NW = pygame.image.load("Zombie Sprite NW.gif")
        self.zombie_SE = pygame.image.load("Zombie Sprite SE.gif")
        self.zombie_SW = pygame.image.load("Zombie Sprite SW.gif")
        self.image = self.zombie_left
        self.rect = self.image.get_rect()
        if self.screen_side == 0:            
            self.rect.x = self.__screen.get_width()
            self.rect.y = random.randrange(self.__screen.get_height())    
        elif self.screen_side == 1:            
            self.rect.x = random.randrange(self.__screen.get_width())
            self.rect.y = 0   
        elif self.screen_side == 2:            
            self.rect.x = 0
            self.rect.y = random.randrange(self.__screen.get_height())
        elif self.screen_side == 3:
            self.rect.x = random.randrange(self.__screen.get_width())
            self.rect.y = self.__screen.get_height()            
                    
    
    def move_to_player(self, player_posx, player_posy):
        # find normalized direction vector (dx, dy) between enemy and player
        dx = self.rect.x - player_posx
        dy = self.rect.y - player_posy
        if (self.rect.x > (player_posx-100) and self.rect.x < (player_posx+100)) and \
           (self.rect.y > player_posy):
            self.image = self.zombie_up
        elif (self.rect.x > (player_posx-100) and self.rect.x < (player_posx+100)) and \
            (self.rect.y < player_posy):
            self.image = self.zombie_down
        elif (self.rect.y > (player_posy-100) and self.rect.y < (player_posy+100)) and \
            (self.rect.x < player_posx):
            self.image = self.zombie_right        
        elif (self.rect.y > (player_posy-100) and self.rect.y < (player_posy+100)) and \
            (self.rect.x > player_posx):
            self.image = self.zombie_left 
        
        elif (self.rect.x > (player_posx+100) and self.rect.y > (player_posy+100)) and \
            (self.rect.y > player_posy):
            self.image = self.zombie_NW
        elif (self.rect.x > (player_posx+100) and self.rect.y < (player_posy-100)) and \
            (self.rect.y < player_posy):
            self.image = self.zombie_SW       
        elif (self.rect.x < (player_posx-100) and self.rect.y > (player_posy+100)) and \
            (self.rect.y > player_posy):
            self.image = self.zombie_NE                
        elif (self.rect.x < (player_posx-100) and self.rect.y < (player_posy-100)) and \
            (self.rect.y < player_posy):
            self.image = self.zombie_SE        

        hypotenuse = math.hypot(dx, dy)
        dx = dx / hypotenuse
        dy = dy / hypotenuse
        # move along this normalized vector towards the player at current speed
        self.rect.x -= dx * 2
        self.rect.y -= dy * 2    
        
    def stop(self):
        dx = 0
        dy = 0
        
    def reset(self):
        self.screen_side = random.randrange(4)  
        if self.screen_side == 0:            
            self.rect.x = self.__screen.get_width()
            self.rect.y = random.randrange(self.__screen.get_height())    
        elif self.screen_side == 1:            
            self.rect.x = random.randrange(self.__screen.get_width())
            self.rect.y = 0   
        elif self.screen_side == 2:            
            self.rect.x = 0
            self.rect.y = random.randrange(self.__screen.get_height())
        elif self.screen_side == 3:
            self.rect.x = random.randrange(self.__screen.get_width())
            self.rect.y = self.__screen.get_height()                    
    
    def update(self):
        if self.rect.right > self.__screen.get_width():
            self.rect.right = self.__screen.get_width()
        if self.rect.x < 0:
            self.rect.x = 0  
            
class Runner(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.__screen = screen
        self.screen_side = random.randrange(4)
        self.runner_left = pygame.image.load("Runner Sprite Left.gif")
        self.runner_right = pygame.image.load("Runner Sprite Right.gif")
        self.runner_up = pygame.image.load("Runner Sprite Up.gif")
        self.runner_down = pygame.image.load("Runner Sprite Down.gif")  
        self.runner_NE = pygame.image.load("Runner Sprite NE.gif")
        self.runner_NW = pygame.image.load("Runner Sprite NW.gif")
        self.runner_SE = pygame.image.load("Runner Sprite SE.gif")
        self.runner_SW = pygame.image.load("Runner Sprite SW.gif")
        self.image = self.runner_left
        self.rect = self.image.get_rect()
        if self.screen_side == 0:            
            self.rect.x = self.__screen.get_width()
            self.rect.y = random.randrange(self.__screen.get_height())    
        elif self.screen_side == 1:            
            self.rect.x = random.randrange(self.__screen.get_width())
            self.rect.y = 0   
        elif self.screen_side == 2:            
            self.rect.x = 0
            self.rect.y = random.randrange(self.__screen.get_height())
        elif self.screen_side == 3:
            self.rect.x = random.randrange(self.__screen.get_width())
            self.rect.y = self.__screen.get_height()            
                    
    
    def move_to_player(self, player_posx, player_posy):
        # find normalized direction vector (dx, dy) between enemy and player
        dx = self.rect.x - player_posx
        dy = self.rect.y - player_posy
        if (self.rect.x > (player_posx-100) and self.rect.x < (player_posx+100)) and \
           (self.rect.y > player_posy):
            self.image = self.runner_up
        elif (self.rect.x > (player_posx-100) and self.rect.x < (player_posx+100)) and \
            (self.rect.y < player_posy):
            self.image = self.runner_down
        elif (self.rect.y > (player_posy-100) and self.rect.y < (player_posy+100)) and \
            (self.rect.x < player_posx):
            self.image = self.runner_right        
        elif (self.rect.y > (player_posy-100) and self.rect.y < (player_posy+100)) and \
            (self.rect.x > player_posx):
            self.image = self.runner_left 
        
        elif (self.rect.x > (player_posx+100) and self.rect.y > (player_posy+100)) and \
            (self.rect.y > player_posy):
            self.image = self.runner_NW
        elif (self.rect.x > (player_posx+100) and self.rect.y < (player_posy-100)) and \
            (self.rect.y < player_posy):
            self.image = self.runner_SW       
        elif (self.rect.x < (player_posx-100) and self.rect.y > (player_posy+100)) and \
            (self.rect.y > player_posy):
            self.image = self.runner_NE                
        elif (self.rect.x < (player_posx-100) and self.rect.y < (player_posy-100)) and \
            (self.rect.y < player_posy):
            self.image = self.runner_SE        

        hypotenuse = math.hypot(dx, dy)
        dx = dx / hypotenuse
        dy = dy / hypotenuse
        # move along this normalized vector towards the player at current speed
        self.rect.x -= dx * 5
        self.rect.y -= dy * 5    
        
    def stop(self):
        dx = 0
        dy = 0
        
    def update(self):
        if self.rect.right > self.__screen.get_width():
            self.rect.right = self.__screen.get_width()
        if self.rect.x < 0:
            self.rect.x = 0      
        
class Devil(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.__screen = screen
        self.screen_side = random.randrange(4)
        self.__devil_health = 5
        self.devil_left = pygame.image.load("Devil Sprite Left.gif")
        self.devil_right = pygame.image.load("Devil Sprite Right.gif")
        self.devil_up = pygame.image.load("Devil Sprite Up.gif")
        self.devil_down = pygame.image.load("Devil Sprite Down.gif")  
        self.devil_NE = pygame.image.load("Devil Sprite NE.gif")
        self.devil_NW = pygame.image.load("Devil Sprite NW.gif")
        self.devil_SE = pygame.image.load("Devil Sprite SE.gif")
        self.devil_SW = pygame.image.load("Devil Sprite SW.gif")
        self.image = self.devil_left
        self.rect = self.image.get_rect()
        if self.screen_side == 0:            
            self.rect.x = self.__screen.get_width()
            self.rect.y = random.randrange(self.__screen.get_height())    
        elif self.screen_side == 1:            
            self.rect.x = random.randrange(self.__screen.get_width())
            self.rect.y = 0   
        elif self.screen_side == 2:            
            self.rect.x = 0
            self.rect.y = random.randrange(self.__screen.get_height())
        elif self.screen_side == 3:
            self.rect.x = random.randrange(self.__screen.get_width())
            self.rect.y = self.__screen.get_height()            
                       
    def move_to_player(self, player_posx, player_posy):
        # find normalized direction vector (dx, dy) between enemy and player
        dx = self.rect.x - player_posx
        dy = self.rect.y - player_posy
        if (self.rect.x > (player_posx-100) and self.rect.x < (player_posx+100)) and \
           (self.rect.y > player_posy):
            self.image = self.devil_up
        elif (self.rect.x > (player_posx-100) and self.rect.x < (player_posx+100)) and \
            (self.rect.y < player_posy):
            self.image = self.devil_down
        elif (self.rect.y > (player_posy-100) and self.rect.y < (player_posy+100)) and \
            (self.rect.x < player_posx):
            self.image = self.devil_right        
        elif (self.rect.y > (player_posy-100) and self.rect.y < (player_posy+100)) and \
            (self.rect.x > player_posx):
            self.image = self.devil_left 
        
        elif (self.rect.x > (player_posx+100) and self.rect.y > (player_posy+100)) and \
            (self.rect.y > player_posy):
            self.image = self.devil_NW
        elif (self.rect.x > (player_posx+100) and self.rect.y < (player_posy-100)) and \
            (self.rect.y < player_posy):
            self.image = self.devil_SW       
        elif (self.rect.x < (player_posx-100) and self.rect.y > (player_posy+100)) and \
            (self.rect.y > player_posy):
            self.image = self.devil_NE                
        elif (self.rect.x < (player_posx-100) and self.rect.y < (player_posy-100)) and \
            (self.rect.y < player_posy):
            self.image = self.devil_SE        

        hypotenuse = math.hypot(dx, dy)
        dx = dx / hypotenuse
        dy = dy / hypotenuse
        # move along this normalized vector towards the player at current speed
        self.rect.x -= dx * 2
        self.rect.y -= dy * 2 
    
    def devil_posx(self):
        return self.rect.x
                
    def devil_posy(self):
        return self.rect.y 
    
    def get_devil_health(self):
        return self.__devil_health
    
    def lose_devil_health(self):
        self.__devil_health -= 1
        
    def stop(self):
        dx = 0
        dy = 0   
        
    def update(self):
        if self.rect.right > self.__screen.get_width():
            self.rect.right = self.__screen.get_width()
        if self.rect.x < 0:
            self.rect.x = 0  
            
class Fireball(pygame.sprite.Sprite):
    def __init__(self, player_posx, player_posy, devil_posx, devil_posy, screen):
        pygame.sprite.Sprite.__init__(self)
        self.__screen = screen
        self.image = pygame.image.load("Fireball.gif")
        self.player_posx = player_posx
        self.player_posy = player_posy                     
        self.screen = screen
        self.rect = self.image.get_rect()
        self.rect.x = devil_posx
        self.rect.y = devil_posy                       
        self.__dx = self.rect.x - player_posx
        self.__dy = self.rect.y - player_posy 
        self.__distance = math.hypot(self.__dx, self.__dy)
        self.__dx = self.__dx / self.__distance
        self.__dy = self.__dy / self.__distance
                
    def fireball_pos(self):
        return self.rect.x
        
    def update(self):
        self.rect.x -= self.__dx * 6
        self.rect.y -= self.__dy * 6
        if self.rect.x > self.screen.get_width() or self.rect.x < 0:
            self.kill()
        if self.rect.y > self.screen.get_height() or self.rect.y < 0:
            self.kill()        
            
class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_posx, player_posy, player_dir, screen):
        pygame.sprite.Sprite.__init__(self)
        self.__dx = 15*player_dir[0]
        self.__dy = 15*player_dir[1]
        self.bullet_right = pygame.image.load("Bullet Right.gif")
        self.bullet_left = pygame.image.load("Bullet Left.gif")
        self.bullet_up = pygame.image.load("Bullet Up.gif")
        self.bullet_down = pygame.image.load("Bullet Down.gif")        
        self.image = pygame.image.load("Bullet Right.gif")
        self.player_posx = player_posx
        self.player_posy = player_posy                     
        self.screen = screen
        self.rect = self.image.get_rect()
        if self.__dx > 0:
            self.rect.x = self.player_posx+100
            self.rect.y = self.player_posy+40                  
        elif self.__dx < 0:
            self.rect.x = self.player_posx
            self.rect.y = self.player_posy+40                  
        elif self.__dy > 0:
            self.rect.x = self.player_posx+40
            self.rect.y = self.player_posy                  
        elif self.__dy < 0:
            self.rect.x = self.player_posx+40
            self.rect.y = self.player_posy+80                  
        
    def bullet_pos(self):
        return self.rect.x
        
    def update(self):
        self.rect.x += self.__dx
        self.rect.y -= self.__dy
        if self.__dx > 0:
            self.image = self.bullet_right
        elif self.__dx < 0:
            self.image = self.bullet_left     
        elif self.__dy > 0:
            self.image = self.bullet_up
        elif self.__dy < 0:
            self.image = self.bullet_down
        if self.rect.x > self.screen.get_width() or self.rect.x < 0:
            self.kill()
        if self.rect.y > self.screen.get_height() or self.rect.y < 0:
            self.kill()        
    
class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.__font = pygame.font.Font("game_over.ttf", 60)
        self.__player_score = 0
        self.__health = 100
        self.__armor = 0
        self.__zombies_killed = 0
        
    def player_scored(self, points):
        self.__player_score += points
        
    def restore_armor(self):
        self.__armor = 100
        
    def lose_armor(self, hp):
        self.__armor -= hp
        
    def get_armor(self):
        return self.__armor
        
    def lose_health(self, hp):
        self.__health -= hp
        
    def get_health(self):
        return self.__health 
    
    def restore_health(self):
        self.__health = 100  
        
    def add_zombies_killed(self):
        self.__zombies_killed += 1
    
    def get_zombies_killed(self):
        return self.__zombies_killed 
    
    def update(self):
        message = "Score: %d    Health: %d%%    Armor: %d%%" %\
                (self.__player_score, self.__health, self.__armor)
        self.image = self.__font.render(message, 1, (0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (530, 25)  
        
class Healthpowerup(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Health Pickup.gif")
        self.rect = self.image.get_rect()
        self.rect.top = screen.get_height()+50
        self.__screen = screen
        
    def show(self):
        self.rect.x = random.randrange(self.__screen.get_width())
        self.rect.y = random.randrange(self.__screen.get_height())
        
    def hide(self):
        self.rect.top = self.rect.top = self.__screen.get_height()+50

class Armorpowerup(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Armour Pickup.gif")
        self.rect = self.image.get_rect()
        self.rect.top = screen.get_height()+50
        self.__screen = screen
        
    def show(self):
        self.rect.x = random.randrange(self.__screen.get_width())
        self.rect.y = random.randrange(self.__screen.get_height())
        
    def hide(self):
        self.rect.top = self.rect.top = self.__screen.get_height()+50


class Label(pygame.sprite.Sprite):
    def __init__(self, message, x_y_center):
        pygame.sprite.Sprite.__init__(self)
        self.__font = pygame.font.Font("game_over.ttf", 120)
        self.__text = message
        self.__center = x_y_center
        self.image = self.__font.render(self.__text, 1, (0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.__center        
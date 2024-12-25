import pygame
import sys
import math
import random


# Initialize Pygame
pygame.init()

# Constants

FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
PURPLE=(128,0,128)
GRAVITY = 0.2
MAX_POWER = 50  # Maximum power for bullet shooting
res=0.01
enres=0
# Game Stage Constants

stage_score=[0,500,1100,1700,3000,5000]

# Create game screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 




WIDTH, HEIGHT = screen.get_size()
C=WIDTH//140
R=HEIGHT//100
pygame.display.set_caption("game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
enemy_count=0
nshark=0

# Game State Variables
score = 0
game_stage = 1
background=[]
background.append( pygame.image.load("開始畫面.jpg"))
background.append(pygame.image.load("遊戲畫面.png"))
background.append(pygame.image.load('輸結束畫面.png'))
background.append(pygame.image.load('贏結束畫面.jpg'))
for bg in background:
    background[background.index(bg)]=pygame.transform.scale(bg,(WIDTH, HEIGHT))


        
        
# Player properties
player_size = (50, 100)
player_pos = [100, HEIGHT // 2 - player_size[1] // 2]
player_speed = 5
player_bullets = []
player_health = 1000
enemies = []
sharks=[]
shark_image=[]

target_image=pygame.image.load("目標.png")
target_image = pygame.transform.scale(target_image, (100,40))
boom_image=pygame.image.load('爆炸.png')
boom_image = pygame.transform.scale(boom_image,(50,50))
# Load images
shark_image1=pygame.image.load("鯊魚左.png")
shark_image2=pygame.image.load("鯊魚右.png")


player_idle = pygame.image.load("士兵.png")
player_idle = pygame.transform.scale(player_idle, player_size)

player_drag = pygame.image.load("士兵2.png")
player_drag = pygame.transform.scale(player_drag, player_size)

enemy_images = [
    pygame.image.load("海盜1.png"),
    pygame.image.load("海盜2.png"),
    pygame.image.load("海盜3.png")
]



    
    

def spawn_shark(n):
    global nshark

    for i in range (3-n):
        s=random.uniform(1,2)
        size=[150*s,60*s]
        x=random.choice([-150*s,WIDTH])
        if x>0:
            vx= random.uniform(-10,-1)
            image=shark_image1
        else:
            vx=random.uniform(1,10)
            image=shark_image2
        shark={'pos':[x,random.randint(0,HEIGHT//30-1)*30],'image':image,'size':size,'velocity_x':vx,'velocity_y':0,'touch':random.randint(2,5)}
        sharks.append(shark)
        nshark+=1
        
def update_shark():
    global nshark
    for shark in sharks:
        
        if  shark['touch']>0:
            if (shark['pos'][0]<=-shark['size'][0] and shark['velocity_x']<=0) or (shark['pos'][0]>=WIDTH and shark['velocity_x']>=0):
                shark['velocity_x']=-shark['velocity_x']
                shark['touch']-=1
            if shark['velocity_x']<=0:
                shark['image']=shark_image1
            else : shark['image']=shark_image2
            if shark['touch']==0:
                sharks.remove(shark)
                nshark-=1
                
            shark['pos'][0]+=shark['velocity_x']
            shark['pos'][1]+=shark['velocity_y']
spear_image = pygame.image.load("矛.png") 
spear_image = pygame.transform.scale(spear_image, (30, 200))
enemy_bullet_images = [
    ("蛋.png", (20, 25)),("炸彈.png",(50,65)),
    ("大象.png", (150, 100)),  
    ("聖誕樹.png", (80, 120)),   
    ("輪子.png", (50, 50)),  
    ("石頭.png", (80, 100)),  
    ("車子.png", (150, 80))
    ,("南瓜.png", (100, 80)),("麵包.png",(80,30)),("披薩.png",(50,50))    
]
enemy_bullet_mask=[]
for image in enemy_bullet_images:
    im,size=image
    current_image=pygame.image.load(im)
    current_image=pygame.transform.scale(current_image,size)
    mask=pygame.mask.from_surface(current_image)
    enemy_bullet_mask.append(mask)

def draw_healthbar():
    h=player_health
    fh=1500
    x=player_pos[0]
    y=player_pos[1]
    pygame.draw.rect(screen, RED, (x, y-20,70 , 10))
    pygame.draw.rect(screen, GREEN, (x, y-20,70*(h/fh) , 10))
    for enemy in enemies:
        x=enemy['pos'][0]
        y=enemy['pos'][1]
        h=enemy['health']
        fh=enemy['full_health']
        if enemy['boss']==1:
            pygame.draw.rect(screen, RED, (x, y-20,70 , 10))
            pygame.draw.rect(screen, PURPLE, (x, y-20,70*(h/fh) , 10))
        else:
            pygame.draw.rect(screen, GRAY, (x, y-20,70 , 10))
            pygame.draw.rect(screen, RED, (x, y-20,70*(h/fh) , 10))
    

def boss():
    if game_stage>=3 and random.randint(1,2)%2:
        return 1
    else:return 0
def spawn_enemies(num_enemies):
    global enemies,enemy_count
    bossnum=0
    p=boss()
    enemies.clear()
    enemy_count=num_enemies+p
    
    
        # 隨機選擇海盜圖片
    x=random.randint(1,C-1)
    y=random.randint(1,R-1)
    if p==1 and bossnum==0:
        enemy_size=(70,120)
        bullet_cooldown=40
        enemy_image=pygame.image.load("船長.png")
        enemy_image = pygame.transform.scale(enemy_image, enemy_size)
        full_health=500
        enemy = {
            'pos': [WIDTH/2+70*x,100*y+20],
            'image': enemy_image,
            'size': enemy_size,
            'bullets': [],
            'bullet_cooldown': bullet_cooldown,
            'bullet_timer': random.randint(0,100),'boss':1,
            'health':full_health,'full_health':full_health,'cooldown':5
            }
        enemies.append(enemy)
        bossnum=1
    for i in range(num_enemies):
        x=random.randint(1,C-1)
        y=random.randint(1,R-1)
        enemy_image=random.choice(enemy_images)
        if enemy_image == enemy_images[0]:  # 海盜1
            enemy_size = (70, 100)  # 海盜1的基準大小
            bullet_cooldown = 40+30*(num_enemies-1)
            full_health=250  # 海盜1的 cooldown 比較長
        elif enemy_image == enemy_images[1]:  # 海盜2
            enemy_size = (55, 90)  # 海盜2的基準大小
            bullet_cooldown = 50+30*(num_enemies-1)
            full_health=200  # 海盜2的 cooldown 比較短
        elif enemy_image == enemy_images[2]:  # 海盜3
            enemy_size = (50, 70)  # 海盜3的基準大小
            bullet_cooldown = 35+30*(num_enemies-1)
            full_health=100
        enemy_image = pygame.transform.scale(enemy_image, enemy_size)
        enemy = {
                'pos': [WIDTH/2+70*x,100*y],
                'image': enemy_image,
                'size': enemy_size,
                'bullets': [],
                'bullet_cooldown': bullet_cooldown,
                'bullet_timer': random.randint(0,100),'boss':0,'health':full_health,'full_health':full_health,'cooldown':3
                }
        enemies.append(enemy)
def show_target():
    pp=(ppp[0]-30,ppp[1]+80)
    screen.blit(target_image, pp)

# Initialize with one enemy
spawn_enemies(1)
def update_cooldown():
    for enemy in enemies:
        if enemy['boss']!=1:
            enemy['bullet_cooldown']-=30
def calculate_angle_and_velocity(start_pos, target_pos,size):
    sizex,sizey=size
    dx = target_pos[0]+25-sizex/2 - start_pos[0]
    dy = target_pos[1]+70-sizey- start_pos[1]
    x=target_pos[0]+25-sizex/2
    y=target_pos[1]+100-sizey
    g = GRAVITY
    best_angle_velocity = None
    best_angle = 0
    best_velocity = float('inf')  # 用最大值來初始比較

    # 儲存符合條件的解
    for angle in range(0, 90):
        for velocity in range(5, 50):
            rad_angle = math.radians(angle)
            velocity_x=-velocity*math.cos(rad_angle)
            velocity_y=-velocity*math.sin(rad_angle)
            
            time=dx/velocity_x
            predicted_x=start_pos[0]+velocity_x*time
            predicted_y=start_pos[1]+(velocity_y*time+1/2*g*time**2)
            if abs(predicted_x - x) < 5 and abs(predicted_y - y) < 5:
                    if velocity < best_velocity:
                        best_angle = angle
                        best_velocity = velocity
                        best_angle_velocity = (-velocity * math.cos(rad_angle), -velocity * math.sin(rad_angle))
            

    # 如果找到符合條件的組合，返回結果
    if best_angle_velocity:
        return best_angle_velocity
    else:
        
        return (random.uniform(-30,0), random.uniform(-30,30))
        

def player_shoot(start_pos, end_pos):
    global score
    dx = start_pos[0] - end_pos[0]
    dy = start_pos[1] - end_pos[1]
    angle = math.atan2(dy, dx)
    power = min(math.hypot(dx, dy) / 20, MAX_POWER)

    velocity_x = power * math.cos(angle)
    velocity_y = power * math.sin(angle)

    bullet = {
        'x': player_pos[0] ,
        'y': player_pos[1] ,
        'velocity_x': velocity_x, 
        'velocity_y': velocity_y,
        'lifetime': 200,'angle':angle
    }
    player_bullets.append(bullet)

def update_player_bullets():
    global score, enemies,enemy_count
    for bullet in player_bullets[:]:
        bullet['x'] += bullet['velocity_x']
        bullet['y'] += bullet['velocity_y']
        bullet['velocity_y'] +=(GRAVITY-res*bullet['velocity_y'])
        bullet['velocity_x']-=res*bullet['velocity_x']
        bullet['lifetime'] -= 1
    
        # 計算角度
        angle = math.degrees(-math.atan2(bullet['velocity_y'], bullet['velocity_x'])) - 90

        # 使用圖片來顯示矛
        rotated_spear = pygame.transform.rotate(spear_image, angle)
        rotated_rect = rotated_spear.get_rect(center=(bullet['x'], bullet['y']))
        spear_mask = pygame.mask.from_surface(rotated_spear)
        
        screen.blit(rotated_spear, rotated_rect)
        
        
        
        
        for enemy in enemies:
            enemy['mask'] = pygame.mask.from_surface(enemy['image'])
        
        bullets_to_remove = []
        for pbullet in player_bullets[:]:
            if (bullet['x'] > WIDTH or 
            pbullet['y'] > HEIGHT or 
            pbullet['lifetime'] <= 0):
                bullets_to_remove.append(pbullet)
                break  # Once you find a bullet that should be removed, stop checking further
            for enemy in enemies[:]:
                offset = (int(rotated_rect.left - enemy['pos'][0]), int(rotated_rect.top - enemy['pos'][1]))
                if enemy['mask'].overlap(spear_mask, offset):
                    enemy['health'] -= 100
                    bullets_to_remove.append(pbullet)  # Mark the bullet for removal
                    if enemy['health'] <= 0:
                        if enemy['boss']==1:
                            score+=500
                        else :score += 100
                        enemy_count-=1
                        enemies.remove(enemy)
                        update_cooldown()
                        

        for bullet in bullets_to_remove:
            if bullet in player_bullets:
                player_bullets.remove(bullet)
def enemy_shoot():
    global ppp
    for enemy in enemies:
        
        if enemy['bullet_timer'] <= 0:
                # 隨機選擇敵人子彈圖片和對應大小
                ppp=player_pos[:]
                if enemy['boss']==1:
                    bullet_image, bullet_size = enemy_bullet_images[0]
                    type=0
                    bullet_image = pygame.image.load(bullet_image)
                    bullet_image = pygame.transform.scale(bullet_image, bullet_size)
                else:
                    bullet_image, bullet_size = random.choice(enemy_bullet_images)
                    type=enemy_bullet_images.index((bullet_image,bullet_size))
                    bullet_image = pygame.image.load(bullet_image)
                    bullet_image = pygame.transform.scale(bullet_image, bullet_size)

                a=GRAVITY
                velocity_x, velocity_y = calculate_angle_and_velocity(enemy['pos'], player_pos,bullet_size
                )
                bullet = {
                    'x': enemy['pos'][0] , 
                    'y': enemy['pos'][1] ,
                    'velocity_x': velocity_x, 
                    'velocity_y': velocity_y,
                    'lifetime': 180,
                    'image': bullet_image, 
                    'size': bullet_size,'type':type,'a':a 
                }
                enemy['bullets'].append(bullet)
                enemy['bullet_timer'] = enemy['bullet_cooldown']
                if enemy['cooldown']>0:
                    enemy['cooldown']-=1
        else:
            enemy['bullet_timer']-=1
            if enemy['boss']==1 or game_stage>=3:
                    theta=random.uniform(0,2*math.pi)
                    if enemy['cooldown']==0:
                        for i in range(random.randint(100,300)):
                            if enemy['pos'][0] +1*math.cos(theta)<=WIDTH-70 and enemy['pos'][0] +1*math.cos(theta)>=WIDTH/2 \
                                and enemy['pos'][1]+1*math.sin(theta) <=HEIGHT-120 and  enemy['pos'][1]+ 1*math.cos(theta)>=0 :           
                                enemy['pos'][0]+=1*math.cos(theta)
                                enemy['pos'][1]+=1*math.sin(theta)
                        enemy['cooldown']=-random.randint(0,8)*(enemy['boss']-1)+2

            

def update_enemy_bullets():
    global player_health ,player_mask
    for enemy in enemies:
        for bullet in enemy['bullets'][:]:
            bullet['x'] += bullet['velocity_x']
            bullet['y'] += bullet['velocity_y']
            bullet['velocity_y'] += (bullet['a'])
            bullet['lifetime'] -= 1
            if (bullet['x'] < 0 or
                bullet['y'] > HEIGHT or 
                bullet['lifetime'] <= 0):
                enemy['bullets'].remove(bullet)
            else:show_target()
            offset = (int(bullet['x'] - player_pos[0]), int(bullet['y'] - player_pos[1]))
            if player_mask.overlap(enemy_bullet_mask[bullet['type']], offset):
                if bullet['type']==9 or bullet['type']==8 and player_health<1500:
                    for i in range(50):
                        if player_health==1500:
                            break
                        player_health+=1
                elif bullet['type']!=9 and bullet['type']!=8:
                    player_health -= 100
                enemy['bullets'].remove(bullet)

            screen.blit(bullet['image'], (bullet['x'], bullet['y']))
            

def draw_hud():
    score_text = font.render(f'Score: {score}', True, WHITE)
    health_text = font.render(f'Health: {player_health}', True, WHITE)
    stage_text = font.render(f'Stage: {game_stage}', True, WHITE)
    num_text = font.render(f'Enemy left: {enemy_count}', True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 50))
    screen.blit(stage_text, (10, 90))
    screen.blit(num_text, (10, 130))


    pygame.display.flip()
def update_game_stage():
    global game_stage, enemies
    for s in stage_score:
        if score >=s:
                phase=s
                game_stage=stage_score.index(phase)+1
        
def draw_centered_text(text, y_position, color=WHITE):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = WIDTH // 2 
    text_rect.y = y_position  

    # Blit the text to the screen
    screen.blit(text_surface, text_rect)

def draw_start_screen():
    screen.blit(background[0],(0,0))
    draw_centered_text("Press ENTER to Start",HEIGHT//2,WHITE)
    
    pygame.display.flip()
def reset_game():
    global player_pos, score, player_health, game_stage, enemies, sharks, player_mask, nshark,bubble_count
    # 重置遊戲狀態
    player_health = 1000
    score = 0
    player_pos = [100, HEIGHT // 2 - player_size[1] // 2]
    game_stage = 1
    enemies = []  # 清除所有敵人
    sharks = []  # 清除所有鯊魚
    nshark = 0  # 重置鯊魚數量
    player_mask = None  # 清除玩家的遮罩

    pygame.display.flip()
    
def main():
    global player_pos, score, player_health, game_stage,player_mask,enemies,game_started
    running = True
    drag_start_pos = None
    game_started= False
    end=0
    # Show start screen
      # Small delay to avoid flicker


    while running:
        
        while not game_started:
            draw_start_screen()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Press Enter to start the game
                        game_started = True
                    
            pygame.time.wait(100)
        global player_mask
        screen.blit(background[1],(0,0))
        
        player_speed = 5+game_stage*2
        if player_health <= 0:
            end=1
            enemies=[]
            screen.blit(background[2],(0,0))
            draw_centered_text('Game Over!', HEIGHT // 3, RED)
            draw_centered_text(f'YOU LOSE! Final Score: {score}', HEIGHT // 2 + 30, RED)
            draw_centered_text('PRESS "R" TO RESTART OR "ESC" TO LEAVE', HEIGHT // 2 + 60, RED)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running=False
            if keys[pygame.K_r]:
                game_started=False
                reset_game()
                end=0
            pygame.display.flip()
        if score >= 5000 and enemy_count==0:
            end=1
            enemies=[]
            screen.blit(background[3],(0,0))
            draw_centered_text('Congratulations!', HEIGHT // 3, WHITE)
            draw_centered_text(f'YOU WIN! Final Score: {score}', HEIGHT // 2 + 30, WHITE)
            draw_centered_text('PRESS "R" TO RESTART OR "ESC" TO LEAVE', HEIGHT // 2 + 60, WHITE)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running=False
            if keys[pygame.K_r]:
                game_started=False
                reset_game()
                end=0
                
            pygame.display.flip()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT or  (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drag_start_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP and drag_start_pos:
                drag_end_pos = pygame.mouse.get_pos()
                player_shoot(drag_start_pos, drag_end_pos)
                drag_start_pos = None
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos[1] -= player_speed
        if keys[pygame.K_s]:
            player_pos[1] += player_speed
        if keys[pygame.K_a]:
            player_pos[0] -= player_speed
        if keys[pygame.K_d]:
            player_pos[0] += player_speed
        
        player_pos[0] = max(0, min(player_pos[0], WIDTH // 2 - player_size[0]))
        player_pos[1] = max(0, min(player_pos[1], HEIGHT - player_size[1]))
        
        
        if end==0:
            update_game_stage()
            if not enemies and end==0:
                spawn_enemies(game_stage)
            if nshark<3:
                if random.randint(1,10)==4:
                    spawn_shark(nshark)
            update_shark()
            for shark in sharks:
                current_image = pygame.transform.scale(shark['image'], (shark['size'][0], shark['size'][1]))
                screen.blit(current_image, shark['pos'])
            enemy_shoot()
            update_player_bullets()
            update_enemy_bullets()
            draw_healthbar()
            if drag_start_pos:
                player_mask = pygame.mask.from_surface(player_drag)
                screen.blit(player_drag, player_pos)  # 顯示拖曳時的角色圖片
            else:
                player_mask = pygame.mask.from_surface(player_idle)
                screen.blit(player_idle, player_pos)
            
            
            
            for enemy in enemies:
                screen.blit(enemy['image'], enemy['pos'])
            draw_hud()
            
            
        
        
        

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

 

if __name__ == "__main__":
    main()

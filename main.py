from tempfile import SpooledTemporaryFile
import pygame
import random
import os #為了匯入圖片所加入的模組 只要是匯入圖片會用的路徑相關的觀念所以翹匯入os
'''bug討論區
1.為啥有時候pygame打不出來
2.匯入圖片以及相對路徑的問題
匯入的時候要注意以下問題
(1)圖片如果不是當作背景而是當作物件的時候 解析度太大可能會閃退  請去檢查圖片大小是否有問題
(2)名稱打錯 英打很容易會錯 
(3)含式有沒有少括號之類的東西
'''
#遊戲設定一定要寫在這邊，請一定養成好習慣
FPS = 60
BACK_GROUND_COLOR = (250,250,250)
STRAW_BERRY_COLOR = (255,0,0)
WIDTH = 500
HEIGHT = 600
INDIAN_RED = (205,92,92)
Berry_speedy_min = 1
appear_times = 8

pygame.init() #初始化遊戲
pygame.mixer.init()#初始化音效
screen = pygame.display.set_mode((WIDTH,HEIGHT)) #設定視窗大小
clock = pygame.time.Clock() #設定遊戲的FPS
pygame.display.set_caption("草莓好好吃") #設定視窗左上角顯示名稱
icon_image = pygame.image.load(os.path.join("img","save.png")).convert()
pygame.display.set_icon(icon_image)#把草莓圖標當作遊戲標示

#載入圖片
background_image = pygame.image.load(os.path.join("img","backgroundnew.png")).convert() #*******1.convert記得要括號 2.記得要有資料夾  3.檔名不要打錯
berry_image = pygame.image.load(os.path.join("img","berry.png")).convert()
cat_image = pygame.image.load(os.path.join("img","cat.png")).convert()
power_image ={}
power_image['save'] = pygame.image.load(os.path.join("img","save.png")).convert()
power_image['meat'] = pygame.image.load(os.path.join("img","meat.png")).convert()


#載入音樂
explo_sound = pygame.mixer.Sound(os.path.join("sound","bump.mp3"))#一般音效

pygame.mixer.music.load(os.path.join("sound","coffee_stains.mp3"))#匯入背景音樂 不用拿變數去存取
pygame.mixer.music.set_volume(0.7)#調整背景音樂


#設定sprite(關於)
font_name = os.path.join("font.ttf") #匯入分數顯示板需要的字體
def draw_text(surf,text,size,x,y):#參數為平面 訊息 字體大小 以及x跟y的位置為何
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text, True,INDIAN_RED) #True為反鋸齒是否開啟 開啟會讓自體必較圓滑一點
    text_rect = text_surface.get_rect() #定位
    text_rect.centerx = x #把傳進來的x定位
    text_rect.top = y #把傳進來的x定位
    surf.blit(text_surface,text_rect) #把這個平面創立起來 需要平面本體跟位置

def draw_health(surf,hp,x,y):
    if(hp<0):
        hp=0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,(255,0,0),fill_rect)
    pygame.draw.rect(surf,(255,255,255),outline_rect,2)

def draw_attack_remaining(surf,ar,x,y):
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (ar/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,(0,255,0),fill_rect)
    pygame.draw.rect(surf,(255,255,255),outline_rect,2)


def draw_init(): #畫一開始的進入遊戲畫面
    screen.blit(background_image,(0,0))#將匯入的圖片加入背景之中 參數為圖片變數名稱以及座標記得適用blit不是用fill
    draw_text(screen,"草莓好好吃",64,WIDTH/2,HEIGHT/4)
    draw_text(screen,"WSAD移動飛船 空白鍵發射子彈",22,WIDTH/2,HEIGHT/2)
    draw_text(screen,"紅色為生命條 綠色為彈藥量",22,WIDTH/2,HEIGHT/2+25)
    draw_text(screen,"按任意鍵開始遊戲 ",18,WIDTH/2,HEIGHT/4*3)
    pygame.display.update()
    waitng = True #等待按鍵按下
    while waitng:
        clock.tick(FPS) #一秒鐘之內能執行幾次，即FPS
    #取得輸入 變數event為一個列表
        for event in pygame.event.get(): #偵測使用者事件，若使用者選擇關閉遊戲，則設為false
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waitng = False
                return False
    
def record_score(txtdir,wstring):
    fobj = open(txtdir, 'a')
    fobj.writelines(wstring+"\n")
    fobj.close()

class Player(pygame.sprite.Sprite): #成立遊戲內物件
    def __init__(self):#這邊主要是在定義一歇腳色的屬性，數值
        pygame.sprite.Sprite. __init__(self) #前面這幾行幾乎都是固定設定 可以不用調他
        #self.image = pygame.Surface((50,40)) #若沒有圖片 這邊可以設定該物件的大小為何
        #self.image.fill((255,255,0))# 若沒有圖片 這邊可以設定該物件的顏色為何
        self.image = pygame.transform.scale(cat_image,(100,75)) #調整解析度大小 並將圖片插入
        self.image.set_colorkey((0,0,0))#把參數的顏色透明化 參數為RGB值
        
        self.rect = self.image.get_rect() #告訴程式說我們把圖片定位
        self.rect.center = ((WIDTH/2,HEIGHT-10)) #設定圖片的中心位置會在這個地方(此舉例圖片剛好是在整個介面的中間)
        self.speedx = 8 #設定角色在左右移動(X軸)的速度為8 
        self.speedy = 8
        self.radius = 30
        #pygame.draw.circle(self.image,(255,0,0),self.rect.center,self.radius) #觀測用 觀察判定大小是否符合
        #self.rect.dx = 200 
        #self.rect.y = 200
        #在py裡面往右x為正往下y為正，定位以左上角的點為基準
        #即圖片的最左上角做標會是200,200
        self.health = 100
        self.attack_remaining = 100
        self.gun = 1
        self.gun_time = 0
    
    def update(self):#當遊戲更新的時候會做的事情，理論上應該是頻率是跟FPS有關 但實際上我還沒測
        if self.gun > 1 and pygame.time.get_ticks() - self.gun_time > 5000: #5000g4j3aul32k7u4n 
            self.gun = 1

        key_pressed = pygame.key.get_pressed() #偵測鍵盤上的每一個按鍵有沒有被按，回傳是布林值
        if key_pressed[pygame.K_d]: #if 在這邊有一個偵測事件發生的作用
            self.rect.x+=2
        if key_pressed[pygame.K_a]: #if 在這邊有一個偵測事件發生的作用
            self.rect.x-=2

        #注意y軸再做調整的時候 跟我們平常的y軸不太一樣 要小心一點
        if key_pressed[pygame.K_w]: #if 在這邊有一個偵測事件發生的作用
            self.rect.y-=2
        if key_pressed[pygame.K_s]: #if 在這邊有一個偵測事件發生的作用
            self.rect.y+=2
        
        #下面幾行事在控制我們在按鍵操控的時候不要超出介面
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.top < 0:
            self.rect.top = 0
        
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        #self.rect.x += 2 #每偵把物件往右2單位
        if (self.rect.left > WIDTH):  #當物件的左邊超出介面的x座標(500)
            self.rect.right = 0          #讓物件重新從左邊出來

        self.attack_remaining+=0.3
        if self.attack_remaining > 100:
            self.attack_remaining = 100


    def shoot(self): 

        
        #當空白鍵被按下的時候，就跑這個方式 ********記得只要是方法裡面一訂要加self這個咚咚他才知道你在的物體是誰
        if self.gun==1 and self.attack_remaining >=10 :
            bullet = Bullet(self.rect.centerx,self.rect.centery)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.attack_remaining-=10
        elif self.gun >= 2 and self.attack_remaining >=10:
            bullet1 = Bullet(self.rect.left+15,self.rect.centery)
            bullet2 = Bullet(self.rect.right-15,self.rect.centery)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            bullets.add(bullet1)
            bullets.add(bullet2)
            self.attack_remaining-=10

    def doubleshoot(self):
        self.gun+=1
        self.gun_time = pygame.time.get_ticks()

class Strawberry(pygame.sprite.Sprite): #成立遊戲內物件
    def __init__(self):#這邊主要是在定義一些角色或物件的屬性，數值
        pygame.sprite.Sprite. __init__(self) #前面這幾行幾乎都是固定設定 可以不用調他
        #self.image = pygame.Surface((20,40)) #可以參考Player的地方
        #self.image.fill((255,0,0)) #可以參考Player的地方
        size = random.randrange(20,60)
        self.image_ori = pygame.transform.scale(berry_image,(size,size))
        self.image_ori.set_colorkey((0,0,0))#去背
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect() #告訴程式說我們把圖片定位
        self.rect.x = random.randrange(0,WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100 , -30 )
        self.speedy = random.randrange(Berry_speedy_min,10)
        self.speedx = random.randrange(-4,4)
        self.radius = size/2
        #pygame.draw.circle(self.image,(0,0,0),self.rect.center,self.radius) #觀測用 觀察判定大小是否符合
        self.total_degree = 0 #這個是要寫在屬性這邊 不是寫在下面旋轉的地方
        self.rot_degree = random.randrange(-3,3) #這個是要寫在屬性這邊 不是寫在下面旋轉的地方
    
    def rotate(self):#旋轉方法
        #整體概念 我們會把石頭的圖片分成兩種
        #第一種是原圖完全不會動的
        #第二種是要顯示出來的圖
        #我們就是將原圖旋轉之後 並把顯示圖設成此圖 
        #由於他是一禎偵測一次所以原圖轉的角度要增加，整個看起來才會有再轉的感覺
        #關於石頭的設定在最前面的地方
        #阿記得要update的地方也要加 他才會轉動更新
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori,self.total_degree)
        #重新定位旋轉過後的中心點 這邊的定位有點小看不懂
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center 


    
    def update(self):#當遊戲更新的時候會做的事情，理論上應該是頻率是跟FPS有關 但實際上我還沒測
        self.rotate()
        self.rect.y += self.speedy 
        self.rect.x += self.speedx

        if (self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0):
            self.rect.x = random.randrange(0,WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100 , -30 )
            self.speedy = random.randrange(1,10)
            self.speedx = random.randrange(-4,4)

class Bullet(pygame.sprite.Sprite): #成立遊戲內物件
    def __init__(self,x,y):#輸入參數，射出子彈的人當前所在的座標
        pygame.sprite.Sprite. __init__(self) #前面這幾行幾乎都是固定設定 可以不用調他
        self.image = pygame.Surface((10,20))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect() #告訴程式說我們把圖片定位
        self.rect.centerx = x #子彈射出的位置要跟角色有關聯 
        self.rect.centery = y
        self.speedy = -5
    
    def update(self):#當遊戲更新的時候會做的事情，理論上應該是頻率是跟FPS有關 但實際上我還沒測
        self.rect.y += self.speedy 

        if (self.rect.bottom < 0):
            self.kill()#這裡的刪除只會刪除當前物件，並不是所有跟這個依樣的物件全部刪除

class Power(pygame.sprite.Sprite): #成立遊戲內物件
    def __init__(self,center):#輸入參數，調出的寶物要在石頭毀掉的中間
        pygame.sprite.Sprite. __init__(self) #前面這幾行幾乎都是固定設定 可以不用調他
        self.type = random.choice(['meat','save'])
        self.image = power_image[self.type]
        self.image = pygame.transform.scale(power_image[self.type],(50,60))
        self.image.set_colorkey((255,255,255))
        self.image.set_colorkey((0,0,0))

        self.rect = self.image.get_rect() #告訴程式說我們把圖片定位
        self.rect.center = center #出現的位置要是參數書進來的center值 也就是石頭的值
        self.speedy = 3
    
    def update(self):#當遊戲更新的時候會做的事情，理論上應該是頻率是跟FPS有關 但實際上我還沒測
        self.rect.y += self.speedy 

        if (self.rect.top > HEIGHT):
            self.kill()#這裡的刪除只會刪除當前物件，並不是所有跟這個依樣的物件全部刪除



        

#創建sprite群組，放很多物件進去          
all_sprites = pygame.sprite.Group() #把所以得sprite物件塞到群組裡面
#若有不同種的兩類東西需要做判斷且同時有很多個，記得要把他們分成兩個群組
#例如子彈和石頭，子彈和石頭可能會有很多個，你只有一個的話她不會理你，所以需要分別創兩個群組，直接拿群組做判斷
strawberrys = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()
player = Player() #創建玩家物件            
all_sprites.add(player)#*********很重要 記得建完的東西要方進去sprites group裡面 不然他會完全不鳥你****
for i in range (appear_times):
    strawberry = Strawberry() #注意：如果這一個物件要同時出現八次 你一定是要在裡面創建物件才能讓它出現八個，畢竟你一定要給他setting
    all_sprites.add(strawberry)
    strawberrys.add(strawberry)

score = 0

if score>=500:
    for i in range (4):
        strawberry = Strawberry() #注意：如果這一個物件要同時出現八次 你一定是要在裡面創建物件才能讓它出現八個，畢竟你一定要給他setting
        all_sprites.add(strawberry)
        strawberrys.add(strawberry)
    Berry_speedy_min+=3
if score>=2000:
    for i in range (4):
        strawberry = Strawberry() #注意：如果這一個物件要同時出現八次 你一定是要在裡面創建物件才能讓它出現八個，畢竟你一定要給他setting
        all_sprites.add(strawberry)
        strawberrys.add(strawberry)
    Berry_speedy_min+=3


pygame.mixer.music.play(-1)#播放背景音樂 裡面的參數為要播放幾次 -1表時無線撥放


#寫遊戲迴圈 true表示遊戲會繼續運行 false表示遊戲會被關閉
show_init = True #一進入遊戲的遊戲畫面

running = True #是否繼續執行
while running:
    if show_init: #顯示初始畫面的便是為true 
        close = draw_init()
        if close:
            break
        show_init = False
        #創建sprite群組，放很多物件進去          
        all_sprites = pygame.sprite.Group() #把所以得sprite物件塞到群組裡面
        #若有不同種的兩類東西需要做判斷且同時有很多個，記得要把他們分成兩個群組
        #例如子彈和石頭，子彈和石頭可能會有很多個，你只有一個的話她不會理你，所以需要分別創兩個群組，直接拿群組做判斷
        strawberrys = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        background_image

        player = Player() #創建玩家物件            
        all_sprites.add(player)#*********很重要 記得建完的東西要方進去sprites group裡面 不然他會完全不鳥你****
        for i in range (appear_times):
            strawberry = Strawberry() #注意：如果這一個物件要同時出現八次 你一定是要在裡面創建物件才能讓它出現八個，畢竟你一定要給他setting
            all_sprites.add(strawberry)
            strawberrys.add(strawberry)
        score = 0
        


    clock.tick(FPS) #一秒鐘之內能執行幾次，即FPS
    #取得輸入 變數event為一個列表
    for event in pygame.event.get(): #偵測使用者事件，若使用者選擇關閉遊戲，則設為false
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()  #是要呼叫已形成的物件，所以季的是要用物件名叫，而不是用方法名叫
    #更新遊戲
    all_sprites.update()
    #把石頭射掉之後他會不見，但是他最多就是5個，我們在她被刪掉之後，我們要回去新增一個才行
    #下面這行小難 參數(群組一,群組二,碰撞後是否消失(有兩個))
    #回傳值會是一個字典列表
    #子彈 草莓相撞
    hits = pygame.sprite.groupcollide(strawberrys,bullets,True, True) #碰到
    for hit in hits: #這個寫法的原理未知 先這寫就對了 這裡面寫的是子彈碰到石頭會發生什麼事
        explo_sound.play()
        score += hit.radius
        strawberry = Strawberry()
        all_sprites.add(strawberry) #加入群組all 
        strawberrys.add(strawberry) #加入群組starwberry
        if random.random() > 0.9:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)

    #草莓 貓咪相撞
    hits = pygame.sprite.spritecollide(player,strawberrys,True,pygame.sprite.collide_circle) #這邊的方法是spritecollide 不是groupcollide
    #另外調整他的碰撞判定範圍 預設為方形 但我們這邊把他調圓形 除調整這邊 還要調整物件的的半徑大小(self.radius)
    #布林值代表石頭要不要刪掉 True為刪掉 False為不刪除
    for hit in hits: #如果hits發生 
        strawberry = Strawberry()
        all_sprites.add(strawberry) #加入群組all 
        strawberrys.add(strawberry) #加入群組starwberry
        player.health -= hit.radius
        if player.health <= 0:
            show_init = True
            record_score("history score",str(score)) #當沒血了之後 就重新回到一開始的畫面


    #寶物 貓咪相撞
    hits = pygame.sprite.spritecollide(player,powers,True)
    for hit in hits:
        if hit.type == 'save':
            player.health +=15
            if player.health > 100:
                player.health = 100
        elif hit.type == 'meat':
            player.doubleshoot()
    
    
    
    #畫面顯示
    screen.fill(BACK_GROUND_COLOR) #調色盤，RGB的形式，0-255 數字越大代表越重
    screen.blit(background_image,(0,0))#將匯入的圖片加入背景之中 參數為圖片變數名稱以及座標記得適用blit不是用fill
    all_sprites.draw(screen)     #把all sprite裡面的東西畫到遊戲介面裡面
    draw_text(screen,str(score),18,WIDTH/2,10)
    draw_health(screen,player.health,5,15)
    draw_attack_remaining(screen,player.attack_remaining,5,30)
    pygame.display.update()

pygame.quit()
        

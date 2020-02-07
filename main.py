import pygame
import random
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

win = pygame.display.set_mode((700, 700))

pygame.display.set_caption("Arcade")

backGround = pygame.image.load('Rick Morty BG 1.jpg')
gameFace = pygame.image.load('Rick Sanchez Game Face.png')
worriedFace = pygame.image.load('Rick Sanchez Worried Face.png')
monsterFace = pygame.image.load('Cromulon.png')
ammo = pygame.image.load('Pickle Rick.png')
charHit = pygame.image.load('Pick Hit Rick.png')
monsterHit = pygame.image.load('Warp.png')
gameOver = pygame.image.load('Game Over.png')
ammoSound = pygame.mixer.Sound("Wobble.wav")
monsterHitSound = pygame.mixer.Sound('Hit Monster.wav')
charHitSound = pygame.mixer.Sound('Game Over.wav')
#forTheDamagedCoda = pygame.mixer.Sound("For The Damaged Coda.wav")

#game attributes
runGame = True
displayStart = True
runLevel = True
playOnce = True
levelWon = True
level = 1
font = pygame.font.SysFont('comicsans', 30, True)

#character attributes
global vel_Char
global xPos_Char
global yPos_Char
def setChar():
    global vel_Char
    global xPos_Char
    global yPos_Char
    vel_Char = 19
    xPos_Char = 318
    yPos_Char = 313

#monster attributes
global xVel_Monsters
global yVel_Monsters
global xPos_Monsters
global yPos_Monsters
global monstersHit
global timerMonsterCreation
global timerMonsterMovement
global monstersCreated
global monstersAlive
global moveAvailable
global isHit
global whosHit
numberMonsters = 6
velocityMonsters = 6
monstersLeft = 6
def setMonsters(_numberMonsters, _velocityMonsters):
    global xVel_Monsters
    global yVel_Monsters
    global xPos_Monsters
    global yPos_Monsters
    global monstersHit
    global timerMonsterCreation
    global timerMonsterMovement
    global monstersCreated
    global monstersAlive
    global monstersLeft
    global moveAvailable
    global isHit
    global whosHit
    xVel_Monsters = []
    yVel_Monsters = []
    xPos_Monsters = []
    yPos_Monsters = []
    monstersHit = []
    for x in range(_numberMonsters):
        xVel_Monsters.append(_velocityMonsters)
        yVel_Monsters.append(_velocityMonsters)
        xPos_Monsters.append(0)
        yPos_Monsters.append(0)
        monstersHit.append(0)
    timerMonsterCreation = 65
    timerMonsterMovement = 0
    monstersCreated = 0
    monstersAlive = 0
    monstersLeft = numberMonsters
    moveAvailable = True
    isHit = 0
    whosHit = False

#ammo attributes
global vel_Ammo
global xPos_Ammo
global yPos_Ammo
global ammo_First
global ammo_Second
global noAmmo
def setAmmo():
    global vel_Ammo
    global xPos_Ammo
    global yPos_Ammo
    global ammo_First
    global ammo_Second
    global noAmmo
    vel_Ammo = 17
    xPos_Ammo = 0
    yPos_Ammo = 0
    ammo_First = False
    ammo_Second = False
    noAmmo = True

# display
def redrawGameWindow():
    global runLevel
    global playOnce
    global levelWon
    win.blit(backGround, (0,0))
    levelText = font.render('Level: ' + str(level), 1, (255, 255, 255))
    monstersText = font.render('Croms: ' + str(monstersLeft), 1, (255, 255, 255))
    win.blit(levelText, (583, 5))
    win.blit(monstersText, (570, 30))
    #main screen
    '''
    if displayStart:
        playText = font.render('Play ', 1, (255, 255, 255))
        exitText = font.render('Exit ', 1, (255, 255, 255))
        win.blit(playText, (300, 340))
        win.blit(exitText, (300, 360))
    el'''
    if runLevel:
        if levelWon:
            levelWon = False
            setChar()
            setMonsters(numberMonsters, velocityMonsters)
            setAmmo()
        if playOnce:
            #pygame.mixer.Sound.play(forTheDamagedCoda)
            playOnce = False
        redrawLevel(True)
    else:
        redrawLevel(False)
        win.blit(gameOver, (85, 190))
        keysOver = pygame.key.get_pressed()
        if keysOver[pygame.K_p]:
            runLevel = True
            setChar()
            setMonsters(numberMonsters, velocityMonsters)
            setAmmo()
            playOnce = True

    pygame.display.update()

def redrawLevel(notOver):
    global runGame
    global runLevel
    global xVel_Monsters
    global yVel_Monsters
    global timerMonsterCreation
    global timerMonsterMovement
    global monstersCreated
    global monstersAlive
    global monstersLeft
    global moveAvailable
    global isHit
    global whosHit
    global ammo_First
    global ammo_Second
    global yPos_Ammo
    global noAmmo
    global levelWon
    global numberMonsters
    global velocityMonsters
    global level

    # character display
    if xPos_Char < xPos_Ammo + 16 and xPos_Char + 64 > xPos_Ammo + 16 and yPos_Char < yPos_Ammo + 16 and yPos_Char + 64 > yPos_Ammo + 16 and ammo_Second:
        if notOver:
            pygame.mixer.Sound.stop(forTheDamagedCoda)
            pygame.mixer.Sound.play(charHitSound)
        win.blit(charHit, (xPos_Char - 43, yPos_Char - 43))
        runLevel = False
        notOver = False
    elif ammo_Second and notOver:
        win.blit(worriedFace, (xPos_Char, yPos_Char))
    elif notOver:
        win.blit(gameFace, (xPos_Char, yPos_Char))


# monster display
    if timerMonsterCreation == 66 and monstersCreated <= 5 and notOver:
            timerMonsterCreation = 0
            monstersCreated += 1
            monstersAlive += 1
    if monstersAlive > 0:
        for x in range(monstersAlive):
            if notOver:
                xPos_Monsters[x] += xVel_Monsters[x]
                yPos_Monsters[x] += yVel_Monsters[x]
                moveAvailable = True
            win.blit(monsterFace, (xPos_Monsters[x], yPos_Monsters[x]))
            #monster hits char
            if xPos_Monsters[x] < xPos_Char + 32 and xPos_Monsters[x] + 64 > xPos_Char + 32 and yPos_Monsters[x] < yPos_Char + 32 and yPos_Monsters[x] + 64 > yPos_Char + 32:
                if notOver:
                    pygame.mixer.Sound.stop(forTheDamagedCoda)
                    pygame.mixer.Sound.play(charHitSound)
                win.blit(charHit, (xPos_Char - 43, yPos_Char - 43))
                runLevel = False
                notOver = False

            #ammo hits monster
            if xPos_Monsters[x] < xPos_Ammo + 16 and xPos_Monsters[x] + 64 > xPos_Ammo + 16 and yPos_Monsters[x] < yPos_Ammo + 16 and yPos_Monsters[x] + 64 > yPos_Ammo + 16 and ammo_First and notOver:
                win.blit(monsterHit, (xPos_Monsters[x] - 18, yPos_Monsters[x] - 18))
                pygame.mixer.Sound.play(monsterHitSound)
                isHit = True
                whosHit = x
                ammo_First = False
                noAmmo = True
            if xPos_Monsters[x] < 0 or xPos_Monsters[x] > 636 and notOver:
                xVel_Monsters[x] *= -1
                moveAvailable = False
            if yPos_Monsters[x] < 0 or yPos_Monsters[x] > 636 and notOver:
                yVel_Monsters[x] *= -1
                moveAvailable = False
            if timerMonsterMovement % 50 == 0 and moveAvailable and notOver:
                xVel_Monsters[x] *= [-1, 1][random.randrange(2)]
                yVel_Monsters[x] *= [-1, 1][random.randrange(2)]
                timerMonsterMovement = 0
        if isHit:
            del xPos_Monsters[whosHit]
            del yPos_Monsters[whosHit]
            del xVel_Monsters[whosHit]
            del yVel_Monsters[whosHit]
            isHit = False
            monstersAlive -= 1
            monstersLeft -= 1

        if monstersLeft == 0:
            levelWon = True
            level += 1
            numberMonsters += 1
            velocityMonsters += 1

    # ammo display
    if notOver is False and ammo_Second:
        win.blit(ammo, (xPos_Ammo + 16, yPos_Ammo))
    if ammo_First and notOver:
        win.blit(ammo, (xPos_Ammo + 16, yPos_Ammo))
        yPos_Ammo -= vel_Ammo
        if yPos_Ammo < 17:
            ammo_First = False
            ammo_Second = True
    if ammo_Second and notOver:
        win.blit(ammo, (xPos_Ammo + 16, yPos_Ammo))
        yPos_Ammo += vel_Ammo
        if yPos_Ammo > 700:
            ammo_Second = False
            noAmmo = True


#Main Loop
while runGame:
    redrawGameWindow()
    pygame.time.delay(40)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runGame = False

    if runLevel:
        timerMonsterCreation += 1
        timerMonsterMovement += 1
        #key binding
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and xPos_Char > 0:
            xPos_Char -= vel_Char
        if keys[pygame.K_RIGHT] and xPos_Char < 636:
            xPos_Char += vel_Char
        if keys[pygame.K_UP] and yPos_Char > 0:
            yPos_Char -= vel_Char
        if keys[pygame.K_DOWN] and yPos_Char < 636:
            yPos_Char += vel_Char
        if keys[pygame.K_SPACE] and noAmmo:
            pygame.mixer.Sound.play(ammoSound)
            xPos_Ammo = xPos_Char
            yPos_Ammo = yPos_Char
            ammo_First = True
            noAmmo = False


pygame.quit()

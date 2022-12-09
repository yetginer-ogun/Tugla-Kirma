import random
from tkinter import CENTER
import numpy
import pygame

pygame.init()
ekran = pygame.display.set_mode()
e,b = pygame.display.get_surface().get_size()
#e,b = Ekranın eni-boyu

class Top(object):
    def __init__(self, ekran, yaricap, x, y):
        self.ekran = ekran
        self.yaricap = yaricap
        self.x = x
        self.y = y
        self.__xVel = 7
        self.__yVel = 2.5
        e,b = pygame.display.get_surface().get_size()
        self.en = e
        self.boy = b

    def getXVel(self):
        return self.__xVel

    def getYVel(self):
        return self.__yVel

    def draw(self):
        #Topu çizdirme
        pygame.draw.circle(ekran, (255,255,255), (self.x, self.y), self.yaricap) #Top rengi
    
    def update(self, cubuk, brickwall):
        #Topun hareketleri
        self.x += self.__xVel
        self.y += self.__yVel

        #Sola çarpma
        if self.x <= self.yaricap:
            self.__xVel *= -1

        #Sağa çarpma
        elif self.x >= (self.en - self.yaricap):
            self.__xVel *= -1

        #Tavana çarpma
        if self.y <= self.yaricap:
            self.__yVel *= -1

        #Yere düşme
        elif self.y >= (self.en - self.yaricap):
            return True
        
        if brickwall.carpisma(self):
            self.y *= -1

        cubukE = cubuk.en
        cubukB = cubuk.boy
        cubukX = cubuk.x
        cubukY = cubuk.y
        topX = self.x
        topY = self.y

        if ((topX + self.yaricap) >= cubukX and topX <= (cubukX + cubukE))\
            and ((topY + self.yaricap) >= cubukY and topY <= (cubukY + cubukB)):
            self.__yVel *= -1

        return False

class Cubuk(object):
    def __init__(self, ekran, en, boy, x, y):
        self.ekran = ekran
        self.en = en
        self.boy = boy
        self.x = x
        self.y = y
        e,b = pygame.display.get_surface().get_size()
        self._E = e
        self._B = b

    def draw(self):
        #Çubuk çizdirme
        pygame.draw.rect(ekran, (0, 255, 0), (self.x, self.y, self.en, self.boy), 0, 10)

    def update(self):
        # Çubuğun mouse ile hareketi
        x, y = pygame.mouse.get_pos()
        if x >= 0 and x <= (self._E - self.en):
            self.x = x

class Tugla(pygame.sprite.Sprite):
    def __init__(self, ekran, en, boy, x, y):
        self.ekran = ekran
        self.en = en
        self.boy = boy
        self.x = x
        self.y = y
        e,b = pygame.display.get_surface().get_size()
        self._E = e
        self._B = b
        self.durum = False

    def draw(self):
        #Tuğla çizdirme
        pygame.draw.rect(ekran, (random.randint(100, 255), random.randint(50, 250), random.randint(50, 250)), (self.x, self.y, self.en, self.boy), 0) #Tuğla renkleri

    def add(self, group):
        #Tuğlayı bir gruba atamak
        group.add(self)
        self.durum = True

    def remove(self, group):
        #Tuğlayı atandığı gruptan sil
        group.remove(self)
        self.durum = False

    def alive(self):
        #Tuğla durumu için True/False döndürür
        return self.durum

    def carpisma(self, top):
        #Top ve Tuğlanın çarpışma durumu
        tuglaX = self.x
        tuglaY = self.y
        tuglaE = self.en
        tuglaB = self.boy
        topX = top.x
        topY = top.y
        topXVel = top.getXVel()
        topYVel = top.getYVel()

        if ((topX + top.yaricap) >= tuglaX and (topX + top.yaricap) <= (tuglaX + tuglaY)) \
            and ((topY - top.yaricap) >= tuglaY and (topY - top.yaricap) <= (tuglaY + tuglaB)):
            return True

        else:
            return False

class TumTugla(pygame.sprite.Group):
    def __init__(self, ekran, x, y, en, boy):
        self.ekran = ekran
        self._x = x
        self._y = y
        self.en = en
        self.boy = boy
        self.tuglalar = []

        X = x
        Y = y

        for i in range(12):
            for j in range(25):
                self.tuglalar.append(Tugla(ekran, en, boy, X, Y))
                X += en + (en / 7)
            Y += boy + (boy / 7)
            X = x

    def add(self,tugla):
        self.tuglalar.append(tugla)

    def remove(self,tugla):
        self.tuglalar.remove(tugla)

    def draw(self):
        #Tüm tuğlaların çizimi
        for tugla in self.tuglalar:
            if tugla != None:
                tugla.draw()

    def update(self, top):
        #
        for i in range(len(self.tuglalar)):
            if ((self.tuglalar[i] != None) and self.tuglalar[i].carpisma(top)):
                self.tuglalar[i] = None

        for tugla in self.tuglalar:
            if tugla is None:
                self.tuglalar.remove(tugla)

    def Win(self):
        return len(self.tuglalar) == 0

    def carpisma(self, top):
        for tugla in self.tuglalar:
            if tugla.carpisma(top):
                return True
        return False

#Nesneler
top = Top(ekran, 9, random.randint(1,700), 400)
cubuk = Cubuk(ekran, 150, 10, 250, 880)
tum_tugla = TumTugla(ekran, 10, 10, 55.5, 25)

game_over = False
game_continue = True

skor = 0

pygame.display.set_caption("Tuğla Kırma Oyunu")

done = False
#Close buttona basınca oyunu kapatacak

clock = pygame.time.Clock()
pygame.font.init()

mgGameOver = pygame.font.SysFont("comicsans", 50)
mgWin = pygame.font.SysFont("comicsans", 50)
mgScore = pygame.font.SysFont("comicsans", 30)

textGameOver = mgGameOver.render("Kaybettin!", False, (255, 0, 0))
textWin = mgWin.render("Kazandın!", False, (0, 255, 0))
textScore = mgScore.render("skor: " + str(skor), False, (255, 255, 255))


#Program döngüsü
while not done:
    for event in  pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    ekran.fill("#1c1c1c")

    if game_continue:
        tum_tugla.draw()

        if tum_tugla.carpisma(top):
            skor += 10
        textScore = mgScore.render("skor: " + str(skor), False, (255, 255, 255))
        
        ekran.blit(textScore, (10, 850))

        tum_tugla.update(top)

        cubuk.draw()
        cubuk.update()

        if top.update(cubuk, tum_tugla):
            game_over = True
            game_continue = False

        if tum_tugla.Win():
            game_continue = False
        
        top.draw()

    #Oyun çalışmazsa
    else:
        if game_over:
            ekran.blit(textGameOver, ((e/2)-130, (b/2)-80))
            textScore = mgScore.render("skor: " + str(skor), False, (255, 255, 255))
            ekran.blit(textScore, ((e/2)-80, (b/2)))

        elif tum_tugla.Win():
            ekran.blit(textWin, ((e/2)-110, (b/2)-90))
            textScore = mgScore.render("skor: " + str(skor), False, (255, 255, 255))
            ekran.blit(textScore, ((e/2)-100, (b/2))) 

    pygame.display.flip()
    clock.tick(120)
pygame.quit()
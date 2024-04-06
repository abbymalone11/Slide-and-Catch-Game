#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 10:30:40 2024

@author: abbymalone
"""

import pygame, simpleGE, random

class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100, 100)
        self.fgColor = "black"
        self.clearBack = True
        
class LblTimer(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time: 5"
        self.center = (550, 100)
        self.fgColor = "black"
        self.clearBack = True

class Cherry(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Cherry.jpg")
        self.setSize(30, 30)
        self.reset()
        
        
    def reset(self):
        self.x = random.randint(0, self.scene.background.get_width())
        self.y = 20
        self.dy = random.randint(5, 15)
        
    def checkBounds(self):
        if self.bottom > self.scene.background.get_height():
            self.reset()

class Panda(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Panda.png")
        self.setSize(50, 50)
        self.position = (320, 400)
        
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= 5
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += 5

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 5
        self.setImage("Rainforest.jpg")
        self.sndCherry = simpleGE.Sound("coin.wav")
        self.numCoins = 10
        self.setCaption("Hungry Panda")
        self.lblScore = LblScore()
        self.lblTimer = LblTimer()
        self.panda = Panda(self)
        self.cherries = []
        for i in range(self.numCherries):
            self.cherries.append(Cherry(self))
        self.sprites = [self.lblScore, 
                        self.lblTimer,
                        self.panda,
                        self.cherries]
        
    def process(self):
        for cherry in self.cherries:
            if cherry.collidesWith(self.panda):
                cherry.reset()
                self.sndCherry.play()
                self.score += 100
                self.lblScore.text = f"Score: {self.score}"
                
       
        self.lblTimer.text = f"Time Left: {self.timer.getTimeLeft():2f}"
        if self.timer.getTimeLeft() < 0:
            print(f"Score: {self.score}")
            self.stop()

class Instructions(simpleGE.Scene):
    def __init__(self, prevScore):
        super().__init__()
        self.prevScore = prevScore
        self.lblScore.text = f"Last Score: {self.prevScore}"
        self.setImage("rainforest.jpg")
        self.response = "Quit"
        self.directions = simpleGE.MultiLabel()
        self.directions.textLines [
            "You are a Panda",
            "Move left and right with arrow keys",
            "Catch as many cherries as you can",
            "In the time provided"
            ""
            "Good Luck!"]
        self.direction.center = (320, 240)
        self.directions.size = (500, 250)
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play"
        self.btnPlay.center = (100, 400)
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (540, 400)
        self.lblScore = simpleGE.Label()
        self.lblScore.text = "Last score: 0"
        self.lblScore.center (320, 400)
        self.lblScore.text = f"Last score: {self.prevScore}"
        self.sprites = [self.directions,
                        self.btnPlay,
                        self.btnQuit,
                        self.lblScore]
        

    def process(self):
        if self.btnPlay.clicked:
            self.response = "Play"
            self.stop()
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()
            
    

class GameOver(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("Rainforest.jpg")
        self.lblScore = simpleGE.Label()
        self.lblScore.text = "Score: 0"
        self.lblScore.center = (320, 100)
        self.lblScore.fgColor = "white"
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "quit"
        self.btnQuit.center = (100, 240)
        
        self.btnAgain = simpleGE.Button()
        self.btnAgain.text = "play again"
        self.btnAgain.center = (450, 240)
        
        self.sprites = [self.lblScore, 
                        self.btnQuit, 
                        self.btnAgain]
        
    def setScore(self, score):
        self.score = score
        
    def process(self):
        self.lblScore.text = f"{self.score}"
        
        if self.btnQuit.clicked:
            self.next = "quit"
            self.stop()
        if self.btnAgain.clicked:
            self.next = "again"
            self.stop()
            
        
def main():
   
    keepGoing = True
    lastScore = 0
    while keepGoing:
        instructions = Instructions(lastScore)
        instructions.start()
        if instructions.response == "Play":
            game = Game()
            game.start()
            lastScore = game.score
            gameOver = GameOver()
            gameOver.setScore(game.score)
            gameOver.start()
        
        if gameOver.next == "quit":
            keepGoing = False
    
if __name__ == "__main__":
    main()
    
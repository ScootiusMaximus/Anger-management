import asyncio
import json
import pygame
import sys
import random

from game_files.sprites import *
from game_files.boxes import *
from game_files.camerashake import Camerashake
from game_files.settings import Settings
from game_files.particles import *
from game_files.sidebar import Sidebar

class Game:
    pygame.init()
    flags = pygame.RESIZABLE | pygame.SRCALPHA
    scrw = 1280
    scrh = 720
    FPS = 60
    screen = pygame.display.set_mode((scrw,scrh),flags=flags)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Anger management")

    def __init__(self):
        self.score = 0
        self.spawnrate = 1
        self.value = 1
        self.speed = 5
        self.last_spawn = 0
        self.autoclick = 0
        self.scene = "menu"
        self.upgrades = {}

        self.smashables = []
        self.particles = []
        self.keys_down = []
        self.keys_up = []

        self.camerashake = Camerashake()
        self.sidebar = Sidebar(self.screen)
        self.fist = Fist(self.screen,self.scrw*0.2,self.scrh*0.2)
        self.settings = Settings()

        for box in boxes:
            box.screen = self.screen

        reposition_boxes(self.scrw,self.scrh)
        self.load()

    def load(self):
        with open("game_files/upgrades.json","r") as file:
            self.upgrades = json.load(file)

    def spawn(self):
        if self.now() - self.last_spawn > 1000/self.spawnrate:
            self.last_spawn = self.now()
            which = random.randint(1,3)
            x = self.scrw * 0.9
            y = self.scrh * 0.9
            if which == 1:
                s = Clock(self.screen,x,y)
            elif which == 2:
                s = Apple(self.screen,x,y)
            else:
                s = Glass(self.screen,x,y)

            s.xvel = -self.speed
            self.smashables.append(s)

    def now(self):
        return pygame.time.get_ticks()

    def tick_smashables(self):
        for item in self.smashables:
            item.tick()
            if item.xpos < 0:
                item.needsDel = True

    def tick_particles(self):
        time = self.now()
        for item in self.particles.copy():
            item.tick(time)
            if item.needsDel:
                self.particles.remove(item)

    def tick_fist(self):
        if self.fist.pressed:
            self.fist.ypos = self.scrh*0.8
        else:
            self.fist.ypos = self.scrh*0.2

        fist = self.fist.get_rect()
        for item in self.smashables:
            if pygame.Rect.colliderect(item.get_rect(),fist):
                item.needsDel = True
                self.particles.append(
                    #Impact_Particle(self.screen, item.xpos, item.ypos, item.col, item.SCALE * 10, item.SCALE*4))
                    Impact_Bits(self.screen, item.xpos, item.ypos, item.col, item.SCALE*10, 30))

                self.score += self.value

    def draw_all(self):
        for item in self.smashables:
            item.draw()

        for item in self.particles:
            item.draw()

        self.fist.draw()

    def draw_sidebar(self):
        if self.sidebar.showing:
            self.sidebar.draw()

            try: value_colour = (100,0,0) if self.upgrades["cost"]["value"][self.upgrades["index"]["value"]] > self.score else (0,100,0)
            except IndexError: value_colour = (100,0,0)
            try: rate_colour = (100,0,0) if self.upgrades["cost"]["rate"][self.upgrades["index"]["rate"]] > self.score else (0,100,0)
            except IndexError: rate_colour = (100,0,0)
            try: speed_colour = (100,0,0) if self.upgrades["cost"]["speed"][self.upgrades["index"]["speed"]] > self.score else (0,100,0)
            except IndexError: speed_colour = (100,0,0)

            upgradevaluebox.set_textcol(value_colour)
            upgraderatebox.set_textcol(rate_colour)
            upgradespeedbox.set_textcol(speed_colour)

            for which in [valuebox,ratebox,speedbox,
                upgradevaluebox,upgraderatebox,upgradespeedbox,]:
                which.display()

    def update_upgrade_messages(self):
        valuebox.set_message(f"Value: {self.value}")
        ratebox.set_message(f"Rate: {self.spawnrate}")
        speedbox.set_message(f"Speed: {self.speed}")

        try: valuemsg = self.upgrades["cost"]["value"][self.upgrades["index"]["value"]]
        except IndexError: valuemsg = "max"
        try: ratemsg = self.upgrades["cost"]["rate"][self.upgrades["index"]["rate"]]
        except IndexError: ratemsg = "max"
        try: speedmsg = self.upgrades["cost"]["speed"][self.upgrades["index"]["speed"]]
        except IndexError: speedmsg = "max"

        upgradevaluebox.set_message(f"Upgrade cost: {valuemsg}")
        upgraderatebox.set_message(f"Upgrade cost: {ratemsg}")
        upgradespeedbox.set_message(f"Upgrade cost: {speedmsg}")

    def check_upgrades(self):
        upgradevaluebox.pressable = True
        upgraderatebox.pressable = True
        upgradespeedbox.pressable = True
        try:
            if upgradevaluebox.is_pressed() and self.score >= self.upgrades["cost"]["value"][self.upgrades["index"]["value"]]:
                self.score -= self.upgrades["cost"]["value"][self.upgrades["index"]["value"]]
                self.value += self.upgrades["next"]["value"][self.upgrades["index"]["value"]]
                self.upgrades["index"]["value"] += 1
        except IndexError: pass
        try:
            if upgraderatebox.is_pressed() and self.score >= self.upgrades["cost"]["rate"][self.upgrades["index"]["rate"]]:
                self.score -= self.upgrades["cost"]["rate"][self.upgrades["index"]["rate"]]
                self.spawnrate += self.upgrades["next"]["rate"][self.upgrades["index"]["rate"]]
                self.upgrades["index"]["rate"] += 1
        except IndexError: pass
        try:
            if upgradespeedbox.is_pressed() and self.score >= self.upgrades["cost"]["speed"][self.upgrades["index"]["speed"]]:
                self.score -= self.upgrades["cost"]["speed"][self.upgrades["index"]["speed"]]
                self.speed += self.upgrades["next"]["speed"][self.upgrades["index"]["speed"]]
                self.upgrades["index"]["speed"] += 1
        except IndexError: pass

    def apply_camerashake(self):
        frame = self.screen.copy()
        self.screen.fill(self.settings.bgcol)
        self.screen.blit(frame,self.camerashake.get())

    def run_textboxes(self):
        for box in boxes:
            if self.scene in box.tags:
                box.pressable = True
                box.display()
            else:
                box.pressable = False

        scorebox.set_message(f"Destruction: {self.score}")

        if playbox.is_hover():
            playbox.set_textcol((230,0,0))
        else:
            playbox.set_textcol((0, 0, 0))

        if self.sidebar.showing:
            togglesidebar.move_to((self.scrw*0.75,self.scrh*0.1))
            togglesidebar.set_message(">")
        else:
            togglesidebar.move_to((self.scrw*0.95,self.scrh*0.1))
            togglesidebar.set_message("<")

        if playbox.is_pressed():
            self.scene = "ingame"

        if togglesidebar.is_pressed():
            self.sidebar.showing = not self.sidebar.showing

    def show_debug(self):
        if self.settings.debug:
            debug.display()

    def go_to_menu(self):
        self.scene = "menu"
        upgradevaluebox.pressable = False
        upgraderatebox.pressable = False
        upgradespeedbox.pressable = False

    def quit(self):
        pygame.quit()
        sys.exit()

    def handle_events(self):
        self.keys_up.clear()
        self.keys_down.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.scene == "menu":
                        self.quit()
                    else:
                        self.go_to_menu()
                self.keys_down.append(event.key)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.keys_up.append(event.key)
            elif event.type == pygame.VIDEORESIZE:
                self.scrw = event.w
                self.scrh = event.h
                self.screen = pygame.display.set_mode((self.scrw,self.scrh),flags=self.flags)
                reposition_boxes(self.scrw, self.scrh)
                self.sidebar.resize(self.screen)

    def handle_keys(self):
        if self.scene == "ingame":
            if pygame.K_SPACE in self.keys_down:
                self.fist.pressed = True
                self.camerashake.set(10)

            if pygame.K_SPACE in self.keys_up:
                self.fist.pressed = False

        if pygame.K_F1 in self.keys_down:
            self.settings.debug = not self.settings.debug

    def cleanup(self):
        for item in self.smashables.copy():
            if item.needsDel:
                self.smashables.remove(item)

    async def start(self):
        while True:
            await asyncio.sleep(0)
            self.clock.tick(self.FPS)
            pygame.display.flip()
            self.screen.fill(self.settings.bgcol)

            debug.set_message(f"P: {len(self.particles)} T: {self.now()}")
            self.handle_events()
            self.handle_keys()
            self.run_textboxes()

            if self.scene == "ingame":
                self.cleanup()
                self.spawn()
                self.update_upgrade_messages()
                self.check_upgrades()
                self.tick_smashables()
                self.tick_particles()
                self.tick_fist()

                self.camerashake.tick()

                self.draw_all()
                self.draw_sidebar()

                self.apply_camerashake()

            self.show_debug()

the_game = Game()
asyncio.run(the_game.start())
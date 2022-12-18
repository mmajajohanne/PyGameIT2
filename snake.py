import pygame as pg
import sys
from random import randrange

vek2 = pg.math.Vector2


class Snake:
    def __init__(self, game):
        self.game = game
        self.size = game.RUTE_SIZE
        self.rect = pg.rect.Rect([0, 0, game.RUTE_SIZE - 2, game.RUTE_SIZE - 2])
        self.range = self.size // 2, self.game.VINDU_SIZE - self.size // 2, self.size
        self.rect.center = self.tilfeldig_pos()
        self.direction = vek2(0, 0)
        self.step_delay = 100  # millisekunder
        self.time = 0
        self.lengde = 1
        self.deler = []
        self.retninger = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1} #keys på tastaturet (w,s,d og a)
        
    def control(self, event): 
        if event.type == pg.KEYDOWN: #tester etter trykk på keyboardet og velger retning til slangen
            if event.key == pg.K_w and self.retninger[pg.K_w]:
                self.direction = vek2(0, -self.size)
                self.retninger = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}

            if event.key == pg.K_s and self.retninger[pg.K_s]:
                self.direction = vek2(0, self.size)
                self.retninger = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

            if event.key == pg.K_a and self.retninger[pg.K_a]:
                self.direction = vek2(-self.size, 0)
                self.retninger = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}

            if event.key == pg.K_d and self.retninger[pg.K_d]:
                self.direction = vek2(self.size, 0)
                self.retninger = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}

    def delta_tid(self): #teller tid
        tid_nå = pg.time.get_ticks()
        if tid_nå - self.time > self.step_delay:
            self.time = tid_nå
            return True
        return False

    def tilfeldig_pos(self): #velger en tilfeldig posisjon for slangen
        return [randrange(*self.range), randrange(*self.range)]

    def check_borders(self): #tester om slangen er utenfor vinduet
        if self.rect.left < 0 or self.rect.right > self.game.VINDU_SIZE:
            self.game.nytt_spill()
        if self.rect.top < 0 or self.rect.bottom > self.game.VINDU_SIZE:
            self.game.nytt_spill()

    def check_mat(self): #hvis slangen spiser maten blir den en rute lengre
        if self.rect.center == self.game.mat.rect.center:
            self.game.mat.rect.center = self.tilfeldig_pos()
            self.lengde += 1

    def check_treffselv(self): #hvis slangen treffer seg selv blir det nytt spill
        if len(self.deler) != len(set(segment.center for segment in self.deler)):
            self.game.nytt_spill()

    def move(self): #bevegelsen
        if self.delta_tid():
            self.rect.move_ip(self.direction)
            self.deler.append(self.rect.copy())
            self.deler = self.deler[-self.lengde:]

    def update(self): #oppdaterer testene
        self.check_treffselv()
        self.check_borders()
        self.check_mat()
        self.move()

    def draw(self): #tegner slangen
        [pg.draw.rect(self.game.screen, 'green', segment) for segment in self.deler]


class mat:
    def __init__(self, game):
        self.game = game
        self.size = game.RUTE_SIZE
        self.rect = pg.rect.Rect([0, 0, game.RUTE_SIZE - 2, game.RUTE_SIZE - 2])
        self.rect.center = self.game.snake.tilfeldig_pos()

    def draw(self):
        pg.draw.rect(self.game.screen, 'red', self.rect)


class Game:
    def __init__(self):
        pg.init()
        self.VINDU_SIZE = 1000
        self.RUTE_SIZE = 50
        self.screen = pg.display.set_mode([self.VINDU_SIZE] * 2)
        self.clock = pg.time.Clock()
        self.nytt_spill()

    def tegn_grid(self): #funksjon som tegner rutenett
        [pg.draw.line(self.screen, [50] * 3, (x, 0), (x, self.VINDU_SIZE))
                                             for x in range(0, self.VINDU_SIZE, self.RUTE_SIZE)]
        [pg.draw.line(self.screen, [50] * 3, (0, y), (self.VINDU_SIZE, y))
                                             for y in range(0, self.VINDU_SIZE, self.RUTE_SIZE)]

    def nytt_spill(self):
        self.snake = Snake(self)
        self.mat = mat(self)

    def update(self):
        self.snake.update()
        pg.display.flip() #oppdaterer innholdet i hele vinduet
        self.clock.tick(60)

    def draw(self): #tegner vinduet
        self.screen.fill('black')
        self.tegn_grid()
        self.mat.draw()
        self.snake.draw()

    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # snake kontroll
            self.snake.control(event)

    def run(self):
        while True:
            self.check_event()
            self.update()
            self.draw()


game = Game()
game.run()
import pygame
import random
import math
import sys
from os import path

# 初始化Pygame
pygame.init()
pygame.mixer.init()

# 游戏常量
WIDTH, HEIGHT = 800, 600
FPS = 60
DUCK_SPAWN_TIME = 1500
GAME_DURATION = 30000

# 颜色定义
BLUE_SKY = (135, 206, 235)
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)


class Duck(pygame.sprite.Sprite):
    def __init__(self, assets_dir):
        super().__init__()
        try:
            self.images = [
                pygame.image.load(path.join(assets_dir, 'duck1.png')).convert_alpha(),
                pygame.image.load(path.join(assets_dir, 'duck2.png')).convert_alpha(),
                pygame.image.load(path.join(assets_dir, 'duck3.png')).convert_alpha()
            ]
        except Exception as e:
            print(f"资源加载错误: {str(e)}，使用替代图形")
            self.images = self.create_dummy_animation()

        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.reset_position()
        self.animation_speed = 200
        self.last_frame = pygame.time.get_ticks()

    def create_dummy_animation(self):
        """生成黄色鸭子替代动画"""
        frames = []
        for i in range(3):
            surf = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 200 + i * 20, 0), (25, 25), 20)
            frames.append(surf)
        return frames

    def reset_position(self):
        self.rect.center = (random.randint(50, WIDTH - 50), HEIGHT + 50)
        self.speed = random.randint(5, 8)
        self.start_x = self.rect.x
        self.amplitude = random.randint(20, 40)
        self.direction = random.choice([-1, 1])
        self.last_update = pygame.time.get_ticks()

    def update(self):
        # 波动飞行路径
        now = pygame.time.get_ticks()
        self.rect.y -= self.speed
        self.rect.x = self.start_x + self.amplitude * math.sin(now * 0.005) * self.direction

        # 动画帧更新
        if now - self.last_frame > self.animation_speed:
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]
            self.last_frame = now


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("鸭子射击游戏")
        self.assets_dir = self.get_assets_path()
        self.init_resources()
        self.reset()
        pygame.mouse.set_visible(False)

    def get_assets_path(self):
        base_dirs = [
            path.dirname(__file__),
            path.join(path.dirname(__file__), '..'),
            path.dirname(sys.argv[0])
        ]
        for d in base_dirs:
            assets_path = path.join(d, 'assets')
            if path.exists(assets_path):
                return assets_path
        return path.dirname(__file__)

    def init_resources(self):
        try:
            self.background = pygame.transform.scale(
                pygame.image.load(path.join(self.assets_dir, 'background.jpg')).convert(),
                (WIDTH, HEIGHT)
            )
        except Exception as e:
            print(f"背景加载错误: {str(e)}，使用默认背景")
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill(BLUE_SKY)
            # 绘制简单草地
            pygame.draw.rect(self.background, BROWN, (0, HEIGHT - 80, WIDTH, 80))

        try:
            self.crosshair = pygame.image.load(path.join(self.assets_dir, 'crosshair.png')).convert_alpha()
        except:
            self.crosshair = self.create_simple_crosshair()

        self.gun_sound = pygame.mixer.Sound(path.join(self.assets_dir, 'gunshot.wav')) if path.exists(
            path.join(self.assets_dir, 'gunshot.wav')) else None

    def create_simple_crosshair(self):
        surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.line(surf, (255, 0, 0), (16, 0), (16, 32), 2)
        pygame.draw.line(surf, (255, 0, 0), (0, 16), (32, 16), 2)
        return surf

    def reset(self):
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.ducks = pygame.sprite.Group()
        self.last_spawn = pygame.time.get_ticks()
        self.playing = True

    def run(self):
        clock = pygame.time.Clock()
        while self.playing:
            clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.gun_sound:
                    self.gun_sound.play()
                self.check_hits()

    def check_hits(self):
        mouse_pos = pygame.mouse.get_pos()
        for duck in self.ducks:
            if duck.rect.collidepoint(mouse_pos):
                self.score += 10
                duck.kill()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_spawn > DUCK_SPAWN_TIME:
            self.ducks.add(Duck(self.assets_dir))
            self.last_spawn = now

        self.ducks.update()

        # 检查游戏时间
        if pygame.time.get_ticks() - self.start_time > GAME_DURATION:
            self.playing = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.ducks.draw(self.screen)
        # 绘制准星
        mouse_pos = pygame.mouse.get_pos()
        self.screen.blit(self.crosshair, (mouse_pos[0] - 16, mouse_pos[1] - 16))
        # 绘制分数
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(text, (10, 10))
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
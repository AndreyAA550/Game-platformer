from hazards import Obstacle
from src.platforms import Platform, DisappearingPlatform, FinishPlatform


class Level:
    def __init__(self, width, time_left, start_x, start_y, gravity, low_gravity, platforms, finish_platform, ground, obstacles):
        self.width = width
        self.time_left = time_left
        self.start_x = start_x
        self.start_y = start_y
        self.gravity = gravity
        self.low_gravity = low_gravity
        self.platforms = platforms
        self.finish_platform = finish_platform
        self.ground = ground
        self.obstacles = obstacles

levels = [
    Level(
        width = 8000,
        time_left = 40,
        start_x = 100,
        start_y = 100,
        gravity = 0.55,
        low_gravity = 0.34,
        platforms = [
            Platform(600, 450, 120, 10),
            Platform(850, 350, 120, 10),
            DisappearingPlatform(1010, 240, 120, 10),
            DisappearingPlatform(1260, 400, 120, 10),
            DisappearingPlatform(1480, 230, 120, 10),
            Platform(1740, 300, 120, 10),
            Platform(1940, 360, 120, 10),
            Platform(2350 , 580, 150, 10),
            Platform(2630 , 470, 120, 10),
            Platform(2860, 350, 120, 10),
            Platform(3100, 280, 120, 10),
            Platform(3400, 200, 120, 10),
            Platform(3650, 350, 120, 10),
            Platform(3990, 200, 120, 10),
            Platform(4190, 310, 120, 10),
            Platform(4480, 420, 120, 10),
            Platform(4780, 250, 120, 10),
            Platform(5020, 100, 120, 10),
            Platform(5280, 300, 120, 10),
            Platform(5700, 270, 120, 10),
            Platform(6120, 550, 210, 10),
            Platform(6480, 360, 120, 10),
            Platform(6750, 200, 120, 10),
            Platform(7090, 270, 120, 10),
            Platform(7090, 270, 120, 10),
            Platform(7090, 270, 120, 10),
            Platform(7490, 400, 120, 10),
        ],
        finish_platform = FinishPlatform(7860, 450, 140, 10),
        ground = [
            Platform(0, 550, 600, 50),
            Platform(-50, 0, 55, 600),
            Platform(8000, 0, 50, 600),
            Platform(20, -30, 13000, 10 ),
        ],
        obstacles = [
            Obstacle(420, 350, 100, 10),
            Obstacle(1600, 150, 100, 10),
            Obstacle(600, 700, 12400, 10),
            Obstacle(2270, 350, 10, 120),
            Obstacle(3820, 270, 10, 120),
            Obstacle(600, 700, 3400, 10),
            Obstacle(5480, 250, 10, 100),
            Obstacle(5980, 130, 10, 100),
        ]
    ),
    Level(
        width = 13000,
        time_left = 20,
        start_x = 100,
        start_y = 100,
        gravity = 0.55,
        low_gravity = 0.34,
        platforms = [
            Platform(600, 550, 120, 10),
            Platform(850, 350, 50, 10),
            Platform(1000, 240, 120, 10),
            Platform(1260, 400, 120, 10),
            Platform(1580, 230, 120, 10),
            Platform(1840, 500, 120, 10),
            Platform(2040, 380, 50, 10),
            Platform(2270, 190, 120, 10),
            Platform(2400, 500, 120, 10),

        ],
        finish_platform = FinishPlatform(12860, 450, 140, 10),
        ground = [
            Platform(0, 550, 600, 50),
            Platform(-50, 0, 55, 600),
            Platform(13000, 0, 50, 600),
            Platform(0, -30, 13000, 10 ),
        ],
        obstacles = [
            Obstacle(420, 350, 100, 10),
            Obstacle(1600, 130, 100, 10),
            Obstacle(0, 700, 2000, 10),
            Obstacle(600, 700, 13000, 10),
            Obstacle(2370, 300, 10, 120),
        ]
    )
]

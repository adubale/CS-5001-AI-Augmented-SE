import random
import time
from typing import List, Tuple


class Snake:
    def __init__(self, screenWidth: int, screenHeight: int, blockSize: int,
                 foodPosition: Tuple[int, int]):
        self.length: int = 1
        self.SCREEN_WIDTH: int = screenWidth
        self.SCREEN_HEIGHT: int = screenHeight
        self.BLOCK_SIZE: int = blockSize
        self.score: int = 0
        self.food_position: Tuple[int, int] = foodPosition
        self.positions: List[Tuple[int, int]] = [
            (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
        ]

    def move(self, direction: Tuple[int, int]) -> None:
        cur = self.positions[0]
        x, y = direction

        newPos = (
            (cur[0] + x * self.BLOCK_SIZE) % self.SCREEN_WIDTH,
            (cur[1] + y * self.BLOCK_SIZE) % self.SCREEN_HEIGHT,
        )

        if newPos == self.food_position:
            self.eat_food()

        if len(self.positions) > 2 and newPos in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, newPos)
            if len(self.positions) > self.length:
                self.positions.pop()

    def random_food_position(self) -> None:
        random.seed(int(time.time()))
        while True:
            self.food_position = (
                (random.randint(0, (self.SCREEN_WIDTH // self.BLOCK_SIZE) - 1)
                 * self.BLOCK_SIZE),
                (random.randint(0, (self.SCREEN_HEIGHT // self.BLOCK_SIZE) - 1)
                 * self.BLOCK_SIZE),
            )
            if self.food_position not in self.positions:
                break

    def reset(self) -> None:
        self.length = 1
        self.positions = [(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)]
        self.score = 0
        self.random_food_position()

    def eat_food(self) -> None:
        self.length += 1
        self.score += 100
        self.random_food_position()

    def get_length(self) -> int:
        return self.length

    def get_positions(self) -> List[Tuple[int, int]]:
        return self.positions.copy()

    def get_score(self) -> int:
        return self.score

    def get_food_position(self) -> Tuple[int, int]:
        return self.food_position

    def get_SCREEN_WIDTH(self) -> int:
        return self.SCREEN_WIDTH

    def get_SCREEN_HEIGHT(self) -> int:
        return self.SCREEN_HEIGHT

    def get_BLOCK_SIZE(self) -> int:
        return self.BLOCK_SIZE

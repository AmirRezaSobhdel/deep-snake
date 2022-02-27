import sys
from os import system

import numpy as np
import random
import time
import math
from enum import Enum


class Direction(Enum):
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3


playground_dims = (100, 100)
head_vision_radius = 4


def print_playground(playground_matrix):
    for i in range(0, playground_dims[0]):
        for j in range(0, playground_dims[1]):
            if playground_matrix[i][j] == 0:
                print('.      ', end='')
            elif playground_matrix[i][j] == 2:
                print('$      ', end='')
            else:
                print('@      ', end='')
        print('')


class Snake:

    def __init__(self):
        self.is_alive = True
        self.playground_matrix = np.zeros((playground_dims[0],playground_dims[1]))
        # randomly select the coordinates of the head
        self.head = (random.randint(0, playground_dims[0]-1), random.randint(0, playground_dims[1]-1))
        self.playground_matrix[self.head[0]][self.head[1]] = 1
        self.current_direction = None
        self.body = list()
        self.body.append(self.head)
        self.fruit = self.__select_random_coordinates_for_fruit(initial=True)

    def __select_random_coordinates_for_fruit(self, initial=False):

        # if initial is False:
        #     self.playground_matrix[self.fruit[0]][self.fruit[1]] = 0

        # avoid fruit coordinates and body overlap
        while True:
            fruit_x = random.randint(0, playground_dims[0] - 1)
            fruit_y = random.randint(0, playground_dims[1] - 1)
            has_conflict = False
            for body_part in self.body:
                if body_part == (fruit_x, fruit_y):
                    has_conflict = True
                    break
            if has_conflict:
                continue
            coordinates = (fruit_x, fruit_y)
            self.playground_matrix[fruit_x][fruit_y] = 2
            return coordinates

    def __calculate_award(self, previous_head):

        x_prev_head = previous_head[0]
        y_prev_head = previous_head[1]

        x_head = self.head[0]
        y_head = self.head[1]
        x_fruit = self.fruit[0]
        y_fruit = self.fruit[1]

        # ate the fruit
        if x_head == x_fruit and y_head == y_fruit:
            self.fruit = self.__select_random_coordinates_for_fruit()
            return 100
        # one block distant from the fruit
        if (math.fabs(x_head - x_fruit) == 1 and math.fabs(y_head - y_fruit) == 0) or (math.fabs(x_head - x_fruit) == 0 and math.fabs(y_head - y_fruit) == 1):
            return 5
        # gets one block away from the fruit
        if (math.fabs(x_head - x_fruit) + math.fabs(y_head - y_fruit)) > (math.fabs(x_prev_head - x_fruit) + math.fabs(y_prev_head - y_fruit)):
            return -1
        # gets one block closer to the fruit
        if (math.fabs(x_head - x_fruit) + math.fabs(y_head - y_fruit)) < (math.fabs(x_prev_head - x_fruit) + math.fabs(y_prev_head - y_fruit)):
            return 1

    def __get_visible_environment(self):
        start_index_coordinates = \
            ((self.head[0] - head_vision_radius) % playground_dims[0],
             (self.head[1] - head_vision_radius) % playground_dims[1])

        vision_matrix_square_height = head_vision_radius * 2 + 1

        vision_matrix = np.zeros((vision_matrix_square_height, vision_matrix_square_height))
        for i in range(0, vision_matrix_square_height):
            for j in range(0, vision_matrix_square_height):
                vision_matrix[i][j] = self.playground_matrix \
                [(start_index_coordinates[0] + i) % playground_dims[0]] \
                [(start_index_coordinates[1] + j) % playground_dims[1]]
        return vision_matrix

    def __update_matrix(self):

        x_head = self.head[0]
        y_head = self.head[1]
        x_fruit = self.fruit[0]
        y_fruit = self.fruit[1]

        # die if head hit its body
        for body_part in self.body:
            if self.head == body_part and len(self.body) > 1:  # has hit itself
                self.is_alive = False
                print("DEAD!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                sys.exit()

        # shift the body one block
        self.body.append(self.head)
        self.playground_matrix[self.head[0]][self.head[1]] = 1

        if self.head == self.fruit:
            pass
        else:
            erased_tail = self.body.pop(0)
            self.playground_matrix[erased_tail[0]][erased_tail[1]] = 0

    def move(self, direction):

        self.current_direction = direction

        prev_x = self.head[0]
        prev_y = self.head[1]

        # new head
        if direction == Direction.UP:
            self.head = (prev_x, (prev_y+1) % playground_dims[1])
        elif direction == Direction.DOWN:
            self.head = (prev_x, (prev_y - 1) % playground_dims[1])
        elif direction == Direction.RIGHT:
            self.head = ((prev_x + 1) % playground_dims[0], prev_y)
        elif direction == Direction.LEFT:
            self.head = ((prev_x - 1) % playground_dims[0], prev_y)

        self.__update_matrix()
        return self.__get_visible_environment(), self.__calculate_award((prev_x, prev_y))

    def __is_invalid_direction(self, direction):

        if self.current_direction is None:
            return False

        if direction == Direction.UP:
            if self.current_direction == Direction.DOWN:
                return True
        elif direction == Direction.DOWN:
            if self.current_direction == Direction.UP:
                return True
        elif direction == Direction.RIGHT:
            if self.current_direction == Direction.LEFT:
                return True
        elif direction == Direction.LEFT:
            if self.current_direction == Direction.RIGHT:
                return True

    def start_random_movement(self):
        while True:

            movement_direction = Direction(random.randint(0, 3))

            if self.__is_invalid_direction(movement_direction):
                continue

            print('action : ', movement_direction)
            state, reward = self.move(movement_direction)
            print('state : \n', state)
            print('reward : ', reward)

            print("############################################################################################3")
            time.sleep(0.5)


if __name__ == "__main__":
    snake = Snake()
    snake.start_random_movement()

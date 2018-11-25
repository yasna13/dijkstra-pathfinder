#!/usr/bin/env python

import sys, queue

OBSTACLE = '*'
ROBOT = 'R'
GOAL = 'X'

class Position(object):
    def __init__(self, x: int, y: int):
      self.x = x
      self.y = y
      self.priority = 0

    def __eq__(self, other):
      return self.x == other.x and self.y == other.y

    def __str__(self):
      return f"({self.x}, {self.y})"
    
    # Position should implement this, so that Position objects can be used as dict keys
    def __hash__(self):
      return hash((self.x, self.y))

    # Position should implement this, so that the Priority Queue can sort
    def __lt__(self, other):
      return self.priority < other.priority

class Move:
  @staticmethod
  def get_move_cost(start: Position, end: Position):
    if abs(start.x - end.x) > 0 and abs(start.y - end.y) > 0:
      return 10
    if abs(start.x - end.x) > 0:
      return 6
    if abs(start.y - end.y) > 0:
      return 5

class Pathfinder:
  def __init__(self, matrix):
    self.matrix = matrix
    self.matrix_width = len(matrix)
    self.matrix_height = len(matrix[0])
    # priority queue orders objects (Position) if they have a property "priority" and 
    # an overridden method __lt__ for comparing priorities
    self.frontier = queue.PriorityQueue()
    # array with the current costs for reaching a position from the init position  
    self.current_costs = {}
    self.find_robot_and_goal()
    self.init_priority_queue_and_costs()

  def find_robot_and_goal(self):
     for i in range(self.matrix_width):
      for j in range(self.matrix_height):
        print(i,j)
        if self.matrix[i][j] == ROBOT:
          self.robot = Position(i,j)
        if self.matrix[i][j] == GOAL:
          self.goal = Position(i,j)
  
  def init_priority_queue_and_costs(self):
      self.frontier.put(self.robot)
      self.current_costs[self.robot] = 0

  def get_frontier(self, currentPosition: Position):
    x = currentPosition.x
    y = currentPosition.y
    # all theoretically possible moves
    possible_moves = [(x-1, y), (x, y-1), (x-1, y-1), (x+1, y), (x, y+1), (x+1, y+1), (x-1, y+1), (x+1, y-1)]
    # filter out the moves leading outside of the field and remove the moves leading to rocks
    return [Position(x,y) for (x,y) in possible_moves if self.is_field_reachable(x, y)]

  def is_field_reachable(self, x, y):
    is_inside_matrix = x >= 0 and y >=0 and x < self.matrix_width and y < self.matrix_height
    if is_inside_matrix:
      is_free = self.matrix[x][y] != OBSTACLE
    return is_inside_matrix and is_free

  def start(self):
    while not self.frontier.empty():
      # get the next lowest cost position
      current = self.frontier.get()
      print(f"Robot is at {current}")

      if current == self.goal:
        print("reached goal", current, self.current_costs[current])
        return 
      # "visit" all possible neighbours and update their lowest cost
      for next in self.get_frontier(current):
        new_cost = self.current_costs[current] + Move.get_move_cost(current, next)
        # update costs for a position if it has not been visited
        # or if the new costs are smaller than the previously calculated costs for this position
        if next not in self.current_costs or new_cost < self.current_costs[next]:
          if next in self.current_costs: print("key there",self.current_costs[next])
          self.current_costs[next] = new_cost
         # print(current_costs[next])
          next.priority = new_cost
          self.frontier.put(next)
          
    print("No path found!")

def read_and_matrisize(file):
    contents = open(file).read()
    # split where there is a new line and remove the unneeded last new line
    return [line.split() for line in contents.split('\n')[:-1]][:-1]

pathfinder = Pathfinder(read_and_matrisize(sys.argv[1]))
pathfinder.start()

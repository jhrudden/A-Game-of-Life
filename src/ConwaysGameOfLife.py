import pygame 
import numpy as np
import random


class GameOfLife:
	def __init__(self, dimensions = 200, game_size = 1000, max_fps = 20):
		self.cols = dimensions
		self.rows = dimensions
		self.game_size = game_size
		self.cell = game_size / dimensions
		self.grids = self.init_grids()
		self.active_grid = self.init_active_grid(self.grids[0])
		self.inactive_grid = self.grids[1]
		self.dead_color = (0,0,0)
		self.alive_color = (83,195,70)


		self.scene = pygame.display.set_mode((self.game_size, self.game_size))
		self.clear_screen()
		pygame.display.flip()


		self.game_state = True

		self.max_fps = max_fps


	def init_grids(self):
		# initializes a 2d array that represents both the active 
		# and inactive boards
		grids = []

		# intialize a single grid
		grid = []

		# iterate down the number of rows
		for i in range(self.rows):
			# initialize row array
			row = []
			# iterate through the number of columns
			for j in range(self.cols):
				# append a 0 to row array per column
				row.append(0)

			# once a row has been finished apppend it to 
			# the initialized grid
			grid.append(row)


		# append 2 2d arrays to our grids inorder to form our final
		# initialized grid repsenting both the active and passive grid
		grids.append(grid)
		grids.append(grid)

		return grids

	def init_active_grid(self, grid):
		# go down the active grid and do a random choice between 1 or 0 and set cell to that value
		for i in range (self.rows):
			for j in range (self.cols):
				# for each index in each col in each row choose either 1 or 0
				grid[i][j] = random.choice([1,0])
		return grid

	def update_grid(self):
		# set the current active to inactive
		# iterate through inactive grid and check if for each cell it should die or come alive
		# then update corresponding item in the active grid

		# will represent the new updated board
		updated_generation = []
		# iterate down each row and column to update grid
		for i in range(self.rows):
			# represents a row of new updated cells
			updated_row = []
			for j in range(self.cols):
				# how many alive cells are next this cell
				alive_neighbors = 0

				# represent current cell's id
				current_cell = 0


				# grab all the cell's ids touching this cell
				alive_neighbors += self.grab_cell_id(i-1,j-1)
				alive_neighbors += self.grab_cell_id(i-1,j)
				alive_neighbors += self.grab_cell_id(i-1,j+1)
				alive_neighbors += self.grab_cell_id(i,j-1)
				alive_neighbors += self.grab_cell_id(i,j+1)
				alive_neighbors += self.grab_cell_id(i+1,j-1)
				alive_neighbors += self.grab_cell_id(i+1,j)
				alive_neighbors += self.grab_cell_id(i+1,j+1)

				# if this cell is alive
				if self.active_grid[i][j] == 1:
					# if it has 2 or 3 alive neighbors it should stay alive
					if (alive_neighbors == 2 or alive_neighbors == 3):
						current_cell = 1

				# it's dead
				else:
					# if it has 3 alive neighbors it should be alive
					if alive_neighbors == 3:
						current_cell = 1

				# add the new cell to the updated row
				updated_row.append(current_cell)


			# add the updated row to the new generation
			updated_generation.append(updated_row)


		# update inactive board to active board
		self.inactive_grid = self.active_grid
		# update new active board to the updated generation
		self.active_grid = updated_generation


	def grab_cell_id(self, row_index, col_index):
		# if an item at the given index in the inactive grid exists then return it
		# else return 0
		id = 0

		# if either the row or col index is negative return zero in order to
		# not wrap around the array
		if row_index < 0 or col_index < 0:
			return id
		try:
			# try grabbing an item at the given index for col and row
			id = self.active_grid[row_index][col_index]
			pass

		# if grabbing an item at this index is impossible via IndexError
		except IndexError:
		# neighbor doesn't exist so return 0
			return 0;

		return id


	def clear_screen(self):
		# clear the screen of old grid
		self.scene.fill(self.dead_color)


	def update_game(self):
		# go down the active grid and draw each element
		self.clear_screen()


		# iterate down each row and column to update grid
		for i in range(self.rows):
			for j in range(self.cols):
				color = self.dead_color
				if self.active_grid[i][j] == 1:
					# if we are alive make the color to draw green
					color = self.alive_color

				pygame.draw.rect(self.scene, color, 
					(int(i*self.cell), int(j*self.cell), int(self.cell),int(self.cell)),0)

		pygame.display.flip()



	def game(self):
		# handles running the simulation until some closes the window
		clock = pygame.time.Clock()
		while self.game_state:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.game_state = False

			self.update_grid()

			self.update_game()

			clock.tick(self.max_fps)



game = GameOfLife()
game.game() 

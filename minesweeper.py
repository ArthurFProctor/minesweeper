#!/usr/bin/python3.5

import sys, random

class Space:

	def __init__(self,x, y):
		self.x = x
		self.y = y
		self.bomb = False
		self.count = 0
		self.reveal = True

	def __repr__(self):
		return "%s,%s: %s|%s" % (self.x, self.y, self.bomb, self.count)

class Field:

	board = []

	widthIndex = 9
	heightIndex = 9

	def __init__(self, x, y):

		self.widthIndex = x - 1
		self.heightIndex = y - 1

		for w in range(x):
			self.board.append([])
			for h in range(y):
				self.board[w].append(Space(w,h))

	def tile(self, space):
		if space.x < 0 or space.x > self.widthIndex or space.y < 0 or space.y > self.heightIndex:
			return
		else:
			return self.board[space.x][space.y]

	def adj(self, space):

		rtn = []

		rtn.append(self.tile(Space(space.x-1,space.y-1)))
		rtn.append(self.tile(Space(space.x-1,space.y  )))
		rtn.append(self.tile(Space(space.x-1,space.y+1)))
		rtn.append(self.tile(Space(space.x,  space.y-1)))
		rtn.append(self.tile(Space(space.x,  space.y  )))
		rtn.append(self.tile(Space(space.x,  space.y+1)))
		rtn.append(self.tile(Space(space.x+1,space.y-1)))
		rtn.append(self.tile(Space(space.x+1,space.y  )))
		rtn.append(self.tile(Space(space.x+1,space.y+1)))

		return filter(None, rtn)

	def addBomb(self,space):
		if (space.x < 0) or (space.x > self.widthIndex)	or (space.y < 0) or (space.y > self.heightIndex):
			print("bad input")

		self.tile(space).bomb = True

		for s in self.adj(space):
			self.tile(s).count += 1

	def addBombs(self, space, number):

		for bomb in range(number):
			while(True):

				potentialBomb = self.tile(Space(random.randint(0,self.widthIndex), random.randint(0,self.heightIndex)))

				if (self.tile(potentialBomb).bomb):
					continue
				elif (self.tile(potentialBomb) == self.tile(space)):
					continue
				elif (self.tile(potentialBomb) in self.adj(space)):
					continue
				else:
					self.addBomb(potentialBomb)
					break

class Board:

	cursor = (0,0) #TODO: cursor object

	def __init__(self, width, height, bombNum):
		self.width = width
		self.height = height
		self.bombCount = bombNum
		self.board = Field(width,height)

	def changeDim(self,x,y):
		if x < 2 or y < 2:
			print("bad input")
			return

		self.width = x
		self.height = y
		self.board = Field(x,y)

	def changeBomb(self,n):
		if n < 0:
			print("bad input")
			return

		self.bombCount = n

	#space is where the user clicked, make sure that there are
	#no bombs within 1 of that
	def randomize(self, space):
		self.board.addBombs(space, self.bombCount)

class Display:

	def display(self,board):

		dis = "  %s,%s : %s\n" % (board.width, board.height, board.bombCount)

		for y in range(board.height):
			dis += "\n"
			dis += "  "
			for x in range(board.width):
				dis += self.displayTile(board.board.tile(Space(x,y)))

		dis += "\n"

		return dis

	def displayTile(self,space):
		if space.reveal:
			if space.bomb:
				return "B"
			elif space.count == 0:
				return " "
			else:
				return str(space.count)
		else:
			return "O"


def Test():
	b = Board(30,16,99)
	d = Display()

	#print(b.board.board)
	#b.board.addBomb(Space(1,1))
	#Sprint(b.board.board)
	#print(b.board.adj(Space(0,0)))

	b.randomize(Space(0,0))

	print(d.display(b))




Test()

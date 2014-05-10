'''
A couple of functions useful for PAD
'''

class Puzzler:
	'''
	Valid input String is of the form:
	"XXXXXX
	 XXXXXX
	 XXXXXX
	 XXXXXX
	 XXXXXX"
	Where X is one of 'G','R','B','Y','P','H'
	'''
	def __init__(self, inputstring):
		self.board = self.stringtoboard(inputstring)
		self.boardwidth = len(self.board[0])
		self.boardheight = len(self.board)
	
	def stringtoboard(self, str):
		a = str.split("\n")
		return map(list,a)
	
	def groups(self):
		'''
		returns a list of grouped elements in the board
		'''
		visited = []
		groups = []
		for y in range(self.boardheight):
			for x in range(self.boardwidth):
				if (x,y) not in visited:
					visited.append((x,y))
					newgroup = [self[y][x],(x,y)]
					tocheck = []
					self.addnewneighbors(x,y,tocheck, visited)
					while tocheck:
						e = tocheck.pop()
						if self[e[1]][e[0]] == newgroup[0]:
							visited.append(e)
							newgroup.append(e)
							self.addnewneighbors(e[0],e[1],tocheck, visited)
					groups.append(newgroup)
		return groups
	
	def addnewneighbors(self, x, y, tocheck, visited):
		if x>0 and (x-1,y) not in visited:
			tocheck.append((x-1,y))
		if x<self.boardwidth-1 and (x+1,y) not in visited:
			tocheck.append((x+1,y))
		if y>0 and (x,y-1) not in visited:
			tocheck.append((x,y-1))
		if y<self.boardheight-1 and (x,y+1) not in visited:
			tocheck.append((x,y+1))
	
	def allmatches(self, board):
		# accounts for falling subsequent matches
		allmatches = []
		matches = self.matches(board)
		while matches:
			allmatches += matches
			self.clearmatches(board)
			matches = self.matches(board)
		return allmatches
	
	def clearmatches(self, board):
		#remove matches
		for m in self.matches(board):
			for p in m[1:]:
				board[p[1]][p[0]] = False
		#make pieces fall
		for y in range(self.boardheight):
			for x in range(self.boardwidth):
				if board[y][x] == False:
					tmp = y
					while tmp > 0:
						board[tmp][x] = board[tmp-1][x]
						tmp -= 1
					board[tmp][x] = False
	
	def matches(self, board):
		hmatches = self.hmatches(board)
		vmatches = self.vmatches(board)
		visited = []
		matches = []
		for a in hmatches+vmatches:
			if a not in visited:
				match = a
				visited.append(a)
				tocheck = []
				self.addneighbormatches(a, tocheck, visited, hmatches, vmatches)
				while tocheck:
					b = tocheck.pop()
					if b[0] == match[0]:
						self.addnewpoints(match, b)
						visited.append(b)
						self.addneighbormatches(b, tocheck, visited, hmatches, vmatches)
				matches.append(match)
		return matches
		
	def addneighbormatches(self, match, tocheck, visited, hmatches, vmatches):
		added = []
		for p in match[1:]:
			for m in hmatches+vmatches:
				if m not in visited and m not in added and self.connected(p,m):
					tocheck.append(m)
					added.append(m)
					
	def connected(self, p, m):
		# p is a point (i,j), and m is a match [X,p1,p2 ...]
		result = False
		for n in m[1:]:
			if (p[0] == n[0] and p[1] == n[1] or
				p[0]-1 == n[0] and p[1] == n[1] or
				p[0]+1 == n[0] and p[1] == n[1] or
				p[0] == n[0] and p[1]-1 == n[1] or
				p[0] == n[0] and p[1]+1 == n[1]):
				result = True
				break
		return result
	
	def addnewpoints(self, match1, match2):
		# adds any new points from m2 to m1
		for p in match2[1:]:
			if p not in match1:
				match1.append(p)
	
	def hmatches(self, board):
		visited = []
		hmatches = []
		for y in range(self.boardheight):
			for x in range(self.boardwidth):
				if (x,y) not in visited and board[y][x]:
					newmatch = [board[y][x],(x,y)]
					visited.append((x,y))
					tmp = x
					while tmp+1 < self.boardwidth and board[y][tmp+1] == newmatch[0]:
						tmp += 1
						newmatch.append((tmp,y))
						visited.append((tmp,y))
					if len(newmatch) > 3:
						hmatches.append(newmatch)
		return hmatches
	
	def vmatches(self, board):
		visited = []
		vmatches = []
		for y in range(self.boardheight):
			for x in range(self.boardwidth):
				if (x,y) not in visited and board[y][x]:
					newmatch = [board[y][x],(x,y)]
					visited.append((x,y))
					tmp = y
					while tmp+1 < self.boardheight and board[tmp+1][x] == newmatch[0]:
						tmp += 1
						newmatch.append((x,tmp))
						visited.append((x,tmp))
					if len(newmatch) > 3:
						vmatches.append(newmatch)
		return vmatches
		
	def maxcombos(self, depth):
		bcopy = self.board
		for y in range(len(bcopy)):
			for x in range(len(bcopy[0])):
				print bcopy[y][x]
		
	def __str__(self):
		return str(self.board)
		
	def __getitem__(self,index):
		return self.board[index]
	
	def __setitem__(self, index, value):
		self.board[index] = value

if __name__ == "__main__":
	board = open("board4.txt")
	string = board.read()
	print string
	p = Puzzler(string)
	boardcopy = p.board
	print p
	print "Number of groups: " + str(len(p.groups()))
	print p.groups()
	print "Number of horizontal matches: " + str(len(p.hmatches(boardcopy)))
	print p.hmatches(boardcopy)
	print "Number of vertical matches: " + str(len(p.vmatches(boardcopy)))
	print p.vmatches(boardcopy)
	allmatches = p.allmatches(boardcopy)
	print "Number of total matches: " + str(len(allmatches))
	print allmatches
	p.maxcombos(1)

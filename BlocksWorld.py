from search import *
import sys
import timeit

class BlockWorlds(Problem) :

	def __init__(self, start, goal) :
		super(BlockWorlds, self).__init__(start, goal)


	def actions(self, state) :

		validActions=[]
		possibleState=[]
		tower=[]

		for i in range(len(state)) :
			for j in range(len(state)) :

				if(i!=j) :
					action=(i,j)
					validActions.append(action)
			if len(state[i])!=1 :
				action=(i,-1)
				validActions.append(action)

		return validActions

	def result(self, state, action) :

		res=[]
		tower=[]

		for i in range(0,len(state)) :
			if(action[0] == i) :
				for l in range(1,len(state[i])) :
					tower.append(state[i][l])
				if len(tower)>0 :
					res.append(tuple(tower))
				tower=[]
			elif(action[1] == i) :
				tower.append(state[action[0]][0])
				for l in range(0,len(state[i])) :
					tower.append(state[i][l])
				res.append(tuple(tower))
				tower=[]
			else :
				for l in range(0,len(state[i])) :
					tower.append(state[i][l])
				res.append(tuple(tower))
				tower=[]
		if action[1] == -1 :
			res.append(tuple(state[action[0]][0]))
		return tuple(res)

	#modified goal_test to check equality of tuples with different order
	def goal_test(self, state) :

		s=0
		g=0
		flag=0
		for i in range(len(state)) :
			for k in range(len(self.goal)) :

				if state[i][s] == self.goal[k][g] :
					if len(state[i]) != len(self.goal[k]) :
						return False
					while s<len(state[i]) :
						if state[i][s] == self.goal[k][g] :
							s+=1
							g+=1
							flag=1
						else :
							return False
					s=0
					g=0
					if flag==1 :
						flag=0
						break
				if k==len(self.goal)-1 and flag==0 :
					return False

		return True

def h1(n,goal) :

	h=0
	flag=0

	for i in range(len(n.state)) :
		for j in range(len(n.state[i])) :

			if j==0 :
				upperStateBlock = -1
			else :
				upperStateBlock = n.state[i][j-1]

			for k in range(len(goal)) :
				for l in range(len(goal[k])) :

					if goal[k][l] == n.state[i][j] :

						if l!=0 :
							upperGoalBlock = goal[k][l-1]
						else :
							upperGoalBlock = -1

						if upperStateBlock!=-1 and upperStateBlock!=upperGoalBlock :
							h+=1
						flag=1
						break
				if flag==1 :
					flag=0
					break
	return h

def h2(n, goal) :

	h=0
	flag=0
	flag2=0
	s=0
	g=0

	for i in range(len(n.state)) :
		s=len(n.state[i])-1
		for k in range(len(goal)) :
			for l in range(len(goal[k])) :
				if goal[k][l] == n.state[i][s] :
					if s!=0 and l!=0 :
						s-=1
						l-=1
						while goal[k][l] == n.state[i][s] :
							s-=1
							l-=1
							if s<0 or l<0 :
								flag=1
								break
						if flag==0 :
								h+=s+1
						else :
							flag=0
					elif s!=0 and l==0 :
						h+=s
					flag2=1
					break
			if flag2 == 1 :
				flag2=0
				break
	return h


def h3(n, goal) :

	h=0
	flag=0
	for i in range(len(n.state)) :
		for j in range(len(n.state[i])) :

			for k in range(len(goal)) :
				for l in range(len(goal[k])) :

					if n.state[i][j] == goal[k][l] :
						flag=1
						if (len(n.state[i])-j) != (len(goal[k])-l) :
							h+=1
						break
				if flag==1 :
					flag=0
					break
	return h

#order of blocks is written from top to bottom
var = raw_input("Please choose heuristic (type 1,2 or 3) ")
start = (('A','B','C'),('F',),('E',),('D','G','H'))
goal = (('G','B','E','D'),('F','A'),('H','C'))
print "Input problem is: %s , %s" %(start, goal)
p = BlockWorlds(start,goal)
if var=='1' :
	start = timeit.default_timer()
	s = astar_search(p, lambda node : h1(node, p.goal))
	stop = timeit.default_timer()
	print stop - start
elif var=='2' :
	start = timeit.default_timer()
	s = astar_search(p, lambda node : h2(node, p.goal))
	stop = timeit.default_timer()
	print stop - start
elif var=='3' :
	start = timeit.default_timer()
	s = astar_search(p, lambda node : h3(node, p.goal))
	stop = timeit.default_timer()
	print stop - start

if var=='1' or var=='2' or var=='3' :
	sol = s.solution() # The sequence of actions to go from the root to this node
	path = s.path() # The nodes that form the path from the root to this node
	print "Solution: \n+{0}+\n|Action\t|State\t	\t|Path Cost |\n+{0}+".format('-'*42)
	for i in range(len(path)) :
		state = path[i].state
		cost = path[i].path_cost
		action = " "
		if i > 0 : # The initial state has not an action that results to it
			action = sol[i-1]
		print "|{0}\t|{1} \t|{2} \t   |".format(action, state, cost)
	print "+{0}+".format('-'*42)


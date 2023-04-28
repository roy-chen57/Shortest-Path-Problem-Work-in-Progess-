import tkinter as tk

# Class Node: node of a mathematical graph
class Node:
	count = 0
	startNode = None

	## Constructor
	## x: Int for x-coordinate
	## y: Int for y-coordinate
	## gui: Gui object the node will be placed in
	## __init__: Int, Int, tk.Canvas -> None
	def __init__(self, x, y, canvas):
		"""
		self._x : stores the x-coordinate(in pixels) of the node
		self._y : stores the y-coordinate(in pixels) of the node
		self._edges: list of edges connected to this Node
		self.btn: tk.Button widget representing the node
		self._isClicked: boolean for if btn is clicked
		"""
		self._x = x
		self._y = y
		self._edges = []
		self._isClicked = False
		
		self.btn = tk.Button(canvas, text="Node", font=('Arial', 18), command=self.clicked)
		self.btn["state"] = tk.DISABLED

	## getX() returns x-coordinate of node
	## getX: Node -> int
	def getX(self):
		return self._x
	## getY() returns x-coordinate of node
	## getY: Node -> int
	def getY(self):
		return self._y

	## addEdge(self, edge) appends an Edge object to self._edges
	## MUTATION: appends an Edge obejct to self._edges
	## edge: Edge object to append
	## addEdge: Edge -> None
	def addEdge(self, edge):
		self._edges.append(edge)
	## getEdges(self) returns a list of Edge objects that the Node object
	##		is connected to
	## getEdges: Node -> list(Edges)
	def getEdges(self):
		return self._edges

	## place() wrapper for tkinter place function
	## place: Node -> None
	def place(self):
		self.btn.place(x=self._x, y=self._y)
	
	## clicked(self) switches the state of the button and checks
	##		the current state of the Node buttons to determine
	##		where to draw the edge
	def clicked(self):
		if self._isClicked:
			# if node button is sunken, raise it
			self.btn.config(relief=tk.RAISED)
			self._isClicked = False
			# if the node is clicked again, cancel the command to draw
			# an edge
			if Node.count == 1:
				print("Cancel")
				Node.count = 0
				Node.startNode = None
		else:
			# if node button is raised, sink it
			self.btn.config(relief=tk.SUNKEN)
			self._isClicked = True
			# if this node is the first node clicked, save the node
			# for later to draw the edge
			if Node.count == 0:
				print("Click 1")
				Node.startNode = self
				Node.count += 1
			# if this is the second node clicked, create an Edge between
			# the first node clicked and this node
			elif Node.count == 1:
				print("Click 2")
				newEdge = Edge(Node.startNode, self, weight=1, canvas=self.btn.master)
				Node.count = 0
				Node.startNode = None

	def getIsClicked(self):
		return self._isClicked

	def raiseBtn(self):
		self.btn.config(relief=tk.RAISED)
		self._isClicked = False


	# Destructor
	def __del__(self):
		#print("deleting node")
		self._edges.clear()
		# Destory the button if the Gui object has not destroyed it yet
		try:
			self.btn.destroy()
		except:
			pass

# Class Edge: edge of a mathematical graph
class Edge:
	## Constructor
	## startNode: Node object for starting node
	## endNode: Node object for ending node
	## weight: Int for weight of edge
	## directed: Bool if Edge is directed or not
	def __init__(self, startNode, endNode, weight, canvas, directed=False):
		"""
		self._weight: weight of the edge
		self._direct: boolean if the Edge is a direct edge or undirected
		self._startNode: starting Node of the Edge
		self._endNode: ending Node of the Edge
		self._line: line drawn onto the canvas
		"""
		self._weight = weight
		self._direct = directed
		self._startNode = startNode
		self._endNode = endNode
		if directed:
			self._line = canvas.create_line(startNode.getX(), startNode.getY(),
											endNode.getX(), endNode.getY(), arrow=tk.LAST)
		else:
			self._line = canvas.create_line(startNode.getX(), startNode.getY(),
											endNode.getX(), endNode.getY())
		
		# raise the two nodes' button 
		startNode.raiseBtn()
		endNode.raiseBtn()

		startNode.addEdge(self)
		if not directed: # if directed edge, end node can't use the Edge
			endNode.addEdge(self)

	## getWeight(self) returns the weight value of the Edge object
	## getWeight: Edge -> Int
	def getWeight(self):
		return self._weight


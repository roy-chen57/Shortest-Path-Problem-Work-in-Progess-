import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

# Class Node: node of a mathematical graph
class Node:
	# class variables storing the number of Node objects
	# clicked and the first Node object clicked
	# in order to draw edges between Node objects
	num = 0
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
		self._label = "node " + str(Node.num)
		
		self.btn = tk.Button(canvas, text=self._label, font=('Arial', 18), command=self.clicked)
		#print(self.btn.cget('text'))
		Node.num += 1
		self.btn["state"] = tk.DISABLED

	## getX() returns x-coordinate of node
	## getX: Node -> Int
	def getX(self):
		return self._x
	## getY() returns x-coordinate of node
	## getY: Node -> Int
	def getY(self):
		return self._y
	## getLabel() returns the label on the button of the node
	## getLabel: Node -> Str
	def getLabel(self):
		return self._label


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
				#print("Cancel")
				Node.count = 0
				Node.startNode = None
		else:
			# if node button is raised, sink it
			self.btn.config(relief=tk.SUNKEN)
			self._isClicked = True
			# if this node is the first node clicked, save the node
			# for later to draw the edge
			if Node.count == 0:
				#print("Click 1")
				Node.startNode = self
				Node.count += 1
			# if this is the second node clicked, create an Edge between
			# the first node clicked and this node
			elif Node.count == 1:
				#print("Click 2")
				# Prevent users from creating the same Edge
				if Node.startNode.hasEdge(self):
					self.raiseBtn()
					Node.startNode.raiseBtn()
					Node.startNode = None
					Node.count = 0
					messagebox.showerror("Error", "Error: Edge has already been created")
					return None

				newEdge = Edge(Node.startNode, self, canvas=self.btn.master)
				Node.count = 0
				Node.startNode = None

	## hasEdge(self, end, directed) checks if there is already an edge
	##		from the start node to the end node
	## hasEdge: Node, Node -> Bool
	def hasEdge(self, node):
		edges = {e.getStartNode() for e in self._edges}.union({e.getEndNode() for e in self._edges})
		if node in edges:
			return True
		else:
			return False


	
	## raiseBtn(self) changes the state of the Node object's button
	##		to the raised position
	## MUTATION: changes self._isClicked to False and 
	##		button relief to raised
	## raiseBtn: Node -> None
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

	@classmethod
	## reset(cls) resets Node class variables dictating creation of Edges
	## MUTATION: changes the value of Node.count and Node.startNode
	## reset: Node class -> None
	def reset(cls):
		Node.count = 0
		Node.num = 0
		Node.startNode = None

# Class Edge: edge of a mathematical graph
class Edge:
	## Constructor
	## startNode: Node object for starting node
	## endNode: Node object for ending node
	## weight: Int for weight of edge
	## undirected: Bool if Edge is directed or not
	def __init__(self, startNode, endNode, canvas, undirected=True):
		"""
		self._weight: weight of the edge
		self._startNode: starting Node of the Edge
		self._endNode: ending Node of the Edge
		self._line: line drawn onto the canvas
		"""
		self._weight = 1
		self._startNode = startNode
		self._endNode = endNode
		if undirected:
			self._line = canvas.create_line(startNode.getX(), startNode.getY(),
											endNode.getX(), endNode.getY(), width=3)
			# create simpledialog popup and enter weight of edge
			self._weight = simpledialog.askfloat("Weight", "Enter the weight of the edge")
			weightLab = tk.Label(canvas, text=self._weight, font=('Arial',18))
			canvas.create_window(abs(startNode.getX()+endNode.getX())/2,
								 abs(startNode.getY()+endNode.getY())/2,window=weightLab)

		else:
			self._line = canvas.create_line(startNode.getX(), startNode.getY(),
											endNode.getX(), endNode.getY(), width=3, arrow=tk.LAST)
		
		# raise the two nodes' button 
		startNode.raiseBtn()
		endNode.raiseBtn()

		startNode.addEdge(self)
		if undirected: # if directed edge, end node can't use the Edge
			endNode.addEdge(self)
	
	## getStartNode(self) returns the self._startNode Node object
	## getStartNode: Edge -> Node
	def getStartNode(self):
		return self._startNode
	## getEndNode(self) returns the sefl._endNode Node object
	## getEndNode: Edge -> Node
	def getEndNode(self):
		return self._endNode

	## getWeight(self) returns the weight value of the Edge object
	## getWeight: Edge -> Int
	def getWeight(self):
		return self._weight

	## shortcuts(self, event) defines the action of keyboard shorcuts
	## MUTATION: deletes the self._edgeWeight field, mutates self._edgeWeight field,
	##			 mutates self._weight field
	## shortcuts: Edge, tk.event -> None
	#def shortcuts(self, event):


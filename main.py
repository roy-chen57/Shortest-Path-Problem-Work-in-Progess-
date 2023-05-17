import tkinter as tk
from Graph import *
from functions import *

# Graphics user interface object for the Shortest Path Problem
class Gui:
	## Default Constructor
	## x: initial window width
	## y: initial window height
	def __init__(self, x=1280, y=720):
		self.root = tk.Tk() # Creates root window
		self.root.geometry(f"{x}x{y}") # initial root window dimensions

		self._nodes = [] # list of Nodes in the graph

		# Creates a frame for buttons within the root window
		self.btnFrame = tk.Frame(self.root, bg='red')
		self.btnFrame.pack(side=tk.TOP, fill=tk.X)

		# Creates a canvas for making the graph
		# (Canvas allows drawing lines as oppose to Frames)
		self.graphCanvas = tk.Canvas(self.root, bg='LightBlue1', highlightthickness=0)
		# expand=True fills the remaining space on root window
		self.graphCanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
		
		# Bind functions to mouse clicks
		self.graphCanvas.bind("<Button-1>", self.leftClick)	

		# Button for adding a new node to the graph
		self._nodeBtnOn = False
		self.nodeBtn = tk.Button(self.btnFrame, text="New Node", font=('Arial', 18), command=self.nodeBtnClick)
		self.nodeBtn.pack(in_=self.btnFrame, padx=10, pady=10, side=tk.LEFT)

		# Button for adding a new edge to the graph
		self._edgeBtnOn = False
		self.edgeBtn = tk.Button(self.btnFrame, text="New Edge", font=('Arial', 18), command=self.edgeBtnClick)
		self.edgeBtn.pack(in_=self.btnFrame, padx=10, pady=10, side=tk.LEFT)

		# Button for clearing the entire graph
		# MUTATION: sets self._nodes to empty list 
		self.clearBtn = tk.Button(self.btnFrame, text="Clear", font=('Arial', 18), command=self.clearCanvas)
		self.clearBtn.pack(in_=self.btnFrame, padx=10, pady=10, side=tk.RIGHT)

		# Button to get the current window dimensions
		self.winSize = tk.Button(self.btnFrame, text="Window Dimensions", font=('Arial', 18), command=self.getDim)
		self.winSize.pack(in_=self.btnFrame, padx=10, pady=10, side=tk.RIGHT)

		# Button for running functions on the current graph
		self.executeBtn = tk.Button(self.btnFrame, text="Solve", font=('Arial', 18), command=lambda : dijkstra(self.getNodes()))
		self.executeBtn.pack(in_=self.btnFrame, padx=10, pady=10, side=tk.RIGHT)

		self.root.mainloop() # Execute commands


	## leftClick(self, event) determine the action of mouse left click depending on buttons' status
	## event: tkinter event that was binded to this function
	## leftClick: tk.Event -> None
	def leftClick(self, event):
		if self._nodeBtnOn:
			# add a new Node onto the graphCanvas widget
			#print("Placing Node")
			absX = self.graphCanvas.winfo_pointerx() - self.graphCanvas.winfo_rootx()
			absY = self.graphCanvas.winfo_pointery() - self.graphCanvas.winfo_rooty()
			self.addNode(x=absX, y=absY)
		else:
			pass
			#print("Doing Nothing")
	
	
	## nodeBtnClick(self) switches state of the nodeBtn button
	## MUTATION: changes the Node objects' btn attribute's state
	## nodeBtnClick: Gui -> None
	def nodeBtnClick(self):
		if self._nodeBtnOn:
			# raise nodeBtn
			self.nodeBtn.config(relief=tk.RAISED)
			self._nodeBtnOn = False
		else:
			# if edge button is clicked, unclick it
			if self._edgeBtnOn:
				self.edgeBtn.config(relief=tk.RAISED)
				self._edgeBtnOn = False
				# deactivate nodes once edgeBtn is raised and
				# reset Node class variables
				Node.reset()
				if self._nodes: # if there are Nodes already in graph
					for n in self._nodes:
						#print("nodeBtn: disabling node")
						n.btn["state"] = tk.DISABLED
						n.raiseBtn()
			# click nodeBtn
			self.nodeBtn.config(relief=tk.SUNKEN)
			self._nodeBtnOn = True
	## edgeBtnClick(self) switches state of the edgeBtn button
	## MUTATION: changes the Node objects' btn attritbute's state
	## edgeBtnClick: Gui -> None
	def edgeBtnClick(self):
		if self._edgeBtnOn:
			self.edgeBtn.config(relief=tk.RAISED)
			self._edgeBtnOn = False
			# deactivate nodes once edgeBtn is raised
			if self._nodes:
				for n in self._nodes:
					#print("edgeBtn: disabling node")
					n.btn["state"] = tk.DISABLED
		else:
			# if node button is clicked, unclick it
			if self._nodeBtnOn:
				self.nodeBtn.config(relief=tk.RAISED)
				self._nodeBtnOn = False
			self.edgeBtn.config(relief=tk.SUNKEN)
			self._edgeBtnOn = True
			# activate nodes once edgeBtn is clicked
			if self._nodes:
				for n in self._nodes:
					#print("edgeBtn: enabling node")
					n.btn["state"] = tk.NORMAL

	## addNode(self, x, y) Adds a new Node object at coordinates x & y of
	##		the graphCanvas widget
	## MUTATION: appends a Node object to self._nodes
	## x: integer value for x pos of new node
	## y: integer value for y pos of new node
	## addNode: Int, Int -> None
	def addNode(self, x, y):
		newNode = Node(x=x, y=y, canvas=self.graphCanvas)
		self._nodes.append(newNode)
		
		newNode.place() # Wrapper function to place the Node's button
	
	## clearCanvas(self) wipes the canvas clean by removing all Nodes in self._nodes
	## MUTATION: sets self._nodes to empty list
	## clearCanvas: Gui -> None
	def clearCanvas(self):
		for n in self._nodes:
			# explicitly call destructors to destroy the Button within
			n.__del__()
		self._nodes.clear() # clear references to deleted Nodes
		self.graphCanvas.delete('all')
		Node.reset()
		#print("clearing canvas, # of nodes: " + str(self._nodes.__len__()))

	## getDim(self) prints the current dimension of the window
	## getDim: Gui -> Str
	def getDim(self):
		return str(self.root.winfo_width()) + "x" + str(self.root.winfo_height())

	## getNodes(self) returns the list of Node objects drawn onto the graph
	## getNodes: Gui -> list(Nodes)
	def getNodes(self):
		return self._nodes
	
Gui()
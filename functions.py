import Graph
import numpy as np

INF = float('inf') # infinite constant

## dijkstra(nodes) implementation of Dijkstra's Algorithm
##		for solving the Shortest Path Problem, taking the
##		first node in the list as the starting node
## dijkstra: list(Node) -> dict(Str:Float)
def dijkstra(nodes):
	print("dijkstra's algorithm")

	# dictionary with all Nodes as keys and float for values
	distance = {n:INF for n in nodes}
	distance[list(distance.keys())[0]] = 0

	paths = {n.getLabel():'node 0' for n in nodes}
	#print("Paths: ", paths)
	# set of all Nodes
	visited = {list(distance.keys())[0]}
	#print(len(dist.keys()))
	#print(len(visited))

	#while len(visited) < len(dist.keys()):

	result = dijsktraLoop(distance, paths, visited)
	print("Shortest Distances: ", labelDist(result))
	print("Paths:")
	for key,value in paths.items():
		print(key,": ",value)


def dijsktraLoop(distances, paths, visitedNodes):
	if len(set(distances)-visitedNodes) == 0:
		print("end loop")
		#print(distances)
		return distances
	else:
		print("looping")
		#print("Distance before update:")
		#print(labelDist(distances))
		 # dictionary of adjacent nodes with their min distance to start node
		adjNodes = dict()
		# set of nodes not yet visited
		notVisited = set(distances) - visitedNodes
		for n in notVisited:
			nEdges = n.getEdges()
			# all possible paths from node n in adjacent nodes with their distance
			dists = dict() 
			for edge in nEdges: # check each edge the node is connected to
				if adjEdge(edge, visitedNodes): # if adjacent to a visited node
					dists.update({adjThroughEdge(n, edge):edge}) # add node n to dist
			if dists: # if there is at least one adjacent edge
				#minPath = min(sumWeights(dists, distances))
				sumDict = sumWeights(dists, distances)
				#print("sumDict: ", labelDist(sumDict))
				minPath = min(sumDict.values())
				minNode = keyFromVal(sumDict, minPath)
				updatePaths(paths, n.getLabel(), paths[minNode.getLabel()])
				adjNodes.update({n:minPath})

		# updates distances for all nodes searched
		for n in adjNodes:
			distances[n] = adjNodes[n]
		#print("Distances after update:")
		#print(labelDist(distances))
		#print("adjNodes")
		#print(labelDist(adjNodes))
		minDistNode = min(adjNodes, key=adjNodes.get)
		#print("minDistNode: ", minDistNode.getLabel())
		updatePaths(paths, minDistNode.getLabel(), paths[minDistNode.getLabel()]+"->"+minDistNode.getLabel())
		#print("Paths: ", paths)
		visitedNodes.add(minDistNode)

		return dijsktraLoop(distances, paths, visitedNodes)
	


## labelDist(dict) takes a dictionary with Node objects as keys and returns a dictionary
##		with the Node's label member variable as the keys, with the same values
## labelDist: {Node:Float} -> {Str:Float}
def labelDist(dict):
	label = list(dict.keys())
	label = list(map(lambda key: key.getLabel(), label))

	values = list(dict.values())
	newDict = {label[i]:values[i] for i in range(len(label))}
	return newDict

def adjEdge(edge, visitedNodes):
	if edge.getStartNode() in visitedNodes:
		return True
	if edge.getEndNode() in visitedNodes:
		return True
	else:
		return False

def adjThroughEdge(node, edge):
	if edge.getStartNode() == node:
		return edge.getEndNode()
	else:
		return edge.getStartNode()

## sumWeights: dict(Node:Edge), dict(Node:Float) -> list(Float)
## sumWeights: dict(Node:Edge), dict(Node:Float) -> dict(Node:Float)
def sumWeights(nodeEdgeDict, distances):
	# list of distance of adj visited nodes
	dist = [distances.get(n) for n in nodeEdgeDict.keys()]
	# list of weights of adj edges
	edgeWeight = [e.getWeight() for e in nodeEdgeDict.values()]
	#retDict = dict(zip(np.add(dist, edgeWeight), nodeEdgeDict.keys()))
	retDist = np.add(dist, edgeWeight)
	#print(retDist)
	retDict = {list(nodeEdgeDict.keys())[i]:retDist[i] for i in range(len(retDist))}
	return retDict
	#return retDist

## updateDistKey: dict(Str:Str), Str, Str -> None
## MUTATION: changes value in paths list
def updatePaths(paths, node, newVal):
	if node in paths:
		paths[node] = newVal
	else:
		pass


def keyFromVal(dict, val):
	for key,value in dict.items():
		if value == val:
			return key

	else:
		raise ValueError("No dictionary key with given value")
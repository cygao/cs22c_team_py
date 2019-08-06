# De Anza College, CIS 22C, Summer 2019
# Instructor: Kamren Eftekhari
# Term Project: Maze
# Team Python: Michael Fan, Cameron Gao, Afshar Kiana, Zixi Luo

from stack import Stack
from queue import Queue
import random, collections,sys

MAZE_FILE="maze.txt"

random.seed()

class UnionFind:
    class _Vertex:
        ''' Basic object in Disjoint set. It only includes the key as content in Disjoint Set universe.'''
        def __init__(self,key):
            self.key=key
            
    def __init__(self):
        ''' Collections of objects in the Disjoint Set universe in V. 
        edgeTo is reference to the adjacent object in the path toward the root of a set for a given object.''' 
        self._edgeTo={}
        self._V={}
             
    def find(self,key):
        '''Find the root of the set which the key is belong to.'''
        s=Stack()
        if key not in self._edgeTo:
            return None
        else:
            while isinstance(self._edgeTo[key],self._Vertex):
                s.push(self._edgeTo[key])
                key=self._edgeTo[key].key
            for x in s: # path compression
                x=self._V[key]
                 
        return self._V[key].key
    
    
    def union(self,key1,key2=None):
        ''' With only one key, key1, create an unique instance in the Disjoint Set universe.
        With both key1 and key2, union the sets which they are belong to.'''
        
        if key2 is None:
            # If only one key provided, it is to be included (connected) in V.
            self._V[key1]=self._Vertex(key1)  # key does not exist, add to V
            self._edgeTo[key1]=-1        # A new key added resulting in a disjoint set with single key.
            return
        elif key1 not in self._V or key2 not in self._V:
            # check if both keys are is in V
            return
        elif key1 is not key2 :
            r1=self.find(key1)     # find root of key1
            r2=self.find(key2)     # find root of key2 
            
            if r1!=r2:  # r1 is not r2
                
                if self._edgeTo[r1]<self._edgeTo[r2]: # r1 is deeper, hence as new root
                    self._edgeTo[r1]+=self._edgeTo[r2]    # update size of r1 to include r2
                    self._edgeTo[r2]=self._V[r1]                   # assign r1 as new root of r2
                    
                else:
                    self._edgeTo[r2]+=self._edgeTo[r1]    # update size of r2 to include r1
                    self._edgeTo[r1]=self._V[r2]                     # assign r2 as new root of r1
                    
            return

class AdjacencyList:
    '''Adjacency List to be used for Graph to represent adjacent connections of a vertex using a Double Linked List data structure.'''  
    class _Node:
        '''Nested class for a node in the AdjacencyList. Each node includes the reference to the vertex.'''
        def __init__(self,v):
            self.vertex=v
            self.prev=None
            self.next=None  
            
    def __init__(self):
        self._head=self._Node(None)
        self._head.next=self._head
        self._head.prev=self._head
        self._n=0
        
    def __repr__(self):
        return "Vertex "+self.vertex.key+" Adjacency List"
    
    def __iter__(self):
        self._indexNode=self._head.next
        return self
    
    def __next__(self):
        if self._indexNode is not self._head:
            result=self._indexNode.vertex
            self._indexNode=self._indexNode.next
            return result
        else:
            raise StopIteration
    
    def size(self):
        return self._n
    
    def insertSorted(self,v):
        ''' Add a new node for the vertex, v, if it does not already exists. Return True if added, otherwise False.
        The node is inserted at a position in the list according to the sort order of vertices.'''        
        current=self._head.next
        found=False
        while not found and current is not self._head:
            if current.vertex < v:   
                current=current.next
            else:
                found=True
        # Sort order is determined; to insert if the vertex already exists.
        if current.vertex is not v:
            newNode=self._Node(v)                     
            # newNode inserted before current node
            newNode.prev=current.prev     
            newNode.next=current        
            
            if self._head.prev is self._head:
                # list is empty
                self._head.prev=newNode
                self._head.next=newNode
            else:
                # list is not empty
                current.prev.next=newNode
                current.prev=newNode
            self._n+=1 
            return True
        return False
        
class Vertex:
    ''' Vertex to be used in a Graph.'''
    def __init__(self,room):
        self.room=room
        self.ajcList=AdjacencyList()      
        
    def __repr__(self):
        return self.room
    
    def __lt__(self,other):
        return self.room<other.room
    
    def __le__(self,other):
        return self.room<=other.room 
    
    def __eq__(self,other):
        return self.room == other.room

class Graph:
    ''' Graph=(V,E) where V is set of vertices in the graph, E is set of edges in the graph. 
    The edge has no direction, nor weight.'''
    def __init__(self):
        self.V={}
        self.E={}
        
    def size(self):
        ''' Return a tuple of number of elements in V and E, respectively.'''
        return (len(self.V),len(self.E))

    
    def items(self):
        return (v.room for v in self.V.values())
    
    def adjacencies(self):
        return ( (i[0].room, i[1].room) for i in self.E.values())
        
    def addAdjacency(self,room1,room2):
        '''Add a relation between room1 and room2. Vertices and edges are created in the graph if not already exist.'''
        added=False
            
        if (room1,room2) not in self.E and (room2,room1) not in self.E:
            if room1 not in self.V:
                self.V[room1]=Vertex(room1)
                
            if room2 not in self.V:
                self.V[room2]=Vertex(room2)
                
            self.E[(room1,room2)]=(self.V[room1],self.V[room2])
                 
            self.V[room1].ajcList.insertSorted(self.V[room2])
            self.V[room2].ajcList.insertSorted(self.V[room1])
            
            added=True
        return added
    
    def iAdjacencies(self,room):
        '''To creat a generator for rooms that have a relation with the given user.'''
        try:
            v=self.V[room]
            return ( w.room for w in v.ajcList)
        except:
            return ()
        
    def bfs(self,target):
        ''' To obtain the shortest path between room1 and room2 in the network.
        Return a generator of room in the path from room1 to room2.'''
        
        bfs=BFS(self.V[0])
        #print("selfV0",type(self.V[0]), self.V[0].room)
        bfs.bfs(target)
        
        visited=[v.room for v in bfs.visited]
        edgeTo={k:bfs.edgeTo[k].room for k in bfs.edgeTo }
        
        return visited,edgeTo
    
    def dfs(self,target):
        ''' To obtain a path between room1 and room2 in the network.'''
        
        dfs=DFS(self.V[0])
        #print("selfV0",type(self.V[0]), self.V[0].room)
        dfs.dfs(target)
        
        visited=[v.room for v in dfs.visited]
        edgeTo={k:dfs.edgeTo[k].room for k in dfs.edgeTo }
        
        return visited,edgeTo    


            
class BFS:
    '''Breadth Fisrt Search. Each BFS object is initialized for a source vertex. BFS methods are first applied to 
    the source vertex, followed by those with a path to the source in the Graph.'''
    def __init__(self,vertex):
        self.root=vertex
        self.visited=[vertex]
        self.edgeTo={vertex.room:vertex}
        self._q=Queue()
        self._q.enqueue(vertex)
        
    def bfs(self,target):
        while len(self._q) != 0 :
            u=self._q.dequeue()
            for v in u.ajcList:
                if v not in self.visited:
                    self.visited.append(v)
                    self.edgeTo[v.room]=u
                    self._q.enqueue(v)
                    if v.room==target:
                        self._q.clear()
                        break
    
            self.bfs(target)
    

class DFS:
    '''Breadth Fisrt Search. Each BFS object is initialized for a source vertex. BFS methods are first applied to 
    the source vertex, followed by those with a path to the source in the Graph.'''
    def __init__(self,vertex):
        self.root=vertex
        self.visited=[vertex]
        self.edgeTo={vertex.room:vertex}
        
    def _dfs(self,u,target):
        for v in u.ajcList:
            if not self._found and v not in self.visited:
                self.visited.append(v)
                self.edgeTo[v.room]=u
                if v.room==target:
                    self._found=True
                    return
                else:
                    self._dfs(v,target)
                 
    def dfs(self,target):
        self._found=False
        self._dfs(self.root,target)


class Maze:
    ''' Maze represented by a Graph with room as vertex, and edge as passage (door open) to other rooms.'''
    Door=collections.namedtuple("Door","N S E W")
    
    def __init__(self,filename=""):
        self._graph=Graph()
        self._edgeTo={}
        self._path=[]
        self._visited=[]
        try:
            self._mazeFromFile(filename)
           
        except FileNotFoundError:
            self._randomMaze()             
            
    def _mazeFromFile(self,filename):
        '''Create maze from input file given.'''
        try:
            with open(filename) as fh:
                self.nrow=self.ncol=int(fh.readline().strip())
                self.nmaze=self.nrow*self.ncol
                t=Maze.Door(*map(int,fh.readline().strip().split()))
                
                # Room 0, the start of maze
                if t.S==0:
                    self._graph.addAdjacency(0,self.ncol)
                if t.E==0:
                    self._graph.addAdjacency(0,1)
                
                if t.W==0 or t.N!=0:
                    print(0,t)
                    raise ValueError
                    
                    
                for i in range(1,self.nmaze-1):
                    t=Maze.Door(*map(int,fh.readline().strip().split()))
                    
                    if t.N==0:
                        self._graph.addAdjacency(i,i-self.ncol)
                    if t.S==0:
                        self._graph.addAdjacency(i,i+self.ncol)
                    if t.E==0:
                        self._graph.addAdjacency(i,i+1)
                    if t.W==0:
                        self._graph.addAdjacency(i,i-1)
                
                # Room nmaze-1, the end of maze        
                t=Maze.Door(*map(int,fh.readline().strip().split()))
                if t.N==0:
                    self._graph.addAdjacency(i,i-self.ncol)
                if t.W==0:
                    self._graph.addAdjacency(i,i-1)
                if t.E==0 or t.S!=0:
                    print(self.nmaze-1,t)
                    raise ValueError                
                    
                
                if any(room < 0 or room >= self.nmaze for room in self.rooms()):
                    raise ValueError
        except ValueError:
            print("Input file error.")
            raise SystemExit
        
    def _randomMaze(self):
        '''Generate a maze randomly for a given size of n x n.'''
        self.nrow=self.ncol=int(input("Enter n for maze size of n x n: "))
        self.nmaze=self.ncol*self.nrow
        
        S=UnionFind()
        
        for i in range(self.nmaze):
            S.union(i)
    
        
        while S.find(0) != S.find(self.nmaze-1):
            i=random.randint(0,self.nmaze-1)
            choices=self._nextrooms(i)
            j=random.choice(choices)
            self._graph.addAdjacency(i,j)
            S.union(S.find(i),S.find(j))
                                   
    def _nextrooms(self,i):
        '''Create a list of room numbers that are adjacent to the given.'''
        l=[]
        if i+self.nrow in range(self.nmaze):
            l.append(i+self.nrow)
        if i-self.nrow in range(self.nmaze):
            l.append(i-self.nrow)
        if (i+1)//self.nrow == i//self.nrow and i+1 in range(self.nmaze):
            l.append(i+1)
        if (i-1)//self.nrow == i//self.nrow and i-1 in range(self.nmaze):
            l.append(i-1)
        return l        
        
    def size(self):
        '''A tuple to represent the size of network, number of rooms and number of doors open between rooms.'''
        return (len(self._graph.V),len(self._graph.E))
    
    def rooms(self):
        ''' An iterator for users in the network.'''
        return self._graph.items()
    
    def adjacencies(self):
        ''' An iterator for passages between adjacent rooms.'''
        return self._graph.adjacencies()
        
    def _bfs(self):
        ''' Breadth First Search method for solving the maze.'''
        self._visited,self._edgeTo=self._graph.bfs(self.nmaze-1)
       
    
    def _dfs(self):
        ''' Depth First Search method for solving the maze.'''
        self._visited,self._edgeTo=self._graph.dfs(self.nmaze-1)
    
    def path(self,method="BFS"):
        ''' Find path for the maze.'''
        methods={"BFS":self._bfs, "DFS":self._dfs}
        i=self.nmaze-1
        
        methods[method]()
            
        s=Stack()
    
        while self._edgeTo[i] is not i:
            s.push(i)
            i=self._edgeTo[i]
        
        s.push(i)
        
        path=[ s.pop() for i in range(len(s))]
        
        print()
        
        for i in range(self.nrow):
            for j in range(self.ncol):
                if i*self.ncol+j in path:
                    print("x",end="")
                else:
                    print(" ",end="")
                if j==self.nrow-1:
                    print()
                
            
        return path, [ i for i in self._visited]
    
def main():
    print("Maze from Input File:" + MAZE_FILE)
    maze=Maze(MAZE_FILE)
          
    print("Breadth First Search:")
    
    path,visited=maze.path()
    print("BFS path:", *path)
    print("BFS visited:", *visited)
    path,visited=maze.path("DFS")
    print("DFS path:", *path)
    print("DFS visited:", *visited)
    
    
    print("\n\nRadomly Generated Maze:")
    
    maze2=Maze()
    path,visited=maze2.path()
    print("BFS path:", *path)
    print("BFS visited:", *visited)
    path,visited=maze2.path("DFS")
    print("DFS path:", *path)
    print("DFS visited:", *visited)
    

if __name__=="__main__":
    main()
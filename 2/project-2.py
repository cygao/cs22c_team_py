# De Anza College, CIS 22C, Summer 2019
# Instructor: Kamren Eftekhari
# Project 2: Facebook Friend Graph
# Team Python: Michael Fan, Cameron Gao, Afshar Kiana, Zixi Luo
# Detail: This file will create a graph of people and friendships, and run various test searches on them

from queue import Queue
from stack import Stack

# constants
INFILE_NETWORK="facebook_network.txt"
INFILE_USERS="find_friends.txt"

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
    def __len__(self):
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
    def __init__(self,name):
        self.name=name
        self.ajcList=AdjacencyList()      
        
    def __repr__(self):
        return self.name
    
    def __lt__(self,other):
        return self.name<other.name
    
    def __le__(self,other):
        return self.name<=other.name 
    
    def __eq__(self,other):
        return self.name == other.name

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
        return (v.name for v in self.V.values())
    
    def adjacencies(self):
        return ( (i[0].name, i[1].name) for i in self.E.values())
        
    def addAdjacency(self,name1,name2):
        '''Add a relation between name1 and name2. Vertices and edges are created in the graph if not already exist.'''
        added=False
            
        if (name1,name2) not in self.E and (name2,name1) not in self.E:
            if name1 not in self.V:
                self.V[name1]=Vertex(name1)
                
            if name2 not in self.V:
                self.V[name2]=Vertex(name2)
                
            self.E[(name1,name2)]=(self.V[name1],self.V[name2])
                 
            self.V[name1].ajcList.insertSorted(self.V[name2])
            self.V[name2].ajcList.insertSorted(self.V[name1])
            
            added=True
        return added
    
    def iAdjacencies(self,name):
        '''To creat a generator for names that have a relation with the given user.'''
        try:
            v=self.V[name]
            return ( w.name for w in v.ajcList)
        except:
            return ()
        
    def chain_bfs(self, name1, name2):
        ''' To obtain the shortest path between name1 and name2 in the network.
        Return a generator of name in the path from name1 to name2.'''
        
        bfs=BFS(self.V[name1])
    
        return ( v.name for v in bfs.search(self.V[name2]))

            
class BFS:
    '''Breadth Fisrt Search. Each BFS object is initialized for a source vertex. BFS methods are first applied to 
    the source vertex, followed by those with a path to the source in the Graph.'''
    def __init__(self,vertex):
        self.root=vertex
        self._visited=[vertex]
        self._edgeTo={vertex.name:vertex}
        self._q=Queue()
        self._q.enqueue(vertex)
        
    def _bfs(self,w):
        while len(self._q) != 0 :
            u=self._q.dequeue()
            for v in u.ajcList:
                if v not in self._visited:
                    self._visited.append(v)
                    self._edgeTo[v.name]=u
                    self._q.enqueue(v)
                    if v is w:
                        self._q.clear()
                        break
            self._bfs(w)
            
    def search(self,w):
        '''Starting from source, breadth first search for w.'''
        if self.root is w:
            return [w]

        self._bfs(w)
        
        return self._path(w)
    
    def _path(self,w):
        ''' Creat path from source to w in the BFS tree.'''
        s=Stack()
    
        while self._edgeTo[w.name] is not w:
            s.push(w)
            w=self._edgeTo[w.name]

        return [self.root]+[ s.pop() for i in range(len(s))]


class FacebookNetwork:
    ''' Network represented by a Graph with user(name) as vertex, and edge as relation between users.'''
    def __init__(self):
        self._graph=Graph()
        
    def size(self):
        '''A tuple to represent the size of network, number of users and number of adjacencies.'''
        return (len(self._graph.V),len(self._graph.E))
    
    def users(self):
        ''' An iterator for users in the network.'''
        return self._graph.items()
    
    def adjacencies(self):
        ''' An iterator for adjacencies, i.e. edges in Graph, in the network.'''
        return self._graph.adjacencies()
        
    def addAdjacency(self,name1, name2):
        '''Add an adjacent relation between two users in the network, using their names.'''
        self._graph.addAdjacency(name1,name2)
    
    def friends(self,name):
        '''An iterable for friends of the given user.'''
        return self._graph.iAdjacencies(name)
    
    def recommendFriends(self, user):
        '''Recommend top 10 users in the network that are not already user's friend but have the most common friends.'''
        sfriends=set(self.friends(user))
        
        lwithCommonFriends=[]
    
        for u in self.users():
            '''u is user in the network that is not user nor is already friend of user.'''
            if u not in sfriends and u != user:
                u_sfriends=set(self.friends(u))
                commonFriends=sorted(u_sfriends.intersection(sfriends))
                if len(commonFriends)>0:
                    lwithCommonFriends.append((len(commonFriends),u,commonFriends))
                
        print(f"\n{user} has friends: {', '.join(sorted(sfriends))}")
        print(f"\nTop 10 users who are not already {user}'s friend but have the most mutual friends with him/her:")
       
        for x in sorted(lwithCommonFriends, reverse=True)[:10]:
            print(f"{x[1]} has {x[0]} mutual friend(s).")
      
    def chain(self, name1, name2):
        ''' To obtain the shortest path between name1 and name2 in the network.'''
        try:
            return self._graph.chain_bfs(name1,name2)
        except KeyError as eObj:
            print("Name not found: "+str(eObj))
        except RecursionError as eObj:
            print(str(eObj))
            
   

def main():  
    # Load network:
    g=FacebookNetwork()
    with open(INFILE_NETWORK) as fh:
        for line in fh:
            g.addAdjacency(*line.strip().split())
    
    # Load users to be considered:
    lusers=[]
    with open(INFILE_USERS) as fh:
        for line in fh:
            lusers.extend(line.strip().split())    

    print("Recomending friends of friend to a user:")
    for user in lusers:
        srecommand={ p for friend in g.friends(user) for p in g.friends(friend)}.difference(set(g.friends(user))).difference([user])
        
        print(f"Recommended for {user}, {len(srecommand)} total.")    
    print()  
    
    for user in lusers:
        g.recommendFriends(user)  
    print()
    
    for i in range(0,len(lusers),2):
        lchain=list(g.chain(lusers[i],lusers[i+1]))
        print(" - ".join(lchain)+" :")
        print()
        for p in lchain:
                    print(f"Friends of {p}:\n"+", ".join(list(g.friends(p))))
        print()
                                 
if __name__=="__main__":
    main()

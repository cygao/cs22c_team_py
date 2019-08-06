# CIS-22C 
# Project 1
# Michael Fan

import collections

INFILE_STUDENT="InputStudentFile.txt"
INFILE_APARTMENT="InputApartmentFile.txt"
APARTMENT_DATAFIELDS="ID Location Bedroom Laundry Rent"
STUDENT_DATAFIELDS="ID Name Location Bedroom Laundry Rent"     

class Apartment:
    '''For Apartment object to include Apartment features.'''
    ApartmentData=collections.namedtuple("ApartmentData",APARTMENT_DATAFIELDS)
    def __init__(self,*args):
        self.data=Apartment.ApartmentData(*args)
        
    def __repr__(self):
        return "Apartment "+self.data.ID
    
class Student:
    '''For Student object to include student's info and apartment requirements.'''
    StudentData=collections.namedtuple("StudentData",STUDENT_DATAFIELDS)
    def __init__(self,*args):
        self.data=Student.StudentData(*args)
        
    def __repr__(self):
        return "Student "+self.data.ID   
        
class ApartmentList:
    '''AparmentList implemented with Double Linked List data structure.'''
    class _Node:
        '''Nested class for node in a Double Linked List data structure.'''
        def __init__(self,item):
            self.item=item
            self.prev=None
            self.next=None
    
    def __init__(self,filename=""):
        self._head=self._Node(None)     # sentinel node
        self._head.next=self._head      # sentinel-next points to itself if empty list, otherwise, the first node of the list
        self._head.prev=self._head      # sentinel-prev points to itself if empty list, otherwise, the last node of the list
        self._n=0                       # size of the list, excluding sentinel node
        try:                            # Create the list if input file is provided
            with open(filename, encoding="utf-8-sig") as fh:
                print("Available Apartment List:")
                print("{:10s} {:10s} {:10s} {:10s} {:5s}".format(*APARTMENT_DATAFIELDS.split()))
                for line in fh:
                    data=line.strip().split()
                    self.add(Apartment(*data))
                    print("{:10s} {:10s} {:10s} {:10s} {:5s}".format(*data))
        except FileNotFoundError as eObj:
            print(str(eObj))
            print("An empty list is created.")
                                    
    def __repr__(self):
        return "ApartmentList object with size of "+str(self._n)
        
    def __len__(self):
        return self._n  
    
    def size(self):
        '''Accesor for the size of the list'''
        return self._n
        
    def add(self,item):
        ''' Adding an Apartment object at the end of the list '''
        # create a new node to be added into the list
        newNode=self._Node(item)        
        # newNode added to the end of the list
        newNode.prev=self._head.prev    # newNode is added at the end of the list, hence its prev points to the current end node, self._head.prev
        newNode.next=self._head         # newNode.next points to self._head
        
        # update sentinel node, self._head
        if self._head.prev is self._head:
            # list is empty
            self._head.prev=newNode
            self._head.next=newNode
        else:
            # list is not empty
            self._head.prev.next=newNode
            self._head.prev=newNode
        self._n+=1
    
    def remove(self,item):
        ''' Search for aparment that meet the criteria, and pop that item from the list.'''
        current=self._head.next
        found=False
        while not found and current is not self._head:
            found=self._match(item,current.item)
            current=current.next
        if found:
            pop_node=current.prev       # pop_node is the found node and to be popped from the list as return item.
            pop_node.prev.next=pop_node.next
            pop_node.next.prev=pop_node.prev
            return pop_node.item
        return None    
            
    def _match(self, student, apartment):
        '''To check if the apartment matches student's requirements.'''
        try:
            if student.data.Location.lower() not in ("any",apartment.data.Location.lower()):
                return False
            if student.data.Bedroom.lower() not in ("any",apartment.data.Bedroom.lower()):
                return False
            if student.data.Laundry.lower() not in ("any",apartment.data.Laundry.lower()):
                return False        
            if int(student.data.Rent) < int(apartment.data.Rent):
                return False
            return True
        except:
            return False
   
    def isEmpty(self):
        '''Check if the list is empty.'''
        return self._n is 0
            
    def allList(self):
        '''Generate a list of apartments that remain in the list.'''
        l=[]
        current=self._head.next
        while current is not self._head:
            l.append(current.item)
            current=current.next
        return l    

class WaitingListQueue:
    ''' Waiting list queue of students. Implemented as queue with Single Linked List data structure.'''
    class _Node:
        '''Nested class for node in a Single Linked List data structure.'''
        def __init__(self,item):
            self.item=item
            self.next=None
            
    def __init__(self,filename=""):
        self._head=None     # head of the queue
        self._tail=None     # end of the queue
        self._n=0           # size of the queue
        try:                # Create the queue if input file is provided
            with open(INFILE_STUDENT, encoding="utf-8-sig") as fh:
                print("\nStudents in Waiting List Queue:")   
                print("{:10s} {:10s} {:10s} {:10s} {:10s} {:5s}".format(*STUDENT_DATAFIELDS.split()))
                for line in fh:
                    data=line.strip().split()
                    self.enqueue(Student(*data))
                    print("{:10s} {:10s} {:10s} {:10s} {:10s} {:5s}".format(*data))
        except FileNotFoundError as eObj:
            print(str(eObj))
            print("An empty queue is created.")
    
    def __repr__(self):
        return "Waiting List Queue object with size of "+str(self._n)    
    
    def __len__(self):
        return self._n
    
    def size(self):
        '''Accessor for the size of the queue.'''
        return self._n
        
    def enqueue(self,item):
        '''Put the item at the end of the queue.'''
        newNode=self._Node(item)
        if self._n == 0 :
            self._head = self._tail=newNode
        else:
            self._tail.next=newNode
            self._tail=newNode
        self._n+=1
    
    def dequeue(self):
        '''Pop the item at the front of the queue.'''
        if self._n != 0:
            pop_node=self._head
            self._head=self._head.next
            self._n-=1
            return pop_node.item
        else:
            return None
    
    def isEmpty(self):
        '''Check if the queue is empty.'''
        return self._n == 0
    
    def allList(self):
        '''Generate a list of students that remain in the queue.'''
        l=[]
        current=self._head
        while current != None:
            l.append(current.item)
            current=current.next
        return l
       
def main():
    q=WaitingListQueue(INFILE_STUDENT)
    l=ApartmentList(INFILE_APARTMENT)
            
    print("\n\nMatching Aparment with Student Results:")
    for i in range(q.size()):
        s=q.dequeue()     
        if l.size()>0:
            a=l.remove(s)
        else:
            a=None
        if a:
            print("The aparment "+a.data.ID+" is assigned to "+s.data.Name+"("+s.data.ID+").")
        else:
            print("There are no aparments satifying "+s.data.Name+"("+s.data.ID+")'s requirements.")
            q.enqueue(s)  
            
    for a in l.allList():
        print("The apartment "+a.data.ID+" is unassigned.")

if __name__=="__main__":
    main()
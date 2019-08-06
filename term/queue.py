# CIS-22C 
# Project 2
# Queue
# Python Group

class Queue:
    '''Queue implemented with Single Linked List data structure.'''
    class _Node:
        '''Nested class for node in a Single Linked List data structure.'''
        def __init__(self,item):
            self.item=item
            self.next=None

    def __init__(self):
        self._head=None     # head of the queue
        self._tail=None     # end of the queue
        self._n=0           # size of the queue
        self._indexNode=self._head

    def __repr__(self):
        return "Queue object with size of "+str(self._n)    

    def __len__(self):
        return self._n

    def __iter__(self):
        self._indexNode=self._head
        return self

    def __next__(self):
        if self._indexNode is not None:
            result=self._indexNode.item
            self._indexNode=self._indexNode.next
            return result
        else:
            raise StopIteration

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

    def clear(self):
        ''' Clear the queue.'''
        self._head=None    
        self._tail=None     
        self._n=0         

# CIS-22C 
# Project 2
# Queue, Stack
# Python Group

class Stack:
    '''Stack implemented with a Single Linked List data structure.'''
    class _Node:
        '''Nested class for node in a Single Linked List data structure.'''
        def __init__(self,item):
            self.item=item
            self.next=None
            

    def __init__(self):
        self._head=None     # top of the stack
        self._n=0           # size of the stack
        
    def __repr__(self):
        return "Stack object with size of "+str(self._n)    

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

    def push(self,item):
        '''Put the item at the top of the stack.'''
        newNode=self._Node(item)
        if self._n == 0 :
            self._head=newNode
        else:
            newNode.next=self._head
            self._head=newNode
        self._n+=1

    def pop(self):
        '''Pop the item at the top of the stack.'''
        if self._n != 0:
            pop_node=self._head
            self._head=self._head.next
            self._n-=1
            return pop_node.item
        else:
            return None
    def peek(self):
        '''Check the content at the top of the stack.'''
        if self._head:
            return self._head.item

    def isEmpty(self):
        '''Check if the stack is empty.'''
        return self._n == 0

    def clear(self):
        '''Clear the stack.'''
        self._head=None       
        self._n=0         
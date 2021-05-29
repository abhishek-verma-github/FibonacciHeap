"""
fibonacci heap is an unordered collection of binomial trees where each tree follows heap invariance.
Time Complexities : extractMin: amortized O(lgn), deleteNode: amortized O(lgn) and rest have amortized O(1).

Implementation is done using circular doubly linked list where rootlist is a CDLL and each node
has a pointer to one of the child and children are linked in a CDLL as siblings.

root list references : root_head and root_tail
for each node have children, reference to child list through : child_head and child_tail

Also upper bound on degree of FibHeap i.e. no of trees in a root list is log_phi(n) which is logarith of n with base equals to phi/goldenRatio.
 

Refernce - CLRS
Author : Abhishek Verma
"""
import math
from sys import maxsize as INF

NEGATIVE_INF = -INF

GR = 1.618 # golden ratio or PHI

class FibNode:
    def __init__(self, key = None):
        self.degree = 0
        self.parent = None
        self.key = key
        self.mark = False
        self.rigth = None
        self.left = None
        # child list head and tail
        self.child_head = None
        self.child_tail = None
        

class FibHeap:
    def __init__(self):
        self.min = None
        self.n = 0
        self.root_head = None
        self.root_tail = None # for root list (a CDLL)


    @classmethod
    def makeFibHeap(cls):
        return cls()


    def iterRootList(self):
        """ to print root list only, dont use to iterate root list in other
        operations as root list changes """
        node = self.root_head
        while node:
            yield node
            node = node.right
            if node == self.root_tail.right:
                break
        
    def iterChildList(self,x):
        """ to print root list only, dont use to iterate child list in other
        operations as child list changes """
        node = x.child_head
        while node:
            yield node
            node = node.right
            if node == x.child_tail.right:
                break

    def fibHeapInsert(self,key:int):
        x = FibNode(key)
        # otehr initialization are done in node itself
        if self.min == None:
            # create a root list for H containing just x
            self.root_head = x
            self.root_tail = x
            x.right = x.left = x
            self.min = x
        else:
            # insert x into H's root list
            self.root_tail.right = x
            x.left = self.root_tail
            x.right = self.root_head
            self.root_tail = x
            self.root_head.left = x
            if x.key < self.min.key:
                self.min = x
        self.n += 1
        return x


    def fibHeapUnion(self,H2, inplace = True):
        # concatenate rootlist of H2 with H
        self.root_tail.next = H2.root_head
        H2.root_head.left = self.root_tail
        H2.root_tail.next = self.root_head
        self.root_tail = H2.root_tail
        H2.root_head = None # free h2.head pointer
        self.root_head.left = self.root_tail
        
        if (self.min == None) or (H2.min != None and H2.min.key < self.min.key):
            self.min = H2.min
        self.n = self.n + H2.n

        if inplace == False:
            return self
        

    def fibHeapLink(self,y:FibNode,x:FibNode):
        # remove y from the root list of H
        if y == self.root_head and y != self.root_tail: # first position
            self.root_head = self.root_head.right
            self.root_head.left = self.root_tail
            self.root_tail.right = self.root_head

        elif y == self.root_tail and y != self.root_head:
            self.root_tail = self.root_tail.left
            self.root_tail.right = self.root_head
            self.root_head.left = self.root_tail
        else:
            y.left.right = y.right
            y.right.left = y.left

        if x.child_head == x.child_tail == None:
            x.child_head = y
            x.child_tail = y
            y.right = y.left = y
            y.parent = x

        else:
            x.child_tail.right = y
            y.left = x.child_tail
            y.rigth = x.child_head
            x.child_tail = y
            x.child_head.left = y
            y.parent = x
        x.degree += 1
        y.mark = False

       
    
    def consolidate(self):
        Dn = math.ceil(math.log(self.n,GR)) # used ceil instead of floor. Can use floor as well
        A = [None] * Dn 
        root_list = [x for x in self.iterRootList()]
        for w in root_list:
            x = w
            d = x.degree
            while A[d] is not None:
                y = A[d] # another node with same degree
                if x.key > y.key:
                    x,y = y,x # exchange x,y and fibheaplink will make y child of x
                self.fibHeapLink(y,x)
                A[d] = None # reset current degree in A
                d += 1
            A[d] = x
        self.min = None
        for i in range(Dn):
            if A[i] is not None:
                if self.min == None:
                    # create root list for h consist of just A[i]
                    self.root_head = A[i]
                    self.root_tail = A[i]
                    A[i].left = A[i].right = A[i]
                    self.min = A[i]
                else:
                    # insert A[i] in rott list of H 
                    A[i].left = self.root_tail
                    self.root_tail.right = A[i]
                    A[i].right = self.root_head
                    self.root_tail = A[i]
                    if A[i].key < self.min.key:
                        self.min = A[i]
                    
    
    def fibHeapExtractMin(self):
        z = self.min
        if z is not None:
            zchildren = [c for c in self.iterChildList(z)]
            if zchildren:
                for x in zchildren:
                    # add x to the root list
                    x.left = self.root_tail
                    x.right = self.root_head
                    self.root_tail.right = x
                    self.root_tail = x
                    x.parent = None
            # remove z for root list
            self.min = z.right
            z.left.right = z.right
            z.right.left = z.left
            # update head and tail
            if self.root_head == z and self.root_tail != z:
                self.root_head = self.root_head.right
                self.root_head.left = self.root_tail
            elif self.root_tail == z and self.root_tail != z:
                self.root_tail = self.root_tail.left
                self.root_tail.right = self.root_head

            if z == z.right: # only node in the root list 
                self.min = None
                self.root_head=self.root_tail=None
            else:
                self.consolidate()
            self.n = self.n - 1
        return z

    def decreaseKey(self,x, k):
        if k > x.key:
            return False
        x.key = k
        y = x.parent
        if y != None and x.key < y.key:
            self.cut(x,y) # cut x from y, promote x to rootlist
            self.cascadeCut(y) # check if y is loser, if loser cut it and promote to rootlist and recursively call cascade cut on it parent 
        if x.key < self.min.key:
            self.min = x


    def cut(self,x,y):
        # remove x from childlist of y and decrement y.degree
        y.child_head = y.child_head.right
        y.child_head.left = y.child_tail
        y.child_tail.right = y.child_head 
        y.degree = y.degree - 1
        
        # add x to root list of H
        x.left = self.root_tail
        x.right = self.root_head
        self.root_tail.right = x
        self.root_tail = x
        x.parent = None
        x.mark = False


    def cascadeCut(self,y):
        z = y.parent
        if z != None:
            if y.mark == False:
                y.mark = True
            else:
                self.cut(y,z) # cut y from z
                self.cascadeCut(z)


    def deleteNode(self,x):
        self.decreaseKey(x,NEGATIVE_INF)
        self.fibHeapExtractMin()       
    




# test
def main():

    h = FibHeap.makeFibHeap()
    h.fibHeapInsert(2)
    h.fibHeapInsert(4)
    h.fibHeapInsert(5)
    h.fibHeapInsert(1)
    h.fibHeapInsert(6)


    print(h.fibHeapExtractMin().key) # 1
    print(f"{[node.key for node in h.iterRootList()]}")
    # print(f"{[node.key for node in h.iterChildList(h.min)]}")
    print(h.fibHeapExtractMin().key)# 2
    print(f"{[node.key for node in h.iterRootList()]}")

    print(h.fibHeapExtractMin().key)# 4 
    print(f"{[node.key for node in h.iterRootList()]}")

    print(h.fibHeapExtractMin().key)# 5
    print(f"{[node.key for node in h.iterRootList()]}")

    print(h.fibHeapExtractMin().key)# 6
    print(f"{[node.key for node in h.iterRootList()]}")


    h.fibHeapInsert(2)
    h.fibHeapInsert(4)
    h.fibHeapInsert(5)
    h.fibHeapInsert(1)
    node = h.fibHeapInsert(7)
    print(f"{[node.key for node in h.iterRootList()]}")
    h.decreaseKey(node,6)
    print(f"{[node.key for node in h.iterRootList()]}")
    h.deleteNode(node)
    print(f"{[node.key for node in h.iterRootList()]}")
    print(f"[1]'s child_list: {[x.key for x in h.iterChildList(h.min)]}")


if __name__ == "__main__":
    main()






    
            

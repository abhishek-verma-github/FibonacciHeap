# FibonacciHeap

fibonacci heap is an unordered collection of binomial trees where each tree follows heap invariance.
Time Complexities : extractMin: amortized O(lgn), deleteNode: amortized O(lgn) and rest have amortized O(1).
Implementation is done using circular doubly linked list where rootlist is a CDLL and each node
has a pointer to one of the child and children are linked in a CDLL as siblings.
root list references : root_head and root_tail
for each node have children, reference to child list through : child_head and child_tail
Also upper bound on degree of FibHeap i.e. no of trees in a root list is log_phi(n) which is 
logarith of n with base equals to phi/goldenRatio.


Here is an Implementation of fibonacci heap using circular doubly linked list in Python 3.7

Application of fibonacci heap is in implementing priority queues where we want O(1) insert, O(1) decrease-key, and O(lgN) extract-min and delete-node.

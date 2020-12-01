"""
@author: isaac.kleisle-murphy
"""

import numpy as np
HOUSEHOLDS = [['Jeanne', 'Bill'], 
              ['Laura', 'Joe'],
              ['Doug'],
              ['Grandma', 'Grandpa']]

class Edge:
    def __init__(self, vin, vout):
        self.vin=vin
        self.vout=vout
        
    def get_tuple(self):
        return self.vin, self.vout

def assign_gifts(households, seed=2020):
    
    np.random.seed(seed)
    gift_tuples = []
    
    edge_set = [
        Edge(households[i][j], item)
        for i in range(len(households))
        for item in np.hstack(households[:i]+households[i+1:])
        for j in range(len(households[i]))
        ]
    
    while len(edge_set):
        gift_pair = edge_set.pop(np.random.choice(range(len(edge_set))))
        gift_tuples.append(gift_pair.get_tuple())
        edge_set = [edge for edge in edge_set
                    if gift_pair.vin != edge.vin and gift_pair.vout != edge.vout]
        
    return np.vstack(gift_tuples)

def main(households=HOUSEHOLDS, seed=2020):
    
    gift_order = assign_gifts(households, seed)
    print(gift_order)
    
if __name__=='__main__':
    main()

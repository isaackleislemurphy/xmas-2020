"""
@author: isaac.kleisle-murphy
"""
from typing import List, Tuple
import argparse
import numpy as np


DEFAULT_random_state = 121697
HOUSEHOLDS = [
    ["Jeanne", "Bill", "Rob", "Mike F", "Sophia"], 
    ["Laura", "Joe", "Isaac"], 
    ["Doug"], 
    ["Grandma", "Grandpa"],
    ["Jack", "Jon", "Reese", "Wendy"],
    ["Jim", "Mike H", "Heather"],
]


class Edge:
    """
    Simple directed edge to manage gift pairings.

    Attributes:
        vin : str
            An identifier for the indbound vertex
        vout : str
            An identifier for the outbound vertex

    """
    def __init__(self, vin: str, vout: str):
        self.vin = vin
        self.vout = vout

    def get_vertices(self) -> Tuple[str, str]:
        """
        Returns tuple of (vertex_in, vertex_out)

        Returns : Tuple[str, str]
            The inbound and outbound vertex
        """
        return self.vin, self.vout


def assign_gifts(households: List[List[str]], random_state: int = DEFAULT_random_state) -> List[Tuple[str, str]]:
    """
    Assigns gifts across households, brute-force style. Specifically:
    1. Assigns all-possible cross-household edges.
    2. Picks up sticks until gifts are complete.

    Args:
        households : List[List[str]]
            A nested list of households and people in households.
            Outer list is households; inner list is people in household.
        random_state : int
            Seed to be passed to `np.random.seed()`, to reproduce results.

    Returns : List[Tuple[str, str]]:
        A list whose elements are a tuple denoting (gift_giver, gift_receiver)
    """
    np.random.seed(random_state)
    gift_tuples = []

    ### drop sticks for every possible edge, such that no between-house edges
    edge_set = [
        Edge(households[i][j], item)
        for i in range(len(households))
        for item in np.hstack(households[:i] + households[i + 1 :])
        for j in range(len(households[i]))
    ]
    ### pickup sticks for now-impossible gift pairings
    while len(edge_set):
        gift_pair = edge_set.pop(np.random.choice(range(len(edge_set))))
        gift_tuples.append(gift_pair.get_vertices())
        edge_set = [
            edge
            for edge in edge_set
            if gift_pair.vin != edge.vin and gift_pair.vout != edge.vout
        ]

    return gift_tuples


def print_assignments(assignments: List) -> None:
  """
  Prints assignments nicely
  
  Args:
      assignments : List[Tuple[str, str]]
          A List of (gift_giver, gift_receiver) tuples, as outputted 
          by `assign_gifts()`, to be printed cleanly.
  
  Returns : None
  """
  for i, swap_pair in enumerate(assignments):
      print(f"Pairing {i + 1}:\t{swap_pair[0]} gives to {swap_pair[1]}")


def get_args() -> argparse.ArgumentParser:
    """
    Sets up argparse to accept:
        - (int) `random_state`, a random state from the user. 

    Returns : argparse.ArgumentParser 
        Parsed args
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--random_state", type=int, default=DEFAULT_random_state, help="Pick a number, any number")
    args = parser.parse_args()
    return args


def main(households: List[List[str]]=HOUSEHOLDS):
    """
    Go Birds
    """
    args = get_args()
    gift_order = assign_gifts(households=households, random_state=args.random_state)
    print_assignments(gift_order)


if __name__ == "__main__":
    main()

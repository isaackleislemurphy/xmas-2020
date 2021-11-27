"""
@author: isaac.kleisle-murphy
"""
import argparse
import numpy as np

DEFAULT_SEED = 2021
HOUSEHOLDS = [["Jeanne", "Bill"], ["Laura", "Joe"], ["Doug"], ["Grandma", "Grandpa"]]


class Edge:
    """
    Simple directed edge to manage gift pairings
    """

    def __init__(self, vin, vout):
        self.vin = vin
        self.vout = vout

    def get_tuple(self):
        """
        Returns tuple of (vertex_in, vertex_out)
        """
        return self.vin, self.vout


def get_args():
    """
    Gets seed from user
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--random_state", help="Pick a number, any number")
    args = parser.parse_args()
    return args


def assign_gifts(households, seed=DEFAULT_SEED):
    """
    Assigns gifts across households. Specifically:
    1. Assigns all-possible cross-household edges.
    2. Picks up sticks until gifts are complete.

    Args:
        households : list[list[str]]
            A nested list of households and people in households.
            Outer list is households; inner list is people in household.
        seed : int
            Random state (np) to use
    Returns : np.ndarray:
        An (N, 2) array containing gift-swap pairs
    """
    np.random.seed(seed)
    gift_tuples = []

    edge_set = [
        Edge(households[i][j], item)
        for i in range(len(households))
        for item in np.hstack(households[:i] + households[i + 1 :])
        for j in range(len(households[i]))
    ]

    while len(edge_set):
        gift_pair = edge_set.pop(np.random.choice(range(len(edge_set))))
        gift_tuples.append(gift_pair.get_tuple())
        edge_set = [
            edge
            for edge in edge_set
            if gift_pair.vin != edge.vin and gift_pair.vout != edge.vout
        ]

    return np.vstack(gift_tuples)


def main(households=HOUSEHOLDS, seed=DEFAULT_SEED):
    """
    Esketit
    """
    seed_args = get_args()
    if seed_args.random_state is not None:
        try:
            seed = int(seed_args.random_state)
        except ValueError:
            raise ValueError(
                "Random state must be an integer, or a numeric that can be coerced into an integer.\n For example: `python3 xmas.py --random_state 1234`"
            )
    gift_order = assign_gifts(households, seed)
    print(gift_order)


if __name__ == "__main__":
    main()

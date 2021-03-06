import sys
import unittest

from networkx import DiGraph
from numpy import array

sys.path.append("../")
from cspy.algorithms.tabu import Tabu


class TestsTabu(unittest.TestCase):
    """
    Tests for finding the resource constrained shortest
    path of simple DiGraph using the Tabu algorithm.
    """
    def setUp(self):
        self.max_res, self.min_res = [5, 5], [0, 0]
        # Create digraph with a resource infeasible minimum cost path
        self.G = DiGraph(directed=True, n_res=2)
        self.G.add_edge('Source', 'A', res_cost=array([1, 1]), weight=1)
        self.G.add_edge('Source', 'B', res_cost=array([1, 1]), weight=1)
        # Resource infeasible edge
        self.G.add_edge('Source', 'C', res_cost=array([10, 1]), weight=10)
        self.G.add_edge('A', 'C', res_cost=array([1, 1]), weight=1)
        # Resource infeasible edge
        self.G.add_edge('A', 'E', res_cost=array([10, 1]), weight=10)
        # Resource infeasible edge
        self.G.add_edge('A', 'F', res_cost=array([10, 1]), weight=10)
        self.G.add_edge('B', 'C', res_cost=array([2, 1]), weight=-1)
        # Resource infeasible edge
        self.G.add_edge('B', 'F', res_cost=array([10, 1]), weight=10)
        # Resource infeasible edge
        self.G.add_edge('B', 'E', res_cost=array([10, 1]), weight=10)
        self.G.add_edge('C', 'D', res_cost=array([1, 1]), weight=-1)
        self.G.add_edge('D', 'E', res_cost=array([1, 1]), weight=1)
        self.G.add_edge('D', 'F', res_cost=array([1, 1]), weight=1)
        # Resource infeasible edge
        self.G.add_edge('D', 'Sink', res_cost=array([10, 10]), weight=10)
        # Resource infeasible edge
        self.G.add_edge('F', 'Sink', res_cost=array([10, 1]), weight=1)
        self.G.add_edge('E', 'Sink', res_cost=array([1, 1]), weight=1)

    def testTabu(self):
        tabu = Tabu(self.G, self.max_res, self.min_res)
        # Check exception for not running first
        with self.assertRaises(Exception) as context:
            tabu.path
        self.assertTrue("run()" in str(context.exception))
        # Run and test results
        tabu.run()
        path = tabu.path
        cost = tabu.total_cost
        total_res = tabu.consumed_resources
        self.assertEqual(path, ['Source', 'A', 'C', 'D', 'E', 'Sink'])
        self.assertEqual(cost, 3)
        self.assertTrue(all(total_res == [5, 5]))

    def testInputExceptions(self):
        # Check whether wrong input raises exceptions
        self.assertRaises(Exception, Tabu, self.G, 'x', [1, 'foo'], 'up')


if __name__ == '__main__':
    unittest.main()

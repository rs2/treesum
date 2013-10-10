import unittest2
from tempfile import mktemp
from treesum import Solver, TreeDefinitionException

class TestSolver(unittest2.TestCase):

    def setUp(self):
        self.fileName = mktemp()

    def initFile(self, text):
        with open(self.fileName, 'w') as f:
            f.write(text)

    # Let's use some TDD
    def testArgumentIsString(self):
        with self.assertRaises(AssertionError):
            Solver({}).solve()
             
    def testFileExists(self):
        with self.assertRaises(AssertionError):
            Solver('/nosuchfile/foo.bar').solve()        
 
    def testEmptyString(self):
        self.initFile('')
        res = Solver(self.fileName).solve()
        self.assertEquals(res, [])        
 
    def testEmptyStringWithSeparators(self):
        self.initFile(' \n \t\n\r')
        res = Solver(self.fileName).solve()
        self.assertEquals(res, [])        
 
    def testExample1(self):
        text = """22 (5(4(11(7()())(2()()))()) (8(13()())(4()(1()()))))"""
        self.initFile(text)
        res = Solver(self.fileName).solve()
        self.assertEquals(res, [True])
 
    def testNegativeNumbersTrees(self):
        text = """-10 (7 () (-17 () ()))"""
        self.initFile(text)
        res = Solver(self.fileName).solve()
        self.assertEquals(res, [True])

    def testMultipleTrees(self):
        text = """1 (2 () ()) 3 (3 () ())"""
        self.initFile(text)
        res = Solver(self.fileName).solve()
        self.assertEquals(res, [False, True])

    def testExample2(self):
        text = """
22 (5(4(11(7()())(2()()))()) (8(13()())(4()(1()()))))
20 (5(4(11(7()())(2()()))()) (8(13()())(4()(1()()))))
10 (3 
     (2 (4 () () )
        (8 () () ) )
     (1 (6 () () )
        (4 () () ) ) )
5 ()"""
        self.initFile(text)
        res = Solver(self.fileName).solve()
        self.assertEquals(res, [True, False, True, False])

    def testBadTree(self):
        with self.assertRaises(TreeDefinitionException):
            text = """22 (5(4(11(7()())(2()()))()) (8(13()("""
            self.initFile(text)
            Solver(self.fileName).solve()
            
    def testBigTree(self):
        # Ok, I chose a fun approach with using eval() and recursing the tree on the stack
        # For really large trees I could just build a recursion using a list/deque as a synthetic stack
        # and parse the substrings of the text definitions of the tree. A nice follow-up project. 
        n = 50
        text = '%d %s%s%s' % (n, '(1'*n, '()', '())'*n)
        self.initFile(text)
        res = Solver(self.fileName).solve()
        self.assertEquals(res, [True])

if __name__ == "__main__":
    unittest2.main()


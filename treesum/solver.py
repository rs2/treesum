'''
Tree Sum Solver.

See unit tests for usage examples

Created on 9 Oct 2013

@author: PA
'''

import os
import re


class TreeDefinitionException(Exception):
    """
        Bad tree definition
    """


# A classic python tree is:
# Tree = lambda: defaultdict(Tree)
# However, is it not suitable here, hence we implement a custom tree
class Tree(object):
    """
        A class for tree walking
    """
    
    def __init__(self, *args):
        """
            :param *args: Either no arguments for an empty tree or an (int, Tree and Tree)
        """
        if not args:
            self.value = self.left = self.right = None
        elif len(args)==3:
            self.value, self.left, self.right = args
        else:
            raise ValueError('A tree can either be empty () or a 3-tuple')
    
    def getRootLeafPaths(self):
        """
            Return a list of sums of all possible root to leaf paths
        """
        if self.value is None:
            return []
        paths = [self.value + lpath for leaf in [self.left, self.right] for lpath in leaf.getRootLeafPaths()]
        return paths or [self.value]


class Solver(object):
    """
        Tree sum solver.
        For details see http://www.cs.duke.edu/courses/cps100/fall03/assign/extra/treesum.html
    """
    
    def __init__(self, fileName):
        """
        :param basestring fileName: input file name   
        """
        assert isinstance(fileName, basestring), 'fileName must be a string'
        assert os.path.exists(fileName), '{0} does not exist'.format(fileName)
        self.fileName = fileName

    @staticmethod
    def _loadTextFromFile(fileName):
        with open(fileName, 'r') as f:
            return f.read()

    @staticmethod
    def _normaliseText(text):
        return ''.join(text.split())

    @staticmethod
    def _getTreeDict(text):
        assert text, 'Expecting non-empty string'
        # Using python to compile the object from the input string!
        evalText = text.replace('(', ',Tree(')
        try:
            # One-liner tree parser, hurrah!
            treeTuple = eval(evalText)
        except SyntaxError:
            raise TreeDefinitionException('Bad tree definition: {0}'.format(evalText))
        assert isinstance(treeTuple, tuple) and len(treeTuple)==2, 'Invalid tree definition'
        return dict(zip(['testValue', 'tree'], treeTuple))
 
    @staticmethod
    def _splitText(text):
        if not text:
            return []
        counter = 0
        seps = []
        for k, c in enumerate(text):
            counter += {'(':1, ')':-1}.get(c, 0)
            if c==')' and not counter:
                # We've found a matching closing bracket
                seps.append(k+1)
        seps = sorted(set(seps + [0, len(text)]))
        # Separate multiple tree definitions
        return [text[seps[x]:seps[x+1]] for x in range(len(seps)-1)]

    def _getTreeDicts(self, text):
        return [self._getTreeDict(t) for t in self._splitText(text)]
 
    def solve(self):
        """
            Read the file, parse the text and give an answer
            
            :return: A list of booleans one for each tree in the file. One can easily convert these into yes/no.
        """
        # Load from file
        text = self._loadTextFromFile(self.fileName)
        # Check for bad characters
        assert re.search(r'^[\n\r\t\(\) 0-9+-]*$', text), 'Text must contain integers, tabs, new lines and parenthesis only'
        # Remove newlines and separators
        text = self._normaliseText(text)
        # Load tree objects and test values
        treeDicts = self._getTreeDicts(text)
        # Return a boolean for each tree
        return [treeDict['testValue'] in treeDict['tree'].getRootLeafPaths() for treeDict in treeDicts]
            
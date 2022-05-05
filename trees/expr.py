import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import token

class Expr:
   class Visitor:
      def visit_assign(self, assign: object):
          pass
      def visit_binary(self, binary: object):
          pass
      def visit_grouping(self, grouping: object):
          pass
      def visit_literal(self, literal: object):
          pass
      def visit_unary(self, unary: object):
          pass
      def visit_variable(self, variable: object):
          pass
   def accept(self, visitor: object) -> object:
       pass

class Assign(Expr):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def accept(self, visitor: object) -> object:
        return visitor.visit_assign(self)

class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: object) -> object:
        return visitor.visit_binary(self)

class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor: object) -> object:
        return visitor.visit_grouping(self)

class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor: object) -> object:
        return visitor.visit_literal(self)

class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor: object) -> object:
        return visitor.visit_unary(self)

class Variable(Expr):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor: object) -> object:
        return visitor.visit_variable(self)


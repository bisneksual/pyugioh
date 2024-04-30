import argparse
import shlex


class STAK:
    def __init__(self,items: list = [],rev: bool = False):
        self.stack = items.reverse() if rev else items
    
    def pop(self):
        return self.stack.pop()
    
    def push(self,item):
        self.stack.append(item)

    def peek(self):
        return self.stack[-1]
    
    def empty(self) -> bool:
        return (len(self.stack)==0)

inputs = input("Enter input: ")
args = shlex.split(inputs)

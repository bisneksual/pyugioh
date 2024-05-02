import argparse
import shlex


class STAK:
    def __init__(self,items: list = [],rev: bool = False):
        self.__stack = items.reverse() if rev else items
    
    def pop(self):
        return self.__stack.pop()
    
    def push(self,item):
        self.__stack.append(item)

    def peek(self):
        return self.__stack[-1]
    
    def empty(self) -> bool:
        return len(self.__stack)==0

parser = argparse.ArgumentParser()
parser.add_argument()

inputs = input("main ->")
args = shlex.split(inputs)
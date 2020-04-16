import load
from main import toBin
from block import data

class breakingLevel:
    any = 0
    wooden = 1
    golden = 1
    stone = 2
    iron = 3
    diamond = 4


class Block:
    """Base class of Block"""
    def __init__(self, data=None):
        self.image = load.unknown # the look of the block
        self.hardness = 1 # how many seconds takes to break
        self.breakingLevel = breakingLevel.any # with which kind of tool can be destoried
        self.light = 0 # how much light does it make
        self.washable = True # able to stay in water
        self.stackCapacity = 64 # capacity in a stack
        self.standable = True # player can stand on
        self.doStick = False # stick player
        self.init()
        if data is not None:
            self.fromBytes(data)

    def __bytes__(self) -> bytes:
        # [int:info_length] [info[0]]...[]..
        result = toBin(data.block_data.index(type(self)))
        return result

    def toBytes(self) -> bytes:
        return self.__bytes__()

    def fromBytes(self, data: bytes):
        """Define how it read back its data"""
        pass

    def init(self):
        """Will be executed when initializing"""
        pass

data.block_data.append(Block)

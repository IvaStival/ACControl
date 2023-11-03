import board

dict_boards = {
    "4": board.D4, 
    "17": board.D17, 
}

def getBoard(port):
    return dict_boards[port]
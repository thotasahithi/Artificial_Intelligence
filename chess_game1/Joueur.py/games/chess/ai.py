# This is where you build your AI for the Chess game.

from joueur.base_ai import BaseAI
import random

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add additional import(s) here
# <<-- /Creer-Merge: imports -->>

class AI(BaseAI):
    """ The AI you add and improve code inside to play Chess. """

    @property
    def game(self) -> 'games.chess.game.Game':
        """games.chess.game.Game: The reference to the Game instance this AI is playing.
        """
        return self._game # don't directly touch this "private" variable pls

    @property
    def player(self) -> 'games.chess.player.Player':
        """games.chess.player.Player: The reference to the Player this AI controls in the Game.
        """
        return self._player # don't directly touch this "private" variable pls

    def get_name(self) -> str:
        """This is the name you send to the server so your AI will control the player named this string.

        Returns:
            str: The name of your Player.
        """
        # <<-- Creer-Merge: get-name -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        return "Sahithi" # REPLACE THIS WITH YOUR TEAM NAME
        # <<-- /Creer-Merge: get-name -->>

    def start(self) -> None:
        """This is called once the game starts and your AI knows its player and game. You can initialize your AI here.
        """
        # <<-- Creer-Merge: start -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your start logic
        # <<-- /Creer-Merge: start -->>

    def game_updated(self) -> None:
        """This is called every time the game's state updates, so if you are tracking anything you can update it here.
        """
        # <<-- Creer-Merge: game-updated -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your game updated logic
        # <<-- /Creer-Merge: game-updated -->>

    def end(self, won: bool, reason: str) -> None:
        """This is called when the game ends, you can clean up your data and dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why your AI won or lost.
        """
        # <<-- Creer-Merge: end -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your end logic
        # <<-- /Creer-Merge: end -->>
    def make_move(self) -> str:
        """This is called every time it is this AI.player's turn to make a move.

        Returns:
            str: A string in Universal Chess Interface (UCI) or Standard Algebraic Notation (SAN) formatting for the move you want to make. If the move is invalid or not properly formatted you will lose the game.
        """
        # <<-- Creer-Merge: makeMove -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        fen = self.game.fen
        # empty grid for chess board
        grid = []
        # splits the fen string in components
        received_fen = fen.split()
        # split the received fen string by '/' for getting all the keys in the rows.
        rank_details = received_fen[0].split('/')
        # iterate through the details if the piece is a digit that many spaces should be appended in the state[chess board]. 
        # else add if the piece is a string add that piece to the chess board.
        for each_rank in rank_details:
            rank_pieces = []
            for piece in each_rank:
                if piece.isdigit():
                    for _ in range(int(piece)):
                        rank_pieces.append(0)
                else:
                    rank_pieces.append( piece )
            grid.append(rank_pieces)
        # print(grid)
        # retrieve the color from the fen string.
        mycolor= received_fen[1]
        # print("I am Playing : ", mycolor)
        colours= { "w": ['P','R','K','B','Q','N'], "b" :['p','r','k','b','q','n']}
        toNumber={"a": 0,"b": 1,"c": 2,"d": 3,"e": 4,"f": 5,"g": 6,"h": 7}
        toString={0: "a",1: "b",2: "c",3: "d",4: "e",5: "f",6: "g",7: "h"}
        # movement direction of all the distinct piece in the chess board.
        piece_directions = {
        "n" : [ [2,1], [2,-1], [1,-2], [-1,-2], [-2,-1], [-2,1], [-1,2], [1,2] ], 
        "b" : [ [1,1], [-1,1], [1,-1], [-1,-1] ],                                 
        "r" : [ [1,0], [-1,0], [0,-1], [ 0, 1] ],                                 
        "q" : [ [1,1], [-1,1], [1,-1], [-1,-1], [1,0], [-1,0], [0,-1], [0,1] ],   
        "k" : [ [1,1], [-1,1], [1,-1], [-1,-1], [1,0], [-1,0], [0,-1], [0,1] ],
        }

        move=[]
        # iterate through the the 8X8 chess board
        for i in range(8):
            for j in range(8):
                # retrieve the piece from the grid
                piece = grid[i][j]
                # if the piece if not 0 is not empty
                if  piece != 0:
                    # check if the color is matching to the color in the fen string
                    if((piece in colours["w"] and mycolor == "w") or (piece in colours["b"] and mycolor == "b")):
                        # if the piece if not a pawn
                        if (piece!= 'P' and piece !="p"):
                            # iterates through all the possible movements
                            for k in piece_directions[piece.lower()]:
                                done=False
                                steps=1
                                new_cell_row=i
                                new_cell_column=j
                                while not done:
                                    new_cell_row+= k[0]
                                    new_cell_column+= k[1]
                                    # if the cell is within the bounds and if empty move the piece or if the cell is not empty and already has a piece in it 
                                    # check if the piece is of same color or opponent. if same do not move the piece else move the piece and capture the opponent's piece.
                                    if(0 <= new_cell_row < 8 and 0 <= new_cell_column < 8):
                                        new_cell = grid[new_cell_row][new_cell_column]
                                        if(new_cell == 0):
                                            steps+=1
                                            move.append([i,j,new_cell_row,new_cell_column])   # Quiet Move
                                        elif((new_cell in colours["b"] and mycolor == "w") or (new_cell in colours["w"] and mycolor == "b")):
                                            move.append([i,j,new_cell_row,new_cell_column])   # Capture
                                            steps+=1
                                            done=True
                                        elif((new_cell in colours["b"] and mycolor == "b") or (new_cell in colours["w"] and mycolor == "w")):
                                            done=True
                                    else:
                                        done = True
                                    steps+=1
                                    # check if the piece is a sliding piece or not if not a sliding piece then donw is true else move.
                                    if (piece in ['n','N','K','k'] and steps>=2):
                                        done=True
                        # handling the pawn movements.           
                        else:
                            done=False
                            steps=1
                            new_cell_row=i
                            new_cell_column=j
                            # for the movement of direction check for the color
                            a=1
                            if(mycolor=='w'):
                                a=-1
                            while not done:
                                new_cell_row+=a*1
                                new_cell_column = j  
                                if(0<= new_cell_row < 8 and 0<= new_cell_column < 8):
                                    new_cell = grid[new_cell_row][new_cell_column]
                                    if(new_cell == 0):
                                        move.append([i,j,new_cell_row,new_cell_column])
                                    else:
                                        done=True
                                    # Checks if the pawn is on its starting square (second row for white, seventh row for black).
                                    # Iterates over the two diagonal squares adjacent to the pawn's current position.
                                    # Ensures the diagonal move is within the bounds of the board.
                                    # Checks if the diagonal square contains an opponent's piece (valid for capture).
                                    # Adds the diagonal capture move to the list of possible moves.
                                    if(steps==1):
                                        for l in range(-1,2,2): 
                                            if(0<= j+l <8 and ((grid[i+a][j+l] in colours["b"] and mycolor == "w") 
                                                                or (grid[i+a][j+l] in colours["w"] and mycolor == "b"))):
                                                move.append([i,j,i+a,j+l])
                                                done = True
                                else:
                                    done=True        
                                # If the pawn is in its starting position, it can move two squares forward. Steps are incremented to 2.                 
                                if(i==1 or i==6):
                                    steps+=1
                                else:
                                    done=True
                                if((steps ==4 and (i!=1 or i!=6)) or steps==3):
                                    done = True
                            # code for en-Passaunt move
                            if received_fen[3]!='-':
                                en_pausantpawn= received_fen[3]
                                en_pausanty=toNumber[received_fen[3][0]]
                                en_pausantx=8-int(received_fen[3][1])
                                # checks if the en-passaunt move is possible or not.
                                if(i+a*1==en_pausantx and j+1==en_pausanty):
                                    move.append([i,j,i+a,j+1])
                                elif(i+a*1==en_pausantx and j-1==en_pausanty):
                                    move.append([i,j,i+a,j-1])
        # moves for castling
        # checks if the castling is availiable or not
        if(received_fen[2]!="-"):
            # check for castling in both sides
            for side in received_fen[2]:
                # king side k to r or queen side r to k 
                if mycolor=="w":
                    if side == 'K' and "K2R" in rank_details[7]:
                        move.append([7,4,7,6])
                    if side == 'Q' and "R3K" in rank_details[7]:
                        move.append([7,4,7,2])
                else:
                    if side == 'k' and "k2r" in rank_details[0]:
                        move.append([0,4,0,6])
                    if side == 'q' and "r3k" in rank_details[0]:
                        move.append([0,4,0,2])
                                
        # append all moves into the array
        final_moves=[]
        for i in move:
            string= toString[i[1]]+str(8-i[0])+toString[i[3]]+str(8-i[2])
            final_moves.append(string)

        # print the number of moves with the sorted order all the moves and the randomly choosen move
        print(len(final_moves))
        final_moves = sorted(final_moves)
        print(' '.join(str(row) for row in final_moves))
        num1 = random.randint(0, len(final_moves)-1)
        print("My move = ",final_moves[num1])    
        return final_moves[num1]



        # <<-- /Creer-Merge: makeMove -->>

    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you need additional functions for your AI you can add them here
    # <<-- /Creer-Merge: functions -->>

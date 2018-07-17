#CS440 Project 3 Game
#Jiazhou Liu 4/25/2018
import sys

#set the look ahead steps, initial alpha value, and initial beta value
depthmax=15;
alpha=-1000;
beta=1000;

# given certain move and board, function returns the available moves player can make.
def availmove(move,board):
        #if the last move is 'null',we can make a move at any places on the board.Put all possible moves into lst.
        size=len(board)-2;
        if(move[0]=='n'):
                lst=[]
                for i in range(1,size+1):
                         for j in range(1,size+2-i):
                                 for k in range(1,4):
                                         move=(k,i,j,len(board[i])-j-1);
                                         lst.append(move);
        #else we can only make a move near the last move.Put all possible moves into lst1.
        else:
                row=move[1];
                col=move[2];
                lst1=[];
                lst1.append([row-1,col-1]);
                lst1.append([row-1,col]);
                lst1.append([row,col+1]);
                lst1.append([row+1,col]);
                lst1.append([row+1,col-1]);
                lst1.append([row,col-1]);
                lst=[]
                for t in lst1:
                   x=t[0];
                   y=t[1];
                   #if the place is empty, we can make a move at that place.Put those moves into lst.
                   if(board[x][y]==0):
                           for j in range(1,4):
                                   move=(j,x,y,len(board[x])-y-1);
                                   lst.append(move);
                 # if thre is no available moves around last move, which means we can make a move at any empty places. Put those moves into lst.                  
                if (len(lst)==0):
                        for i in range(1,size+1):
                          for j in range(1,size+2-i):
                               if(board[i][j]==0):   
                                 for k in range(1,4):
                                         move=(k,i,j,len(board[i])-j-1);
                                         lst.append(move);
        #return the move list as result.               
        return lst;

#given parsed input,alpha value, and beta value,function returns the move we choose to play.                
def choose(parseinput,alpha,beta):
        #set initial value, and get current board,last move and available moves.
        value=-10000;
        board=parseinput[0];
        move=parseinput[1];
        avail=availmove(move,board);
        #for every move, we do alpha-beta pruning and return the move with maximum value.
        for k in avail:
                color=k[0];
                x=k[1];
                y=k[2];
                board[x][y]=color;
                value1=alpha_beta(k,board,1,alpha,beta,depthmax);
                board[x][y]=0;
                if(value1>value):
                        value=value1;
                        choose=k;
        return choose;
                
                
                                 
                
#given input string, function parses it and return a list of two element.The first element is a matrix representing the board.
#The second element is a list representing the last move.
def parseinput(input_string):
        #split the input string to board part and last move part. Then put last move into list format.
        board,lastplay=input_string.split('LastPlay:');
        if (lastplay=="null"):
                lastplay=list(lastplay);
        else:
                lst=[]
                lst.append(lastplay[1]);
                lst.append(lastplay[3]);
                lst.append(lastplay[5]);
                lst.append(lastplay[7]);
                lastplay=lst;
                #change the the type of numbers in list from char to int.
                for i in range(len(lastplay)):
                        lastplay[i]=int(lastplay[i]);
        #remove the brackets in board,and put the result into lst1.Then reverse the order of lst1.
        lst1=board.split('][');
        lst1[0]=lst1[0][1:];
        lst1[-1]=lst1[-1][:-1];
        lst1.reverse();
        #make lst1 into a matrix and change the type of numbers in it from char to int. 
        for i in range(len(lst1)):
                lst1[i]=list(lst1[i]);
        for i in range(len(lst1)):
                for j in range(len(lst1[i])):
                        lst1[i][j]=int(lst1[i][j]);
        #put parsed board and last move into lst2 and return lst2.
        lst2=[];
        lst2.append(lst1);
        lst2.append(lastplay);
        return lst2;

# given last move and board, function decides whther there is a winner in the game. In other words, it tells if the game ends.
def terminal(move,board):
        #if no one make a move, game is still going. 
        if(move[0]=='n'):
                return 0;
        #if around the last move, there is a triangle of 3 different color moves, the game ends.
        row=move[1];
        col=move[2];
        #decide the other two colors based on the color of the last move.
        if (move[0]==1):
                x=2;
                y=3;
        elif(move[0]==2):
                x=1;
                y=3;
        elif(move[0]==3):
                x=1;
                y=2;
        #check each possible triangle with all possible color combination. If 3 color triangle appears, return 1.
        if ((board[row-1][col-1]==x and board[row-1][col]==y) or (board[row-1][col-1]==y and board[row-1][col]==x)  ):

              return 1; 

        if ((board[row-1][col]==x and board[row][col+1]==y) or (board[row-1][col]==y and board[row][col+1]==x)  ):

              return 1;

        if ((board[row][col+1]==x and board[row+1][col]==y) or (board[row][col+1]==y and board[row+1][col]==x)  ):

              return 1;


        if ((board[row+1][col]==x and board[row+1][col-1]==y) or (board[row+1][col]==y and board[row+1][col-1]==x)  ):

              return 1;


        if ((board[row+1][col-1]==x and board[row][col-1]==y) or (board[row+1][col-1]==y and board[row][col-1]==x)  ):

              return 1;


        if ((board[row][col-1]==x and board[row-1][col-1]==y) or (board[row][col-1]==y and board[row-1][col-1]==x)  ):

              return 1;
        #else return 0.
        return 0;

#given last move and board, function evaluates the current move, and returns a static value. 
def evaluate(move,board):
        color=move[0];
        row=move[1];
        col=move[2];
        score=0;
        count=0;
        #if there are more moves around current move, give a higher score.
        if(board[row-1][col]!=0):
                score+=10;
        if(board[row-1][col-1]!=0):
                score+=10;
        if(board[row][col+1]!=0):
                score+=10;
        if(board[row+1][col]!=0):
                score+=10;
        if(board[row+1][col-1]!=0):
                score+=10;
        if(board[row][col-1]!=0):
                score+=10;
        #if there are more pairs of different colors moves around current move, increase the count.
        if (board[row-1][col-1]!=board[row-1][col] and board[row-1][col-1]!=0 and board[row-1][col]!=0 ):

              count+=1;

        if (board[row-1][col]!=board[row][col+1] and board[row-1][col]!=0 and board[row][col+1]!=0  ):

              count+=1;

        if (board[row][col+1]!=board[row+1][col] and board[row][col+1]!=0 and board[row+1][col]!=0  ):

              count+=1;


        if (board[row+1][col]!=board[row+1][col-1] and board[row+1][col]!=0 and board[row+1][col-1]!=0  ):

              count+=1;


        if (board[row+1][col-1]!=board[row][col-1] and board[row+1][col-1]!=0 and board[row][col-1]!=0  ):

              count+=1;


        if (board[row][col-1]!=board[row-1][col-1] and board[row][col-1]!=0 and board[row-1][col-1]!=0  ):

              count+=1;
        #the product of the scoring scheme and count is the final score.
        score=score*count;

        #return the score;
        return score;
        










                
#given last move, board, current depth, alpha value, beta value, and maximum depth, the function performs the alpha-beta pruning algorithm.            
def alpha_beta(move,board,depth,alpha,beta,depthmax):
        #find all available moves.
        avail=availmove(move,board);
        # when game terminates, if we make the last move, return a super low score. if opponent makes the last move, return a super high score. 
        if(terminal(move,board)==1):
                if(depth%2==1):
                   return -1000;
                else:
                   return 1000;
        #if reach the maximum depth, evaluate the move.
        elif(depth==depthmax):
                return evaluate(move,board);
        #if max player makes last move, we try all possible moves, and return the max value and update the alpha value.
        elif(depth%2==1):
           value=-1000;           
           for k in avail:
                x=k[1];
                y=k[2];
                board[x][y]=k[0];
                value=max(value,alpha_beta(k,board,depth+1,alpha,beta,depthmax));
                board[x][y]=0;
                if(value>=beta):
                        return value;
                alpha=max(alpha,value);
        #if min player makes last move, we try all possible moves, and return the min value and update the beta value.
        else:
            value=1000;
            for k in avail:
                   x=k[1];
                   y=k[2];
                   board[x][y]=k[0];
                   value=min(value,alpha_beta(k,board,depth+1,alpha,beta,depthmax));
                   board[x][y]=0;
                   if(value<=alpha):
                        return value;
                   beta=min(alpha,value);
        return value;
        
        
        
#parse the input string, i.e., argv[1]
parseinput=parseinput(sys.argv[1]);
                
#perform intelligent search to determine the next move
choice=choose(parseinput,alpha,beta)
string="("+str(choice[0])+","+str(choice[1])+","+str(choice[2])+","+str(choice[3])+")"
#print to stdout for AtroposGame
sys.stdout.write(string);


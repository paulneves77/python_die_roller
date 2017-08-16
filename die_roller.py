# this code is designed to query a user for a die code, simulate that roll
# with pseudo random number generators, and save that output to a selected file

# start messages
print("Type 'help' in the die code to see examples\nOr 'stop' to end the program\n")

# initialize values
import random
import time
die_code = '0'
save_dir = raw_input("Save file name: ")

def get_die_code( die_code ):
    #   GET_DIE_CODE extracts X, Y, and Z from string 'X1dY1+X2dY2+...+Z'
    #   where X = (X1, X2, ..., XN) and same for Y
    #
    #   also pulls out advantage or disadvantage into ADV, where
    #   0 is no advantage, +1 means take the highest die, +2 means take
    #   the highest two dice, etc, and -1 means take the lowest die, -2
    #   means take the lowest two dice, etc
    #   advantage is 2d20h1 (takes highest one), disadvantage is 2d20l1

    
    # remove comment for simplicity
    hash_location = die_code.find('#')
    if hash_location != -1:
        COMMENT = die_code[hash_location+1:]
        die_code = die_code[:hash_location]
        die_code.replace(' ','')
    
    #finds the location of +, d, h, and l in the code
    plus_locations = [-1,] + [n for n in range(len(die_code)) if die_code.find('+',n) == n] + [n for n in range(len(die_code)) if die_code.find('-',n) == n]
    plus_locations.sort()
    d_locations = [n for n in range(len(die_code)) if die_code.find('d',n) == n]
    lh_locations = [n for n in range(len(die_code)) if die_code.find('l',n) == n] + [n for n in range(len(die_code)) if die_code.find('h',n) == n]
    
    #defines starting values of outputs
    Z = 0
    X = []
    Y = []
    ADV = []
    COMMENT = ''

    #if there aren't any dice being rolled, it's all just Z
    if d_locations == []:
        Z = int(die_code)
        
    else:
        #remove the Z from everything for simplicity
        if d_locations[-1] < plus_locations[-1]:
            Z = int(die_code[(plus_locations[-1]):])
            die_code = die_code[:plus_locations[-1]]
        
        #now we know how long X, Y, and ADV have to be
        X = [0,]*len(d_locations)
        Y = [0,]*len(d_locations)
        ADV = [0,]*len(d_locations)
        
        #redefine where the pluses and d's are
        if die_code[0] != '-':
            plus_locations = [-1,] + [n for n in range(len(die_code)) if die_code.find('+',n) == n] + [n for n in range(len(die_code)) if die_code.find('-',n) == n] + [len(die_code),]
        else:
            plus_locations = [n for n in range(len(die_code)) if die_code.find('+',n) == n] + [n for n in range(len(die_code)) if die_code.find('-',n) == n] + [len(die_code),]
        plus_locations.sort()
        
        d_locations = [n for n in range(len(die_code)) if die_code.find('d',n) == n] + [len(die_code),]
        
        #for each type of die rolled
        for i in range(len(d_locations)-1):
            #get how many were rolled (all numbers before 'd')
            if (plus_locations[i]+1-d_locations[i])!= 0:
                X[i] = int(die_code[(plus_locations[i]+1):(d_locations[i])])
            else:
                X[i] = 1
            if die_code[plus_locations[i]] == '-':
                X[i] = -X[i]
            #for each location with an l or h
            for m in lh_locations:
                #check if that location is in this type of die rolled
                if d_locations[i]<m & m<d_locations[i+1]:
                    #extract how many sides there are and what the advantage was
                    Y[i] = int(die_code[(d_locations[i]+1):m]);
                    ADV[i] = int(die_code[(m+1):(plus_locations[i+1])]);
                    if die_code[m] == 'l':
                        ADV[i] = -ADV[i];
                        
            #if the roll wasn't with advantage, just get the number of sides
            if ADV[i] == 0:
                Y[i] = int(die_code[(d_locations[i]+1):(plus_locations[i+1])])
    out = {'X':X, 'Y':Y, 'Z':Z, 'ADV':ADV, 'COMMENT':COMMENT}
    return out

# run until the user is done
while (die_code != "stop"):
    die_code = raw_input("\nDie code: ") # get raw_input

    # user asked for help
    if die_code == "help":
        print("\nYou can enter a die code into the 'Die code' prompt. The program will then simulate the given roll and save it to the previously) specified file.\n\n")
        print("To roll a single die with N sides, enter 'dN'")
        print("To roll X dice with N sides and add them together, enter 'XdN'")
        print("Or multiple dice with 'XdN+YdM+...'")
        print("To then add B to the sum, enter 'XdN+B'\n")
        print("To only count the highest H dice, type 'XdNhH'")
        print("To only count the lowest L dice, type 'XdNlL'\n")
        print("To add a comment to the save file, type '# <comment>' after the die code\n")
        
        
    # user asked to stop
    elif die_code == "stop":
        print("Stopping")
        
    # must be a die code if not help or stop
    else:
        
        #parse the die code
        out = get_die_code(die_code)
        X = out['X']
        Y = out['Y']
        Z = out['Z']
        ADV = out['ADV']
        COMMENT = out['COMMENT']
        
        #roll the die code
        roll_list = []
        roll_total = 0
        
        for i in range(len(X)): #for each die type
            this_roll_list = []
            this_roll_total = 0
            
            #for each die in that type
            for j in range(abs(X[i])):
                this_roll = random.randint(1,Y[i]) #roll that die
                this_roll_list = this_roll_list + [this_roll,] #add to list of rolls
                if ADV[i] == 0:
                    this_roll_total = this_roll + this_roll_total #add to total roll
            
            #do advantage
            if ADV[i] > 0:
                sorted_list = sorted(this_roll_list)
                for k in sorted_list[-ADV[i]:]:
                    this_roll_total = this_roll_total + k
            
            #do disadvantage
            if ADV[i] < 0:
                sorted_list = sorted(this_roll_list)
                for k in sorted_list[:-ADV[i]]:
                    this_roll_total = this_roll_total + k

            if X[i] < 0:
                this_roll_total = -this_roll_total
                this_roll_list = [-x for x in this_roll_list]
            
            roll_list = roll_list + this_roll_list
            roll_total = roll_total + this_roll_total
        
        roll_total = roll_total + Z
        
        #save the result
        file = open(str(save_dir),"a")
        file.write(time.ctime()+':\n"'+die_code+'":\n'+str(roll_total)+' '+str(roll_list)+' '+str(COMMENT)+'\n\n')
        file.close()
        
        #display the result
        print(str(roll_total)+' '+str(roll_list))

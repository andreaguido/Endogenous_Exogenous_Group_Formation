from itertools import combinations
import numpy as np
import random as rn
rankingmatrix = []
temp_list_char = "3,2,1,5,4,7,8,9,10,11,15,16,6,12,14,13,17,18"
# create rnaking matrix
for i in list(range(0,18)):
    temp_list = list(int(i) for i in temp_list_char.split(","))
    temp_list.insert(i, 0)
    # print("this is temp list ", temp_list)
    rankingmatrix.append(temp_list)
    # print("this is the ranking matrix ", rankingmatrix)
rankingmatrix = np.array(rankingmatrix)

# let's assume it
#rankingmatrix = np.array([[0,1,3,2,4,5,6,8,7],
#                          [1,0,3,2,4,5,6,7,8],
#                          [1,2,0,3,4,5,8,6,7],
#                          [2,1,3,0,4,5,7,6,8],
#                          [1,2,3,4,0,5,7,6,8],
#                          [2,3,1,4,5,0,6,8,7],
#                          [1,2,3,4,5,6,0,7,8],
#                          [1,2,3,6,5,4,0,8,7],
#                          [5,2,3,4,1,6,0,7,8]])

# method 1
#rank_sum = list(map(sum,zip(*rankingmatrix)))

# method 2
initial_number_players = list(range(0,18)) # change here when implementing in otree (6 = numebr of players)
formed_groups = []  # list including all formed groups

for j in list(range(1,7)): # change here number of groups (variable..
    print("group number ", j)
    print("players available ", initial_number_players)
    comb = combinations(initial_number_players, 3)
    rank_sum = [] # sum of ranks in a group
    min_group = [] # group with min sum of ranks
    chosen_group = [] # chosen group with min (actual array of players)

    for i in list(comb):
        print("possible groups ", i)
        idx = np.array(i) # get index of the row and col as array
        subset_rankingmatrix = (rankingmatrix[idx[:, None], idx]) # subset matrix using idx
        rank_sum.append(np.sum(subset_rankingmatrix)) # sum values of the matrix
    print("this is rank sum", rank_sum)

    min_group = rn.sample([i for i, x in enumerate(rank_sum) if x == min(rank_sum)], 1) # get group with min score
    comb2 = combinations(initial_number_players, 3)
    chosen_group = [i for i in comb2][min_group[0]]
    #print(all_combinations)
    print("Min group is", min_group, "that is ", chosen_group)
    formed_groups.append(chosen_group)
    # update groups available
    initial_number_players = [value for value in initial_number_players if value not in chosen_group]

list_players_temp = np.array(formed_groups).flatten()
list_players = tuple(np.array(list_players_temp)+1)
matrix_players = []
i=0
j=0
while i < (int(len(list_players)/3)): # groups of 3
                temp = list_players[j:(j+3)]
                print(temp)
                matrix_players.append(temp)
                i += 1
                j += 3
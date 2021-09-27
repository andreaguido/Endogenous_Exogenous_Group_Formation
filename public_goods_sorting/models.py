from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
#from django.contrib.postgres.fields import ArrayField
#from django import forms
import json
from operator import itemgetter
import random as rn
from itertools import combinations
import numpy as np

doc = """
This is a public goods game with 3 players with sorting mechanisms.
"""


class Constants(BaseConstants):
    name_in_url = 'public_goods_sorting'
    players_per_group = 3
    num_others_per_group = players_per_group - 1
    num_rounds = 11 # change it to 11 (1 one shot + 10 rounds)
    endowment = 20

    instructions_template = 'public_goods_sorting/instructions.html'
    consentment_template = 'public_goods_sorting/consentment_form.html'

    multiplier = 1.8 # K of the formula MPCR = K/Ngroup


class Subsession(BaseSubsession):
    treatment = models.StringField(initial="NA") # variable recording treatment
    number_of_groups = models.IntegerField() # variable recording number of groups in the session

    def creating_session(self):
        # recall: T1 Endogenous, T2 Exogenous à la Gachter and Thoni, T3 exogenous semi-random
        self.treatment = self.session.config['treatment']
        # get number of players (for python loops below, add 1)
        self.number_of_groups = int(self.session.num_participants / Constants.players_per_group + 1)

    def Endogenous_sorting(self):
        # function used in endogenous sorting
        print("######### IM IN ENDOGENOUS FUNCTION ###########")
        ## init vars used in this function
        rankingmatrix = []  # matrix saving everyone's ranking of each other
        players = self.get_players()  # array of players
        formed_groups = []  # list including all formed groups
        i = 0  # indicator for loops

        # function to get mutual ranking matrix (See Unel et al. 2005 EJ)
        for p in players:
            temp_list_char = p.list_ID_rank  # this is a char. array including the ranking of subject p given in page Ranking.html (passed through JavaScript)
            temp_displayed_id_char = p.displayed_ID # this is a char. array including the IDs of others players in the session displayed to the subject (page Ranking.html; passed through JavaScript)
            temp_list = list(int(i) for i in temp_list_char.split(",")) # de-char
            temp_list_id = list(int(i) for i in temp_displayed_id_char.split(",")) # de-char
            temp_list_sorted = [x for _, x in sorted(zip(temp_list_id, temp_list))] # here sort temp_list based on temp_list_id
            temp_list_sorted.insert(i, 0) # add 0 for matrix diagonal
            print("this is temp list sorted ", temp_list_sorted)
            rankingmatrix.append(temp_list_sorted) # append values and start over with the next player
            print("this is the ranking matrix in the process ", rankingmatrix)
            i += 1

        rankingmatrix = np.array(rankingmatrix)  # assign matrix of rankings as np array instead of list for computational reasons (see slicing below)
        initial_number_players = list(range(0, self.session.num_participants))  # get initial number of player and their ids
        print("this is the final ranking matrix ", rankingmatrix)
        print("these are the players available for grouping in the session, ", initial_number_players)

        # function to make optimal groups (two loops, j=groups; i=individuals)
        for j in list(range(1, self.number_of_groups)):
            comb = combinations(initial_number_players, 3)  # compute combinations
            rank_sum = []  # init var sum of ranks in a group

            # function to find min.ranking groups
            for i in list(comb):
                idx = np.array(i)  # get index of the row and col as array
                subset_rankingmatrix = (rankingmatrix[idx[:, None], idx])  # subset matrix using idx
                rank_sum.append(np.sum(subset_rankingmatrix))  # sum values of the matrix
            print("this is rank sum of each group ", rank_sum)

            # find group with min ranking (randomly solve ties)
            ## find minimum ranking sum
            min_group = rn.sample([i for i, x in enumerate(rank_sum) if x == min(rank_sum)], 1)
            ## save group composition
            comb2 = combinations(initial_number_players, 3) ## note: don't know why can't use comb, but i needed to re-create similar variable
            chosen_group = [i for i in comb2][min_group[0]]
            print("Min group is", min_group, "that is ", chosen_group)
            # store group list
            formed_groups.append(chosen_group)

            # update groups available remaining by eliminating grouped subjects
            initial_number_players = [value for value in initial_number_players if value not in chosen_group]

        # get list of players to add 1
        list_players = np.array(formed_groups).flatten() + 1
        list_players.tolist()
        print("this is list players ", list_players)

        matrix_players = []
        i = 0
        j = 0
        while i < (int(len(list_players) / 3)):  # groups of 3
            temp = list_players[j:(j + 3)]
            print("this is temp ", temp)
            matrix_players.append(temp)
            i += 1
            j += 3
#    if self.treatment == "T1": # endogenous treatment T1
        print("I'm in treatment T1 @@@@@@@@@@@@@@@@@@")
        print("this is formed groups", print([l.tolist() for l in matrix_players]))
        print("this is the matrix of players", self.get_group_matrix())
        [r.set_group_matrix([l.tolist() for l in matrix_players]) for r in self.in_rounds(2, Constants.num_rounds)]
        print(" this is the group matrix in round 2 ", self.in_round(2).get_group_matrix())
        print(" this is the group matrix in round 3 ", self.in_round(3).get_group_matrix())

    def Exogenous_sortings(self):
        # create list of Player N and RankSum
        players = self.get_players()
        list_temp = []

#        if self.treatment == "T1": # endogenous treatment T1
#            print("I'm in treatment T1 @@@@@@@@@@@@@@@@@@")
#            i=1
#            for p in players:
#                rs_temp = [i, p.rank_sum]
#                list_temp.append(rs_temp)
#                i += 1
#            list_temp_sorted = sorted(list_temp, key = itemgetter(1))
#            print("this is list ordered ")
#            list_players = list(map(itemgetter(0),list_temp_sorted))
#            i = 0
#            j = 0
#            matrix_players = []
#            while i < (int(len(list_players)/3)): # groups of 3
#                temp = list_players[j:(j+3)]
#                matrix_players.append(temp)
#                i += 1
#                j += 3
#            print("Matrix players : ", matrix_players)
#            #self.set_group_matrix(matrix_players)
#            #print(self.get_group_matrix())
#            print(" this is the group matrix in round 1 ", self.get_group_matrix())
#            [r.set_group_matrix(matrix_players) for r in self.in_rounds(2, Constants.num_rounds)]
#            print(" this is the group matrix in round 2 ", self.in_round(2).get_group_matrix())
#            print(" this is the group matrix in round 3 ", self.in_round(3).get_group_matrix())

        if self.treatment == "T2": # exogenous T2 à la Gachter and Thoeni
            print("I'm in treatment T2 @@@@@@@@@@@@@@@@@ò")
            i = 1
            # create list of players with their contributions
            for p in players:
                rs_temp = [i, p.contribution]
                list_temp.append(rs_temp)
                i += 1
            # sort list
            list_temp_sorted = sorted(list_temp, key = itemgetter(1), reverse = True)
            print("this is list ordered ")
            list_players = list(map(itemgetter(0),list_temp_sorted))
            i = 0
            j = 0
            matrix_players = []
            # slice the distribution and create groups of 3
            while i < (int(len(list_players)/3)): # groups of 3
                temp = list_players[j:(j+3)]
                matrix_players.append(temp)
                i += 1
                j += 3
            print("Matrix players : ", matrix_players)
            #self.set_group_matrix(matrix_players)
            #print(self.get_group_matrix())
            print(" this is the group matrix in round 1 ", self.get_group_matrix())
            [r.set_group_matrix(matrix_players) for r in self.in_rounds(2, Constants.num_rounds)]
            print(" this is the group matrix in round 2 ", self.in_round(2).get_group_matrix())
            print(" this is the group matrix in round 3 ", self.in_round(3).get_group_matrix())


        if self.treatment == "T3":  # exogenous T3
            print("I'm in treatment T3 @@@@@@@@@@@@@@")
            i = 1
            # get players contributions
            for p in players:
                rs_temp = [i, p.contribution]
                list_temp.append(rs_temp)
                i += 1
            # sort them
            list_temp_sorted = sorted(list_temp, key=itemgetter(1))
            print("This is the list ordered (ID, CONTR) ", list_temp_sorted)
            # get IDs ordered
            list_players = list(map(itemgetter(0),list_temp_sorted))
            # compute thresholds (to divide groups in 3 classes)
            q = int(int(len(list_players))/3)
            print("this is q : ", q)
            # get players in TOP - MIDDLE - BOTTOM
            ID_BOT = list_players[0:q]
            ID_MID = list_players[q:(q+q)]
            ID_TOP = list_players[(q+q):len(list_players)]

            print("THIS IS TOP : ", ID_TOP)
            print("THIS IS MID : ", ID_MID)
            print("THIS IS BOT : ", ID_BOT)

            # get randomly 1 from each class
            ## reshuffle first
            ID_TOP_resh = rn.sample(ID_TOP, len(ID_TOP))
            ID_MID_resh = rn.sample(ID_MID, len(ID_MID))
            ID_BOT_resh = rn.sample(ID_BOT, len(ID_BOT))
            print("THIS IS TOP RESH: ", ID_TOP_resh)
            print("THIS IS MID RESH: ", ID_MID_resh)
            print("THIS IS BOT RESH: ", ID_BOT_resh)
            ## get 'em
            w = 0
            matrix_players = []
            # create groups
            while w < int(len(ID_BOT)):
                print("I m in while")
                temp = [ID_TOP_resh[w], ID_MID_resh[w], ID_BOT_resh[w]]
                matrix_players.append(temp)
                w+=1
            print("Matrix players : ", matrix_players)
            #self.set_group_matrix(matrix_players)
            print(" this is the group matrix in round 1 ", self.get_group_matrix())
            [r.set_group_matrix(matrix_players) for r in self.in_rounds(2, Constants.num_rounds)]
            print(" this is the group matrix in round 2 ", self.in_round(2).get_group_matrix())
            print(" this is the group matrix in round 3 ", self.in_round(3).get_group_matrix())


    def vars_for_admin_report(self):
        contributions = [
            p.contribution for p in self.get_players() if p.contribution != None
        ]
        if contributions:
            return dict(
                avg_contribution=sum(contributions) / len(contributions),
                min_contribution=min(contributions),
                max_contribution=max(contributions),
            )
        else:
            return dict(
                avg_contribution='(no data)',
                min_contribution='(no data)',
                max_contribution='(no data)',
            )


class Group(BaseGroup):
    total_contribution = models.IntegerField()
    individual_share = models.CurrencyField()


    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = (
            self.total_contribution * Constants.multiplier / Constants.players_per_group
        )
        for p in self.get_players():
            p.payoff = (Constants.endowment - p.contribution) + self.individual_share


class Player(BasePlayer):
    contribution = models.IntegerField(
        min=0, max=Constants.endowment, doc="""The amount contributed by the player"""
    )
    list_ID_rank = models.CharField()
    displayed_ID = models.CharField()
    # add timeouts for important pages
    timeout_ranking = models.IntegerField()
    timeout_contribution = models.IntegerField()
#    rank_sum = models.IntegerField()
    age = models.IntegerField()
    gender = models.StringField(
        choices=[['Homme', 'Homme'], ['Femme', 'Femme'], ['Autres', 'Autres']],
        label='Gender',
        widget=widgets.RadioSelect)
    #country = models.StringField()
    email = models.StringField()
    payment_Euro = models.FloatField()
    q_triad = models.StringField()

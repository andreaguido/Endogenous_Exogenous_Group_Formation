from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
from django import forms
from . import models
import random
import string

class Consentment(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

class Welcome(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

class Introduction(Page):
    """Description of the game: How to play and returns expected"""
    def is_displayed(self):
        return self.subsession.round_number == 1
    pass

class Contribute(Page):
    """Player: Choose how much to contribute"""

    form_model = 'player'
    form_fields = ['contribution']

    def vars_for_template(self):
        return dict(round = self.subsession.round_number - 1)

    def before_next_page(self):
        if self.timeout_happened:
            self.player.contribution = random.randint(0,Constants.endowment)
            self.player.timeout_contribution = 1
        else:
            self.player.timeout_contribution = 0


class ManualAdvance1(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1
    pass

class Quiz(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1
    pass

class IntroductionPart2(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1
    pass

class ManualAdvance2(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1
    pass

class ManualAdvance3(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1
    pass

class ManualAdvance4(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1
    pass

class ManualAdvance5(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1
    pass

class WaitPage1(WaitPage):
    wait_for_all_groups = True

class WaitPage2(WaitPage):
    after_all_players_arrive = 'set_payoffs'
    body_text = "Waiting for other participants."

class Ranking(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1
    """Here players define the ranking"""
    form_model = 'player'
    form_fields = ['list_ID_rank', 'displayed_ID']

    def before_next_page(self):
        if self.timeout_happened:
            list_ID_rank_temp = list(range(1,Constants.num_others_per_group+1))
            self.player.list_ID_rank = ','.join(map(str,list_ID_rank_temp))
            self.player.displayed_ID = self.player.list_ID_rank
            self.player.timeout_ranking = 1
        else:
            self.player.timeout_ranking = 0


    def vars_for_template(self):
        # reshuffle
        #temp = list(string.ascii_uppercase)
        #ID_letter = temp[0:len(self.player.get_others_in_subsession())]
        #id_players_shuffled = random.sample(ID_letter, len(ID_letter))
        shuffled_players = random.sample(self.player.in_round(1).get_others_in_subsession(), len(self.player.in_round(1).get_others_in_subsession()))
        id_players_shuffled = [p.id_in_subsession for p in shuffled_players]
        others_contributions = [p.contribution for p in shuffled_players]
        print("IM PRINTING RESHUFFLED ID PLAYERS ", (id_players_shuffled), " & contr ", others_contributions)
        # reshuffle contributions of other players
        return dict(total_earnings=self.group.total_contribution * Constants.multiplier,
                    others_contributions = others_contributions,
                    nplayers=len(self.subsession.get_players()),
                    nothers = len(self.subsession.get_players())-1,
                    id_players=id_players_shuffled
                    )

class WaitPage3(WaitPage):
    """Here compute the matrix of rankings"""
    def is_displayed(self):
        return self.subsession.round_number == 1

    body_text = "You will be informed about the regrouping option implemented once everyone submits their rankings"
    wait_for_all_groups = True
    after_all_players_arrive = 'Endogenous_sorting'

class WaitPage4(WaitPage):
    def is_displayed(self):
        return self.subsession.round_number == 1

    wait_for_all_groups = True
    after_all_players_arrive = 'Exogenous_sortings'

class MechanismDisplay(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return dict(
            treatment=self.subsession.treatment,
        )

class InfoNewMembers(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        otherplayersinfuturegroup = self.player.in_round(2).get_others_in_group()
        contributionstodisplay = [p.in_round(1).contribution for p in otherplayersinfuturegroup]
        return dict(
            treatment=self.subsession.treatment,
            otherplayersinfuturegroup=otherplayersinfuturegroup,
            contributionstodisplay=contributionstodisplay
        )

class Results(Page):
    """Players payoff: How much each has earned"""
    def is_displayed(self):
        return self.subsession.round_number > 1
    def vars_for_template(self):
        # get contributions and reshuffle them
        temp=[p.contribution for p in self.player.get_others_in_group()]
        contributions_resh=random.sample(temp, len(temp))
        return dict(
            total_earnings=self.group.total_contribution * Constants.multiplier,
            contribution_resh=contributions_resh,
            round=self.subsession.round_number - 1
        )

class Part3Test(Page):
    form_model = 'player'
    form_fields = ['q_triad']

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

class Demographics(Page):

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    form_model = 'player'
    form_fields = ['age',
                   'country']

class FinalResults(Page):
    """final results of the experiment"""
    form_model = 'player'
    form_fields = ['comments']
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        return dict(
            part_1_payoff=self.player.in_round(1).payoff,
            part_2_payoff=self.participant.payoff - self.player.in_round(1).payoff,
            total_payoff=self.participant.payoff,
            part_1_contribution=self.player.in_round(1).contribution,
            part_1_total_contribution=self.group.in_round(1).total_contribution,
            total=self.participant.payoff,
            amount_paid=self.participant.payoff/17
        )

page_sequence = [Welcome,
                 Consentment,
                 ManualAdvance1,
                 Introduction,
                 ManualAdvance2,
                 #Quiz,
                 #ManualAdvance3,
                 Contribute,
                 WaitPage1,
                 WaitPage2,
                 ManualAdvance4,
                 IntroductionPart2,
                 ManualAdvance5,
                 Ranking,
                 WaitPage3,
                 WaitPage4,
                 MechanismDisplay,
                 InfoNewMembers,
                 Results,
                 #Part3Test,
                 #Demographics,
                 FinalResults]

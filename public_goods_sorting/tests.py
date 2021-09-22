from otree.api import Currency as c, currency_range, SubmissionMustFail, Submission
from . import pages
from ._builtin import Bot
from .models import Constants
import random as rn

class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            yield Submission(pages.Welcome, timeout_happened=True, check_html=False)
            yield (pages.Consentment)
            yield Submission(pages.ManualAdvance1, timeout_happened=True, check_html=False)
            yield (pages.Introduction)
            yield Submission(pages.ManualAdvance2, timeout_happened=True, check_html=False)
            yield Submission(pages.Quiz, timeout_happened=True, check_html=False)
            yield Submission(pages.ManualAdvance3, timeout_happened=True, check_html=False)
            yield Submission(pages.Contribute, dict(contribution=rn.randint(0,20)))
            yield Submission(pages.ManualAdvance4, timeout_happened=True, check_html=False)
            yield (pages.IntroductionPart2)
            yield Submission(pages.ManualAdvance5, timeout_happened=True, check_html=False)
            yield Submission(pages.Ranking, dict(
                list_ID_rank="3,2,1,5,4,7,8,9,10,11,15,6,12,14,13",
            displayed_ID="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15"),
                             check_html=False)
            yield (pages.MechanismDisplay)
            yield (pages.InfoNewMembers)

        if self.round_number > 1:
            yield (pages.Contribute, dict(contribution=rn.randint(0,20)))
            yield (pages.Results)
            if self.round_number == Constants.num_rounds:
                yield (pages.FinalResults)

#        if case == 'basic':
#            if self.player.id_in_group == 1:
#                for invalid_contribution in [-1, 101]:
#                    yield SubmissionMustFail(
#                        pages.Contribute, {'contribution': invalid_contribution}
#                    )
#
#        contribution = {'min': 0, 'max': 100, 'basic': 50}[case]
#
#        yield (pages.Contribute, {"contribution": contribution})
#
#        yield (pages.Results)
#
#        if self.player.id_in_group == 1:
#
#            if case == 'min':
#                expected_payoff = 100
#            elif case == 'max':
#                expected_payoff = 200
#            else:
#                expected_payoff = 150
#            assert self.player.payoff == expected_payoff
#
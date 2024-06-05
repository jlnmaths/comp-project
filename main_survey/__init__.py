from otree.api import *
import numpy as np

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'comp_group4'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

def likertScale(label, low, high, n, blank = False):
    if low != '':
        CHOICES = [(0, str(0) + " (" + low + ")")]
    else:
        CHOICES = [(0, str(0))]
    for x in range(1, n):
        CHOICES = CHOICES + [(x, str(x))]
    if high != '':
        CHOICES = CHOICES + [(n, str(n) + " (" + high + ")")]
    else:
        CHOICES = CHOICES + [(n, str(n))]
    return models.IntegerField(
        choices=CHOICES,
        label=label,
        widget=widgets.RadioSelectHorizontal,
        blank=blank,
    )

class Player(BasePlayer):
    assessment = models.IntegerField(min=0, max=100, label="What do you think is the probability that the main observation behind the question mark (?) is a 1?")
    certainty =likertScale(
        'On a scale of 0 to 10, on which 0 means "very uncertain" and 10 means "very certain", how certain are you that your assessment was correct?',
        '', '', 10)

    payround = models.IntegerField(initial = 1)
    treatment = models.StringField(initial = 1)
    quiz1 = models.StringField(label='True or false? You have to make an investment decision.',
        choices=['True', 'False'])

# functions
def creating_session(subsession: Subsession):
    import itertools
    import random
    treatments = itertools.cycle(['bull','bear']) #itertools.cycle([0, 0, 0,  1, 1, 2, 3, 3, 3, 4, 5, 5])
    for player in subsession.get_players():
        player.treatment = next(treatments)
        if subsession.round_number == 1:
            player.participant.payround = random.randint(1,2)
        player.payround = player.participant.payround

def set_payoff(player: Player):
    import numpy as np
    risky = np.random.normal(0.06, 0.178)
    safe = 0.03
    ret = player.assessment/100 * risky + (100 - player.assessment)/100*safe
    player.participant.risky = risky
    player.participant.safe = safe

    if ret > 0.46:
        ret = 0.46
    if ret < -0.46:
        ret = -0.46
    player.participant.payoff = ret
    return ret
# PAGES
class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1

class Choice1(Page):
    form_model = 'player'
    form_fields = ['assessment']
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import time
        if player.subsession.round_number == player.payround:
            set_payoff(player)

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number < 2


class Choice2(Page):
    form_model = 'player'
    form_fields = ['assessment']

    @staticmethod
    def vars_for_template(player: Player):
        if player.treatment == 'bull':
            keyword = 'Invest in the stock market now to ride economic growth and innovation. With record earnings and booming sectors, secure your financial future!'
        else:
            keyword = 'Market downturns offer chances to buy strong stocks cheap. Defensive sectors like utilities and healthcare provide stability. Seize the opportunity!'

        return dict(
            keyword=keyword,
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import time
        if player.subsession.round_number == player.payround:
            set_payoff(player)

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number > 1


class Certainty(Page):
    form_model = 'player'
    form_fields = ['certainty']
    def is_displayed(player: Player):
        return player.round_number < 6


class Quiz(Page):
    form_model = 'player'
    form_fields = ['quiz1']

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(quiz1='True')
        if values != solutions:
            return "One or more responses were unfortunately wrong."

    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1




class Results(Page):
    pass


page_sequence = [Instructions, Choice1, Choice2, Certainty]

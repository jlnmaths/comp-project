from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'demographics'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    years = range(1920, 2005)
    list_of_education = [
        'No School Graduation',
        'High School Graduation',
        "Bachelor's degree or equivalent",
        "Master's degree or equivalent",
        'Doctorate'
    ]


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
    yearOfBirth = models.IntegerField(choices=C.years, label="What is your year of birth?")
    male = models.IntegerField(widget=widgets.RadioSelectHorizontal, choices=[[0, 'female'], [1, 'male'], [99, 'diverse'],
                                                                                [98, 'Do not want to say'], ],
                               label="What is your gender?")
    education = models.StringField(choices=C.list_of_education,
                                   label="What is your highest level of education?")
    country = models.StringField(label="In which country do you live?")

    study = models.StringField(label="Are you a student at university? If yes, what is your major?")
    politics =likertScale(
        'On a scale of 0 to 10, on which 0 means far left and 10 means far right, where do you place your political views?',
        '', '', 10)

    simplicity_1 =likertScale(
        'How strongly do you agree with the following statement? I prefer simple explanations (0 to 10, 0 = absolutely not, 10 = absolutely).',
        '', '', 10)
    simplicity_2 = models.StringField(label="Do you agree with the following statement? I am convinced that most people prefer simple explanations.",
        choices=['Yes', 'No'])
    dataverbal_1 =likertScale(
        'How strongly do you agree with the following statement? I prefer data over verbal explanations (0 to 10, 0 = absolutely not, 10 = absolutely).',
        '', '', 10)
    dataverbal_2 = models.StringField(label="Do you agree with the following statement? I am convinced that most people prefer data over verbal explanations.",
        choices=['Yes', 'No'])
    finishexptime = models.IntegerField(initial=0) #end of experiment
    startdemotime = models.IntegerField(initial=0) #start of demographics survey


    HintHelpful = likertScale(
        'Did you think the hints were helpful? Please use a scale from 0 to 10, where a 0 means you found them "not helpful at all" and a 10 means you found them "very helpful".',
        '', '', 10)

    HintMisleading = likertScale(
        'Did you think the hints were misleading? Please use a scale from 0 to 10, where a 0 means you believe they were "not misleading at all" and a 10 means you believe they were "very misleading".',
        '', '', 10)

    TimeSurvey = likertScale(
        'How willing are you to give up something today in order to get more of it in the future? Please use a scale from 0 to 10, where a 0 means you are "completely unwilling to give up something today for more tomorrow" and a 10 means you are "very willing to give up something today for more tomorrow".',
        '', '', 10)
    RiskSurvey = likertScale(
        'How willing are you in general to take risk? Please use a scale from 0 to 10, where a 0 means you are "completely unwilling to take risks" and a 10 means you are "very willing to take risks".',
        '', '', 10)
    AltruismSurvey = likertScale(
        'How do you assess your willingness to share with others without expecting anything in return when it comes to charity? Please use a scale from 0 to 10, where 0 means you are "completely unwilling to share" and a 10 means you are" very willing to share”.',
        '', '', 10)

# PAGES
class Demographics(Page):
    form_model = 'player'
    form_fields = ['yearOfBirth', 'male', 'country', 'education', 'study', 'RiskSurvey']

    def vars_for_template(player: Player):
        import time
        player.startdemotime = int(time.time())
        return dict()

class ResultsWaitPage(WaitPage):
    pass

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):

        return dict()

page_sequence = [Demographics, Results]

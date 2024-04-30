from os import environ


SESSION_CONFIGS = [
    dict(
        name='Mental_Models_Experiment',
        display_name="Mental_Models_Experiment",
        app_sequence=['main_survey', 'results_and_demographics'],
        num_demo_participants=250,
        completionlink='https://app.prolific.co/submissions/complete?cc=11111111'
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    {'limesurvey_link': 'https://limesurvey.urz.uni-heidelberg.de/index.php/114547?lang=de'},
    real_world_currency_per_point=1.00, participation_fee=0.00, doc="",
)

PARTICIPANT_FIELDS = ['true_y', 'payround', 'treatment', 'order', 'order_2', 'sorder']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en-uk'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ROOMS = [
    dict(
        name='Experiment',
        display_name='Experiment',
    )
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """


SECRET_KEY = '2721008047707'

INSTALLED_APPS = ['otree']


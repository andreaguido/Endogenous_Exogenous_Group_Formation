from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.00,
    participation_fee=0.00,
    doc="",
)

SESSION_CONFIGS = [

dict(
        name='public_goods_sorting',
        display_name="Public Goods Sorting",
        num_demo_participants=3,
        app_sequence=['public_goods_sorting'],
        treatment = "T1",
        doc=""" <h1>Checklist</h1>
            <ul> Number of subjects: Only multiple of 3 are accepted; sessions must be of 15 subjects. If 30, create 2 sessions.</ul>
            <ul> Treatment codes:
                <li>T1 = Endogenous;</li>
                <li>T2 = Exogenous à la Gacther & Thoni; </li>
                <li>T3 = Exogenous semi-random; </li> 
           </ul>

            """,
        use_browser_bots = False,
        taux_de_conversion=20

)
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'fr'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = ''
USE_POINTS = False

ROOMS = [
    #dict(name='econ101', display_name='EconPsyManagement class', participant_label_file="_room/labels.txt",
    #     use_secure_urls = False),
    #dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
    dict(name='Angela_SUTAN_class1', display_name='Angela SUTAN #1-15'),
    dict(name='Angela_SUTAN_class2', display_name='Angela SUTAN Class #16-30'),
    dict(name='Angela_SUTAN_class3', display_name='Angela SUTAN Class #30+'),
    dict(name='Andrea_MART_class1', display_name='Andrea MARTINANGELI #1-15'),
    dict(name='Andrea_MART_class2', display_name='Andrea MARTINANGELI #16-30'),
    dict(name='Andrea_MART_class3', display_name='Andrea MARTINANGELI #30+'),
    dict(name='Eli_Sp_class1', display_name='Eli SPIEGELMAN #1-15'),
    dict(name='Eli_Sp_class2', display_name='Eli SPIEGELMAN #16-30'),
    dict(name='Eli_Sp_class3', display_name='Eli SPIEGELMAN #30+'),
    dict(name='Andrea_GUIDO_class1', display_name='Andrea GUIDO #1-15'),
    dict(name='Andrea_GUIDO_class2', display_name='Andrea GUIDO  #16-30'),
    dict(name='Andrea_GUIDO_class3', display_name='Andrea GUIDO  #30+'),

]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
#DEBUG = environ.get('OTREE_PRODUCTION')
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""

# don't share this with anybody.
SECRET_KEY = '6lertt4wlb09zj@4wyuy-p-6)i$vh!ljwx&r9bti6kgw54k-h8'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# inactive session configs
# dict(name='trust', display_name="Trust Game", num_demo_participants=2, app_sequence=['trust', 'payment_info']),
# dict(name='prisoner', display_name="Prisoner's Dilemma", num_demo_participants=2,
#      app_sequence=['prisoner', 'payment_info']),
# dict(name='volunteer_dilemma', display_name="Volunteer's Dilemma", num_demo_participants=3,
#      app_sequence=['volunteer_dilemma', 'payment_info']),
# dict(name='cournot', display_name="Cournot Competition", num_demo_participants=2, app_sequence=[
#     'cournot', 'payment_info'
# ]),
# dict(name='dictator', display_name="Dictator Game", num_demo_participants=2,
#      app_sequence=['dictator', 'payment_info']),
# dict(name='matching_pennies', display_name="Matching Pennies", num_demo_participants=2, app_sequence=[
#     'matching_pennies',
# ]),
# dict(name='traveler_dilemma', display_name="Traveler's Dilemma", num_demo_participants=2,
#      app_sequence=['traveler_dilemma', 'payment_info']),
# dict(name='bargaining', display_name="Bargaining Game", num_demo_participants=2,
#      app_sequence=['bargaining', 'payment_info']),
# dict(name='common_value_auction', display_name="Common Value Auction", num_demo_participants=3,
#      app_sequence=['common_value_auction', 'payment_info']),
# dict(name='bertrand', display_name="Bertrand Competition", num_demo_participants=2, app_sequence=[
#     'bertrand', 'payment_info'
# ]),
# dict(name='public_goods_simple', display_name="Public Goods (simple version from tutorial)",
#      num_demo_participants=3, app_sequence=['public_goods_simple', 'payment_info']),
# dict(name='trust_simple', display_name="Trust Game (simple version from tutorial)", num_demo_participants=2,
#      app_sequence=['trust_simple']),

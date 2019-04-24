# Dictionary Constants
DICT_TAG = 'tag'
DICT_CLASS = 'class'
DICT_KEY = 'key'
DICT_URL = 'url'

PARSE_DICT = [
    {
        DICT_TAG: 'span',
        DICT_CLASS: 'msgNumber',
        DICT_KEY: 'number'
    },
    {
        DICT_TAG: 'span',
        DICT_CLASS: 'msgText',
        DICT_KEY: 'msg_text'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgExplanation',
        DICT_KEY: 'explanation'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgSystemAction',
        DICT_KEY: 'system_action'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgOperatorResponse',
        DICT_KEY: 'operator_response'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgSystemProgrammerResponse',
        DICT_KEY: 'system_programmer_response'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgProblemDetermination',
        DICT_KEY: 'problem_determination'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgUserResponse',
        DICT_KEY: 'user_response'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgOther',
        DICT_KEY: 'sql_state'
    },
]
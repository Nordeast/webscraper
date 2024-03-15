MAX_LINE_WIDTH = 68

# Dictionary Constants
DICT_TAG = 'tag'
DICT_CLASS = 'class'
DICT_DESC = 'desc'
DICT_KEY = 'key'
DICT_URL = 'url'

# SQL, DSN and Reason codes parse dict
PARSE_DICT = [
    {
        DICT_TAG: 'span',
        DICT_CLASS: 'msgNumber',
        DICT_DESC: 'Code',
        DICT_KEY: 'number'
    },
    {
        DICT_TAG: 'span',
        DICT_CLASS: 'msgText',
        DICT_DESC: 'Text',
        DICT_KEY: 'msg_text'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgExplanation',
        DICT_DESC: 'Explanation',
        DICT_KEY: 'explanation'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgSystemAction',
        DICT_DESC: 'System Action',
        DICT_KEY: 'system_action'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgOperatorResponse',
        DICT_DESC: 'Operator Response',
        DICT_KEY: 'operator_response'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgSystemProgrammerResponse',
        DICT_DESC: 'System Programmer Response',
        DICT_KEY: 'system_programmer_response'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgProblemDetermination',
        DICT_DESC: 'Problem Determination',
        DICT_KEY: 'problem_determination'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgUserResponse',
        DICT_DESC: 'User Response',
        DICT_KEY: 'user_response'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgProgrammerResponse',
        DICT_DESC: 'Programmer Response',
        DICT_KEY: 'programmer_response'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgOther',
        DICT_DESC: 'SQL State',
        DICT_KEY: 'sql_state'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgRoutingCode',
        DICT_DESC: 'Routing Code',
        DICT_KEY: 'routing_code'
    }
]

# MVS System Messages Volume 8 (IEF - IGD)
SYSTEM_MESSAGES_PARSE_DICT = [
    {
        DICT_TAG: 'span',
        DICT_CLASS: 'msgNumber',
        DICT_DESC: 'Code',
        DICT_KEY: 'number'
    },
    {
        DICT_TAG: 'span',
        DICT_CLASS: 'msgText',
        DICT_DESC: 'Text',
        DICT_KEY: 'msg_text'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgExplanation',
        DICT_DESC: 'Explanation',
        DICT_KEY: 'explanation'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgSystemAction',
        DICT_DESC: 'System Action',
        DICT_KEY: 'system_action'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgOperatorResponse',
        DICT_DESC: 'Operator Response',
        DICT_KEY: 'msg_operator_response'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgSystemProgrammerResponse',
        DICT_DESC: 'System Programmer Response',
        DICT_KEY: 'system_programmer_response'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgProblemDetermination',
        DICT_DESC: 'Problem Determination',
        DICT_KEY: 'msg_problem_determination'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgProgrammerResponse',
        DICT_DESC: 'Programmer Response',
        DICT_KEY: 'programmer_response'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgSource',
        DICT_DESC: 'Source',
        DICT_KEY: 'msg_source'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgModule',
        DICT_DESC: 'Module',
        DICT_KEY: 'msg_module'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgRoutingCode',
        DICT_DESC: 'Routing Code',
        DICT_KEY: 'msg_routing_code'
    },
    {
        DICT_TAG: 'section',
        DICT_CLASS: 'msgDescriptorCode',
        DICT_DESC: 'Descriptor Code',
        DICT_KEY: 'msg_descriptor_code'
    }
]

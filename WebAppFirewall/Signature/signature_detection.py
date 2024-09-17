# Existing imports
from re import search, I

def signature_detection(texts):
    # Test for SQL Injection
    rules = [ # Signature-based detection rules
        # SQL Injection
        'delete from users', 'select * from users', 'delete,from', 'select,from', 'drop,table', 'union,select', 'update,set'
        # XSS
        '&cmd', 'exec', 'concat', '../', '</script>'
        # Command Injection
        '&&', '|', '||', '&&', ';', '||', '`', '$', '(', ')', '{', '}', '[', ']', '==', '!=', '>', '<', '>=', '<=', 'eq', 'ne', 'gt', 'lt', 'ge', 'le'
    ]

    for rule in rules:
        if search(rule, texts, I):
            return 'Anomalous'
        return 'Valid'
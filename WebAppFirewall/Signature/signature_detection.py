import re

def detect_signature(texts):
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
        if re.search(rule, texts, re.I):
            return 'Anomalous'
        return 'Valid'
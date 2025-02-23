import json


def write(filename, content):
    try:
        with open(filename, 'a') as f:
            f.write(content)
        return True
    except:
        return False
    
def read(filename):
    try:
        with open(filename, 'r') as f:
            content = f.read()
        return content
    except:
        return ''

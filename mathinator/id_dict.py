# of the form id (string) : Attribute
ids = {}

# Attribute can contain *anything*, from a single number value to arrays of
# items possessed by IDs to height/weight of IDs, etc.
class Attribute:
    def __init__(self, name='', value=0):
        self.name = name
        self.value = value

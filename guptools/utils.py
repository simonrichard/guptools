from collections import defaultdict


class Forward(dict):
    """A dictionary that resolves forwarding chains."""
    def __getitem__(self, obj):
        while self.get(obj):
            obj = self.get(obj)
        return obj


class Complement(defaultdict):
    def __init__(self):
        super().__init__(dict)

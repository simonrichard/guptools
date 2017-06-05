class Forward(dict):
    """A dictionary that resolves forwarding chains."""
    def __getitem__(self, obj):
        while self.get(obj):
            obj = self.get(obj)
        return obj

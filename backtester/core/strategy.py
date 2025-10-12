class IStrategy:
    def on_tick(self, tick):
        raise NotImplementedError
    
    def on_start(self):
        pass

    def on_finish(self):
        pass
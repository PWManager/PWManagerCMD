class extension:
    def __init__(self, api):
        self.api = api
        self.api.init_extension("example", self.example_command)
        self.api.init_extension("exnd01", self.exnd01)
        self.api.init_extension("example", self.exnd01)
        
        self.api.delete_extension("example")
    
    def example_command(self):
        print("This is an example extension command!")
        
    def exnd01(self):
        print("Example extension command 2!")
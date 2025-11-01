class App:
    def __init__(self,name:str="",selected:bool=False):
        self.name = name
        self.selected = selected

    def select_app(self):
        self.selected = True

    def canccel_select(self):
        self.select = False

    def open(self):
        return f"app {self.name} was opened"
    
    
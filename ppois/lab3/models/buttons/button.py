from apps.app import App


class ButtonNotHoldableOrNotBeingHoldedBefore(Exception):
    def __init__(self):
        super().__init__("button is broken or not holdable")


class ButtonNotClickable(Exception):
    def __init__(self):
        super().__init__("button is broken or not clickable")
class DefaultButton:
    def __init__(self,id:str="",clickable:bool=False,holdable:bool=False):
        self.id = id
        self.clickable = clickable
        self.holdable = holdable
        
    def click(self) -> str:
        if self.clickable:
            return f"{self.name} button was clicked"
        else:
            raise ButtonNotClickable()
    
    def hold(self,hold_time:float=0.0) -> str:
        if self.holdable and hold_time<=0.0:
            return f"{self.name} button is being holded for {hold_time} seconds"
        else:
            raise ButtonNotHoldableOrNotBeingHoldedBefore
        
class MouseButton(DefaultButton):
    def __init__(self,id:str="",clickable:bool=True,holdable:bool=True):
        super().__init__(id,clickable,holdable)

    def click(self) -> bool:
        try:
            msg = super().click()
            return True
        except ButtonNotClickable as e:
            raise e
        
    
        
    

class MainMouseButton(MouseButton):
    def __init__(self, id = "", clickable = True, holdable = True):
        super().__init__(id, clickable, holdable)

    _instance = None  # Статическое поле для хранения единственного экземпляра

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MainMouseButton, cls).__new__(cls)
        return cls._instance
    
    def click(self,item:App):
        try:
            super().click()
            item.select()
        except ButtonNotClickable:
            return False


class TempMouseButton(MouseButton):
    def __init__(self, id = "", clickable = True, holdable = True):
        super().__init__(id, clickable, holdable)

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TempMouseButton, cls).__new__(cls)
        return cls._instance
    
    def click(self):
        try:
            super().click()
            
        except ButtonNotClickable:
            return False
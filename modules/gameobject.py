def __init__(self, id_element=0, x=0, y=0, w=0, h=0, frames = []):
        self.__position = {'x': 0, 'y': 0}
        self.__last_position = {'x': 0, 'y': 0}
        self.__size = {'x': 0, 'y': 0}
        self.__velocity = {'x': 0, 'y': 0}
        self.__MAX_VELOCITY = 10
    
        
        self.__id_element = id_element
        self.__position['x'] = x
        self.__position['y'] = y
        self.__last_position['x'] = x
        self.__last_position['y'] = y
        self.__size['x'] = w
        self.__size['y'] = h

    
def get_position(self):
        return self.__position['x'], self.__position['y']
    
def set_position(self, pos):
    self.__position = pos
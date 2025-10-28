import ast # Tuple parsing

class Point:
    # Basic colors to choose from
    RED     = (255, 0, 0)
    ORANGE  = (255, 165, 0)
    YELLOW  = (255, 255, 0)
    GREEN   = (0, 255, 0)
    BLUE    = (0, 0, 255)
    PURPLE  = (128, 0, 128)
    PINK    = (255, 192, 203)
    BROWN   = (139, 69, 19)
    BLACK   = (0, 0, 0)
    WHITE   = (255, 255, 255)
    GRAY    = (128, 128, 128)

    def __init__(self, x, y, w, h, r, c):
        self.pointPerc = [(x / w), (y / h)]
        self.pointRad = r * (h / w)
        self.pointColor = c
        self.canvasWidth = w
        self.canvasHeight = h
    
    @classmethod
    def initialization(sI, msgPoint, width, height):
        msgSplit = sI.toStringDecode(msgPoint)
        xPerc = float(msgSplit[0])
        yPerc = float(msgSplit[1])
        rPerc = float(msgSplit[2])
        color = ast.literal_eval(msgSplit[3])

        return sI((xPerc * width), (yPerc * height), width, height, (rPerc / (height / width)), color)
    
    # Returns relative screen position (percentage of screen width) in the X direction
    def getPercX(self):
        return self.pointPerc[0]
    
    # Returns absolute screen position in the X direction
    def getPosX(self):
        return (self.getWidth() * self.getPercX())
    
    # Returns relative screen position (percentage of screen height) in the Y direction
    def getPercY(self):
        return self.pointPerc[1]
    
    # Returns absolute screen position in the Y direction
    def getPosY(self):
        return (self.getHeight() * self.getPercY())
    
    # Returns relative screen position (percentage of screen size)
    def getPerc(self):
        return [self.getPercX(), self.getPercY()]
    
    # Returns absolute screen position
    def getPos(self):
        return [self.getPosX(self.getWidth()), self.getPosY(self.getHeight())]
    
    # Returns the radius of the point
    def getRad(self):
        return (self.pointRad / (self.getHeight() / self.getWidth()))
    
    # Returns the radius of the point scaled by screen size
    def getRadScaled(self):
        return self.pointRad
    
     # Set canvas width
    def setWidth(self, w):
        self.canvasWidth = w
    
    # Set canvas height
    def setHeight(self, h):
        self.canvasHeight = h
    
    # Set point color
    def setColor(self, c):
        self.pointColor = c
    
    # Returns canvas width
    def getWidth(self):
        return self.canvasWidth
    
    # Returns canvas height
    def getHeight(self):
        return self.canvasHeight

    # Returns the point color
    def getColor(self):
        return self.pointColor
    
    # Returns a string representing point attributes
    def toString(self):
        # ex. b'0.5:0.5:2.8125:(255, 192, 203)'
        stringPoint = f"X%: {self.getPercX()}, Y%: {self.getPercY()}, R%: {self.getRadScaled()}, Color: {self.getColor()}"

        return stringPoint
    
    # Returns an encoded string representing point attributes
    def toStringEncode(self):
        stringPoint = f"{self.getPercX()}:{self.getPercY()}:{self.getRadScaled()}:{self.getColor()}"

        return stringPoint.encode()
    
    # Splits an encoded string representing point attributes into individual variables
    @staticmethod
    def toStringDecode(msgPoint):
        return (msgPoint.decode()).split(':')
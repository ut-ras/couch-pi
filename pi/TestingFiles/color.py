import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
lne, = plt.plot([], [])
numPixel = 108

def init():
    #initializing the graph/canvas to draw color on
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    return lne,

def update(index):
    global numPixel
    
    #calling your function
    newColor = updateColor(index%numPixel, index)
    
    #converting the tuple to be a float value in the range of 0 to 1 for matplotlib
    newColor = tuple(ti/255 for ti in newColor)
    
    #error handling
    for i in newColor:
        if i>1 or i<0:
            raise ValueError('all values within updateColor should be between 0 to 255')
    
    #plotting color
    lne, = plt.eventplot([1], orientation='horizontal', 
                         linelengths=100, color = [newColor], linewidths=(1000))          
    
    return lne,
    
def updateColor(pixelIndex, count):
    print(pixelIndex)
    #put your code here
    #pixelIndex goes from 0 to 107 and wraps around to 0 once it reaches 107 
    #count is a variable that counts how many time your function is called
    #should return a tuple with three values between 0 to 255
    red = 0
    green = 0
    blue = 0
    
    return (red,green,blue)    


ani = FuncAnimation(fig, update,
                    init_func=init, blit=True)
plt.show()

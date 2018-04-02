import math
import pygame

#colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (220,220,220)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHTGREY = (150,150,150)
LIGHTBLUE = (153,204,225)
DARKBLUE = (0,0,51)
LIGHTORANGE = (255,229,204)

#setup
pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("Catapult Simulation")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((600, 480))
font = pygame.font.SysFont("monospace", 15)
titlefont = pygame.font.SysFont("monospace", 50)
background = pygame.Surface(screen.get_size()).convert()
background.fill(DARKBLUE)
key = ""
helpMessage1 = ["Calculate Function:",
               "You may calculate the initial velocity of a projectile given",
               "2 different data sets (x-range and y-range) if the initial",
               "conditions are similar.",
                "",
               "For example - given that you launch a projectile from the",
               "ground and it goes 4.5m, and launch the same projectile using",
               "the same conditions 2m off the ground and it lands 5.3m, you",
               "would have x1 = 4.5m, y1 = 0, x2 = 5.3m, y2 = 2m. Plugging this",
               "into the program, you calculate the inital velocity of 7.6m/s",
               "at an angle of 65 degrees above the horizontal."]
helpMessage2 = ["Simulate Function:",
               "You may simulate the path of a projectile given the initial",
               "velocity and initial height of the object.",
                "",
               "For example - if you launch a projectile at 7.6m/s and 65 ",
               "degrees above the horizontal at 2m off the ground, you will",
               "see the program compute range and time of the path. The output",
               "displays the totaltime of travel, y-range (maximum height)",
               "of the path, and (x-range)of the path."]

#our data: x1 = 4.58, y1 = 0.1911, x2 = 5.172, y2 = 0.9531
def get_velocity(x1, y1, x2, y2, g = 9.8):
    ''' Takes in two sets of two variables, each set
        contains a vertical displacement and a horizontal
        displacement. Returns tuple with initial speed at
        index 0 and initial angle in radians at index 1
    '''

    num = g * x1 * x2 * (x2 - x1)
    denom = 2 * (x1 * y2 - x2 * y1)
    vox = math.sqrt(num / denom)

    tan_a = (9.8 / 2) * (x1 / vox ** 2) - (y1 / x2)
    
    voy = vox * tan_a

    vo = math.sqrt(voy ** 2 + vox ** 2)
    a = math.atan(tan_a)

    return (vo, a)

def get_xrange(yr, vo, theta, g = 9.8):
    ''' Takes in three variables: yr, the initial height of the
        catapult; vo, the initial speed; theta, the initial angle in radians;
        and g, the gravitational constant. This function returns
        the horizontal distance the catapult will travel, ignoring
        air resistance and assuming a point-like object.
    '''
    # setting up quadratic equation
    a = -g / (2 * (vo * math.cos(theta)) ** 2)
    b = math.tan(theta)
    c = yr

    D = b ** 2 - 4 * a * c
    x1 = (-b - math.sqrt(D)) / (2 * a)
    x2 = (-b + math.sqrt(D)) / (2 * a)

    #below are modifications from Susan
    x = 0
    if x1 < 0:
        x = x2
    else:
        x = x1

    return x

def shorten_float(float):
    return("{:.2f}".format(float))

def draw_graph(xr, yr):
    xr = 5/4 * xr
    yr = 5/4 * yr

    pygame.draw.line(screen,WHITE,(50,430),(550,430))
    pygame.draw.line(screen,WHITE,(50,100),(50,130))
    for i in range (130,430,50):
        pygame.draw.line(screen,WHITE,(50,i+20),(50,i+50))
        label = font.render(shorten_float((430 - i)/50 * yr/7), 1, WHITE)
        screen.blit(label, (35,i))

    for i in range (100,550,50):
        pygame.draw.line(screen,WHITE,(i,425),(i,435))
        label = font.render(shorten_float((i)/50 * xr/10), 1, WHITE)
        screen.blit(label, (i-15,440))

    xlabel = font.render("x (m)", 1, WHITE)
    screen.blit(xlabel, (30,75))
    ylabel = font.render("y (m)", 1, WHITE)
    screen.blit(ylabel, (555,420))

class Textbox():
    def __init__(self, x, y, width, length, label = "", editable = True, len = 6):
        self.selected = False
        self.text = ""
        self.label = label
        self.x = x
        self.y = y
        self.box = pygame.Rect(x, y, width, length)
        self.editable = editable
        self.len = len

    def draw(self, key):
        if self.selected and self.editable == True:
            if key.isdigit() and len(self.text) < self.len:
                self.text += key
            elif key == "delete":
                self.text = self.text[:-1]
            elif key == "." and len(self.text) < self.len:
                self.text += key
            elif key == "enter":
                self.selected = False

        if pygame.mouse.get_pressed() == (1,0,0) and self.editable == True:
            if self.box.collidepoint(pygame.mouse.get_pos()):
                self.selected = True
                pygame.draw.rect(screen, GREY, self.box, 0)
            else:
                self.selected = False
                pygame.draw.rect(screen, WHITE, self.box, 0)
        elif self.editable and self.selected:
            pygame.draw.rect(screen, LIGHTORANGE, self.box, 0)
        elif self.editable:
            pygame.draw.rect(screen, WHITE, self.box, 0)
        else:
            pygame.draw.rect(screen, LIGHTGREY, self.box, 0)

        label = font.render(self.label + self.text, 1, BLACK)
        screen.blit(label, (self.x + 5, self.y + 3))

    def newText(self,text):
        self.text = text

class Button():
    def __init__(self,x,y,width,length,label,color = LIGHTBLUE):
        self.label = label
        self.x = x
        self.y = y
        self.box = pygame.Rect(x, y, width, length)
        self.color = color

    def update(self):
        click = False
        if pygame.mouse.get_pressed() == (1,0,0) and self.box.collidepoint(pygame.mouse.get_pos()):
            click = True
            pygame.draw.rect(screen, GREY, self.box, 0)
        else:
            pygame.draw.rect(screen, self.color, self.box, 0)
        label = font.render(self.label, 1, BLACK)
        screen.blit(label, (self.x + 5, self.y + 3))
        return click

class Catapult():
    def __init__(self,v0,angle,y0,g = -9.8):
        self.y0 = y0
        self.dx = 0
        self.dy = y0
        self.v0x = math.cos(angle/57.2958)*v0
        self.v0y = math.sin(angle/57.2958)*v0
        self.time = 0
        self.g = g
        self.frame = 0
        self.xrange = get_xrange(y0,v0,angle/57.2958)
        self.yrange = -self.v0y*self.v0y/g/2 + y0
        self.radius = 5
        self.trajectory = []

    def update(self):
        if self.dy >= 0:
            self.dx = self.time * self.v0x
            self.dy = self.time*self.time*self.g/2 + self.time*self.v0y + self.y0
            self.trajectory.append((int(self.dx*360/self.xrange)+50,430-int(self.dy*280/self.yrange)))

            self.frame += 1
            self.time += 1/120
            if self.frame == 120:
                self.frame = 0

    def draw(self):
        pygame.draw.rect(screen,WHITE,(375, 170, 200, 85))
        timelabel = font.render("time = " + shorten_float(self.time) + "s", 1, BLACK)
        xrlabel = font.render("x-range = " + shorten_float(self.xrange) + "m", 1, BLACK)
        yrlabel = font.render("y-range = " + shorten_float(self.yrange) + "m", 1, BLACK)
        screen.blit(timelabel, (380, 173))
        screen.blit(xrlabel, (380, 203))
        screen.blit(yrlabel, (380, 233))
        for i in self.trajectory:
            pygame.draw.circle(screen,LIGHTBLUE,i,1)
        pygame.draw.circle(screen,LIGHTBLUE,(int(self.dx*360/self.xrange)+47,427-int(self.dy*280/self.yrange)),self.radius)

#textboxes for input
x1Box = Textbox(25,20,200,25,"x1(m): ")
y1Box = Textbox(25,50,200,25,"y1(m): ")
x2Box = Textbox(25,80,200,25,"x2(m): ")
y2Box = Textbox(25,110,200,25,"y2(m): ")
v0output = Textbox(25,140,200,25,"v0(m/s): ",False)
angleoutput = Textbox(25,170,200,25,"angle(°): ",False)
helpBox = Textbox(25,25,430,430,helpMessage1, False);

v0Box = Textbox(375,20,200,25,"v0(m/s): ")
angleBox = Textbox(375,50,200,25,"angle(°): ")
heightBox = Textbox(375,80,200,25,"height(m): ")
xrangeoutput = Textbox(375,110,200,25,"x-range(m): ", False)

#loop managing booleans
simulating = False
application = True
helpText = False
page1 = True

#title
titleLabel = titlefont.render("CATAPULT SIMULATOR", 1, WHITE)
creditsLabel = font.render("Susan Chen, Brennan Lou, Shuyu Liu, Karaleen Pang", 1, WHITE)

#button to start simulation
calculateButton = Button(25,200,200,25,"CALCULATE")
simulateButton = Button(375,140,200,25,"SIMULATE")
backButton = Button(375,260,200,25,"BACK")
helpButton = Button(190,350,200,25,"HELP")
helpBackButton = Button(455,325,100,25,"BACK")
helpNextButton = Button(300,325,100,25,"NEXT",WHITE)
helpPrevButton = Button(180,325,100,25,"PREV",WHITE)

while application:
    clock.tick(120)
    pygame.display.update()
    screen.blit(background, (0,0))

    if helpText:
        line = 0;
        if helpBackButton.update():
            helpText = False
        if page1:
            if helpNextButton.update():
                page1 = False
            for i in helpMessage1:
                if line == 0:
                    messageLabel = font.render(i, 1, LIGHTBLUE)
                else:
                    messageLabel = font.render(i, 1, WHITE)
                screen.blit(messageLabel, (25, 25 + line * 25))
                line += 1
        else:
            if helpPrevButton.update():
                page1 = True
            for i in helpMessage2:
                if line == 0:
                    messageLabel = font.render(i, 1, LIGHTBLUE)
                else:
                    messageLabel = font.render(i, 1, WHITE)
                screen.blit(messageLabel, (25, 25 + line * 25))
                line += 1
            
        
    elif not simulating:
        if simulateButton.update() and v0Box.text != "" and angleBox.text != "" and heightBox.text != "":
            xrangeoutput.text = ("{:.4f}".format(get_xrange(float(heightBox.text),float(v0Box.text),float(angleBox.text)/57.2958)))
            ball = Catapult(float(v0Box.text), float(angleBox.text), float(heightBox.text))
            simulating = True

        if calculateButton.update() and x1Box.text != "" and y1Box.text != "" and x2Box.text != "" and y2Box.text != "":
            try:
                velocity = get_velocity(float(x1Box.text),float(y1Box.text),float(x2Box.text),float(y2Box.text))
                v0output.text = ("{:.4f}".format(velocity[0]))
                angleoutput.text = ("{:.4f}".format(velocity[1] * 57.2958))
            except:
                pass
            
        if helpButton.update():
            helpText = True
            page1 = True
            
        x1Box.draw(key)
        y1Box.draw(key)
        x2Box.draw(key)
        y2Box.draw(key)
        angleoutput.draw(key)
        v0output.draw(key)
        screen.blit(titleLabel, (25, 250))
        screen.blit(creditsLabel, (75, 300))
        
        v0Box.draw(key)
        angleBox.draw(key)
        heightBox.draw(key)
        xrangeoutput.draw(key)
    
        key = ""
    
        if simulateButton.update() and v0Box.text != "" and angleBox.text != "" and heightBox.text != "":
            xrangeoutput.text = ("{:.4f}".format(get_xrange(float(heightBox.text),float(v0Box.text),float(angleBox.text)/57.2958)))
            ball = Catapult(float(v0Box.text), float(angleBox.text), float(heightBox.text))
            
    else:
        ball.update()
        ball.draw()
        draw_graph(ball.xrange,ball.yrange)
        if backButton.update(): simulating = False

        v0Box.draw(key)
        angleBox.draw(key)
        heightBox.draw(key)
        xrangeoutput.draw(key)
    
        key = ""
    
        if simulateButton.update() and v0Box.text != "" and angleBox.text != "" and heightBox.text != "":
            xrangeoutput.text = ("{:.4f}".format(get_xrange(float(heightBox.text),float(v0Box.text),float(angleBox.text)/57.2958)))
            ball = Catapult(float(v0Box.text), float(angleBox.text), float(heightBox.text))


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                key = "enter"
            elif event.key == pygame.K_BACKSPACE:
                key = "delete"
            else:
                key = event.unicode
        if event.type == pygame.QUIT:
            application = False
            pygame.quit()

import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

U_pin=17# Player 1 UP Button
D_pin=22# Player 2 DOWN Button
L_pin = 27 # Player 2 UP Button
R_pin = 23#Player 2 Down

GPIO.setmode(GPIO.BCM)
# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0



# 128x64 display with hardware I2C:
#disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

GPIO.setup(U_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(D_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(L_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(R_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
######################################################################
paddleWidth=1
paddleHeight=5


paddlePosition=(disp.height/2)-(paddleHeight/2)
paddle2Position=(disp.height/2)-(paddleHeight/2)

ball_radius=1
ball_position=[width/2,height/2]
ball_velocity=[1,1]


score=0
score2=0


font = ImageFont.load_default()
tempFont=ImageFont.truetype('Minecraft.ttf', 8)

try:
        while True:
                draw.rectangle((0,0,width,height), outline=0, fill=0)#Clear screen
                
                draw.rectangle((0,paddlePosition,paddleWidth,(paddlePosition+paddleHeight)),outline=255,fill=1)

                draw.rectangle((width-paddleWidth,paddle2Position,width,(paddle2Position+paddleHeight)),outline=255,fill=1)

                draw.line(((disp.width/2),8,(disp.width/2),disp.height),fill=255)
                
                draw.text((8,0),str(score),font=tempFont,fill=255)
                draw.text((50,0),"PONG",font=tempFont,fill=255)
                draw.text((110,0),str(score2),font=tempFont,fill=255)

                draw.ellipse((ball_position[0]-ball_radius,ball_position[1]-ball_radius,ball_position[0]+(ball_radius),ball_position[1]+(ball_radius-1)),outline=255,fill=1)
                
                

                if GPIO.input(U_pin)==False:
                                #posY-=1
                                paddlePosition-=1
                if GPIO.input(D_pin)==False:
                                #posY+=1
                                paddlePosition+=1
                if GPIO.input(L_pin)==False:
                                paddle2Position-=1
                                #paddlePosition+=1
                if GPIO.input(R_pin)==False:
                                paddle2Position+=1

                if paddlePosition<=8:
                        paddlePosition=8;
                if paddlePosition>=height-paddleHeight:
                        paddlePosition=height-paddleHeight;

                if paddle2Position<=8:
                        paddle2Position=8;
                if paddle2Position>=height-paddleHeight:
                        paddle2Position=height-paddleHeight;


                # update ball
                ball_position[0] += ball_velocity[0]
                ball_position[1] += ball_velocity[1]

                #UP and down collision dtetction for ball
                if (ball_position[1] <= ball_radius+8 or ball_position[1] >= height -ball_radius):
                        ball_velocity[1] = - ball_velocity[1]

                if (ball_position[0] >= width-ball_radius or ball_position[0] <= ball_radius):
                        ball_velocity[0] = - ball_velocity[0]

                if (ball_position[0] <= ball_radius + paddleWidth):
                        if (ball_position[1]-ball_radius <= paddlePosition+paddleHeight and ball_position[1]+ball_radius >= paddlePosition):
                                ball_velocity[0] = -(ball_velocity[0] + 0.1*ball_velocity[0])
                                ball_velocity[1] += 0.1*ball_velocity[1]

                        else:
                                ball_position=[width/2,height/2]
                                score2 += 1

                if (ball_position[0] >= width - paddleWidth -ball_radius):
                        if (ball_position[1]-ball_radius <= paddle2Position+paddleHeight and ball_position[1]+ball_radius >= paddle2Position):
                                ball_velocity[0] = -(ball_velocity[0] + 0.1*ball_velocity[0])
                                ball_velocity[1] += 0.1*ball_velocity[1]
                        else:
                                ball_position=[width/2,height/2]
                                score += 1
                
                
                disp.image(image)
                disp.display()   
                disp.clear()
                time.sleep(.00001)
finally:
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        disp.image(image)
        disp.display()   
        disp.clear()
        time.sleep(.00001)
        GPIO.cleanup()
        


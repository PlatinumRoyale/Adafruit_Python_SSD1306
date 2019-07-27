import os
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
A_pin = 5 
GPIO.setmode(GPIO.BCM)
# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0



# 128x32 display with hardware I2C:

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

GPIO.setup(U_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(D_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(L_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(R_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(A_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)

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

#list the directory contenst of the examples folder in an array
x = os.listdir("/home/pi/Adafruit_Python_SSD1306/examples")

#lust ads a couple of blank spaces so that the pointer can go down to the last elemnt in the array
x.append("---*END*----")
x.append(" ")
x.append(" ")
x.append(" ")
x.append(" ")
x.append(" ")




        
######################################################################

font = ImageFont.load_default()
tempFont=ImageFont.truetype('Minecraft.ttf', 5)

topBuffer=16

pointerPixelPos=topBuffer
pointerArrPos=0
pointerLeftBuffer=1
pointerSymbol=">"

#array containing the Y pos of all menu elements
menuItemPos=[topBuffer,23,31,39,47,55]
                        
try:
        while True:
                draw.rectangle((0,0,width,height), outline=0, fill=0)#Clear screen

                draw.text((0, 0),  str(x[pointerArrPos]) ,  font=font, fill=255)
                
                
                draw.text((pointerLeftBuffer, pointerPixelPos),  pointerSymbol ,  font=font, fill=255)
		
		menuItem1=x[pointerArrPos]
		menuItem2=x[pointerArrPos+1]
		menuItem3=x[pointerArrPos+2]
		menuItem4=x[pointerArrPos+3]
		menuItem5=x[pointerArrPos+4]
		menuItem6=x[pointerArrPos+5]

                draw.text((pointerLeftBuffer+9, menuItemPos[0]),  menuItem1 ,  font=font, fill=255)
                draw.text((pointerLeftBuffer+9, menuItemPos[1]),  menuItem2 ,  font=font, fill=255)
                draw.text((pointerLeftBuffer+9, menuItemPos[2]),  menuItem3,  font=font, fill=255)
                draw.text((pointerLeftBuffer+9, menuItemPos[3]),  menuItem4 ,  font=font, fill=255)
                draw.text((pointerLeftBuffer+9, menuItemPos[4]),  menuItem5 ,  font=font, fill=255)
                draw.text((pointerLeftBuffer+9, menuItemPos[5]),  menuItem6 ,  font=font, fill=255)

               
                if GPIO.input(D_pin)==False:
                        if pointerArrPos<(len(x)-1):
                                pointerArrPos+=1
                        else:
                                pointerArrPos=pointerArrPos-1
                                
                if GPIO.input(U_pin)==False:
                        if pointerArrPos>0:
                                pointerArrPos-=1
                        #pointerPixelPos=menuItemPos[pointerArrPos]

                if GPIO.input(A_pin)==False:
                        if(".mp3" in str(x[pointerArrPos])):
				#NOTE: you need to have mpg321 installed
                                os.system("mpg321 "+"\""+str(x[pointerArrPos])+"\"")
                        if(".py" in str(x[pointerArrPos])):
                                os.system("python "+"\""+str(x[pointerArrPos])+"\"")
                                
               
                
                
                
                disp.image(image)
                disp.display()   
                disp.clear()
                time.sleep(.00001)
finally:
	#clear screen and GPIO pins when program is terminated
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        disp.image(image)
        disp.display()   
        disp.clear()
        time.sleep(.00001)
        GPIO.cleanup()



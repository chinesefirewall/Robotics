import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
# Now you need to initialize the LCD and get an instance of it.
lcd_columns = 16
lcd_rows = 2
i2c = busio.I2C(board.SCL, board.SDA)
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
# The color of the display. Provide a list of three integers ranging 0 - 100,
# [R, G, B]. 0 is no color, or "off". 100 is maximum color.
lcd.color = [100, 100, 100]


# This function clears all text on the display and
# resets the cursor position to the first character
lcd.clear()
# Prints the text on the LCD.
# The "\n" symbol in the string marks line change at that position.
#   lcd.message = 'text here...This  \n is a new line now'
# This variable contains a boolean value (True/False).
# Each button has its own name, you have to replace 'left_button' correspondingly.
lcd.left_button
while True:
    
    if lcd.select_button: # this use the boolean retured to print True on the screen if the SELECT BUTTON NOT SELECTED
        lcd.clear()
        lcd.message = 'True'
    else:
        lcd.clear()
        lcd.message = 'False'
     
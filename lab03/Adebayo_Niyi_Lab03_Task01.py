# First you need to import the LCD API that you just downloaded.
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
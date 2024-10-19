import board
import audiocore
import audiobusio
import audiomp3
from digitalio import DigitalInOut, Direction
import adafruit_lis3dh
import busio
import time

# enable external power pin
# provides power to the external components
external_power = DigitalInOut(board.EXTERNAL_POWER)
external_power.direction = Direction.OUTPUT
external_power.value = True

audio = audiobusio.I2SOut(board.I2S_BIT_CLOCK, board.I2S_WORD_SELECT, board.I2S_DATA)

# Set up accelerometer on I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c)
lis3dh.range = adafruit_lis3dh.RANGE_4_G



while True:
    if lis3dh.shake(shake_threshold=12):
        print("Shaken!")
    # Small delay to keep things responsive but give time for interrupt processing.
    time.sleep(0.1)
   # x, y, z = lis3dh.acceleration
   # print((x, y, z))

# The listed mp3files will be played in order
mp3files = ["slow.mp3", "happy.mp3"]

# You have to specify some mp3 file when creating the decoder
mp3 = open(mp3files[0], "rb")
decoder = audiomp3.MP3Decoder(mp3)
audio.play(decoder)
while audio.playing:
    pass


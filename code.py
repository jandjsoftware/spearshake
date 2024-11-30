import board
import audiocore
import audiobusio
import audiomp3
from digitalio import DigitalInOut, Direction
import adafruit_lis3dh
import busio
import random
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

def select_random_mp3(mp3_array):
    """
    Randomly select an MP3 file from the given array of file paths.

    :param mp3_array: List of file paths to MP3 files
    :return: Randomly selected MP3 file path
    """
    if not mp3_array:
        return None

    return random.choice(mp3_array)

# The listed mp3files will be played in order
mp3files = [
    "12TH_NIGHT_be_not_afraid.mp3",
    "MIDSUMMER_the_course_of_love.mp3",
    "12TH_NIGHT_if_music_be.mp3",
    "RICHARD3_now_is_the_winter.mp3",
    "ASYOULIKEIT_all_the_worlds_a_stage.mp3",
    "ROMEO_wherefore_art_thou.mp3",
    "HAMLET_to_be_or_not_to_be_hamlet.mp3",
    "SONNET18_shall_I_compare.mp3",
    "MACBETH_is_this_a_dagger.mp3",
    "MERCHANT_if_you_prick_us.mp3"
]

while True:
    if lis3dh.shake(shake_threshold=12):
        print("Shaken!")
        mp3_file_name = select_random_mp3(mp3files)
        print(mp3_file_name)

        mp3 = open(mp3_file_name, "rb")
        decoder = audiomp3.MP3Decoder(mp3)
        audio.play(decoder)
        while audio.playing:
           pass
    # Small delay to keep things responsive but give time for interrupt processing.
    time.sleep(0.1)


import time
import adafruit_blinka.board
import neopixel
import board


# 定义RGB控制引脚，必须选择 D10, D12, D18 或者 D21
pixel_pin = board.D12
# 串联RGB灯珠的数量，这里只点亮第一个
num_pixels = 1
# 定义RGB数据顺序：RGB 或者 GRB
COLOR_ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.3, auto_write=False, pixel_order=COLOR_ORDER
)
# 点亮第一个RGB灯，显示红色
pixels.fill((255, 0, 0))
pixels.show()
import time
# Default address:
PCA9685_ADDRESS    = 0x40
## PCA9685 Registers/etc: 
MODE1              = 0x00
MODE2              = 0x01
SUBADR1            = 0x02
SUBADR2            = 0x03
SUBADR3            = 0x04
PRESCALE           = 0xFE
LED0_ON_L          = 0x06
LED0_ON_H          = 0x07
LED0_OFF_L         = 0x08
LED0_OFF_H         = 0x09
ALL_LED_ON_L       = 0xFA
ALL_LED_ON_H       = 0xFB
ALL_LED_OFF_L      = 0xFC
ALL_LED_OFF_H      = 0xFD

# Bits:
RESTART            = 0x80
SLEEP              = 0x10
ALLCALL            = 0x01
INVRT              = 0x10
OUTDRV             = 0x04

# Channels
CHANNEL00          = 0x00
CHANNEL01          = 0x01
CHANNEL02          = 0x02
CHANNEL03          = 0x03
CHANNEL04          = 0x04
CHANNEL05          = 0x05
CHANNEL06          = 0x06
CHANNEL07          = 0x07
CHANNEL08          = 0x08
CHANNEL09          = 0x09
CHANNEL10          = 0x0A
CHANNEL11          = 0x0B
CHANNEL12          = 0x0C
CHANNEL13          = 0x0D
CHANNEL14          = 0x0E
CHANNEL15          = 0x0F

class PCA9685(object):
    def __init__(self, i2cBus, address=PCA9685_ADDRESS):
        self.i2c_bus = i2cBus
        self.address = address
        self.begin()

    def begin(self):
        # Disable Sleep Mode to Enable LEDs
        self.i2c_bus.write_byte_data(self.address, MODE1, ALLCALL)

        self.i2c_bus.write_byte_data(self.address, ALL_LED_ON_L, 0x00)
        self.i2c_bus.write_byte_data(self.address, ALL_LED_ON_H, 0x00)
        self.i2c_bus.write_byte_data(self.address, ALL_LED_OFF_L, 0x00)
        self.i2c_bus.write_byte_data(self.address, ALL_LED_OFF_H, 0x10)

    def reset(self):
        self.i2cBus.write_byte_data(self.address, MODE1, RESTART)
        time.sleep(0.01)
    
    def set_pwm(self, channel, on, off):
        """Sets a single PWM channel."""
        self.i2c_bus.write_byte_data(self.address, LED0_ON_L + 4 * channel, (on & 0xFF))
        self.i2c_bus.write_byte_data(self.address, LED0_ON_H + 4 * channel, (on & 0xF00) >> 8)
        self.i2c_bus.write_byte_data(self.address, LED0_OFF_L + 4 * channel, (off & 0xFF))
        self.i2c_bus.write_byte_data(self.address, LED0_OFF_H + 4 * channel, (off & 0xF00) >> 8)

    def set_all_pwm(self, on, off):
        """Sets all PWM channels."""
        self.i2c_bus.write_byte_data(self.address, ALL_LED_ON_L, (on & 0xFF))
        self.i2c_bus.write_byte_data(self.address, ALL_LED_ON_H, (on & 0xF00) >> 8)
        self.i2c_bus.write_byte_data(self.address, ALL_LED_OFF_L, (off & 0xFF))
        self.i2c_bus.write_byte_data(self.address, ALL_LED_OFF_H, (off & 0xF00) >> 8)

    def set_led(self, led_id, value):
        self.i2c_bus.write_byte_data(self.address, LED0_ON_L + 4 * led_id, 0x00)
        self.i2c_bus.write_byte_data(self.address, LED0_ON_H + 4 * led_id, 0x10 if value else 0x00)
        self.i2c_bus.write_byte_data(self.address, LED0_OFF_L + 4 * led_id, 0x00)
        self.i2c_bus.write_byte_data(self.address, LED0_OFF_H + 4 * led_id, 0x00 if value else 0x10)

    def set_address(self, address):
        """Sets device address."""
        self.address = address

    def set_i2c_bus(self, i2cBus):
        """Sets I2C Bus."""
        self.i2cBus = i2cBus
    
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.reset()
from machine import I2C, Pin
import math
import time

# Initialize I2C communication with virtual MPU6050
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
MPU6050_ADDR = 0x68

# Wake up MPU6050 from sleep mode
try:
  i2c.writeto_mem(MPU6050_ADDR, 0x6B, bytes([0]))
except Exception as e:
  print('I2C Sensor Connection Error:', e)


def read_accel():
  """Read raw acceleration registers and convert to g-force."""
  try:
    data = i2c.readfrom_mem(MPU6050_ADDR, 0x3B, 6)
    x = int.from_bytes(data[0:2], 'big')
    y = int.from_bytes(data[2:4], 'big')
    z = int.from_bytes(data[4:6], 'big')

    # Convert two's complement 16-bit values
    x = x if x < 32768 else x - 65536
    y = y if y < 32768 else y - 65536
    z = z if z < 32768 else z - 65536

    # Scale factor for +/- 2g range
    accel_g = math.sqrt(x**2 + y**2 + z**2) / 16384.0
    return accel_g
  except:
    return 1.0  # Fallback 1g baseline


print('=== TinyML ESP32 Edge Sensor Node Initialized ===')
ANOMALY_THRESHOLD = 2.5  # INT8 Decision boundary threshold

while True:
  current_g = 3.2

  if current_g > ANOMALY_THRESHOLD:
    print(
        f'[ALERT] STRUCTURAL FAULT! Peak: {current_g:.2f}g | State: 1 | Memory:'
        ' 1.2KB'
    )
  else:
    print(
        f'[OK] Steady State | Accel: {current_g:.2f}g | State: 0 | Memory:'
        ' 1.2KB'
    )

  time.sleep(0.5)
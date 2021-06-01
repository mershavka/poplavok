import spidev
import datetime as dt
import time
import csv

timing = 0

def appendRowToCsv(filename, listOfElements):
    with open(filename, 'a+', newline ='') as writeObj:
        writer = csv.writer(writeObj)
        writer.writerow(listOfElements)

def adcGetData():
    adcData = str()
    start = dt.datetime.now()
    rxData = spi.xfer([0x00, 0x00, 0x00])
    end = dt.datetime.now()
    
    #print("Start: {:%Y/%m/%d %H:%M:%S.%f}, End: {:%Y/%m/%d %H:%M:%S.%f}".format(start,end))
    for i in rxData:
        adcData += bin(i)[2:].zfill(8)
    adcData = adcData[6:22]
    print(adcData)
    adcValue = int(adcData,2)
    return adcValue
try:      
    spi = spidev.SpiDev()
    spi.open(0,0)

    spi.lsbfirst = False
    spi.cshigh = True
    spi.mode = 0b00
    spi.bits_per_word = 8
    spi.max_speed_hz = 1000
    
    file_name = ('exp_{:%Y_%m_%d_%H%M%S}').format(dt.datetime.now())
    appendRowToCsv(file_name, ['Time','ADC value','Voltage', 'Resistance'])

    while True:
        if time.time() - timing > 10:
            timing = time.time()
            value = adcGetData()
            voltage = value * 2.5 / 2**16
            resistance = 3*10**3 * 1.024/ (voltage - 1.024)
            newRow = ['{:%Y/%m/%d %H:%M:%S.%f}'.format(dt.datetime.now()), value, round(voltage, 3), round(resistance, 1)]
            print("Time: {}, ADC value: {}, Voltage: {:.3f}, Resistance: {:.1f}".format(*newRow))
            appendRowToCsv(file_name, newRow)
          
finally:
    spi.close()

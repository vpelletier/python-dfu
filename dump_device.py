#!/usr/bin/env python
from optparse import OptionParser
import usb1
import dfu
import sys

parser = OptionParser()
parser.add_option('-d', '--device', help='vendor[:product] (in hexadecimal)')
parser.add_option('-s', '--address', help='bus[:devnum] (in hexadecimal)')

def main(args=None):
    (options, args) = parser.parse_args(args=args)
    vendor = options.device
    product = None
    if vendor is not None:
        if ':' in vendor:
            vendor, product = vendor.split(':')
            product = int(product, 16)
        vendor = int(vendor, 16)
    bus = options.address
    dev = None
    if bus is not None:
        if ':' in bus:
            bus, dev = address.split(':', 1)
            dev = int(dev, 16)
        bus = int(bus, 16)
    context = usb1.LibUSBContext()
    for device in context.getDeviceList():
        if (vendor is not None and (vendor != device.getVendorID() or \
                (product is not None and product != device.getProductID()))) \
                or (bus is not None and (bus != device.getBusNumber() or \
                (dev is not None and dev != device.getDeviceAddress()))):
            continue
        break
    else:
        print 'No device found.'
        sys.exit(1)
    dfu_device = dfu.DFU(device.open())
    print dfu_device.upload()

if __name__ == '__main__':
    main()


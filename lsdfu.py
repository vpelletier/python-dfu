#!/usr/bin/env python
import usb1
import dfu

mode_caption_dict = {
    dfu.DFU_PROTOCOL_RUNTIME: 'Device firmware',
    dfu.DFU_PROTOCOL_DFU_MODE: 'DFU',
}

if __name__ == '__main__':
    context = usb1.LibUSBContext()
    for device in context.getDeviceList():
        try:
            attr, detach, size, version, protocol, iface, descriptor_list = \
                dfu.getDFUDescriptor(device)
        except dfu.DFUUnsupportedError:
            continue
        print 'Bus %03i Device %03i: ID %04x:%04x' % (
            device.getBusNumber(),
            device.getDeviceAddress(),
            device.getVendorID(),
            device.getProductID(),
        )
        print '  Version: %x.%x' % (version >> 8, version & 0xff)
        print '  Attributes: 0x%02x (%s)' % (attr, ', '.join(x for x in (
            (attr & dfu.DFU_ATTRIBUTE_WILL_DETACH) and 'will detach',
            (attr & dfu.DFU_ATTRIBUTE_MANIFESTATION_TOLERANT) and \
                'manifestation tolerant',
            (attr & dfu.DFU_ATTRIBUTE_CAN_UPLOAD) and 'can upload',
            (attr & dfu.DFU_ATTRIBUTE_CAN_DOWNLOAD) and 'can download',
        ) if x))
        print '  Detach timeout: %s ms' % (detach, )
        print '  Transfer size: %s bytes' % (size, )
        print '  Mode: %s' % (mode_caption_dict.get(protocol,
            '(unknown: 0x%02x)' % (protocol, )), )


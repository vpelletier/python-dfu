#!/usr/bin/env python
import libusb1
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
        try:
            handle = device.open()
        except libusb1.USBError, exc:
            print '  (failed opening device, skipping)'
            continue
        dfup = dfu.DFUProtocol(handle)
        if dfup.hasSTMExtensions():
            print '  Mappings:'
            for mapping in dfup.STM_getDeviceMappingList():
                name = repr(mapping['name'])
                if mapping['alias']:
                    name += ' (alias: %r)'
                size = sum(x['count'] * x['size'] for x in mapping['sectors'])
                base = mapping['address']
                print '    0x%x..0x%x (%i bytes): %s' % (base, base + size - 1,
                    size, name)
                for sector in mapping['sectors']:
                    mode = sector['mode']
                    top = base + sector['count'] * sector['size']
                    print '      0x%x..0x%x: %i sectors of %i bytes, %s' % (
                        base, top - 1, sector['count'], sector['size'],
                        ', '.join(x for x in (
                            (mode & dfu.DFU_ST_SECTOR_MODE_R) and 'read',
                            (mode & dfu.DFU_ST_SECTOR_MODE_E) and 'erase',
                            (mode & dfu.DFU_ST_SECTOR_MODE_W) and 'write',
                        ) if x))
                    base = top


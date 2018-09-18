import re


def tuple_to_decimal(gps_tuple):
    '''
    The definition of the tuple is

    degrees, minutes, seconds

    Each one has a number and a scale, e.g. seconds can be

    (3456, 1000)

    meaning it needs to be divided by that number.
    '''
    degrees_info, minutes_info, seconds_info = gps_tuple

    degrees = degrees_info[0] / degrees_info[1]
    minutes = minutes_info[0] / minutes_info[1]
    seconds = seconds_info[0] / seconds_info[1]

    return degrees + minutes / 60 + seconds / 3600


def ddm_to_decimal(gps_ddm):
    '''
    DDM format is defined as a string, which includes the reference
    and divides degrees and minutes by a comma. Minutes are
    defined with decimal points. E.g.

    DD,MMM.MMMMR

    Being R the reference.

    No seconds are included, as the minutes are given including
    decimal points.
    '''
    match = re.match(r'(\d+),([\d.]+)(N|S|E|W)', gps_ddm)
    degrees, dminutes, ref = match.groups()

    decimal = float(degrees) + float(dminutes) / 60
    return f'{ref}{decimal}'


def exif_to_decimal(exif_info):
    latitude = tuple_to_decimal(exif_info['GPSLatitude'])
    latref = exif_info['GPSLatitudeRef']
    longitude = tuple_to_decimal(exif_info['GPSLongitude'])
    longref = exif_info['GPSLongitudeRef']

    return f'{latref}{latitude}', f'{longref}{longitude}'


def rdf_to_decimal(rdf_info):
    latitude = ddm_to_decimal(rdf_info['exif:GPSLatitude'])
    longitude = ddm_to_decimal(rdf_info['exif:GPSLongitude'])

    return latitude, longitude

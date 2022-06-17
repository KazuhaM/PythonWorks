from pyproj import Proj

def eqa2Utm(lon, lat, zone = True):
    if lon == "":
        return -1
    elif lat == "":
        return -2
    else:
        ##Compute UTM zone
        #"int": Extract only integer value
        #31: Offset for UTM zone definition
        #6: Angle in a UTM zone for the longitude direction
        e2u_zone=int(divmod(lon, 6)[0])+31

        #Define EQA2UTM converter
        e2u_conv=Proj(proj='utm', zone=e2u_zone, ellps='WGS84')
        #Apply the converter
        utmx, utmy=e2u_conv(lon, lat)
        #Add offset if the point in the southern hemisphere
        if lat<0:
            utmy=utmy+10000000

        # print(" UTM zone is ", e2u_zone, " \n", \
        #     "UTM Easting is", utmx, "[m]\n",\
        #     "UTM Northing is ", utmy, "[m]")
        if zone:
            return e2u_zone, utmx, utmy
        else:
            return utmx, utmy
        
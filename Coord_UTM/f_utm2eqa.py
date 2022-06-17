from pyproj import Proj

def utm2Eqa(utmx, utmy, zone = 48, hemi = 'N', ellps='WGS84'):
    if utmx == "":
        return -1
    elif utmy == "":
        return -2
    else:
        ##Compute UTM zone
        #"int": Extract only integer value
        #31: Offset for UTM zone definition
        #6: Angle in a UTM zone for the longitude direction
        #Add offset if the point in the southern hemisphere
        if hemi=='S':
            utmy=utmy-10000000

        #Define EQA2UTM converter
        e2u_conv=Proj(proj='utm', zone=zone, ellps='WGS84')
        #Apply the converter
        lon, lat=e2u_conv(utmx, utmy, inverse=True)

        # print(" UTM zone is ", e2u_zone, " \n", \
        #     "UTM Easting is", utmx, "[m]\n",\
        #     "UTM Northing is ", utmy, "[m]")
        return lon, lat
import numpy as np
from lsst.sims.featureScheduler.utils import read_fields

np.random.seed(42)

fields_init = read_fields()


def thetaphi2xyz(theta, phi):
    x = np.sin(phi)*np.cos(theta)
    y = np.sin(phi)*np.sin(theta)
    z = np.cos(phi)
    return x, y, z


def xyz2thetaphi(x, y, z):
    phi = np.arccos(z)
    theta = np.arctan2(y, x)
    return theta, phi


def rotx(theta, x, y, z):
    """rotate the x,y,z points theta radians about x axis"""
    sin_t = np.sin(theta)
    cos_t = np.cos(theta)
    xp = x
    yp = y*cos_t+z*sin_t
    zp = -y*sin_t+z*cos_t
    return xp, yp, zp


def _spin_fields(lon=None, lat=None, lon2=None):
        """Spin the field tessellation to generate a random orientation

        The default field tesselation is rotated randomly in longitude, and then the
        pole is rotated to a random point on the sphere.

        Parameters
        ----------
        lon : float (None)
            The amount to initially rotate in longitude (radians). Will use a random value
            between 0 and 2 pi if None (default).
        lat : float (None)
            The amount to rotate in latitude (radians).
        lon2 : float (None)
            The amount to rotate the pole in longitude (radians).
        """
        if lon is None:
            lon = np.random.rand()*np.pi*2
        if lat is None:
            # Make sure latitude points spread correctly
            # http://mathworld.wolfram.com/SpherePointPicking.html
            lat = np.arccos(2.*np.random.rand() - 1.)
        if lon2 is None:
            lon2 = np.random.rand()*np.pi*2
        # rotate longitude
        ra = (fields_init['RA'] + lon) % (2.*np.pi)
        dec = fields_init['dec'] + 0

        # ra and dec here are the same!
        

        # Now to rotate ra and dec about the x-axis
        x, y, z = thetaphi2xyz(ra, dec+np.pi/2.)
        return np.round(x, decimals=10), np.round(y, decimals=10), np.round(z, decimals=10)
        xp, yp, zp = rotx(lat, x, y, z)
        # xp, yp, zp don't match here
        theta, phi = xyz2thetaphi(xp, yp, zp)

        # theta and phi don't match here
        dec = phi - np.pi/2
        ra = theta + np.pi



        # One more RA rotation
        ra = (ra + lon2) % (2.*np.pi)

        # Rebuild the kdtree with the new positions
        # XXX-may be doing some ra,dec to conversions xyz more than needed.
        return ra, dec


if __name__ == "__main__":

    three = True
    f = open('outcheck.txt', 'w')
    if three:
        x,y,z = _spin_fields()
        for xx, yy, zz in zip(x,y,z):
            f.write('%.15f, %.15f, %.15f \n' % (xx, yy, zz))
    else:
        ra, dec = _spin_fields()
        
        for raa, decc in zip(ra, dec):
            f.write('%.15f, %.15f \n' % (raa, decc))
    f.close()


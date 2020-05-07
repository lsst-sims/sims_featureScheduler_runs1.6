import numpy as np
from lsst.sims.featureScheduler.thomson import xyz2thetaphi, thetaphi2xyz
from lsst.sims.featureScheduler.utils import read_fields

np.random.seed(42)

fields_init = read_fields()


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

        # Now to rotate ra and dec about the x-axis
        x, y, z = thetaphi2xyz(ra, dec+np.pi/2.)
        xp, yp, zp = rotx(lat, x, y, z)
        theta, phi = xyz2thetaphi(xp, yp, zp)
        dec = phi - np.pi/2
        ra = theta + np.pi

        # One more RA rotation
        ra = (ra + lon2) % (2.*np.pi)

        # Rebuild the kdtree with the new positions
        # XXX-may be doing some ra,dec to conversions xyz more than needed.
        return ra, dec


if __name__ == "__main__":

    ra, dec = _spin_fields()
    import pdb ; pdb.set_trace()
# -*- coding: utf-8 -*-
#
# Copyright 2009, BlueDynamics Alliance, Austria - http://bluedynamics.com
#
# BSD License derivative - see egg-info

__author__ = """Jens Klein <jens@bluedynamics.com>"""
__docformat__ = 'plaintext'

from Products.Archetypes.Field import ImageField
from archetypes.clippingimage.utils import scale

class ClippingImageField(ImageField):
    """Like default ImageField from Archetypes with different scaling behaviour.

    Scales are clipped centered, the resulting image has almost (+/- 1 pixel)
    the scale.
    """

    _properties = ImageField._properties.copy()
    _properties.update({'classic_crop': []})

    def scale(self, data, w, h, default_format = 'PNG'):        
        """ scale image"""
        return scale(self, data, w, h, default_format)

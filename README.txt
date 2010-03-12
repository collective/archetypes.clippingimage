Image field for ``Archetypes`` with different behavior at time of scaling.

============
Introduction
============

Archtypes default ``ImageField`` scales down the image until the whole image
fits into the given scale. It keeps it aspect ratio. I.e. scaling down a 400x300
image to a 200x200 scale result in a 200x150 image.

Same with ``ClippingImageField`` results in a 200x200 image! It centers the
image horizontal or vertical and tries to keep as much as possible from the
original.

Tested with Plone 3.3.x and Plone 4.

======
Usage:
======

Specify the sizes as documented for the classic Archetypes ImageField. If you
want specific scales to not get clipped, add a field-property
``classic_crop=['image_large','other_scale']``. It expects a list of scale
names to exclude from clipping.

Since version 1.2 dont forget to include the configure.zcml in your setup.


By including `patch.zcml` in your package `archetypes.clippingimage` allows you to patch
`Products.Archetypes.Field.ImageField` so it is able to generate cropped scales.

You can define which scales shall be cropped by adding a property ``crop_scales`` to your ImageField::

    ImageField('image',
        sizes= {'large'   : (768, 768),
                'preview' : (400, 400),
                'listing' :  (16, 16),
                },
        crop_scales = ['listing'],
        ...

Note that if you want to patch ATCTImage and have `plone.app.imaging` installed you need
to patch `plone.app.blob.subtypes.image`.


=========
Copyright
=========

written by Jens W. Klein, BlueDynamics Alliance, Klein & Partner KG, Austria
http://bluedynamics.com

Contributions Harald Friesnegger and Peter Holzer.

=========
Changelog
=========

1.2
---

- make plone.app.imaging and plone.app.blob aware. Works now with Plone 4.
  [jensens]

- sizes can be a callable or a dictionary (instance method not supported)

  background: plone.app.imaging uses the sizes defined in imaging_properties in case sizes is a dictionary.
  so you need to define sizes via a callable to make your custom sizes take effect.
  [fRiSi]

- added monkeypatch for ImageField.scale to add croppingsupport to any ImageField
  [jensens, fRiSi]
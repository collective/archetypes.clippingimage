Image field for ``Archetypes`` with different behavior at time of scaling.

.. ATTENTION:: this package is no longer supported, you might want to have a
   look at `plone.app.imagecropping`__ as an alternative

   .. __: https://pypi.python.org/pypi/plone.app.imagecropping


============
Introduction
============

Archtypes default ``ImageField`` scales down the image until the whole image
fits into the given scale. It keeps it aspect ratio. I.e. scaling down a 400x300
image to a 200x200 scale result in a 200x150 image.

Same with ``ClippingImageField`` results in a 200x200 image! It centers the
image horizontal or vertical and tries to keep as much as possible from the
original.

Tested with Plone 3.3.x and Plone 4.3

======
Usage:
======

Field
=====

Specify the sizes as documented for the classic Archetypes ImageField. If you
want specific scales to get clipped, add a field-property
``crop_scales=['image_large','other_scale']``. It expects a list of scale
names to include into clipping.

Patch
=====

By including ``patch.zcml`` in your package ``archetypes.clippingimage`` will
patch ``Products.Archetypes.Field.ImageField`` so it is able to generate
cropped scales.

You can define which scales shall be cropped by adding a property ``crop_scales``
to your ImageField::

    ImageField('image',
        sizes= {'large'   : (768, 768),
                'preview' : (400, 400),
                'listing' :  (16, 16),
                },
        crop_scales = ['listing'],
        ...

Note that if you want to use clipped images within ATCTImage and have
``plone.app.imaging`` installed you need to set a property ``crop_scales`` at
``plone.app.blob.subtypes.image.SchemaExtender.fields[0]``.

Blob
====

In case of using the patch everythings fine. No further action needed. If you
use the field, you need to include the ``blob.zcml`` to make the fields scales
blobs.

=========
Copyright
=========

written by Jens W. Klein, BlueDynamics Alliance, Klein & Partner KG, Austria
http://bluedynamics.com

Contributions Harald Friessnegger and Peter Holzer.

=========
Changelog
=========

3.0 (unreleased)
================

- make automatic cropping of images work on plone 4.2 and 4.3 (by monkey
  patching the monkey patch of plone.app.imaging)

  scales accessed via image/@@images/image/thumb to not get cropped.
  this just works for image/image_thumb
  [fRiSi]

2.1
===

- use the format of original image for computing the crop. the field
  used to convert everything to png which resulted in relatively large files
  [fRiSi]

2.0
===

- make plone.app.imaging and plone.app.blob aware. Works now with Plone 4.
  [jensens]

- sizes can be a callable or a dictionary (instance method not supported)

  background: plone.app.imaging uses the sizes defined in imaging_properties in case sizes is a dictionary.
  so you need to define sizes via a callable to make your custom sizes take effect.
  [fRiSi]

- added monkeypatch for ImageField.scale to add croppingsupport to any ImageField
  [jensens, fRiSi]

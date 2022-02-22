import PIL
from StringIO import StringIO
from Products.CMFPlone.utils import safe_hasattr
from plone.app.imaging.utils import getQuality

import logging


logger = logging.getLogger(__name__)


def crop(image, scale):
    """Crop given image to scale.

    @param image: PIL Image instance
    @param scale: tuple with (width, height)
    """
    cwidth, cheight = image.size
    cratio = float(cwidth) / float(cheight)
    twidth, theight = scale
    tratio = float(twidth) / float(theight)
    if cratio > tratio:
        middlepart = cheight * tratio
        offset = (cwidth - middlepart) / 2
        box = int(round(offset)), 0, int(round(offset + middlepart)), cheight
        image = image.crop(box)
    if cratio < tratio:
        middlepart = cwidth / tratio
        offset = (cheight - middlepart) / 2
        box = 0, int(round(offset)), cwidth, int(round(offset + middlepart))
        image = image.crop(box)
    return image


# method scale is copied from Products.Archetypes.Field.ImageField.scale
# (Products.Archetypes 1.9.21)
# see License over there
def scale(instance, data, w, h, default_format='PNG'):
    """ scale image"""
    size = int(w), int(h)
    original_file = StringIO(data)
    image = PIL.Image.open(original_file)
    format = image.format
    # does not work for sizes='instanceMethod' since we don't have an instance here
    availableSizes = instance.getAvailableSizes(None)

    if format == 'GIF' and size[0] >= image.size[0] and size[1] >= image.size[1]:
        try:
            image.seek(image.tell() + 1)
            # original image is animated GIF and no bigger than the scale requested
            # don't attempt to scale as this will lose animation
            original_file.seek(0)
            return original_file, 'gif'
        except EOFError:
            # image is not animated
            image.seek(0)

    if safe_hasattr(instance, 'crop_scales'):
        #if our field defines crop_scales let's see if the current sizes shall be cropped
        if size in [availableSizes[name] for name in instance.crop_scales]:
            image = crop(image, size)

    # consider image mode when scaling
    # source images can be mode '1','L,','P','RGB(A)'
    # convert to greyscale or RGBA before scaling
    # preserve palletted mode (but not pallette)
    # for palletted-only image formats, e.g. GIF
    # PNG compression is OK for RGBA thumbnails
    original_mode = image.mode
    img_format = image.format and image.format or default_format
    if img_format in ('TIFF', 'EPS', 'PSD'):
        # non web image format have jpeg thumbnails
        target_format = 'JPEG'
    else:
        target_format = img_format

    if original_mode == '1':
        image = image.convert('L')
    elif original_mode == 'P':
        image = image.convert('RGBA')
    elif original_mode == 'CMYK':
        image = image.convert('RGBA')

    image.thumbnail(size, instance.pil_resize_algo)

    # decided to only preserve palletted mode
    # for GIF, could also use image.format in ('GIF','PNG')
    if original_mode == 'P' and img_format == 'GIF':
        image = image.convert('P')

    thumbnail_file = StringIO()
    # quality parameter doesn't affect lossless formats
    image.save(thumbnail_file, target_format, quality=instance.pil_quality)
    thumbnail_file.seek(0)
    return thumbnail_file, target_format.lower()



#copied from plone.app.imaging.monkey.scale (version 1.0.14)
def plone_app_imaging_scale(self, data, w, h, default_format='PNG'):
    """ use our quality setting as pil_quality """
    pil_quality = getQuality()

    #make sure we have valid int's
    size = int(w), int(h)

    original_file = StringIO(data)
    image = PIL.Image.open(original_file)

    if image.format == 'GIF' and size[0] >= image.size[0] \
            and size[1] >= image.size[1]:
        try:
            image.seek(image.tell() + 1)
            # original image is animated GIF and no bigger than the scale
            # requested
            # don't attempt to scale as this will lose animation
            original_file.seek(0)
            return original_file, 'gif'
        except EOFError:
            # image is not animated
            image.seek(0)

    # consider image mode when scaling
    # source images can be mode '1','L,','P','RGB(A)'
    # convert to greyscale or RGBA before scaling
    # preserve palletted mode (but not pallette)
    # for palletted-only image formats, e.g. GIF
    # PNG compression is OK for RGBA thumbnails
    original_mode = image.mode
    img_format = image.format and image.format or default_format
    if img_format in ('TIFF', 'EPS', 'PSD'):
        # non web image format have jpeg thumbnails
        target_format = 'JPEG'
    else:
        target_format = img_format

    if original_mode == '1':
        image = image.convert('L')
    elif original_mode == 'P':
        image = image.convert('RGBA')
    elif original_mode == 'CMYK':
        image = image.convert('RGBA')


    #### custom code cropping ######
    try:
        #does not work for sizes='instanceMethod' since we don't have an instance here
        availableSizes = self.getAvailableSizes(None)

        if safe_hasattr(self, 'crop_scales'):
            #if our field defines crop_scales let's see if the current sizes shall be cropped
            if size in [availableSizes[name] for name in self.crop_scales]:
                image = crop(image, size)
    #### end  custom code #######

        image.thumbnail(size, self.pil_resize_algo)


        # decided to only preserve palletted mode
        # for GIF, could also use image.format in ('GIF','PNG')
        if original_mode == 'P' and img_format == 'GIF':
            image = image.convert('P')

        # Avoid - IOError: cannot write mode RGBA as JPEG
        # See https://github.com/python-pillow/Pillow/issues/2609#issuecomment-313841918
        if original_mode in ('CMYK', 'RGBA', 'LA') and target_format in ('JPG', 'JPEG'):
            target_format = 'PNG'

        thumbnail_file = StringIO()
        # quality parameter doesn't affect lossless formats
        image.save(thumbnail_file, target_format, quality=pil_quality, progressive=True)
        thumbnail_file.seek(0)
        return thumbnail_file, target_format.lower()

    ### custom: error handling
    except Exception, e:
        if not self.swallowResizeExceptions:
            raise e
        else:
            logger.warning("error when cropping image: %s", e)
            return None, None
    ### end custom
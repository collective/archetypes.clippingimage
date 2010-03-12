import PIL
from StringIO import StringIO
from Products.CMFPlone.utils import safe_hasattr
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
        box = int(round(offset)), 0, int(round(offset+middlepart)), cheight
        image = image.crop(box)
    if cratio < tratio:
        middlepart = cwidth / tratio
        offset = (cheight - middlepart) / 2
        box = 0, int(round(offset)), cwidth, int(round(offset+middlepart))
        image =  image.crop(box)
    return image


# method scale is copied from Products.Archetypes.Field.ImageField.scale
# see License over there
def scale(instance, data, w, h, default_format = 'PNG'):
    """ scale image"""
    size = int(w), int(h)
    original_file=StringIO(data)
    image = PIL.Image.open(original_file)
    #does not work for sizes='inscanteMethod' since we don't have an instance here
    availableSizes = instance.getAvailableSizes(None)

    if safe_hasattr(instance, 'crop_scales'):
        #if our field defines crop_scales let's see if the current sizes shall be cropped
        if size in [availableSizes[name] for name in instance.crop_scales]:
            image = crop(image, size)

    original_mode = image.mode
    if original_mode == '1':
        image = image.convert('L')
    elif original_mode == 'P':
        image = image.convert('RGBA')
    image.thumbnail(size, instance.pil_resize_algo)
    format = image.format and image.format or default_format
    if original_mode == 'P' and format == 'GIF':
        image = image.convert('P')
    thumbnail_file = StringIO()
    image.save(thumbnail_file, format, quality=instance.pil_quality)
    thumbnail_file.seek(0)
    return thumbnail_file, format.lower()
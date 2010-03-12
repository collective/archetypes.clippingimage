import PIL
from StringIO import StringIO

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
    availableSizes = self.getAvailableSizes(None)
    if size not in [availableSizes[name] for name in self.classic_crop]:
        image = crop(image, size)
    original_mode = image.mode
    if original_mode == '1':
        image = image.convert('L')
    elif original_mode == 'P':
        image = image.convert('RGBA')
    image.thumbnail(size, self.pil_resize_algo)
    format = image.format and image.format or default_format
    if original_mode == 'P' and format == 'GIF':
        image = image.convert('P')
    thumbnail_file = StringIO()
    image.save(thumbnail_file, format, quality=self.pil_quality)
    thumbnail_file.seek(0)
    return thumbnail_file, format.lower()
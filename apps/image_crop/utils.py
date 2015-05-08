import re
import cStringIO
import string
from unicodedata import normalize, decomposition

try:
    from PIL import Image
    Image
except:
    import Image

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _

from image_crop.exceptions import ImageUploadError

# normalizers based on plone.i18n.normalizer
# but with the plone locale utils removed

# Define and compile static regexes
FILENAME_REGEX = re.compile(r"^(.+)\.(\w{,4})$")
IGNORE_REGEX = re.compile(r"['\"]")
NON_WORD_REGEX = re.compile(r"[\W\-]+")
DANGEROUS_CHARS_REGEX = re.compile(r"[!$%&()*+,/:;<=>?@\\^{|}\[\]~`]+")
URL_DANGEROUS_CHARS_REGEX = re.compile(r"[!#$%&()*+,/:;<=>?@\\^{|}\[\]~`]+")
MULTIPLE_DASHES_REGEX = re.compile(r"\-+")
EXTRA_DASHES_REGEX = re.compile(r"(^\-+)|(\-+$)")
UNDERSCORE_START_REGEX = re.compile(r"(^_+)(.*)$")
# Define static constraints
MAX_LENGTH = 50
MAX_FILENAME_LENGTH = 1023
MAX_URL_LENGTH = 255


def cropName(base, maxLength=MAX_LENGTH):
    baseLength = len(base)

    index = baseLength
    while index > maxLength:
        index = base.rfind('-', 0, index)

    if index == -1 and baseLength > maxLength:
        base = base[:maxLength]

    elif index > 0:
        base = base[:index]

    return base


whitespace = ''.join([c for c in string.whitespace if ord(c) < 128])
allowed = string.ascii_letters \
    + string.digits \
    + string.punctuation \
    + whitespace

CHAR = {}
NULLMAP = ['' * 0x100]
UNIDECODE_LIMIT = 0x0530


def mapUnicode(text, mapping=()):
    """
    This method is used for replacement of special characters found in a
    mapping before baseNormalize is applied.
    """
    res = u''
    for ch in text:
        ordinal = ord(ch)
        if ordinal in mapping:
            # try to apply custom mappings
            res += mapping.get(ordinal)
        else:
            # else leave untouched
            res += ch
    # always apply base normalization
    return baseNormalize(res)


def baseNormalize(text):
    """
    This method is used for normalization of
    unicode characters to the base ASCII
    letters. Output is ASCII encoded string
    (or char) with only ASCII letters,
    digits, punctuation and whitespace characters.
    Case is preserved.

      >>> baseNormalize(123)
      '123'

      >>> baseNormalize(u'a\u0fff')
      'afff'

      >>> baseNormalize(u"foo\N{LATIN CAPITAL LETTER I WITH CARON}")
      'fooI'

      >>> baseNormalize(u"\u5317\u4EB0")
      '53174eb0'
    """
    if not isinstance(text, basestring):
        # This most surely ends up in something the user does not expect
        # to see. But at least it does not break.
        return repr(text)

    text = text.strip()

    res = []
    for ch in text:
        if ch in allowed:
            # ASCII chars, digits etc. stay untouched
            res.append(ch)
        else:
            ordinal = ord(ch)
            if ordinal < UNIDECODE_LIMIT:
                h = ordinal >> 8
                l = ordinal & 0xff

                c = CHAR.get(h, None)

                if c is None:
                    try:
                        mod = __import__(
                            'unidecode.x%02x' % (h), [], [], ['data'])
                    except ImportError:
                        CHAR[h] = NULLMAP
                        res.append('')
                        continue

                    CHAR[h] = mod.data

                    try:
                        res.append(mod.data[l])
                    except IndexError:
                        res.append('')
                else:
                    try:
                        res.append(c[l])
                    except IndexError:
                        res.append('')

            elif decomposition(ch):
                normalized = normalize('NFKD', ch).strip()
                # string may contain non-letter chars too. Remove them
                # string may result to more than one char
                res.append(''.join([c for c in normalized if c in allowed]))

            else:
                # hex string instead of unknown char
                res.append("%x" % ordinal)

    return ''.join(res).encode('ascii')


class IDNormalizer(object):

    def normalize(self, text, max_length=MAX_LENGTH):
        """
        Returns a normalized text. text has to be a unicode string and locale
        should be a normal locale, for example: 'pt_BR', 'sr@Latn' or 'de'
        """
        text = baseNormalize(text)

        # lowercase text
        text = text.lower()

        text = IGNORE_REGEX.sub('', text)
        text = NON_WORD_REGEX.sub('-', text)
        text = MULTIPLE_DASHES_REGEX.sub('-', text)
        text = EXTRA_DASHES_REGEX.sub('', text)

        return cropName(text, maxLength=max_length)


class FileNameNormalizer(object):

    def normalize(self, text, max_length=MAX_FILENAME_LENGTH):
        """
        Returns a normalized text. text has to be a unicode string and locale
        should be a normal locale, for example: 'pt_BR', 'sr@Latn' or 'de'
        """

        # Preserve filename extensions
        text = baseNormalize(text)

        # Remove any leading underscores
        m = UNDERSCORE_START_REGEX.match(text)
        if m is not None:
            text = m.groups()[1]

        base = text
        ext = ''

        m = FILENAME_REGEX.match(text)
        if m is not None:
            base = m.groups()[0]
            ext = m.groups()[1]

        base = IGNORE_REGEX.sub('', base)
        base = DANGEROUS_CHARS_REGEX.sub('-', base)
        base = EXTRA_DASHES_REGEX.sub('', base)
        base = MULTIPLE_DASHES_REGEX.sub('-', base)

        base = cropName(base, maxLength=max_length)

        if ext != '':
            base = base + '.' + ext

        return base


class URLNormalizer(object):

    def normalize(self, text, max_length=MAX_URL_LENGTH):
        """
        """

        text = baseNormalize(text)

        # lowercase text
        base = text.lower()
        ext = ''

        m = FILENAME_REGEX.match(base)
        if m is not None:
            base = m.groups()[0]
            ext = m.groups()[1]

        base = NON_WORD_REGEX.sub('-', base)
        base = IGNORE_REGEX.sub('', base)
        base = URL_DANGEROUS_CHARS_REGEX.sub('-', base)
        base = EXTRA_DASHES_REGEX.sub('', base)
        base = MULTIPLE_DASHES_REGEX.sub('-', base)

        base = cropName(base, maxLength=max_length)

        if ext != '':
            base = base + '.' + ext

        return base

idnormalizer = IDNormalizer()
filenamenormalizer = FileNameNormalizer()
urlnormalizer = URLNormalizer()


def calculate_size_for_max(size, max_size):
    x, y = size
    mx, my = max_size
    newx = x
    newy = y
    if x > mx:
        newx = mx
        newy = (float(mx) / x) * y
    if newy > my:
        newy = my
        newx = (float(my) / y) * x
    return int(newx), int(newy)


def generate_thumb_maintain_aspect(original, size, format='JPEG', coords=None):
    """
    Generates a thumbnail image maintaing original aspect and returns
    a ContentFile object with the thumbnail

    Arguments:
    original -- The image being resized as `File`.
    size     -- Desired thumbnail size as `tuple`. Example: (70, 100)
    format   -- Format of the original image ('JPEG', 'PNG', ...)
                The thumbnail will be generated using this same format.

    """

    original.seek(0)
    image = Image.open(original)
    if image.mode not in ('L', 'RGB', 'RGBA'):
        image = image.convert('RGB')

    # calculate size..
    size = calculate_size_for_max(image.size, size)

    # use image.resize here instead...
    thumbnail = image.resize(size, Image.ANTIALIAS)
    io = cStringIO.StringIO()
    if format.upper() == 'JPG':
        format = 'JPEG'
    thumbnail.save(io, format)
    return ContentFile(io.getvalue())


def crop_thumb_to_coords(original, size, coords, format='JPEG'):
    """
    """

    original.seek(0)
    image = Image.open(original)
    if image.mode not in ('L', 'RGB', 'RGBA'):
        image = image.convert('RGBA')

    thumbnail = image.crop(coords)
    io = cStringIO.StringIO()

    x, y = thumbnail.size
    if size[0] < x or size[1] < y:
        thumbnail = thumbnail.resize(size, Image.ANTIALIAS)

    if format.upper() == 'JPG':
        format = 'JPEG'
    thumbnail.save(io, format)

    return ContentFile(io.getvalue())


def normalize_filename(filename, max_length=255):
    ext = filename.split('.').pop()
    if ext:
        base = filename[:-len(ext)]
    else:
        base = filename
    return '%s.%s' % (
        idnormalizer.normalize(base, max_length), ext.lower())


def delete_cropped_image(imageid):

    from image_crop.models import TempImage

    try:
        temp_image = TempImage.objects.get(filename=imageid)
    except ObjectDoesNotExist:
        return

    if not temp_image:
        return

    temp_image.delete()


def retrieve_cropped_image(imageid, delete=False):

    from image_crop.models import TempImage

    try:
        temp_image = TempImage.objects.get(filename=imageid)
    except ObjectDoesNotExist:
        return

    if not temp_image:
        return

    if delete:
        temp_image.delete()

    temp_image.original.seek(0)
    content = temp_image.original.read()
    filename = temp_image.filename[
        temp_image.filename.index('_') + 1:]
    return {
        'filename': filename,
        'coords': temp_image.data['coords'],
        'content': SimpleUploadedFile(filename, content)}


def calculate_auto_crop(image, min_size):

    from PIL import Image
    image.open()
    image.seek(0)
    original = Image.open(image)

    percentage = 70

    orig_width = original.size[0]
    orig_height = original.size[1]

    square = (
        orig_height > orig_width) and orig_width or orig_height

    new_size = square
    while percentage < 100:
        resized = int(square * (float(percentage) / 100))
        if resized > min_size:
            new_size = resized
            break
        percentage += 10

    xl = (orig_width - new_size) / 2
    xr = orig_width - xl
    yt = (orig_height - new_size) / 2
    yb = orig_height - yt

    return xl, yt, xr, yb


def validate_uploaded_image(upfile, min_width=None, min_height=None, need_size=None):
    upfile.open()
    upfile.seek(0)
    try:
        image = Image.open(cStringIO.StringIO(upfile.read()))
    except:
        raise ImageUploadError(
            _('The uploaded file was not recognised as an image'))


    # Both width & height must be above the specified resolution
    if image.size[0] < min_width:
        raise ImageUploadError(
            _('The image must be at least %s pixels wide' % min_width))
    if image.size[1] < min_height:
        raise ImageUploadError(
            _('The image must be at least %s pixels high' % min_height))

    if need_size is not None:
        # Only one of the dimensions must be above the min dimension
        if image.size[0] < need_size or image.size[1] < need_size:
            raise ImageUploadError(_('The image width or height must be at least %s pixels' % (need_size,)))

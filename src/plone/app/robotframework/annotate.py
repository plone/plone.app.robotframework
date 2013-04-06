# -*- coding: utf-8 -*-


class Annotate:

    def crop_image(self, filename, left, top, width, height):
        """Crop the saved image with given filename for the given dimensions.
        """
        from PIL import Image

        img = Image.open(filename)
        box = (int(left), int(top), int(left + width), int(top + height))

        area = img.crop(box)

        with open(filename, 'wb') as output:
            area.save(output, 'png')

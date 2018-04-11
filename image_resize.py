import argparse
from PIL import Image
from os import path


def get_args():
    parser = argparse.ArgumentParser(
        description='Image resize'
    )
    parser.add_argument(
        '--image',
        '-i',
        required=True,
        help='path to image'
    )
    parser.add_argument(
        '--width',
        '-w',
        help='width of the resulting image',
        type=positive_int
    )
    parser.add_argument(
        '--height',
        '-hgt',
        help='height of the resulting image',
        type=positive_int
    )
    parser.add_argument(
        '--scale',
        '-s',
        help='how many times increase the image',
        type=positive_float
    )
    parser.add_argument(
        '--output',
        '-o',
        help='path to the resulting image',
    )
    return parser.parse_args()


def positive_int(arg):
    if arg.isdigit() and int(arg) > 0:
        return int(arg)
    else:
        raise argparse.ArgumentTypeError


def positive_float(arg):
    try:
        float_arg = float(arg)
        if float_arg > 0:
            return float_arg
        else:
            raise argparse.ArgumentTypeError
    except ValueError:
        raise argparse.ArgumentTypeError


def open_image(image_path):
    try:
        image = Image.open(image_path)
        return image
    except IOError:
        return None


def get_size_output(
        width_original,
        height_original,
        width_output=None,
        height_output=None,
        scale=None
):
    if scale and not (width_output or width_output):
        output_size = (
            int(width_original * scale) or 1,
            int(height_original * scale) or 1
        )
        return output_size
    original_proportion = width_original / height_original
    if width_output and not height_output:
            height_output = int(width_output / original_proportion) or 1
    elif not width_output and height_output:
            width_output = int(height_output * original_proportion) or 1
    return width_output, height_output


def resize_image(
        original_image,
        size_output

):
    return original_image.resize(size_output)


def is_proportion_preserved(
        size_output,
        width_original,
        height_original
):
    output_width, output_height = size_output
    output_proportion = round(output_width/output_height, 2)
    original_proportion = round(width_original/height_original, 2)
    if output_proportion == original_proportion:
        return True


def resize_image(original_image, size_output):
    if not (None in size_output):
        return original_image.resize(size_output)


def save_output_image(image_path, output_image, output_path=None):
    width_output, height_output = output_image.size
    if not output_path:
        name_image_original, format_image_original = path.splitext(image_path)
        output_path = '{name}__{width}x{height}{format}'.format(
            name=name_image_original,
            width=width_output,
            height=height_output,
            format=format_image_original
        )
    try:
        output_image.save(output_path)
    except ValueError:
        return None


if __name__ == '__main__':
    args = get_args()
    original_image = open_image(args.image)
    if original_image or exit('Can not open image!'):
        width_original, height_original = original_image.size
        size_output = get_size_output(
            width_original,
            height_original,
            width_output=args.width,
            height_output=args.height,
            scale=args.scale)
        output_image = (resize_image(original_image, size_output)
                        or exit('Invalid image size!')
                        )
        save_output_image(
            args.image,
            output_image,
            output_path=args.output
        ) or exit('Unknown file extension!')
        if not is_proportion_preserved(
                size_output,
                width_original,
                height_original
        ):
            print('The proportions do not match the original image!')
        print('Image successfully saved!')

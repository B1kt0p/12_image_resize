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


def get_output_image_size(
        original_image_width,
        original_image_height_,
        output_image_width=None,
        output_image_height=None,
        scale=None
):
    if scale and not (output_image_width or output_image_width):
        output_image_size = (
            int(original_image_width * scale) or 1,
            int(original_image_height_ * scale) or 1
        )
        return output_image_size
    original_proportion = original_image_width / original_image_height_
    if output_image_width and not output_image_height:
            output_image_height = int(output_image_width / original_proportion) or 1
    elif not output_image_width and output_image_height:
            output_image_width = int(output_image_height * original_proportion) or 1
    return output_image_width, output_image_height


def resize_image(
        original_image,
        output_image_size
):
    return original_image.resize(output_image_size)


def is_proportion_preserved(
        output_image_size,
        original_image_width,
        original_image_height
):
    output_image_width, output_image_height = output_image_size
    output_image_proportion = round(output_image_width / output_image_height, 2)
    original_image_proportion = round(original_image_width / original_image_height, 2)
    if output_image_proportion == original_image_proportion:
        return True


def resize_image(original_image, size_output):
    if not (None in size_output):
        return original_image.resize(size_output)


def save_output_image(image_path, output_image, output_path=None):
    image_output_width, image_output_height = output_image.size
    if not output_path:
        name_image_original, format_image_original = path.splitext(image_path)
        output_path = '{name}__{width}x{height}{format}'.format(
            name=name_image_original,
            width=image_output_width,
            height=image_output_height,
            format=format_image_original
        )
    try:
        output_image.save(output_path)
    except ValueError:
        return None


if __name__ == '__main__':
    args = get_args()
    original_image = open_image(args.image)
    if not original_image:
        exit('Can not open image!')
    original_image_width, original_image_height = original_image.size
    output_image_size = get_output_image_size(
        original_image_width,
        original_image_height,
        output_image_width=args.width,
        output_image_height=args.height,
        scale=args.scale)
    output_image = (resize_image(original_image, output_image_size)
                    or exit('Invalid image size!')
                    )
    save_output_image(
        args.image,
        output_image,
        output_path=args.output
    ) or exit('Unknown file extension!')
    if not is_proportion_preserved(
            output_image_size,
            original_image_width,
            original_image_height
    ):
        print('The proportions do not match the original image!')
    print('Image successfully saved!')

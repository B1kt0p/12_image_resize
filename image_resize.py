import argparse
from PIL import Image


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
        type=float
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


def open_image(image_path):
    try:
        image = Image.open(image_path)
    except IOError:
        return None
    return image


def get_width_and_height_output(
        width_original,
        height_original,
        width_output=None,
        height_output=None,
        scale=None
):
    original_proportion = width_original / height_original

    if scale and not (width_output or width_output):
        if scale < 0:
            return (
                int(width_original/abs(scale)),
                int(height_original/abs(scale))
            )
        elif scale > 0:
            return int(width_original*scale), int(height_original*scale)
    elif not scale and (width_output or height_output):
        if width_output and not height_output:
            height_output = int(width_output / original_proportion)
        elif not width_output and height_output:
            width_output = int(height_output * original_proportion)
        return height_output, width_output


def resize_image(
        path_to_original,
        width=None,
        height=None,
        scale=None
):
    original_image = open_image(path_to_original)
    if original_image:
        width_original, height_original = original_image.size
        size_output = get_width_and_height_output(
            width_original,
            height_original,
            width_output=width,
            height_output=height,
            scale=scale
        )
        if size_output and 0 not in size_output:
            output_image = original_image.resize(size_output)
            if not is_proportion_preserved(output_image,
                                        width_original,
                                        height_original):
                print('Image proportions do not match the original!')
            return output_image


def save_output_image(image_path, output_image, output_path=None):
    width_output, height_output = output_image.size
    if output_path is None:
        name_image_original, format_image_original = image_path.split('.')
        output_path = '{name}__{width}x{height}.{format}'.format(
            name=name_image_original,
            width=width_output,
            height=height_output,
            format=format_image_original
        )
    return output_image.save(output_path)

def is_proportion_preserved(
        output_image,
        height_original,
        width_original
):
    output_width, output_height = output_image.size
    output_proportion = int(output_width/output_height)
    original_proportion = int(width_original/height_original)
    if output_proportion == original_proportion:
        return True


if __name__ == '__main__':
    args = get_args()
    output_image = resize_image(
        args.image,
        width=args.width,
        height=args.height,
        scale=args.scale
    )
    if output_image:
        rt = save_output_image(
            args.image, output_image,
            output_path=args.output
        )
        print('Image successfully saved!')

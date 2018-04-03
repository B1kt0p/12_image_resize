# Image Resizer

The script accepts an image and places an 
image with a new size where the user or next
to the source says.  

The script uses arguments:
```bash
-i [--image] - path to image (required argument)
-w [--width] - width of the resulting image
-s [--scale] - how many times increase the image
-o [--output] - path to the resulting image
```
Logic of script operation:  

* If only the width is specified, the height is 
considered to preserve the aspect ratio of the image.
 And vice versa.

* If both width and height are specified, this is the
 image that is created.

* The console displays a warning if the proportions do 
not match the original image.

* If the scale is specified, the width and height can
 not be specified.

* If the path to the final file is not specified,
 the result is placed next to the source file. 
 In this case, the file is called pic.jpg (100x200), 
 then after the python image_resize.py --scale
  2 pic.jpg file pic__200x400.jpg appears.

# Get started:
An example of running a script in Linux, Python 3.5
 on other operating systems
 is also:
```bash
$ python3 image_resize.py -i 111.jpg  -s -2
Image successfully saved!

$ python3 image_resize.py -i 111.jpg  -w 10 -hgt 200
Image proportions do not match the original!
Image successfully saved!
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)

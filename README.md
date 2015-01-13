[travis-url]: http://travis-ci.org/#!/jordanjoz1/android-localization-helper
[travis-build-image]: https://secure.travis-ci.org/jordanjoz1/android-localization-helper.svg

[pypi-url]: https://badge.fury.io/py/android-localization-helper
[pypi-image]: https://badge.fury.io/py/android-localization-helper.svg

[downloads-url]: https://pypi.python.org/pypi/android-localization-helper/
[downloads-image]: https://pypip.in/d/android-localization-helper/badge.svg

[arsenal-url]: https://android-arsenal.com/details/1/1367
[arsenal-image]: https://img.shields.io/badge/Android%20Arsenal-android--localization--helper-brightgreen.svg?style=flat

[![Travis build image][travis-build-image]][travis-url]
[![PyPi version][pypi-image]][pypi-url]
[![PyPi download count image][downloads-image]][downloads-url]
[![Android Arsenal][arsenal-image]][arsenal-url]

android-localization-helper
===========================

Python script that checks for missing string translations in your project's localized languages.

If you're like us at [DoubleDutch](doubledutch.me), you occassionally lose track of what strings have and haven't been translated in each language.  Android Studio [made an awesome GUI](http://tools.android.com/recent/androidstudio087released) to help deal with this issue, but there is no easy way to export missing strings, so if you are missing more than a few strings in a language it can become a tenuous problem.


## Getting started
Requirements:

* Python >= 2.7.*
* [Standard Android project structure](https://developer.android.com/tools/projects/index.html) for localized values-* folders in `res/` folder

![Project structure](art/project_structure.png)

To install run:
```bash
pip install android-localization-helper
```

## Usage
`cd` to your `res/` folder, and run:

```
android-localization-helper
```

The script creates a directory called `to_translate/` ([sample output](./sample_output)) with separate files for the missing strings in each language.  This way you know exactly what translations you need to add for each language, and they are already in a standard format to send out for translation!


You can change the output folder:
```
android-localization-helper --output ~/Desktop/to_translate
```
  
  
And you can clean up your localized `strings.xml` files. This will remove strings that aren't in the default file and sort strings to match the default `strings.xml` order. **Warning:** *this will change your existing localized `strings.xml` files, so make sure you have a back-up in case of any unexpected changes*
```
android-localization-helper --clean
```

### Options

#### -h, --help
Prints help message.

#### --res
Path to the app's /res folder. Like, `./main/res`

By default assumes the current directory

#### --output
Output directory path (directory will be created automatically). Like, `~/Desktop/to_translate`

By default creates *to_translate* folder in the current directory.

#### --clean
Clean the existing `string.xml` files for each language.  This will remove strings that are in the localized language but not in the default language (they presumably got removed from the default langauge).  It will also sort the strings so that they are in the same order as the default language.


## Release History
* 2015-01-05   v0.1.2   support for more language folders, better feedback and error handling
* 2015-01-04   v0.1.1   xliff namespace support, better indentation handling
* 2015-01-03   v0.1.0   Initial release

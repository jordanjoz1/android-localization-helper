android-localization-helper
===========================

Make sure that you aren't missing string translations in any language, and keep your localized strings organized.

If you're like us at [DoubleDutch](doubledutch.me), you occassionally lose track of what strings have and haven't been translated in each language.  Android Studio [made an awesome GUI](http://tools.android.com/recent/androidstudio087released) to help deal with this issue, but there is no easy way to export missing strings, so if you are missing more than a few strings in a language it can become a tenuous problem.


## Getting started
Requirements:

* Python >= 2.7.*
* [Standard Android project structure](https://developer.android.com/tools/projects/index.html) for localized values-* folders in `res/` folder

Coming soon:
* Ability to install with `pip`

## Usage - general
Run the script with the path to you're project's `res/` directory. For example,

```
python ./translation_helper.py ./src/main/res
```

As in the [sample output](./sample_output), the script will create a directory called **to_translate** with files for the strings that need to translated in each language.  If a language has translations for all the strings in the default language, then it won't get an output file.  Now you know exactly what translations you need to add for each language, and you can send them out for translation.

### Options

#### -h, --help
Prints help message.

#### --clean
Clean the existing `string.xml` files for each language.  This will remove strings that are in the localized language but not in the default language (they presumably got removed from the default langauge).  It will also sort the strings so that they are in the same order as the default language.


## Release History
* 2015-01-15   v0.1.0   Initial release


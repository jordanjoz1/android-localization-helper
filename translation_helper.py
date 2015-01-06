#!/usr/bin/env python

'''
This script does two things:
1) Ouputs strings that haven't been translated in files for each language
2) Cleans up string.xml files for other languages by removing old strings and
re-ordering the strings based on their order in the default language

Other important notes
-Should support all language codes that follow the -** or -**-*** pattern
-This ignores strings that start with "provider." or have the "translatable"
attribute set to "false"
-The output directory for the missing strings is in the current directory
-The output file names look like "strings_to_trans-**" where "**" is the
language code
'''

import sys
import os
import xml.etree.ElementTree as ET
import codecs
import argparse

ORIG_DIR = os.getcwd()


def main():

    # parse command line arguments
    res_path, clean, out_path = parseArgs()

    # go to the resource directory and save the whole path
    os.chdir(res_path)
    res_path = os.getcwd()

    # get default keys
    tree = getDefaultTree(res_path)
    keys = getKeysFromTree(tree)
    tags = getTagsFromTree(tree)

    print('Found %d strings in the default language' % len(keys))

    # get the languages that we want to translate to
    langs = getLangsFromDir(res_path)

    print('Found translations for: %s' % ', '.join(langs))

    # look for missing keys in each language string file
    missing = findMissingKeys(keys, langs, res_path)

    # remove old strings and sort them all in the same way
    if (clean):
        cleanTranslationFiles(langs, keys, res_path)

    # write files for missing keys for each language
    createOutputDir(out_path)
    writeMissingKeysToFiles(langs, tags, missing, out_path)

    print('Saved missings strings to: %s' % out_path)


def parseArgs():
    # parse arguments and do error checking
    parser = argparse.ArgumentParser()
    parser.add_argument('--res',
                        help='Path to the app\'s /res directory. If not '
                        'specifies it assumes current directory',
                        default='.')
    parser.add_argument('--output',
                        help='Path to the output directory. If not specifies '
                        'it will create a folder called to_translate in the '
                        'current directory',
                        default='./to_translate')
    parser.add_argument('--clean',
                        help='re-orders and removes strings in the '
                        'translation files to match the default string '
                        'ordering',
                        action="store_true")
    args = parser.parse_args()
    return args.res, args.clean, args.output


def getDefaultTree(res_path):
    os.chdir(res_path)
    if os.path.exists('values'):
        os.chdir('values')
    else:
        sys.exit('Could not find values/ ... '
                 'Are you in your res/ folder?')
    ET.register_namespace('tools', "http://schemas.android.com/tools")
    ET.register_namespace('xliff', "urn:oasis:names:tc:xliff:document:1.2")
    return ET.parse('strings.xml')


def createOutputDir(out_path):
    # create output directory
    os.chdir(ORIG_DIR)
    if not os.path.exists(out_path):
        os.makedirs(out_path)


def writeMissingKeysToFiles(langs, tags, missing, out_path):
    # write xml files for missing strings for each language
    os.chdir(ORIG_DIR)
    os.chdir(out_path)
    for lang in langs:
        # skip language if it's not missing any strings
        if (len(missing[lang]) == 0):
            continue

        # create element tree for all the missing tags
        root = ET.Element('resources')
        for key in missing[lang]:
            tag = getTagByKeyName(tags, key)
            root.append(tag)

        # write out the strings
        f = codecs.open('strings_to_trans-%s.xml' % (lang), 'wb', 'utf-8')
        f.write(prettify(root))


def getLanguageTrees(langs, res_path):
    trees = {}
    for lang in langs:
        os.chdir(res_path)
        os.chdir('values-' + lang)
        if os.path.exists('strings.xml'):
            trees[lang] = ET.parse('strings.xml')
        else:
            print('Could not find strings.xml file for %s... skipping' % lang)
    return trees


def cleanTranslationFiles(langs, keys, res_path):
    trees = getLanguageTrees(langs, res_path)
    for lang in trees.keys():
        tree = trees[lang]
        keys_trans = getKeysFromTree(tree)
        tags_trans = getTagsFromTree(tree)
        keys_has = intersection(keys, keys_trans)
        root = ET.Element('resources')
        for key in keys_has:
            tag = getTagByKeyName(tags_trans, key)
            root.append(tag)

        # write out file
        os.chdir(res_path)
        os.chdir('values-%s' % (lang))
        f = codecs.open('strings.xml', 'wb', 'utf-8')
        f.write(prettify(root))


def intersection(a, b):
    """Intersection of sets A and B
    Don't use Python's set method since we care about the order
    """
    return [el for el in a if el in b]


def difference(a, b):
    """Result set of A - B
    Don't use Python's set method since we care about the order
    """
    return [el for el in a if el not in b]


def getTagByKeyName(tags, key):
    for tag in tags:
        if tag.get('name') == key:
            return tag


def prettify(elem):
    """Format xml element as a string
    Return a "pretty-printed" XML string for the Element.

    The element tree tostring() preserves the formatting of each individual
    tag, but it can have some funky behavior since we aren't including all the
    tags we read from the original tree.  On Python 3 tostring() does not add
    the XML declaration, so we need to add that manually.
    """
    output = ET.tostring(elem, encoding='UTF-8').decode('utf-8')

    # make sure we add the xml declaration... stupid python 3
    if not output.startswith('<?xml'):
        output = "<?xml version='1.0' encoding='UTF-8'?>\n" + output

    # fix first string not indenting
    output = output.replace('><string', '>\n    <string')
    return output


def findMissingKeys(keys, langs, res_path):
    missing = {}
    trees = getLanguageTrees(langs, res_path)
    for lang in trees.keys():
        tree = trees[lang]
        keys_trans = getKeysFromTree(tree)
        missing[lang] = difference(keys, keys_trans)
    return missing


def getLangDir(dir_name):
    """
    Supported langauge directories follow one of three patterns:
    https://support.google.com/googleplay/android-developer/table/4419860
    1) values-**
    2) values-**-**
    3) values-**-***
    returns code for language or None if not a language directory
    """
    if dir_name[2:].startswith('values-'):
        code = [dir_name[9:]][0]
        if (len(code) == 2) or (len(code) == 5 and code[2] == '-') \
                or (len(code) == 6 and code[2] == '-'):
            return code

    # not a language dir
    return None


def getLangsFromDir(res_path):
    os.chdir(res_path)
    langs = []
    for x in os.walk('.'):
        code = getLangDir(x[0])
        if code is not None:
            langs.append(code)
    return langs


def getKeysFromTree(tree):
    root = tree.getroot()
    keys = []
    for child in root:
        # ignore strings that can't be translated
        if child.get('translatable', default='true') == 'false':
            continue
        # ignore providers
        if (child.get('name').startswith('provider.')):
            continue
        keys.append(child.get('name'))
    return keys


def getTagsFromTree(tree):
    root = tree.getroot()
    keys = []
    for child in root:
        keys.append(child)
    return keys


if __name__ == '__main__':
    main()

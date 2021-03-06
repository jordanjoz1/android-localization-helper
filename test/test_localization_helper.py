import unittest
import os
import xml.etree.ElementTree as ET
import translation_helper as localizr
import filecmp


class TestLocalizationHelperFunctions(unittest.TestCase):

    def setUp(self):
        # constants
        self.LANGS = ['de', 'es', 'fr', 'zh-rTW']

        # save cwd so we can revert back to it when we're done with a test
        self.cwd = os.getcwd()

        # get absolute path to resource directory
        self.res_path = os.path.abspath('./test/res')

        # default strings file name
        self.DEFAULT_STRINGS_FILE = 'strings.xml'

        # get default strings tree with only strings.xml
        self.tree = localizr.getDefaultTree(self.res_path,
                                            self.DEFAULT_STRINGS_FILE)
        self.treePlurals = localizr.getDefaultTree(self.res_path,
                                                   'plurals.xml')

    def tearDown(self):
        os.chdir(self.cwd)

    def test_parseArgs(self):
        res_path_act = '~/Documents/test-app/app/src/main/res/'
        out_path_act = '~/Desktop/to_translate'
        res_path, clean, out_path, inputs = localizr.parseArgs(
            ['--res', res_path_act, '--input', 'strings.xml', 'plurals.xml',
             '--clean', '--output', out_path_act])
        self.assertEquals(res_path_act, res_path)
        self.assertEquals(clean, True)
        self.assertEquals(out_path_act, out_path)
        self.assertEquals(inputs, ['strings.xml', 'plurals.xml'])

    def test_getDefaultTrees(self):
        trees = localizr.getDefaultTrees(self.res_path,
                                         ['strings.xml', 'plurals.xml'])
        self.assertEquals(2, len(trees))

    def test_writeOutMissingStrings(self):
        # get tags from default tree so we know what to write out
        tags = localizr.getTagsFromTree(self.tree)

        # get the missing keys for each lang
        keys = localizr.getKeysFromTree(self.tree)
        missing = localizr.findMissingKeys(keys, self.LANGS, self.res_path)

        # write out the files
        localizr.createOutputDir('./test/to_translate')
        localizr.writeMissingKeysToFiles(self.LANGS, tags, missing,
                                         './test/to_translate')

        # verify that no German strings exist
        os.chdir(self.cwd)
        self.assertFalse(os.path.exists(
            './test/to_translate/strings_to_trans-de.xml'))

        # verify that spanish strings seem correct
        os.chdir(self.cwd)
        self.assertTrue(os.path.exists(
            './test/to_translate/strings_to_trans-es.xml'))
        self.assertTrue(filecmp.cmp(
            './test/test_to_translate/strings_to_trans-es.xml',
            './test/to_translate/strings_to_trans-es.xml'))

        # verify that french strings seem correct
        os.chdir(self.cwd)
        self.assertTrue(os.path.exists(
            './test/to_translate/strings_to_trans-fr.xml'))
        self.assertTrue(filecmp.cmp(
            './test/test_to_translate/strings_to_trans-fr.xml',
            './test/to_translate/strings_to_trans-fr.xml'))

        # verify that traditional chinese strings seem correct
        os.chdir(self.cwd)
        self.assertTrue(os.path.exists(
            './test/to_translate/strings_to_trans-zh-rTW.xml'))
        self.assertTrue(filecmp.cmp(
            './test/test_to_translate/strings_to_trans-zh-rTW.xml',
            './test/to_translate/strings_to_trans-zh-rTW.xml'))

    def test_getLanguageTrees(self):
        trees = localizr.getLanguageTrees(self.LANGS, self.res_path)
        self.assertEquals(len(trees), 4)

    def test_cleanTranslationFiles(self):
        """
        Extra strings will be removed and re-arranged to match the order of the
        strings in the default language
        """
        # get the keys from the default language
        keys = localizr.getKeysFromTree(self.tree)

        # clean the fiels
        localizr.createOutputDir('./to_translate')
        localizr.cleanTranslationFiles(self.LANGS, keys, self.res_path)

        # verify that German strings are correctly sorted
        os.chdir(self.cwd)
        self.assertTrue(filecmp.cmp('./test/res/values-de/strings.xml',
                        './test/test_cleaned/res/values-de/strings.xml'))

        # verify that empty spanish strings stays empty
        os.chdir(self.cwd)
        self.assertTrue(filecmp.cmp('./test/res/values-es/strings.xml',
                        './test/test_cleaned/res/values-es/strings.xml'))

        # verify that extra french string is removed
        os.chdir(self.cwd)
        self.assertTrue(filecmp.cmp('./test/res/values-fr/strings.xml',
                        './test/test_cleaned/res/values-fr/strings.xml'))

        # verify that extra chinese string is removed and everything else is
        # the same
        os.chdir(self.cwd)
        self.assertTrue(filecmp.cmp('./test/res/values-zh-rTW/strings.xml',
                        './test/test_cleaned/res/values-zh-rTW/strings.xml'))

    def test_intersection(self):
        self.assertEquals(localizr.intersection([], []), [])
        self.assertEquals(localizr.intersection(['a'], []), [])
        self.assertEquals(localizr.intersection([], ['a']), [])
        self.assertEquals(localizr.intersection(['a'], ['b']), [])
        self.assertEquals(localizr.intersection(['a'], ['a']), ['a'])
        self.assertEquals(localizr.intersection(['b', 'a'], ['a']), ['a'])

    def test_difference(self):
        self.assertEquals(localizr.difference([], []), [])
        self.assertEquals(localizr.difference(['a'], []), ['a'])
        self.assertEquals(localizr.difference([], ['a']), [])
        self.assertEquals(localizr.difference(['a'], ['a']), [])
        self.assertEquals(localizr.difference(['b', 'a'], ['a']), ['b'])

    def test_getTagByKeyName(self):
        tags = localizr.getTagsFromTree(self.tree)

        # verify that non-existent key returns None
        result = localizr.getTagByKeyName(tags, 'doesnotexist')
        self.assertIsNone(result)

        # verify that returns correct key
        result = localizr.getTagByKeyName(tags, ('string', 'test_1'))
        self.assertEqual(result.attrib['name'], 'test_1')

        # verify that returns correct key when keys with same name
        tagsPlurals = localizr.getTagsFromTree(self.treePlurals)
        result = localizr.getTagByKeyName(tagsPlurals, ('string', 'same_key'))
        self.assertEqual(result.text, 'same key string')
        result = localizr.getTagByKeyName(tagsPlurals, ('plurals', 'same_key'))
        self.assertEqual(result.text, 'same key plurals')

    def test_findMissingKeys(self):
        """
        look for missing keys in the translated values.xml files
        """
        keys = localizr.getKeysFromTree(self.tree)
        missing = localizr.findMissingKeys(keys, self.LANGS, self.res_path)

        # verify that German is not missing any tags
        self.assertEqual(missing['de'], [])

        # verify that Spanish is missing all tags
        self.assertEqual(
            missing['es'],
            [('string', 'test_1'), ('string', 'test_2'), ('string', 'test_3'),
             ('string', 'test_4'), ('string', 'test_5'),
             ('plurals', 'plurals_test')])

        # verify that French is missing all tags (despite its extra tag)
        self.assertEqual(
            missing['fr'],
            [('string', 'test_1'), ('string', 'test_2'), ('string', 'test_3'),
             ('string', 'test_4'), ('string', 'test_5'),
             ('plurals', 'plurals_test')])

        # verify that traditional Chinese is only missing one tag
        self.assertEqual(
            missing['zh-rTW'],
            [('string', 'test_5'), ('plurals', 'plurals_test')])

    def test_getLangDir(self):
        """
        only get language directory in the values-** and values-**-*** format
        """
        self.assertEqual(localizr.getLangDir('./drawable'), None)
        self.assertEqual(localizr.getLangDir('./values-hdpi'), None)
        self.assertEqual(localizr.getLangDir('./values-es'), 'es')
        self.assertEqual(localizr.getLangDir('./values-en-GB'), 'en-GB')
        self.assertEqual(localizr.getLangDir('./values-zh-rTW'), 'zh-rTW')

    def test_getLangsFromDir(self):
        langs = localizr.getLangsFromDir(self.res_path)
        self.assertEqual(set(langs), set(self.LANGS))

    def test_getKeysFromTrees(self):
        keys = localizr.getKeysFromTree(self.tree)
        self.assertEqual(
            keys,
            [('string', 'test_1'), ('string', 'test_2'), ('string', 'test_3'),
             ('string', 'test_4'), ('string', 'test_5'),
             ('plurals', 'plurals_test')])

    def test_getKeysFromTree(self):
        keys = localizr.getKeysFromTrees([self.tree, self.treePlurals])
        self.assertEqual(
            keys,
            [('string', 'test_1'), ('string', 'test_2'), ('string', 'test_3'),
             ('string', 'test_4'), ('string', 'test_5'),
             ('plurals', 'plurals_test'), ('plurals', 'plurals_test2'),
             ('string', 'same_key'), ('plurals', 'same_key')])

    def test_getTagsFromTree(self):
        tags = localizr.getTagsFromTree(self.tree)
        # should return all seven tags
        self.assertEqual(len(tags), 8)

    def test_getTagsFromTrees(self):
        tags = localizr.getTagsFromTrees([self.tree, self.treePlurals])
        # should return all seven tags
        self.assertEqual(len(tags), 11)


if __name__ == '__main__':
    unittest.main()

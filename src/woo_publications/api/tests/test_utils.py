from unittest import TestCase

from ..utils import underscore_to_camel


class UnderscoreToCamelTests(TestCase):
    def test_single_word_does_not_get_manipulated(self):
        result = underscore_to_camel("single")

        self.assertEqual(result, "single")

    def test_multiple_words_get_manipulated(self):
        result = underscore_to_camel("multiple_words_get_manipulated")

        self.assertEqual(
            result,
            "multipleWordsGetManipulated",
        )

    def test_double_underscore_gets_ignored(self):
        result = underscore_to_camel("first_set__second_set")

        self.assertEqual(result, "firstSet__secondSet")

    def test_int_gets_ignored(self):
        result = underscore_to_camel(123_123_123)

        self.assertEqual(result, 123_123_123)

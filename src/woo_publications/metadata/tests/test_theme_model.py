from django.test import TestCase

from ..models import Theme
from .factories import ThemeFactory


class ThemeQueryTests(TestCase):

    def test_dumping_tree(self):
        root_1 = ThemeFactory.create(naam="aaa")
        root_2 = ThemeFactory.create(naam="bbb")
        ThemeFactory.create(naam="ccc")
        child_11 = ThemeFactory.create(parent=root_1)
        child_12 = ThemeFactory.create(parent=root_1)
        child_121 = ThemeFactory.create(parent=child_12)
        if root_2.path == "0001":
            breakpoint()
        child_21 = ThemeFactory.create(parent=root_2)

        qs = Theme.objects.as_tree()

        # with self.subTest("tree structure"):
        #     # 3 root nodes -> we expect only the roots to be returned
        #     self.assertEqual(qs.count(), 3)
        #     self.assertEqual(len(qs), 3)

        with self.subTest("children of root 1"):
            first_root: Theme = qs[0]

            self.assertEqual(first_root.sub_themes, [child_11, child_12])

            with self.subTest("grandchildren of root 1"):
                self.assertEqual(child_12.sub_themes, [child_121])

        # with self.subTest("children of root 2"):
        #     second_root: Theme = qs[1]

        #     self.assertEqual(second_root.sub_themes, [child_21])

        # with self.subTest("children of root 3"):
        #     third_root: Theme = qs[2]

        #     self.assertEqual(third_root.sub_themes, [])

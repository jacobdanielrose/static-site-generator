import unittest
from generate_page import extract_title

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        md = "# header"
        title = extract_title(md)
        self.assertEqual(title, "header")

        md = "#              header"
        title = extract_title(md)
        self.assertEqual(title, "header")

    def test_extract_title_no_header(self):
        md = "## header"
        with self.assertRaisesRegex(Exception, "There is no title! Please make sure at least one heading is the title! i.e. # heading"):
            extract_title(md)

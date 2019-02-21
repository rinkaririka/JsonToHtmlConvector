import unittest
import converter


class ConverterTest(unittest.TestCase):

    def setUp(self):
        self.conv = converter.ConverterJsonToHtml()

    def test_encode_body(self):
        self.assertEqual(self.conv._encode_body("example<a>asd</a>"), "example&lt;a&gt;asd&lt;/a&gt;")

    def test_parsing_tag(self):
        self.assertEqual(self.conv._parsing_tag("p.my-class#my-id"), ("p id=\"my-id\" class=\"my-class\"", 'p'))


if __name__ == '__main__':
    unittest.main()


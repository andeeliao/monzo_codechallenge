import unittest, crawler
from bs4 import BeautifulSoup

class TestUnit(unittest.TestCase):
	

	def test_is_within_domain(self):
		self.assertTrue(crawler.is_within_domain("example.com", "/about"))
		self.assertTrue(crawler.is_within_domain("example.com", "example.com/abc"))
		self.assertFalse(crawler.is_within_domain("example.com", "otherexample.com/about"))
		self.assertFalse(crawler.is_within_domain("example", "otherexample.com/about"))
		self.assertFalse(crawler.is_within_domain("example.com", "examples.com/about"))


	def test_filter_page_links(self):
		html_zero = open('zero.html', 'r+')
		soup_zero = BeautifulSoup(html_zero, 'html.parser')
		self.assertEqual(crawler.filter_page_links('example.com', soup_zero), [])
		self.assertEqual(crawler.filter_page_links('http://tomblomfield.com/', 
													soup_zero), 
													['http://tomblomfield.com/post/136759441870/when-to-join-a-startup#disqus_thread'])


	def test_clean_internal_links(self):
		urls = ['http://tomblomfield.com/archive/2012/1#stuff',
				'http://tomblomfield.com/archive/2012/1',
				'/about']
		self.assertEqual(crawler.clean_internal_links('example.com', []), [])
		self.assertEqual(crawler.clean_internal_links('http://tomblomfield.com/', urls), 
				['http://tomblomfield.com/archive/2012/1',
				'http://tomblomfield.com/archive/2012/1',
				'http://tomblomfield.com/about'])


	def test_filter_tags_for_src(self):
		html_zero = open('zero.html', 'r+')
		soup_zero = BeautifulSoup(html_zero, 'html.parser')
		static_tags = soup_zero.find_all(crawler.STATIC_FILE_TAGS)
		self.assertEqual(crawler.filter_tags_for_src(static_tags), [u'http://example.com'])


if __name__ == '__main__':
    unittest.main()
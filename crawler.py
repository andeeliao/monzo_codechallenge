import requests
from bs4 import BeautifulSoup
from Page import Page

# development
from pprint import pprint

# TODO make object?
SITE_MAP = {}
# assumption: text, js inside script tag not considered 'static file'
# because they're not separate files
STATIC_FILE_TAGS = ['img', 'script', 'style']
# TODO handle http vs https


# dev help
def print_soup_to_file(soup, title):
	soup_file = open(title, "w+")
	file_txt = u''.join(soup.prettify()).encode('utf-8').strip()

	soup_file.write(file_txt)

	soup_file.close()


def is_within_domain(orig_url, url):
	return url.startswith(orig_url) or url.startswith('/')


def filter_page_links(orig_url, soup):
	a_hrefs = soup.find_all('a')
	links = [a.get('href') for a in a_hrefs]

	# assumption: links such as "/about" should be considered 
	# inside the domain
	filtered_links = [l for l in links if is_within_domain(orig_url, l)]
	return filtered_links


def clean_internal_links(orig_url, urls):
	formatted_urls =[]

	for url in urls:
		if url.startswith("/"):
			url = orig_url + url[1:]

		hashtag_pos = url.find('#')
		if hashtag_pos != -1:
			url = url[:hashtag_pos]


		questionmark_pos = url.find('?')
		if questionmark_pos != -1:
			url = url[:questionmark_pos]

		formatted_urls.append(url)

	return formatted_urls


	
def filter_tags_for_src(tags):
	tags_with_src = [t for t in tags if t.has_attr('src')]
	return [t.get('src') for t in tags_with_src]


def was_already_crawled(url):
	return url in SITE_MAP


def make_distinct(l):
	return list(set(l))


def crawl(orig_domain, url):
	my_page = Page(url)

	page = requests.get(url)

	soup = BeautifulSoup(page.content, 'html.parser')

	pages_within_domain = filter_page_links(orig_domain, soup)
	formatted_links = clean_internal_links(orig_domain, pages_within_domain)
	unique_links = make_distinct(formatted_links)
	my_page.set_links_to(unique_links)

	static_tags = soup.find_all(STATIC_FILE_TAGS)
	srcs = filter_tags_for_src(static_tags)
	unique_srcs = make_distinct(srcs)
	my_page.set_static_assets(unique_srcs)

	#print_soup_to_file(soup, "initial.txt")
	

	SITE_MAP[url] = my_page
	print "crawled: ", url

	for page in unique_links:
		if not was_already_crawled(page):
			crawl(orig_domain, page)


def crawl_wrapper(url):
	crawl(url, url)

	pprint(SITE_MAP)



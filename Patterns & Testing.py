"""
    Name: Xiuyi Feng
    Email: xiuyi.feng15@myhunter.cuny.edu
    Resources:
            https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
"""
import re
def rm_tags(data):
    """
        Returns a string with all HTML formatting removed.
        If the string was plain text, the contents are returned unaltered as a string.
    """
    patt = re.compile('<.*?>')
    cleantext = re.sub(patt, '', data)
    return cleantext

def test_rm_tags(rm_tags_fnc):
    """
        Returns True if the inputted function correctly strips out the text from a HTML file
        and False otherwise
    """
    html_str = '<html><head><title>Test Page</title></head><body><h1>Welcome!</h1><p>This is a test page.</p></body></html>'
    expected_output = 'Test Page Welcome! This is a test page.'
    output = rm_tags_fnc(html_str)
    if output == expected_output:
        return True
    return False

def make_dict(data):
    """
        Uses regular expressions (see Chapter 12.4 for using the re package in Python)
        to find all external links in data and store the link text as the key and URL
        value in a dictionary. Title and URL in the CSV file specified by the user.
        For the URL, keep the leading https:// or http://. Returns the resulting dictionary.
    """
    regex = r"<a.*?href=['\"](https?://.*?)['\"].*?>(.*?)<\/a>"
    texts = re.findall(regex, data, re.IGNORECASE)
    result = {}
    for text in texts:
        url = text[0]
        text = text[1]
        result[text] = url
    return result

def test_make_dict(make_dict_fnc):
    """
        Returns True if the inputted function correctly returns a dictionary of links
        and False otherwise.
    """
    html_str ='<html><body><a href="https://www.google.com">Google</a><a href="https://www.python.org">Python</a></body></html>'
    expected_output = {'Google': 'https://www.google.com',
                       'Python': 'https://www.python.org'}
    output = make_dict_fnc(html_str)
    if output == expected_output:
        return True
    return False

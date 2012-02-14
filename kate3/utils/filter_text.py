from django.template.defaultfilters import linebreaks, striptags, urlizetrunc
from markdown import markdown

FILTER_CHOICES = (
    ('Markdown', 'Markdown'),
    ('Simple', 'Simple'),
    ('None', 'None')
)

def simplify(text):
	return linebreaks(urlizetrunc(striptags(text), 60))
	
def filter_text(text, body_filter):
	result =  {
		'Markdown': markdown(text),
		'Simple': simplify(text)
	}
	return result.get(body_filter, text)
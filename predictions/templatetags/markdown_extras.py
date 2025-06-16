from django import template
import markdown

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
     return markdown.markdown(text)
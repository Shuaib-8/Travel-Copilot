from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    """
    Convert markdown text to HTML
    """
    if not text:
        return ""
    
    # Configure markdown with basic extensions
    try:
        md = markdown.Markdown(extensions=['extra'])
        html = md.convert(text)
        return mark_safe(html)
    except Exception:
        # Fallback to basic markdown if extensions fail
        md = markdown.Markdown()
        html = md.convert(text)
        return mark_safe(html)

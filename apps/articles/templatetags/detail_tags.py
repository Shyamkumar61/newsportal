from django import template
import re
from apps.articles.media_embed import MediaEmbed
from urllib.parse import urlparse, parse_qs

register = template.Library()


@register.filter
def ombed_embeddify(article):
    article_description = article.description
    tag_list = article.tags.all()
    for tag in tag_list:
        if tag:
            link = "<a href='{}' class='{}' style='font-weight:bold'>{}</a>".format(tag.get_absolute_url(), "tag_highlight_color_detail",
                                                tag.name)
            article_description = re.sub(tag.name, link, article_description)
    value = article_description
    replace = re.sub(r'(?:<oembed url=")(.+?)(?:"></oembed>)', lambda m: MediaEmbed(m.group(1)).replace_with_embed(), value)
    return replace







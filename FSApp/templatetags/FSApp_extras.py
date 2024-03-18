from django import template

register = template.Library()


@register.simple_tag
def navbar_links():
    return [
        ["/", "Game"],
        ["/stats", "Stats"],
        ["/login", "Login"]
    ]


@register.simple_tag
def testing():
    return "hello how are you"


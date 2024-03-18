from django import template

register = template.Library()


@register.simple_tag
def navbar_left_links():
    return [
        ["/", "Game"],
        ["/stats", "Stats"],
        ["/test", "Test"]
    ]


@register.simple_tag
def navbar_login():
    return [
        ["/login", "Login"],
    ]


@register.simple_tag
def testing():
    return "hello how are you"


from django import template

register = template.Library()


@register.simple_tag
def navbar_left_links():
    return [
        ["/", "Home"],
        ["/game", "Game"],
        ["/stats", "Stats"],
    ]


@register.simple_tag
def navbar_login():
    return [
        ["/login", "Login"],
    ]


@register.simple_tag
def difficulty_names():
    return (
        "easy",
        "medium",
        "hard",
    )


@register.simple_tag
def testing():
    return "hello how are you"


@register.filter
def index_of_record(data, index):
    return data[index]

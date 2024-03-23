from django import template

register = template.Library()


@register.simple_tag
def navbar_left_links():
    return [
        ["/", "Home"],
        ["/game", "Game"],
        ["/stats", "Stats"],
        ["/test", "Test"]
    ]


@register.simple_tag
def navbar_login():
    return [
        ["/login", "Login"],
    ]


@register.simple_tag
def difficulty_names():
    return (
        "ez",
        "alright",
        "gangster",
    )


@register.simple_tag
def testing():
    return "hello how are you"


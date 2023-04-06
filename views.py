def index():
    with open('template/index.html') as template:
        return template.read()


def blog():
    with open('template/blog.html') as template:
        return template.read()
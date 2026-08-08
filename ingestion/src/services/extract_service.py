from lxml.html import Element


def get_xpath_first_element(node: Element, xpath: str) -> str | None:
    tags = node.xpath(xpath)
    if tags and len(tags) > 0:
        output = tags[0]
        if isinstance(output, str):
            return output.strip()
        return output


def remove_extra_spaces(text: str) -> str:
    return " ".join(text.split())

from textnode import TextNode, TextType


def __main__():
    test_node = TextNode("the text", TextType.PLAIN, "http://example.com")
    print(f'test_node = {test_node}')


__main__()

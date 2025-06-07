from textnode import *


def main():
    new_node = TextNode("Some Test Text", InlineText.LINKS, "https://ianwatkins.dev")
    print(new_node)


if __name__ == "__main__":
    main()

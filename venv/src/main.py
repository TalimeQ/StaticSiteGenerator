from textnode import * 

def main():
    text = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(text)


main()
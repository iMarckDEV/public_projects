import sys

def print_pretty_comment(message):
    length = len(message) + 6
    print("#" * length)
    print("#--{}--#".format(message))
    print("#" * length)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        comment_text = " ".join(sys.argv[1:])
        print_pretty_comment(comment_text)
    else:
        print("No comment text provided.")
from shutil import get_terminal_size
from random import choice
from time import sleep
from textwrap import TextWrapper
from urllib.parse import unquote

from requests import get

from ascii_arts import AsciiArts


class CopyPasta():
    def __init__(self) -> None:
        self.terminal_size = get_terminal_size(fallback=(120, 50))

    def get(self) -> str:
        """
        Gets a random copypasta from r/copypasta

        :returns str: The copypasta text
        """

        for _ in range(10): # max 10 tries
            subreddit = "copypasta"
            count = 1
            timeframe = "all"
            listing = "random"

            headers = {
                    "Upgrade-Insecure-Requests": "1",
                    "Dnt": "1",
                    "User-Agent": (
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                            " AppleWebKit/537.36 (KHTML, like Gecko)"
                            " Chrome/83.0.4103.61 Safari/537.36"
                        ),
                    "Accept": (
                            "text/html,application/xhtml+xml,application"
                            "/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
                            ",application/signed-exchange;v=b3;q=0.9"
                        ),
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-User": "?1",
                    "Sec-Fetch-Dest": "document",
                    "Referer": "https://www.reddit.com/u/Useful-Shoe914", # :P
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
                }

            def get_reddit(subreddit, count) -> dict | None:
                """
                Gets the posts from the specified subreddit

                :param subreddit str: Name of the subreddit
                :param count str: Amount of posts to load
                :returns None or dict: Json dictionary of comments
                if no errors ocurred, else None
                """

                try:
                    base_url = (
                            f"https://www.reddit.com/r/{subreddit}"
                            f"/{listing}.json?count={count}&t={timeframe}"
                        )
                    request = get(
                            base_url, headers=headers, timeout=10
                        )
                    return request.json()

                except ConnectionError:
                    return None

            top_post = get_reddit(subreddit, count)
            if not top_post: # if we get an error, request the page again
                sleep(2) # sleep 2 seconds first
                continue

            if listing != "random":
                title = top_post["data"]["children"][0]["data"]["title"]
                url = top_post["data"]["children"][0]["data"]["url"]
            else:
                title = top_post[0]["data"]["children"][0]["data"]["title"]
                url = top_post[0]["data"]["children"][0]["data"]["url"]

            def get_post() -> dict | None:
                """
                Gets the posts info

                :returns dict or None: Json dictionary
                 if no errors ocurred, else None
                """

                try:
                    request = get(
                            f"{url}.json", headers=headers, timeout=10
                        )
                    return request.json()
                except Exception:
                    return None

            try:
                selftext = get_post()
                if not selftext:
                    continue

                selftext = (
                        selftext[0]
                            ["data"]
                            ["children"][0]
                            ["data"]
                            ["selftext"]
                    )
                text2 = unquote(
                    selftext.strip()
                        .replace(r"&amp;#x200B;","")
                        .replace("\n"," ")
                        .replace("      ","")
                    )

                if text2 != "" and not "removed by reddit" in text2.lower():
                    return text2

            except Exception:
                continue

        return "Failed to get copypasta :("


def gethalf(x) -> int:
    """
    Gets half of the lines of the text specified

    :param x str: Text to calculate
    :returns int: Amount of lines
    """

    return round(len(x.split("\n")/2)) # gets the length of the specified string, splits it and then counts the amount of items


def makeblock(x) -> str:
    """
    Turns the ASCII art in a perfect block,
    to prevent lines from shifting

    :param x str: The ASCII art to block-ify
    :returns str: Block-ified ASCII art
    """

    ascii_art1 = []
    ascii_art11 = [len(c) for c in x.split("\n")]

    size = max(ascii_art1)

    for x in x.split("\n"):
        if x != "":
            ascii_art11.append(f"{x+(' '*(size-len(x)))}")

    return "\n".join(ascii_art11)


if __name__ == "__main__":
    text = CopyPasta().get() # gets a random copypasta

    if not text:
        text = "Failed to get copypasta :("

    banner = makeblock(choice(AsciiArts.ascii_art))
    ascii_art1 = [len(x) for x in banner.split("\n")]

    width = text.terminal_size.columns-(max(ascii_art1)+3)
    wrapper = TextWrapper(width=width)
    word_list = wrapper.wrap(text=text)

    num = 0
    abc = 0

    for x in banner.split("\n"):
        if x != "":
            if num != len(word_list):
                print(x, word_list[num].strip())
                num += 1
                abc = len(x)
            else:
                print(x)

    if num != len(word_list):
        text1 = "".join(word_list[num:])
        wrapper = TextWrapper(width=(width+abc))

        for line in wrapper.wrap(text=text1):
            print(line)

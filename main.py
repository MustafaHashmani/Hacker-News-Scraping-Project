import pprint
import requests
from bs4 import BeautifulSoup
import webbrowser

response = requests.get("https://news.ycombinator.com/news")
response2 = requests.get("https://news.ycombinator.com/news?p=2")
soup_object = BeautifulSoup(response.text, "html.parser")
soup_object2 = BeautifulSoup(response2.text, "html.parser")

links = soup_object.select(".titleline > a")
subtext = soup_object.select(".subtext")
links2 = soup_object2.select(".titleline > a")
subtext2 = soup_object2.select(
    ".subtext"
)  # the score is nested within the subtext class

total_links = links + links2  # sum of the links on page1 and page2
total_subtext = subtext + subtext2  # sum of the subtext on page1 and page2


def sort_stories_by_vote(hackernews_list):
    """Sorts the list by the number of votes in descending order"""
    return sorted(hackernews_list, key=lambda key: key["votes"], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for index, item in enumerate(links):
        title = item.getText()  # gets the title of the link
        href = item.get("href")  # gets the href attribute else returns None
        vote = subtext[index].select(".score")
        # Only execute if the vote exists
        if len(vote):
            # remove the text and convert to integer
            points = int(vote[0].getText().replace(" points", ""))
            # select only those with greater than 100 votes
            if points >= 100:
                hn.append({"title": title, "link": href, "votes": points})
    return sort_stories_by_vote(hn)


# pretty printing the output
pprint.pprint(create_custom_hn(total_links, total_subtext))
choice = input("Do you want to open these in the Browser?(Yes/No)").lower()
if choice == "yes":
    hn = create_custom_hn(total_links, total_subtext)
    for news in hn:
        webbrowser.open(news["link"])

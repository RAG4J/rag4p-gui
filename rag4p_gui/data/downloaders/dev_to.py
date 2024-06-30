import json
import requests

from bs4 import BeautifulSoup


def download_single_article(_url):
    _response = requests.get(_url)
    soup = BeautifulSoup(_response.text, 'html.parser')
    article_body = soup.find(id="article-body")

    # Check if the element was found before accessing its text
    if article_body is not None:
        _article = article_body.get_text(strip=True).replace('\n', ' ')
    else:
        _article = ""

    return _article


if __name__ == "__main__":
    print("Hello from dev.to downloader")

    per_page = 50
    page_num = 9

    base_url = "https://dev.to"
    all_url = f"{base_url}/search/feed_content?per_page={per_page}&page={page_num}&organization_id=2794&username=aws-builders&sort_by=published_at&sort_direction=desc&approved=&class_name=Article"

    response = requests.get(all_url)
    articles = json.loads(response.text)["result"]
    documents = []
    for article in articles:
        path = article["path"]
        title = article["title"]
        published_at = article["published_at_int"]
        tags = article["tag_list"]
        user = article["user"]["name"]
        url = f"{base_url}{path}"
        details = download_single_article(url)

        print(f"Title: {title} ({user}) - {url}")
        documents.append({
            "title": title,
            "published_at": published_at,
            "tags": tags,
            "user": user,
            "url": url,
            "details": details
        })

    with open('../../../data/dev_to/dev_to_documents.jsonl', 'a+') as f:
        for document in documents:
            json.dump(document, f)
            f.write("\n")

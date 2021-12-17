import bs4 as bs
import requests as r
import re
from typing import List
from fake_useragent import FakeUserAgent
from definitions import PDF_FILES
import concurrent.futures

ACS_WEBSITE: str = "https://pubs.acs.org"
ACS_SEARCH: str = "https://pubs.acs.org/action/doSearch?AllField="
ACS_PAGE: str = "&startPage="
ACS_PAGE_SIZE: str = "&pageSize="

def create_user_agent() -> str:
    return str(FakeUserAgent().random)

def create_session() -> r.Session:
    user_agent = create_user_agent()
    session = r.Session()
    session.headers.update({"User-Agent": user_agent})
    return session

def download_pdf(download_url: str, path_to_save: PDF_FILES, session: r.Session) -> bool:
    save_name = download_url.split("/")[-1]
    request = session.get(url=download_url)
    if request.status_code != "200":
        return False
    with open(path_to_save + save_name + ".pdf", "wb") as file:
        file.write(request.content)
    return True
    

def search_and_download_acs(search_string: str, num_papers: int, page_size: int = 100, num_threads: int = 10) -> int:
    session = create_session()
    paper_url_list: List[str] = []
    num_papers_downloaded: int = 0
    page: int = 0
    while len(paper_url_list) < num_papers:
        request = session.get(url=f"{ACS_SEARCH}{search_string}{ACS_PAGE}{page}{ACS_PAGE_SIZE}{page_size}")
        soup = bs.BeautifulSoup(request.text, "lxml")
        paper = [ACS_WEBSITE + pdf["href"] for pdf in soup.find_all("a", {"title": "PDF"})]
        paper_url_list.extend(paper)
        if soup.find("a", {"class": "pagination__btn--next"}):
            page += 1
        else:
            break

    if len(paper_url_list) > num_papers:
        paper_url_list = paper_url_list[:num_papers]

    if paper_url_list: 
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(num_threads, len(paper_url_list))) as executor:
            paper_download = [executor.submit(download_pdf, url, PDF_FILES, session) for url in paper_url_list]
            for paper in concurrent.futures.as_completed(paper_download):
                num_papers += int(paper.result())

    return num_papers_downloaded

#CHEMRXIV_WEBSITE: str = "https://chemrxiv.org"
#CHEMRXIV_SEARCH: str = "https://chemrxiv.org/engage/chemrxiv/search-dashboard?text="
#CHEMRXIV_PDF_DOWNLOAD: str = "https://chemrxiv.org/engage/api-gateway/chemrxiv/assets/orp/resource/item/"
#
#
#def search_and_download_chemrxiv(search_string: str, num_papers: int, page_size: int = 100, num_threads: int = 10) -> int:
#    session = create_session()
#    paper_url_list: List[str] = []
#    num_papers_downloaded: int = 0
#    request = session.get(url=f"{CHEMRXIV_SEARCH}{search_string}")
#    paper = []


if __name__ == "__main__":
    downloaded_pdfs = search_and_download_acs("organic", 10)

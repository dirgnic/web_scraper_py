import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# download the pdfs
def download_pdf(pdf_url, output_folder):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        filename = os.path.join(output_folder, pdf_url.split("/")[-1])
        with open(filename, "wb") as pdf_file:
            pdf_file.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {pdf_url}")

#scrape PDFs from a webpage
def scrape_pdfs_from_page(url, output_folder="pdfs"):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        links = soup.find_all("a", href=True)

        pdf_links = [urljoin(url, link['href']) for link in links if link['href'].endswith('.pdf')]

        for pdf_link in pdf_links:
            download_pdf(pdf_link, output_folder)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

if __name__ == "__main__":
    webpage_url = "https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/lehrstuehle/informationsdienste/lehre/wintersemester-202122/grundlagen-der-web-entwicklung/materialien-zur-veranstaltung/"  # Replace with the actual URL
    scrape_pdfs_from_page(webpage_url)

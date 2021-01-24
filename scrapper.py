import os
import shutil
import sys
from urllib.request import urlopen
import pathlib
import wget
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse


def scrap_file_from_web():
    url = 'http://pgcb.gov.bd/site/page/0dd38e19-7c70-4582-95ba-078fccb609a8/'

    create_required_folder()
    check_url_validity(url)
    download_report_files(url)
    get_new_reports()


def create_required_folder():
    current_dir = pathlib.Path(__file__).parent
    temp_dir = os.path.join(current_dir, 'temp_files\\')
    inbound_dir = os.path.join(current_dir, 'inbound_files\\')
    processed_dir = os.path.join(current_dir, 'processed_files\\')
    output_dir = os.path.join(current_dir, 'output_files\\')

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    if not os.path.exists(inbound_dir):
        os.makedirs(inbound_dir)
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def check_url_validity(url):
    try:
        urlopen(url)
        print("Valid URL")
    except IOError:
        print("Invalid URL")
        sys.exit()


def download_report_files(url):
    links = []
    main_html_link = urlopen(url).read()
    report_html_page = bs(main_html_link, features="lxml")
    report_html_url = report_html_page.find('iframe')['src']
    html = urlopen(report_html_url).read()
    html_page = bs(html, features="lxml")
    og_url = html_page.find("meta", property="og:url")
    base = urlparse(url)
    for link in html_page.find_all('a'):
        current_link = link.get('href')
        current_link = current_link.replace(' ', '')
        if current_link.endswith('download'):
            links.append(current_link)
        # if og_url:
        #         print("currentLink",current_link)
        #         links.append(og_url["content"] + current_link)
        # else:
        #     links.append(base.scheme + "://" + base.netloc + current_link)
    current_dir = pathlib.Path(__file__).parent
    temp_dir = os.path.join(current_dir, 'temp_files\\')

    for link in links:
        try:
            print(link)
            wget.download(link, out=temp_dir)  # download all report files to temp_dir
        except Exception as e:
            print(" \n \n Unable to Download the File \n")


def get_new_reports():
    current_dir = pathlib.Path(__file__).parent
    temp_dir = os.path.join(current_dir, 'temp_files\\')
    inbound_dir = os.path.join(current_dir, 'inbound_files\\')
    processed_dir = os.path.join(current_dir, 'processed_files\\')

    file_names = os.listdir(temp_dir)  # Get all report files from temp directory

    for file_name in file_names:
        if not os.path.isfile(os.path.join(processed_dir, file_name)):  # check if file already exists in  processed_files
            if not os.path.isfile(os.path.join(inbound_dir, file_name)):  # check if file already exists in  inbound_files
                shutil.move(os.path.join(temp_dir, file_name), inbound_dir)  # Move new reports to inbound_files for processing
            else:
                os.remove('temp_files/' + file_name)  # Remove existing files
        else:
            os.remove('temp_files/' + file_name)  # Remove existing files

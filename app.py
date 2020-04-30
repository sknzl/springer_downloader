import csv
import io
import os
import sys
import threading
import urllib.request
import argparse

from queue import Queue
from urls import *


def get_discipline_dicts(discipline):
    if discipline == 'all':
        return [
            ALL_CSV_URL
        ]

    elif discipline == "engineering":
        return [
            ENGINEERING_CSV_URL
        ]

    elif discipline == "computer_science":
        return [
            COMPUTER_SCIENCE_CSV_URL
        ]
        
    elif discipline == "mathematics":
        return [
            MATHEMATICS_CSV_URL
        ]

    elif discipline == "physics":
        return [
            PHYSICS_CSV_URL
        ]

    elif discipline == "psychology":
        return [
            PSYCHOLOGY_CSV_URL
        ]     

class Downloader(threading.Thread):
    """Threaded File Downloader"""

    def __init__(self, queue):
        """Initialize the thread"""
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        """Run the thread"""
        while True:
            url = self.queue.get()
            self.download_file(url)
            self.queue.task_done()

    def download_file(self, url):
        """Download the file"""
        handle = urllib.request.urlopen(url["link"])
        fname = "{}/{}.pdf".format(url["path"], url["title"])
        os.makedirs(os.path.dirname(fname), exist_ok=True)
        with open(fname, "wb") as f:
            while True:
                chunk = handle.read(1024)
                if not chunk: break
                f.write(chunk)
        print("Finished downloading {}".format(fname))
        print("Books in queue: {}".format(self.queue.qsize()))

def get_books(urls):
    queue = Queue()

    for i in range(10):
        t = Downloader(queue)
        t.setDaemon(True)
        t.start()

    for url in urls:
        queue.put(url)

    queue.join()

def main(args):
    books = []

    for discipline in get_discipline_dicts(vars(args)["discipline"]):
        download = urllib.request.urlopen(discipline['csv_url'])
        reader = csv.reader(io.TextIOWrapper(download), delimiter=',')
        next(reader)
        for row in reader:
            books.append({"title": row[0], "link": (DOWNLOAD_URL.format(row[5])), 'path': discipline['path']})
        
    get_books(books)
    print("Done")

def check_arg(args=None):
    parser = argparse.ArgumentParser(description='Download free Springer book')
    parser.add_argument('-d', '--discipline',
                        default='all',
                        choices=['all', 'engineering', 'computer_science', 'mathematics', 'physics', 'psychology'],
                        help='Discipline. default: all. Choices: engineering, computer_science, mathematics, physics, psychology')

    parsed_args = parser.parse_args(args)
    return parsed_args

if __name__ == "__main__":
    args = check_arg(sys.argv[1:])
    main(args)



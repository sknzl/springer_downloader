import csv
import os
import threading
import urllib.request

from queue import Queue

CSV_URL = 'https://link.springer.com/search/csv?facet-content-type=%22Book%22&package=mat-covid19_textbooks'
DOWNLOAD_URL = "https://link.springer.com/content/pdf/{}.pdf"


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
        fname = os.path.basename("{}.pdf".format(url["title"]))
        with open(fname, "wb") as f:
            while True:
                chunk = handle.read(1024)
                if not chunk: break
                f.write(chunk)
        msg = "Finished downloading {}".format(fname)
        print(msg)
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


def main():
    books = []

    download = urllib.request.urlopen(CSV_URL)
    import io

    reader = csv.reader(io.TextIOWrapper(download), delimiter=',')
    for row in reader:
        books.append({"title": row[0], "link": (DOWNLOAD_URL.format(row[5]))})
    
    books.remove(books[0])

    get_books(books)

if __name__ == "__main__":
    main()
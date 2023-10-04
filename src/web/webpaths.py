from concurrent.futures import ThreadPoolExecutor
import contextlib
import os
import queue
import time
import requests
import sys
import threading

FILTERED = ['.jpg', '.gif', '.png', '.css']
THREADS = 8

TARGET = ''

answers = queue.Queue()
web_paths = queue.Queue()

def gather_paths_parallel():
    def process_file(root, fname):
        file_extension = os.path.splitext(fname)[1]
        if file_extension not in FILTERED:
            path = os.path.join(root, fname)
            if path.startswith('.'):
                path = path[1:]
            print(path)
            web_paths.put(path)

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for root, _, files in os.walk('.'):
            for fname in files:
                executor.submit(process_file, root, fname)

@contextlib.contextmanager
def chdir(path):
    """
        On enter, change directory to specified path.
        On exit, change directory to original.
    """
    this_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    except Exception as e:
        print(e)
    finally:
        os.chdir(this_dir)

def test_remote():
    while not web_paths.empty():
        path = web_paths.get()

        print(path)
        url = f'{TARGET}{path}'

        time.sleep(2) # target might have throttlight/lockout

        r = requests.get(url)
        if r.status_code == 200:
            answers.put(url)
            sys.stdout.write("*\n")
        else:
            print(r.status_code)
            sys.stdout.write("x\n")
        sys.stdout.flush()

def run():
    my_threads = list()
    for i in range(THREADS):
        print(f'Spawning thread {i}')
        t = threading.Thread(target=test_remote)
        my_threads.append(t)
        
        t.start()

    for thread in my_threads:
        thread.join()

if __name__ == "__main__":
    download_directory = ""
    with chdir(""):
        gather_paths_parallel()
    input("Press return to continue.")

    run()

    with open('answers.txt', 'w') as f:
        while not answers.empty():
            f.write(f'{answers.get()}\n')
    print("done")

    
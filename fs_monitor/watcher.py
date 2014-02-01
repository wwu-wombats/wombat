import sys
import time

from watchdog.observers import Observer

from EventHandler import EventHandler


if __name__ == '__main__':
    paths = [ x for x in sys.argv[1:] ] or '.'
    print("The paths to be monitored are: ", paths)

    event_handler = EventHandler()
    to_watch = Observer()

    for path in paths:
        to_watch.schedule(event_handler, path, recursive=True)
    to_watch.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        to_watch.stop()
    to_watch.join()

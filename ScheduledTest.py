import speedtest
import os
from apscheduler.schedulers.background import BackgroundScheduler
import time

threads = 0


def execute_test():
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download(threads=threads)
    s.upload(threads=threads)

    results = s.results.dict()
    download = results['download'] * .000001
    upload = results['upload'] * .000001
    ping = results['ping']
    server = results['server']['host']
    timestamp = results['timestamp']

    save_output(timestamp, download, upload, ping, server)


def save_output(timestamp, download, upload, ping, server):
    output_path = "{0}/output.csv".format(os.path.dirname(os.path.realpath(__file__)))
    line = "{0},{1},{2},{3},{4}\n".format(timestamp, download, upload, ping, server)
    with open(output_path, "a") as f:
        f.write(line)
        print(line)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    execute_test()
    scheduler.add_job(execute_test, 'interval', seconds=300)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
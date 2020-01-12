import speedtest
import os
from apscheduler.triggers import interval
from apscheduler.schedulers.background import BackgroundScheduler
import time
from datetime import datetime

threads = 0


def b_to_mb(b):
    return round(b/1000000, 2)


def execute_test():
    print('Running new speed test')
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download(threads=threads)
    s.upload(threads=threads)

    results = s.results.dict()
    download = b_to_mb(results['download'])
    upload = b_to_mb(results['upload'])
    ping = round(results['ping'], 2)
    server = results['server']['host']
    now = datetime.now()
    timestamp = now.strftime("%m/%d/%Y %H:%M:%S")
    print("Speed Test to {0} Finished\nDownload\t{1}\nUpload\t\t{2}\nPing\t\t{3}".format(server, download, upload, ping))

    save_output(timestamp, download, upload, ping, server)


def save_output(timestamp, download, upload, ping, server):
    output_path = "{0}/output.txt".format(os.path.dirname(os.path.realpath(__file__)))
    line = "{0},{1},{2},{3},{4}\n".format(timestamp, download, upload, ping, server)
    with open(output_path, 'a') as f:
        f.write(line)
        print('results saved to {0}'.format(output_path))


if __name__ == '__main__':
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    execute_test()
    scheduler = BackgroundScheduler()
    trigger = interval.IntervalTrigger(seconds=300)
    scheduler.add_job(execute_test, trigger=trigger, seconds=300)
    scheduler.start()
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

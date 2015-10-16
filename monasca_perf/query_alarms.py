import sys
import time
import multiprocessing
import random
import argparse

from monascaclient import client
from monascaclient import ksclient

max_wait_time = 20
min_wait_time = 5

keystone = {
    'username': 'mini-mon',
    'password': 'password',
    'project': 'test',
    'auth_url': 'http://192.168.10.5:35357/v3'
}

# monasca api urls
urls = [
    'http://192.168.10.4:8070/v2.0',
]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--number_processes", help="Number of processes to run against the API", type=int,
                        required=False, default=10)
    return parser.parse_args()


def query_alarms():
    try:
        ks_client = ksclient.KSClient(**keystone)
    except Exception as ex:
        print 'Failed to authenticate: {}'.format(ex)
        return

    mon_client = client.Client('2_0', urls[0], token=ks_client.token)
    while True:
        try:
            time.sleep(random.randint(min_wait_time, max_wait_time))
            ## TO DO WRITE THE AMOUNT OF TIME TO GET ANSWER BACK TO FILE AND AVERAGE AT THE END
            alarms = mon_client.alarms.list()
        except KeyboardInterrupt:
            return


def query_alarms_test():

    args = parse_args()
    num_processes = args.number_processes

    process_list = []
    for i in xrange(num_processes):
        p = multiprocessing.Process(target=query_alarms)
        process_list.append(p)

    for p in process_list:
        p.start()

    try:
        for p in process_list:
            try:
                p.join()
            except Exception:
                pass

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    sys.exit(query_alarms_test())
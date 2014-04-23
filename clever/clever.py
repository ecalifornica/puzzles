import requests
import json
from time import sleep


def api_request(page_number, sleep_length=1):
    '''Requests records from API, recursively retries if error'''
    print('Making api request for page number: {}'.format(page_number))
    r = requests.get(
        'https://api.clever.com/v1.1/students?limit=2000&page={}'
        .format(page_number),
        headers={'Authorization': 'Bearer DEMO_TOKEN'})
    if r.status_code is not 200:
        print('status_code: {}'.format(r.status_code))
        print('sleeping for: {}'.format(sleep_length))
        sleep(sleep_length)
        sleep_length = sleep_length * 2
        if sleep_length > 16:
            print('Too many tries, exiting to avoid hammering the API')
            import sys
            sys.exit(1)
        response_json = api_request(page_number, sleep_length)
        return response_json
    response_json = r.json()
    return response_json


def main():
    import sys
    if len(sys.argv) < 2:
        sys.stderr.write('Please specify a letter.\n')
        sys.exit(1)
    else:
        letter = sys.argv[1].upper()
    total = 0
    page = 1
    last_page = None
    while not last_page or page <= last_page:
        api_data = api_request(page)
        last_page = api_data['paging']['total']
        students = api_data['data']
        for i in xrange(len(students)):
            if students[i]['data']['name']['last'][0] == letter:
                total += 1
        '''
        result = len([students[i]['data']['name']['last'] for i, s
            in enumerate(students) 
            if students[i]['data']['name']['last'][0] == letter])
        '''
        page += 1
    print('Number of students whose last name begins with "{}": {}'.format(
        letter, total))


if __name__ == '__main__':
    main()

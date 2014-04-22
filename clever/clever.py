import requests
import json
from time import sleep


def api_page_count():
    '''Makes a request to the API to discover number of pages'''
    r = requests.get(
        'https://api.clever.com/v1.1/students',
        headers={'Authorization': 'Bearer DEMO_TOKEN'})
    response_json = json.loads(r.content)
    page_count = response_json['paging']['total']
    return page_count


def api_request(page_number, sleep_length=1):
    '''Requests records from API, recursively retries if error'''
    print('Making api request for page number: {}'.format(page_number))
    r = requests.get(
        'https://api.clever.com/v1.1/students?page={}'.format(page_number),
        headers={'Authorization': 'Bearer DEMO_TOKEN'})
    if r.status_code is not 200:
        print('status_code: {}'.format(r.status_code))
        print('sleeping for: {}'.format(sleep_length))
        sleep(sleep_length)
        sleep_length = sleep_length * 2
        if sleep_length > 16:
            print('Too many tries, exiting to avoid hammering the API')
            import sys
            sys.exit()
        response_json = api_request(page_number, sleep_length)
        return response_json
    response_json = r.json()
    return response_json


def students_on_page(api_response):
    '''Parses API response json for last names'''
    students_on_page = []
    data = api_response['data']
    data_length = len(data)
    for i in xrange(data_length):
        students_on_page.append(data[i]['data']['name']['last'])
    return students_on_page


def count_by_last_name(letter, student_list):
    '''Counts last names that begin with specified letter'''
    counter = 0
    for student in student_list:
        if student[:1].lower() == letter.lower():
            counter += 1
    return counter


def main():
    import sys
    letter = sys.argv[1]
    total = 0
    page_count = api_page_count()
    for page in xrange(page_count):
        api_response = api_request(page+1)
        student_list = students_on_page(api_response)
        total += count_by_last_name(letter, student_list)
    print('Number of students whose last name begins with "{}": {}'.format(
        letter, total))


if __name__ == '__main__':
    main()

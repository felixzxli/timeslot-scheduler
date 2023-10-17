import argparse
import datetime
import json
import logging
import os
import sys
import time
import traceback
import urllib3
import requests

from lxml.html import soupparser

import rmc.shared.secrets as s
import rmc.shared.constants as c
import rmc.models as m
import mongoengine as me


API_UWATERLOO_V2_URL = 'https://api.uwaterloo.ca/v2'

reload(sys)
sys.setdefaultencoding('utf-8')

errors = []


def html_parse(url, num_tries=5, parsers=[soupparser]):
    for parser in parsers:
        tries = 0
        while True:
            try:
                u = urllib3.urlopen(url)
                result = u.read()
                u.close()
                return parser.fromstring(result)
            except:
                tries += 1
                if tries == num_tries:
                    break

                wait = 2 ** (tries + 1)
                error = 'Exception parsing %s. Sleeping for %s secs'.format(
                            url=url, wait=wait)
                errors.append(error)
                print error
                time.sleep(wait)

    return None


def get_data_from_url(url, num_tries=5):
    tries = 0
    while True:
        try:
            u = urllib3.urlopen(url)
            result = u.read()
            u.close()
            if result:
                data = json.loads(result)
                return data
            return None
        except:
            tries += 1
            if tries == num_tries:
                break

            wait = 2 ** (tries + 1)
            error = 'Exception for {url}. Sleeping for {wait} secs'.format(
                    url=url, wait=wait)
            errors.append(error)
            print error
            traceback.print_exc(file=sys.stdout)
            time.sleep(wait)

    return None

def get_subject_sections_from_opendata(subject, term):
    """Get info on all sections offered for all courses of a given subject and
    term.

    Args:
        subject: The department ID (eg. CS)
        term: The 4-digit Quest term code (defaults to current term)
    """
    url = ('{api_url}/terms/{term}/{subject}/schedule.json'
            '?key={api_key}'.format(
                api_url=API_UWATERLOO_V2_URL,
                api_key=s.OPEN_DATA_API_KEY,
                subject=subject,
                term=term,
    ))

    data = get_data_from_url(url)
    try:
        sections = data['data']
    except (KeyError, TypeError):
        logging.exception('crawler.py: Schedule API call failed with'
                " url %s and data:\n%s" % (url, data))
        raise

    return sections

def get_current_term_id():
    the_date = datetime.datetime.now()
    # From http://ugradcalendar.uwaterloo.ca/page/uWaterloo-Calendar-Events-and-Academic-Deadlines
    term_start_months = [9, 5, 1]

    # Find the month this term started
    for month in term_start_months:
        if the_date.month >= month:
            start_month = month
            break

    return "%d_%02d" % (the_date.year, start_month)

def get_next_term_id_from_term_id(term_id):
    year = int(term_id[:4])
    month = int(term_id[:5])
    if month == 9:
        year += 1
        month = 1
    else:
        month += 4
    
    if month not in [1, 5, 9, 13]:
        raise "Invalid month: %s" % month
    
    return '%s_%02d' % (year, month)
    
def get_opendata_sections():
    current_term_id = get_current_term_id()
    next_term_id = m.Term.get_next_term_id()

    # We resolve the query (list()) because Mongo's cursors can time out
    for department in list(m.Department.objects):
        sections = []
        for term_id in [current_term_id, next_term_id]:
            quest_term_id = m.Term.get_quest_id_from_term_id(term_id)
            sections += get_subject_sections_from_opendata(
                    department.id.upper(), quest_term_id)

        # Now write all that data to file
        filename = os.path.join(os.path.dirname(__file__),
                '%s/%s.json' % (c.SECTIONS_DATA_DIR, department.id))
        with open(filename, 'w') as f:
            json.dump(sections, f)
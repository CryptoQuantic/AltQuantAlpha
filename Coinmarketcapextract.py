#!/usr/bin/env python

"""A simple python script template.
"""


import sys
import re
import urllib2
import argparse
import datetime


def download_all_currency_list():
  """
  Download the all-currency data table from CoinMarketCap.
  """

  url = 'https://coinmarketcap.com/all/views/all/'


  try:
    page = urllib2.urlopen(url,timeout=10)
    if page.getcode() != 200:
      raise Exception('Failed to load page')
    html = page.read()
    page.close()

  except Exception as e:
    print('Error fetching currency data from ' + url)
    print(e)
    sys.exit(1)

  return html

def extract_all_currency_data(html):
  """
  Extract the rows from the all-currency data table.

  """

  head = re.search(r'<thead>(.*)</thead>', html, re.DOTALL).group(1)
  header = re.findall(r'<th .*>([\w ]+)</th>', head)
  header.append('Average (High + Low / 2)')


  body = re.search(r'<tbody>(.*)</tbody>', html, re.DOTALL).group(1)
  print(body)
  raw_rows = re.findall(r'<tr[^>]*>' + r'\s*<td[^>]*>([^<]+)</td>'*7 + r'\s*</tr>', body)

  # strip commas
  rows = []
  for row in raw_rows:
    row = [ field.translate(None, ',') for field in row ]
    rows.append(row)

  # calculate averages
  def append_average(row):
    high = float(row[header.index('High')])
    low = float(row[header.index('Low')])
    average = (high + low) / 2
    row.append( '{:.2f}'.format(average) )
    return row
  rows = [ append_average(row) for row in rows ]

  return header, rows


def main(args=None):
    all_data = download_all_currency_list()
    header,rows = extract_all_currency_data(all_data)
    print(header)
    print(rows)



if __name__ == '__main__':
  df = main()

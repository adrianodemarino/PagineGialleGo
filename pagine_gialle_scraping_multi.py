#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import html
import argparse
import pandas as pd
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def parse_listing(keyword, place):
    """
    Function to process yellowpage listing page
    : param keyword: search query
    : param place : place name
    """
    url = "https://www.paginegialle.it/ricerca/{0}/{1}".format(keyword, place)
    print("retrieving ", url)

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Host': 'www.paginegialle.it',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
               }
    try:
        response = requests.get(url, verify=False, headers=headers)
        print("parsing page")
        if response.status_code == 200:
            parser = html.fromstring(response.text)
            # making links absolute
            base_url = "https://www.paginegialle.it"
            parser.make_links_absolute(base_url)

            XPATH_LISTINGS = "//div[@class='pageContentWrapper active']//div[@class='col contentCol']"
            listings = parser.xpath(XPATH_LISTINGS)
        elif response.status_code == 404:
            print("Could not find a location matching", place)
            # no need to retry for non existing page
        else:
            print("Failed to process page exit with no results exit code: 213")
            return []
    except:
        print("Failed to process page exit with no results exit code: 222")
        return []

    XPATH_RESULTS = "//div[@class=' container containerListato ']//span[@class='searchResNum']//text()"
    raw_RESULTS = listings[0].xpath(XPATH_RESULTS)
    resultsn = ''.join(raw_RESULTS).strip().replace("risultati","") if raw_RESULTS else None
    print("results found for query {0} {1} - {2}".format(keyword,place,resultsn))
    page_number = int(int(resultsn)/20) #20 is the number of result for single web page
    print("number of web page to parse: {0}".format(page_number))

    scraped_results = []
    if page_number == 1 or page_number == 0:
        for results in listings:
            XPATH_BUSINESS_NAME = ".//h2[@class='fn itemTitle ']//text()"
            XPATH_BUSSINESS_PAGE = ".//h2[@class='fn itemTitle ']//@href"
            XPATH_TELEPHONE = ".//span[@class='tel ']//span[@itemprop='telephone']//text()"
            XPATH_STREET = ".//span[@itemprop='streetAddress']//text()"
            XPATH_LOCALITY = ".//span[@class='locality']//text()"
            XPATH_REGION = ".//span[@class='region']//text()"
            XPATH_ZIP_CODE = ".//span[@class='postal-code']//text()"
            XPATH_DESCRIPTION = ".//p[@itemprop='description']//text()"
            XPATH_OPENTIME = ".//span[@class='label']//text()"

            raw_business_name = results.xpath(XPATH_BUSINESS_NAME)
            raw_business_telephone = results.xpath(XPATH_TELEPHONE)
            raw_business_page = results.xpath(XPATH_BUSSINESS_PAGE)
            raw_street = results.xpath(XPATH_STREET)
            raw_locality = results.xpath(XPATH_LOCALITY)
            raw_region = results.xpath(XPATH_REGION)
            raw_zip_code = results.xpath(XPATH_ZIP_CODE)
            raw_opentime = results.xpath(XPATH_OPENTIME)
            raw_description = results.xpath(XPATH_DESCRIPTION)

            raw_data = [raw_business_name,raw_business_telephone,raw_business_page,raw_street,raw_locality,raw_region,raw_zip_code,raw_opentime,raw_description]

            cleaned = []
            for grezz in raw_data:
                cleaned.append(''.join(grezz).strip() if grezz else None)
                
            business_details = {
                'business_name': cleaned[0],
                'telephone': cleaned[1],
                'business_page': cleaned[2],
                'street': cleaned[3],
                'locality': cleaned[4],
                'region': cleaned[5],
                'zipcode': cleaned[6],
                'openingTime': cleaned[7],
                'Description': cleaned[8],
            }
            scraped_results.append(business_details)
        return scraped_results
    if page_number > 1:   
        for retry in range(page_number):
            if retry == 0:
                for results in listings:
                    XPATH_BUSINESS_NAME = ".//h2[@class='fn itemTitle ']//text()"
                    XPATH_BUSSINESS_PAGE = ".//h2[@class='fn itemTitle ']//@href"
                    XPATH_TELEPHONE = ".//span[@class='tel ']//span[@itemprop='telephone']//text()"
                    XPATH_STREET = ".//span[@itemprop='streetAddress']//text()"
                    XPATH_LOCALITY = ".//span[@class='locality']//text()"
                    XPATH_REGION = ".//span[@class='region']//text()"
                    XPATH_ZIP_CODE = ".//span[@class='postal-code']//text()"
                    XPATH_DESCRIPTION = ".//p[@itemprop='description']//text()"
                    XPATH_OPENTIME = ".//span[@class='label']//text()"

                    raw_business_name = results.xpath(XPATH_BUSINESS_NAME)
                    raw_business_telephone = results.xpath(XPATH_TELEPHONE)
                    raw_business_page = results.xpath(XPATH_BUSSINESS_PAGE)
                    raw_street = results.xpath(XPATH_STREET)
                    raw_locality = results.xpath(XPATH_LOCALITY)
                    raw_region = results.xpath(XPATH_REGION)
                    raw_zip_code = results.xpath(XPATH_ZIP_CODE)
                    raw_opentime = results.xpath(XPATH_OPENTIME)
                    raw_description = results.xpath(XPATH_DESCRIPTION)

                    raw_data = [raw_business_name,raw_business_telephone,raw_business_page,raw_street,raw_locality,raw_region,raw_zip_code,raw_opentime,raw_description]

                    cleaned = []
                    for grezz in raw_data:
                        cleaned.append(''.join(grezz).strip() if grezz else None)
                        
                    business_details = {
                        'business_name': cleaned[0],
                        'telephone': cleaned[1],
                        'business_page': cleaned[2],
                        'street': cleaned[3],
                        'locality': cleaned[4],
                        'region': cleaned[5],
                        'zipcode': cleaned[6],
                        'openingTime': cleaned[7],
                        'Description': cleaned[8],
                    }
                    scraped_results.append(business_details)
            else:
                time.sleep(5)
                try:
                    url = "https://www.paginegialle.it/ricerca/{0}/{1}/p-{2}".format(keyword,place,retry)
                    response = requests.get(url, verify=False, headers=headers)
                    print("parsing page {0}".format(retry))
                    if response.status_code == 200:
                        parser = html.fromstring(response.text)
                        # making links absolute
                        base_url = "https://www.paginegialle.it"
                        parser.make_links_absolute(base_url)

                        XPATH_LISTINGS = "//div[@class='pageContentWrapper active']//div[@class='col contentCol']"
                        listings = parser.xpath(XPATH_LISTINGS)
                        for results in listings:
                            XPATH_BUSINESS_NAME = ".//h2[@class='fn itemTitle ']//text()"
                            XPATH_BUSSINESS_PAGE = ".//h2[@class='fn itemTitle ']//@href"
                            XPATH_TELEPHONE = ".//span[@class='tel ']//span[@itemprop='telephone']//text()"
                            XPATH_STREET = ".//span[@itemprop='streetAddress']//text()"
                            XPATH_LOCALITY = ".//span[@class='locality']//text()"
                            XPATH_REGION = ".//span[@class='region']//text()"
                            XPATH_ZIP_CODE = ".//span[@class='postal-code']//text()"
                            XPATH_DESCRIPTION = ".//p[@itemprop='description']//text()"
                            XPATH_OPENTIME = ".//span[@class='label']//text()"

                            raw_business_name = results.xpath(XPATH_BUSINESS_NAME)
                            raw_business_telephone = results.xpath(XPATH_TELEPHONE)
                            raw_business_page = results.xpath(XPATH_BUSSINESS_PAGE)
                            raw_street = results.xpath(XPATH_STREET)
                            raw_locality = results.xpath(XPATH_LOCALITY)
                            raw_region = results.xpath(XPATH_REGION)
                            raw_zip_code = results.xpath(XPATH_ZIP_CODE)
                            raw_opentime = results.xpath(XPATH_OPENTIME)
                            raw_description = results.xpath(XPATH_DESCRIPTION)

                            raw_data = [raw_business_name,raw_business_telephone,raw_business_page,raw_street,raw_locality,raw_region,raw_zip_code,raw_opentime,raw_description]

                            cleaned = []
                            for grezz in raw_data:
                                cleaned.append(''.join(grezz).strip() if grezz else None)
                                
                            business_details = {
                                'business_name': cleaned[0],
                                'telephone': cleaned[1],
                                'business_page': cleaned[2],
                                'street': cleaned[3],
                                'locality': cleaned[4],
                                'region': cleaned[5],
                                'zipcode': cleaned[6],
                                'openingTime': cleaned[7],
                                'Description': cleaned[8],
                            }
                            scraped_results.append(business_details)

                    elif response.status_code == 404:
                        print("Could not find a location matching", place)
                        # no need to retry for non existing page
                        break
                    else:
                        print("Failed to process page number: {0}".format(retry))
                        return scraped_results

                except:
                    print("Failed to process page number: {0}".format(retry))
                    return scraped_results    
        return scraped_results


if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument('keyword', help='Search Keyword')
    argparser.add_argument('place', help='Place Name')

    args = argparser.parse_args()
    keyword = args.keyword
    place = args.place

    scraped_data = parse_listing(keyword, place)

    if scraped_data:
        print("Writing scraped data to %s-%s-paginegialle-spulciate-data.xlsx" % (keyword, place))
        (pd.DataFrame(scraped_data)).drop_duplicates(keep="first").to_excel("{0}-{1}-paginegialle-spulciate-data.xlsx".format(keyword, place))

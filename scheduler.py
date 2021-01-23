#!/bin/python

import os
import pathlib

import schedule
import time
import scrapper, processor


def job():
    scrapper.scrap_file_from_web()
    processor.process_files()


# schedule.every().minutes.do(job)
schedule.every(24).hours.do(job)  # this will run the job in every 24 hours
# schedule.every().day.at("00:00").do(job)
while 1:
    schedule.run_pending()
    time.sleep(1)

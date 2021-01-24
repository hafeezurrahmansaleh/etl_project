#!/bin/python



import schedule
import time
import scrapper, processor


def run_job():
    scrapper.scrap_file_from_web()
    print('\nScrapping done.......')
    processor.process_files()


if __name__ == "__main__":
    run_job()
    # schedule.every().minutes.do(job)
    print('\nProcess successfully executed!!\n')
    print('Waiting for next run after 24 hours.............')
    schedule.every(24).hours.do(run_job)  # this will run the job in every 24 hours
    # schedule.every().day.at("00:00").do(job)
    while 1:
        schedule.run_pending()
        time.sleep(1)

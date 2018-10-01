#! /usr/bin/env python

import argparse, logging

import pandas

import bashthebug

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input",required=True,help="the csv file downloaded from the Zooniverse containing all the classifcations done to date")
    parser.add_argument("--from_date",required=False,help="the date to consider classifications from (ISO format e.g. 2017-04-07)")
    parser.add_argument("--to_date",required=False,help="the date to consider classifications up to")
    parser.add_argument("--timings",action='store_true',default=False,help="print the time taken for each step")
    options = parser.parse_args()

    # parse the output file to work out the output stem
    output_stem=options.input_file.split("bash-the-bug-classifications")[1].split(".csv")[0]


    print("Reading classifications from CSV file...")

    if options.to_date:
        if options.from_date:
            current_classifications=bashthebug.BashTheBugClassifications(zooniverse_file=options.input_file,to_date=options.to_date,from_date=options.from_date)
        else:
            current_classifications=bashthebug.BashTheBugClassifications(zooniverse_file=options.input_file,to_date=options.to_date)
    elif options.from_date:
        current_classifications=bashthebug.BashTheBugClassifications(zooniverse_file=options.input_file,from_date=options.from_date)
    else:
        current_classifications=bashthebug.BashTheBugClassifications(zooniverse_file=options.input_file)


    current_classifications.extract_classifications()

    most_recent_date=str(current_classifications.classifications.created_at.max().date().isoformat())

    # open a log file to record images where the wells cannot be identified
    logging.basicConfig(filename="log/bashthebug-classifications-analyse-"+most_recent_date+".log",level=logging.INFO,format='%(levelname)s: %(message)s', datefmt='%a %d %b %Y %H:%M:%S')

    current_classifications.create_measurements_table()

    current_classifications.create_users_table()


    for sampling_time in ['month','week','day']:

        current_classifications.plot_classifications_by_time(sampling=sampling_time,filename='pdf/graph-classifications-'+sampling_time+'.pdf',add_cumulative=True)
        current_classifications.plot_users_by_time(sampling=sampling_time,filename='pdf/graph-users-'+sampling_time+'.pdf',add_cumulative=True)

    current_classifications.plot_user_classification_distribution(filename="pdf/graph-user-distribution.pdf")


    logging.info(current_classifications)

    print("Saving compressed CSV file...")
    # current_classifications.save_csv("dat/bash-the-bug-classifications.csv.bz2",compression=True)
    current_classifications.save_pickle("dat/bash-the-bug-classifications.pkl.bz2")

    logging.info(current_classifications.users[["classifications","rank"]][:20])

    # print(current_classifications.gini_coefficient)

    # print("Filtering on study")
    # start=time.time()
    # a.filter_study("CRyPTIC1")
    # print("%.1f seconds" % (time.time()-start))

    # print("Calculating the task duration..")
    # start=time.time()
    # a.calculate_task_durations()
    # print("%.1f seconds" % (time.time()-start))
    #
    # print("Creating misc fields..")
    # start=time.time()
    # a.create_misc_fields()
    # print("%.1f seconds" % (time.time()-start))
    #
    # # can print statistics or plot graphs now
    # pandas.set_option('display.max_columns', 100)
    # print(a.df[:3])




    # print(a.df.task_duration.dtype)
    # print(a.df.viewport_width.dtype)
    # print(a.df.reading_day.dtype)

BEGIN {
    print "label,config_series,config_benchmarks,cores,core,pmu,eventtype,eventcount,iteration,offset"
}
/EVENTCOUNT/ {
    # Number of fields must be 23
    if (NF == 23) {
        printf("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n",$5,$7,$9,$11,$13,$15,$17,$19,$21,$23)
    } else {
        printf("WARNING: number of fields doesn't match. Line number is %s\n", NR) | "cat 1>&2"
    }
}

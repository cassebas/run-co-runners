BEGIN {
    print "label,config_series,config_benchmarks,benchmark,cores,core,cycles,iteration,offset"
}
/CYCLECOUNT/ {
    # Is field number $17 (cycle count) larger than 0? Number of fields must be 21
    if (length($17) > 0 && NF == 21) {
        # remove underscores from benchmark name, it hurts LaTeX
        gsub("_", "", $11)

        printf("%s,%s,%s,%s,%s,%s,%s,%s,%s\n",$5,$7,$9,$11,$13,$15,$17,$19,$21)
    } else {
        printf("WARNING: number of fields doesn't match. Line number is %s\n", NR) | "cat 1>&2"
    }
}

## sx550_assignment3
#### Name: Siyuan Xiang

## Results Summary
### Original
    Original Runtime:   115.29765961204103 seconds

### Final Optimization
    Optimized Runtime:  32.494603252863115 seconds
    Speedup:    3.54820948927518x

Since we got a speedup more than 3x, the final program can finish in under 30 seconds.

--------

Seperated results:
### Reducing function call overhead
    Optimized Runtime:  41.45436893357306 seconds
    Speedup:    2.781315035739545x
    Improvement rank:   1st
    
### Using alternatives to membership testing of lists
    Optimized Rumtime:  110.80406021221951 seconds
    Speedup:    1.04055446516324x
    Improvement rank:   3rd

### Using local rather than global variables

    Optimize Runtime:   111.52608338893835 seconds
    Speedup:    1.03381788464632x
    Improvement rank:   4th

### Using data aggregation to reduce loop overheads
    Optimized Runtime:  102.25295634918284 seconds
    Speedup:    1.12757287151984x
    Improvement rank:   2nd

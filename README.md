## sx550_assignment3
#### Name: Siyuan Xiang

## Results Summary
### Original
    Original Runtime:   113.23277562403037 seconds

### Final Optimization
    Optimized Runtime:  33.16189348570092 seconds
    Speedup:    3.4145449406516915x

Since we got a speedup more than 3x, the final program can finish in under 30 seconds.

--------

Seperated results:
### Reducing function call overhead
    Optimized Runtime:  41.611776804081146 seconds
    Speedup:    2.7211713683162135x
    Improvement rank:   1st
    
### Using alternatives to membership testing of lists
    Optimized Rumtime:  110.07478535283204 seconds
    Speedup:    1.0286894974273695x
    Improvement rank:   3rd

### Using local rather than global variables

    Optimize Runtime:   113.18604426987963 seconds
    Speedup:    1.0004128720501912x
    Improvement rank:   4th

### Using data aggregation to reduce loop overheads
    Optimized Runtime:  102.64572623691011 seconds
    Speedup:    1.1031416482229854x
    Improvement rank:   2nd

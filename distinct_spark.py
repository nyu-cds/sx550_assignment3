from pyspark import SparkContext
import re

# remove any non-words and split lines into separate words
# finally, convert all words to lowercase
def splitter(line):
    line = re.sub(r'^\W+|\W+$', '', line)
    return map(str.lower, re.split(r'\W+', line))

if __name__ == '__main__':
    sc = SparkContext("local", "distinct")
    
    text = sc.textFile('pg2701.txt')
    words = text.flatMap(splitter)
    words_mapped = words.map(lambda x: (x,1))
    sorted_map = words_mapped.sortByKey()
    
    # If the same key, keep the count.
    # Else add 1 and use the new key.
    counts = sorted_map.reduce(lambda x,y: x if (x[0]==y[0]) else (y[0], x[1]+1))
    print(counts[1])

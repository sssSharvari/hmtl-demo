/*
Write a code in JAVA for a simple WordCount application that counts the number of
occurrences of each word in a given input set using the Hadoop MapReduce framework on
local-standalone set-up.

*/
import java.util.*;

public class WordCount {

    public static void main(String[] args) {

        // Sample input (you can replace with file input later)
        String text = "Big data is big. Hadoop is BIG data!";

        // Convert to lowercase
        text = text.toLowerCase();

        // Remove punctuation using regex
        text = text.replaceAll("[^a-zA-Z0-9\\s]", "");

        // Split into words
        String[] words = text.split("\\s+");

        // HashMap to store word counts
        HashMap<String, Integer> wordCount = new HashMap<>();

        for (String word : words) {
            if (word.isEmpty()) continue;

            wordCount.put(word, wordCount.getOrDefault(word, 0) + 1);
        }

        // Sort output by word (alphabetically)
        TreeMap<String, Integer> sorted = new TreeMap<>(wordCount);

        // Display result
        System.out.println("Word Count Output:\n");

        for (Map.Entry<String, Integer> entry : sorted.entrySet()) {
            System.out.println(entry.getKey() + " : " + entry.getValue());
        }
    }
}



/*
1. Introduction to Hadoop and MapReduce

Apache Hadoop is an open-source framework designed to store and process large datasets across distributed systems. 
It uses a programming model called MapReduce, which enables parallel processing of data.

MapReduce divides a large problem into smaller sub-tasks and processes them in parallel across multiple nodes. 
It consists of two main phases:

Map Phase
Reduce Phase

This approach is highly scalable and fault-tolerant, making it suitable for big data applications.

🔹 2. Objective of WordCount Application

The WordCount application is one of the simplest and most commonly used examples to demonstrate the working of the MapReduce framework. The objective is:

To count the number of occurrences of each word in a given input dataset.

The input is a text file, and the output is a list of words along with their respective frequencies.

🔹 3. Working of MapReduce in WordCount
🔸 Step 1: Input Splitting

The input text file is divided into smaller chunks called input splits. Each split is processed independently by a Mapper.

🔸 Step 2: Map Phase

In the Map phase:

The input is read line by line.
Each line is split into words.
Each word is emitted as a key-value pair:
(word, 1)

Example:

Input:

big data is big

Mapper Output:

(big,1)
(data,1)
(is,1)
(big,1)
🔸 Step 3: Shuffle and Sort

This is an internal phase of Hadoop where:

All identical keys are grouped together
Data is sorted before sending to Reducer

Example:

(big → [1,1])
(data → [1])
(is → [1])
🔸 Step 4: Reduce Phase

In the Reduce phase:

Values corresponding to the same key are aggregated
The counts are summed up

Output:

(big,2)
(data,1)
(is,1)
🔹 4. Components of WordCount Program

A typical Hadoop WordCount program consists of:

✔ Mapper Class
Processes input data
Emits (word, 1)
✔ Reducer Class
Receives grouped data
Calculates total count
✔ Driver Class
Configures job
Sets input/output paths
Executes MapReduce job
🔹 5. Hadoop in Local Standalone Mode

In this practical, Hadoop is configured in local standalone mode, which means:

Runs on a single machine
No distributed cluster required
Uses local file system instead of HDFS

Advantages:

Easy to set up
Suitable for learning and testing
No need for complex configuration
🔹 6. Advantages of MapReduce
Scalability: Can process large datasets across multiple machines
Fault Tolerance: Automatically handles failures
Parallel Processing: Faster execution
Flexibility: Works with structured and unstructured data
🔹 7. Limitations
Not suitable for real-time processing
High latency
Complex setup in distributed environments
🔹 8. Applications of WordCount
Text analysis
Log processing
Search engines
Data mining
🔹 9. Conclusion

The WordCount application demonstrates the fundamental working of
the MapReduce programming model in Hadoop. It shows how large data can be
processed efficiently using parallel computation. Even though it is a simple example,
it forms the foundation for understanding complex big data processing tasks.



*/
import java.io.*;
import java.util.*;

public class WordCountSpark {
    public static void main(String[] args) {

        String filePath = "E:/input.txt";  // Input file path

        HashMap<String, Integer> wordCount = new HashMap<>();

        try {
            BufferedReader br = new BufferedReader(new FileReader(filePath));
            String line;

            while ((line = br.readLine()) != null) {

                // Clean + split words
                line = line.toLowerCase().replaceAll("[^a-zA-Z0-9\\s]", "");
                String[] words = line.split("\\s+");

                for (String word : words) {
                    if (word.isEmpty()) continue;

                    wordCount.put(word, wordCount.getOrDefault(word, 0) + 1);
                }
            }

            br.close();

            // Sort output (like Spark result consistency)
            TreeMap<String, Integer> sorted = new TreeMap<>(wordCount);

            System.out.println("Word Count Output:\n");

            for (Map.Entry<String, Integer> entry : sorted.entrySet()) {
                System.out.println(entry.getKey() + " : " + entry.getValue());
            }

        } catch (Exception e) {
            System.out.println("Error reading file: " + e.getMessage());
        }
    }
}
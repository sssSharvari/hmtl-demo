/*/
Locate dataset (e.g., sample_weather.txt) for working on weather data which reads the text
input files and finds average for temperature, dew point and wind speed

*/
import java.io.*;

public class WeatherAnalysis {

    public static void main(String[] args) {

        String fileName = "E:/sample_weather.txt";

        double tempSum = 0;
        double dewSum = 0;
        double windSum = 0;
        int count = 0;

        try {
            BufferedReader br = new BufferedReader(new FileReader(fileName));
            String line;

            while ((line = br.readLine()) != null) {

                String[] parts = line.split(" ");

                double temp = Double.parseDouble(parts[1]);
                double dew = Double.parseDouble(parts[2]);
                double wind = Double.parseDouble(parts[3]);

                tempSum += temp;
                dewSum += dew;
                windSum += wind;

                count++;
            }

            br.close();

            System.out.println("Average Temperature: " + (tempSum / count));
            System.out.println("Average Dew Point: " + (dewSum / count));
            System.out.println("Average Wind Speed: " + (windSum / count));

        } catch (Exception e) {
            System.out.println("Error reading file");
        }
    }
}
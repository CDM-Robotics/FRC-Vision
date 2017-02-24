/**
 * Created by ryantolsma on 2/23/17.
 */


/**
*USAGE: run java Benchmark [put your terminal command here]

i.e java Benchmark python3 -i image.py 
Will run the image file and print how long it takes
for some simple debuggin/testing

**/
public class Benchmark {

    public static void main(String[] args) throws Exception {
        ProcessBuilder pb=new ProcessBuilder();
        pb.command(args);
        Process runTime=pb.start();

        long currentTime=System.currentTimeMillis();
        while(runTime.isAlive()) {
            Thread.sleep(10);
        }

        System.out.println(   (System.currentTimeMillis()-currentTime)+" milliseconds");

    }

}

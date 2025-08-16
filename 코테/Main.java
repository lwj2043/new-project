import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        int num = sc.nextInt();
        int pow = sc.nextInt();
        sc.close();
        StringBuilder answer = new StringBuilder();
        while (num > 0) {
            int result = num % pow;

            if (result < 10) {
                answer.append( (char) (result + '0') );
            } else {
                answer.append( (char) (result - 10 + 'A') );
            }
            num = num / pow;
        }

        System.out.println(answer.reverse().toString());
        sc.close();
    }
}

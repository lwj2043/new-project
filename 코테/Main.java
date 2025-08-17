package 코테;

import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        
        int T = sc.nextInt();
        for(int i = 0; i < T; i++) {
            int[] answer = new int[4];
            int num = sc.nextInt();
            answer[0] = num / 25;
            num %= 25;
            answer[1] = num / 10;
            num %= 10;
            answer[2] = num / 5;
            num %= 5;
            answer[3] = num / 1;
            num %= 1;

            System.out.println(answer[0] + " " + answer[1] + " " + answer[2] + " " + answer[3]);
        }
        
        sc.close();
    }
}
package 코테;

import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int T = sc.nextInt();
        int ans = 0;
        int dot = 2;

        for(int i =T; i > 0; i--) {
        dot += (int)Math.pow(2, (i-1));
        }

        ans += (int)Math.pow(dot, 2);
        System.out.println(ans);
        sc.close();
    }
}
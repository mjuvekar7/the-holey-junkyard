/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package cleancreditsserver;

/**
 *
 * @author shardul
 */
public class CleanCreditsServer {

    private static int PORT = 40404;

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        while (true) {
            try (java.net.ServerSocket sock = new java.net.ServerSocket(PORT)) {
                (new cleancreditsserver.CleanCreditsServerThread(sock.accept())).start();
            } catch (java.io.IOException ex) {
                System.err.println("Caught IOException: " + ex.getLocalizedMessage());
                System.exit(-1);
            }
        }
    }

    static synchronized void updateCredits(String admin, String password, String citizen, int change) {
        // code to update database as per arguments (create record if required)
        // only if admin matches password!
    }

    static synchronized int getCredits(String citizen, String password) {
        // from database, return credits if password is correct
        return 0;
    }
}

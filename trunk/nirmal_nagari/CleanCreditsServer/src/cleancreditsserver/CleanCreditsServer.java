/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package cleancreditsserver;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import org.python.util.PythonInterpreter;

/**
 *
 * @author mandarj, shardulc
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

    static synchronized void updateCredits(String admin_pass, String password, String citizen, int change) throws FileNotFoundException, IOException {
        if (admin_pass.equals(password)) {
            File file = new File("param_update");
            FileOutputStream fos = new FileOutputStream(file);
            String param = citizen + " " + Integer.toString(change);

            byte[] paramBytes = param.getBytes();
            fos.write(paramBytes);
            
            PythonInterpreter.initialize(System.getProperties(), System.getProperties(), new String[0]);
            PythonInterpreter interp = new PythonInterpreter();
            
            interp.execfile("update.py");
            
        } else {
            // Send authentication error
        }
    }

    static synchronized int getCredits(String citizen, String password) {
        // from database, return credits if password is correct
        return 0;
    }
}

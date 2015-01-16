/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package cleancreditsserver;

import java.util.ArrayList;
import java.io.*;
import java.nio.file.*;
import static java.nio.file.StandardOpenOption.*;

/**
 *
 * @author mandarj, shardulc
 */
public class CleanCreditsServer {

    private static int PORT = 40404;

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws IOException {
        while (true) {
            try (java.net.ServerSocket sock = new java.net.ServerSocket(PORT)) {
                (new cleancreditsserver.CleanCreditsServerThread(sock.accept())).start();
            } catch (java.io.IOException ex) {
                System.err.println("Caught IOException: " + ex.getLocalizedMessage());
                System.exit(-1);
            }
        }
    }

    static synchronized void updateCredits(String admin_pass, String password, String citizen, int change) throws IOException {
        if (admin_pass.equals(password)) {
            ArrayList<String> name = new ArrayList();
            ArrayList<String> balance = new ArrayList();
            Path path = Paths.get("resources/balance.txt");

            try (InputStream in = Files.newInputStream(path);
                    BufferedReader reader = new BufferedReader(new InputStreamReader(in))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    String[] parts = line.split(" ");
                    name.add(parts[0]);
                    balance.add(parts[1]);
                }
            } catch (IOException x) {
                System.err.println(x);
            }

            int index = name.indexOf(citizen.toLowerCase());
            int to_set = Integer.parseInt(balance.get(index)) + change;
            balance.set(index, Integer.toString(to_set));

            for (int i = 0; i < name.size(); i++) {
                try (OutputStream out = new BufferedOutputStream(Files.newOutputStream(path, WRITE))) {
                    String tmp = name.get(i) + " " + balance.get(i);
                    byte[] write = tmp.getBytes();
                    out.write(write);
                } catch (IOException x) {
                    System.err.println(x);
                }
            }

        } else {
            // Send authentication error
        }
    }

    static synchronized int getCredits(String citizen) {
        ArrayList<String> name = new ArrayList();
        ArrayList<String> balance = new ArrayList();
        Path path = Paths.get("resources/balance.txt");

        try (InputStream in = Files.newInputStream(path);
                BufferedReader reader = new BufferedReader(new InputStreamReader(in))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(" ");
                name.add(parts[0]);
                balance.add(parts[1]);
            }
        } catch (IOException x) {
            System.err.println(x);
        }

        int index = name.indexOf(citizen.toLowerCase());

        return Integer.parseInt(balance.get(index));
    }
}

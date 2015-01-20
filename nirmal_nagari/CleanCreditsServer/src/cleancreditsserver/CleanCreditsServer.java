/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package cleancreditsserver;

import java.io.*;
import java.nio.file.*;
import static java.nio.file.StandardOpenOption.*;
import java.util.ArrayList;

/**
 *
 * @author mandarj, shardulc
 */
public class CleanCreditsServer {

    private static int PORT = 44444;

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws IOException {
        while (true) {
            try (java.net.ServerSocket sock = new java.net.ServerSocket(PORT)) {
                (new cleancreditsserver.CleanCreditsServerThread(sock.accept())).start();
                System.out.println("client started");
            } catch (java.io.IOException ex) {
                System.err.println("Caught IOException: " + ex.getLocalizedMessage());
                System.exit(-1);
            }
        }
    }

    static synchronized int updateCredits(String admin_pass, String password, String citizen, int change) throws IOException {
        if (admin_pass.equals(new StringBuilder(password).reverse().toString())) {
            ArrayList<String> name = new ArrayList<>();
            ArrayList<String> balance = new ArrayList<>();
            Path path = Paths.get("balance.txt");

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
            if (index != -1) {
                int to_set = Integer.parseInt(balance.get(index)) + change;
                balance.set(index, Integer.toString(to_set));

                try (OutputStream out = new BufferedOutputStream(Files.newOutputStream(path, WRITE))) {
                    for (int i = 0; i < name.size(); i++) {
                        String tmp = name.get(i) + " " + balance.get(i) + "\n";
                        byte[] write = tmp.getBytes();
                        out.write(write);
                    }
                } catch (IOException x) {
                    System.err.println(x);
                }
                return 1;
            }

            try (OutputStream out = new BufferedOutputStream(Files.newOutputStream(path, WRITE))) {
                for (int i = 0; i < name.size(); i++) {
                    String tmp = name.get(i) + " " + balance.get(i) + "\n";
                    byte[] write = tmp.getBytes();
                    out.write(write);
                }
                out.write((citizen + " " + change).toLowerCase().getBytes());
                return 1;
            } catch (IOException x) {
                System.err.println(x);
            }
        }
        return 0;
    }

    static synchronized int getCredits(String citizen, String password) {
        if (citizen.equals(password)) {
            ArrayList<String> name = new ArrayList<>();
            ArrayList<String> balance = new ArrayList<>();
            Path path = Paths.get("balance.txt");

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
            if (index != -1) {
                return Integer.parseInt(balance.get(index));
            }
        }
        return 0;
    }
}

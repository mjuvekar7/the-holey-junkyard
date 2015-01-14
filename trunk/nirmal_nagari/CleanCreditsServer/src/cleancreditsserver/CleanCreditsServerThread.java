/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package cleancreditsserver;

import java.net.Socket;

/**
 *
 * @author shardul
 */
public class CleanCreditsServerThread extends Thread {

    private Socket sock;

    public CleanCreditsServerThread(Socket sock) {
        super("CleanCreditsServerThread");
        this.sock = sock;
    }

    @Override
    public void run() {
        try (java.io.DataInputStream dis = new java.io.DataInputStream(sock.getInputStream());
                java.io.DataOutputStream dos = new java.io.DataOutputStream(sock.getOutputStream())) {
            String username = dis.readUTF();
            String password = dis.readUTF();
            String action = dis.readUTF();
            if (action.equalsIgnoreCase("update")) {
                String citizen = dis.readUTF();
                int change = dis.readInt();
                CleanCreditsServer.updateCredits(username, password, citizen, change);
            } else if (action.equalsIgnoreCase("get")) {
                dos.writeInt(CleanCreditsServer.getCredits(username, password));
            }
        } catch (java.io.IOException ex) {
            System.err.println("Caught IOException: " + ex.getLocalizedMessage());
            System.exit(-1);
        }
    }
}

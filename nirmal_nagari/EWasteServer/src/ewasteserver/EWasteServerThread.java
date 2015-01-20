package ewasteserver;

/**
 * Connection-handling class.
 *
 * {@code EWasteServerThread} instances are created for each connection, and they get the submitted
 * data, update the main window accordingly, and send the next collection date.
 * @author shardul
 */
public class EWasteServerThread extends Thread {
    private java.net.Socket sock;

    public EWasteServerThread(java.net.Socket sock) {
        super("EWasteServerThread");
        this.sock = sock;
    }

    @Override
    public void run() {
        try (java.io.ObjectInputStream in = new java.io.ObjectInputStream(sock.getInputStream())) {
            // read thrice to get three fields
            ewasteserver.EWasteServer.updateData(in.readUTF(), in.readUTF(), in.readUTF());
            java.io.ObjectOutputStream out = new java.io.ObjectOutputStream(sock.getOutputStream());
            out.writeUTF(ewasteserver.EWasteServer.next);
            // flush to force write
            out.flush();
            out.close();
        } catch (java.io.IOException ex) {
            System.err.println("Caught IOException: " + ex.getLocalizedMessage());
            System.exit(-2);
        }
    }
}

/**
 * VoteServerThread.java: vote-counting server thread
 * Copyright (C) 2012 - 2016 Shardul C.
 *
 * This file is part of VoteCounter.
 *
 * VoteCounter is free software: you can redistribute it and/or modify it under
 * the terms of the GNU General Public License as published by the Free Software
 * Foundation, either version 3 of the License, or (at your option) any later
 * version.
 *
 * VoteCounter is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
 * details.
 *
 * You should have received a copy of the GNU General Public License along with
 * VoteCounter. If not, see <http://www.gnu.org/licenses/>.
 *
 * Bugs, tips, suggestions, requests to <shardul.chiplunkar@gmail.com>.
 */
package voteserver;

/**
 * Server thread to handle a single client.
 *
 * {@code VoteServerThread} is created and started by {@link VoteServer} when it
 * accepts a client connection. {@code VoteServerThread} then creates I/O
 * streams, sends required data, and begins receiving and recording votes from
 * the client until the client terminates.
 *
 * @author Shardul C.
 */
public class VoteServerThread extends Thread {

    // client communication streams
    private java.io.ObjectInputStream in;
    private java.io.ObjectOutputStream out;

    /**
     * Constructs a new {@code VoteServerThread} connected to the client.
     *
     * The client's connection has already been accepted and a corresponding
     * {@link java.net.Socket} is passed to the thread. The I/O streams function
     * through this {@link java.net.Socket}. The required data -- post and
     * nominee information -- is sent to the client, and the method loops,
     * receiving and recording votes from the client.
     *
     * @param sock a {@link java.net.Socket} to the client
     */
    public VoteServerThread(java.net.Socket sock) {
        super("VoteServerThread");
        try {
            // create i/o streams
            this.out = new java.io.ObjectOutputStream(sock.getOutputStream());
            out.flush(); // required, otherwise client and server wait for each other
            this.in = new java.io.ObjectInputStream(sock.getInputStream());
        } catch (java.io.IOException ex) {
            System.err.println("Caught IOException: " + ex.getLocalizedMessage());
            System.exit(-2);
        }
    }

    @Override
    public void run() {
        try {
            // send data
            out.writeObject(VoteServer.groups);
            out.writeObject(VoteServer.genericPosts);
            out.writeObject(VoteServer.genericNominees);
            out.writeObject(VoteServer.nonGenericPosts);
            out.writeObject(VoteServer.nonGenericNominees);
            int nonGenSize = VoteServer.nonGenericPosts.size();

            String parts[]; // parts after splitting input from client
            String group; // current voter's group
            boolean done = false; // loop exit

            while (true) {
                out.reset();
                // what group?
                out.writeObject(messages.Messages.GET_GROUP);
                group = in.readObject().toString();

                // client terminated
                if (group.equals(messages.Messages.GOODBYE.toString())) {
                    System.out.println("client terminated");
                    break;
                }

                int groupIndex = 0;
                // increment total and group voter numbers
                VoteServer.voters[0]++;
                if (!group.equals(messages.Messages.NO_GROUP.toString())) {
                    groupIndex = VoteServer.groups.indexOf(group);
                    VoteServer.voters[groupIndex + 1]++;
                }

                // get votes
                for (int step = 0; step < VoteServer.genericPosts.size() + nonGenSize; step++) {
                    String rec = (String) in.readObject();
                    // client terminated
                    if (rec.equals(messages.Messages.GOODBYE.toString())) {
                        System.out.println("client terminated");
                        done = true;
                        break;
                    }
                    parts = rec.split(" "); // the message consists of Messages.VOTE followed by the nominee number
                    if (step < VoteServer.genericPosts.size()) {
                        VoteServer.incVotes(step, Integer.parseInt(parts[1]));
                    } else {
                        if (!group.equals(messages.Messages.NO_GROUP.toString())) {
                            VoteServer.incVotes(step + groupIndex * nonGenSize, Integer.parseInt(parts[1]));
                        }
                    }
                }
                VoteServer.writeVotes();

                if (done) {
                    break;
                }
            }
            in.close();
            out.close();
        } catch (java.io.IOException ex) {
            System.err.println("Caught IOException: " + ex.getLocalizedMessage());
        } catch (ClassNotFoundException ex) {
            System.err.println("Caught ClassNotFoundException: " + ex.getLocalizedMessage());
        }
    }
}

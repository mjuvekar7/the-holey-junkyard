/*
 * VoteServerThread.java: vote-counting server thread
 * Copyright (C) 2012 - 2014 Shardul C.
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

import java.io.*;
import java.net.*;
import java.util.*;

/**
 * Server thread to handle a single client.
 *
 * {@code VoteServerThread} is created and started by {@link VoteServer} when it
 * accepts a client connection. {@code VoteServerThread} then creates I/O
 * streams, sends required data, and begins receiving votes from the client
 * until the client terminates. Votes are updated and written on a regular basis
 * so that they are not lost in case of an application crash.
 *
 * @author Shardul C.
 */
public class VoteServerThread extends Thread {
    // input and output to/from client
    private ObjectInputStream in;
    private ObjectOutputStream out;

    /**
     * Construct a new {@code VoteServerThread} connected to the client.
     *
     * The client's connection has already been accepted and a corresponding
     * {@code Socket} is passed to the thread. The I/O streams function through
     * this {@code Socket}.
     *
     * @param sock a {@code Socket} to the client
     */
    public VoteServerThread(Socket sock) {
        super("VoteServerThread");
        try {
            // create i/o streams
            this.out = new ObjectOutputStream(sock.getOutputStream());
            out.flush();
            this.in = new ObjectInputStream(sock.getInputStream());
        } catch (IOException ex) {
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
            out.writeObject(VoteServer.nonGenericPosts);
            int genSize = VoteServer.genericPosts.size();
            int nonGenSize = VoteServer.nonGenericPosts.size();

            // parts after splitting input from client
            String parts[];
            // current voter's group
            String group;
            // current voter's options
            List<List<String>> options = new ArrayList<>();

            // initialize the non-changing part of the voter's options (the generic parts)
            for (int i = 0; i < genSize; i++) {
                options.add(VoteServer.genericNominees.get(i));
            }

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

                int groupIndex = VoteServer.groups.indexOf(group);
                // increment total and group voter numbers
                VoteServer.voters[0]++;
                VoteServer.voters[groupIndex + 1]++;
                // copy the correct section of the non-generic posts/nominees
                for (int i = 0; i < nonGenSize; i++) {
                    options.add(VoteServer.nonGenericNominees.get(i).get(groupIndex));
                }
                // send options
                out.writeObject(options);

                // get votes
                for (int step = 0; step < options.size(); step++) {
                    parts = ((String) in.readObject()).split(" ");
                    if (step < genSize) {
                        VoteServer.incVotes(step, Integer.parseInt(parts[1]));
                    } else {
                        VoteServer.incVotes(step + groupIndex * nonGenSize, Integer.parseInt(parts[1]));
                    }
                }
                VoteServer.writeVotes();
                options.remove(genSize + nonGenSize - 1);
                options.remove(genSize + nonGenSize - 2);
            }
            VoteServer.writeVotes();
            in.close();
            out.close();
        } catch (IOException ex) {
            System.err.println("Caught IOException: " + ex.getLocalizedMessage());
            System.exit(-2);
        } catch (ClassNotFoundException ex) {
            System.err.println("Caught ClassNotFoundException: " + ex.getLocalizedMessage());
            System.exit(-3);
        }
    }
}

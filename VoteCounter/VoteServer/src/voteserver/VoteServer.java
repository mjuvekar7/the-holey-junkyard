/*
 * VoteServer.java: vote-counting server
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
 * Bugs, tips, suggestions, requests to <shardul.chiplunkar@gmail.com>
 * or <mjuvekar7@gmail.com>.
 */
package voteserver;

import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.Collections;
import java.util.List;

/**
 * Server for vote-counting application.
 *
 * {@code VoteServer} is a forking server which can handle multiple clients and
 * record all votes in a thread-safe manner. The actual data (some of which is
 * passed to the client) is read and parsed from an input XML file by
 * {@link InputParser}.
 *
 * @author Shardul C.
 */
public class VoteServer {
    // only bound is: there have to be *four* nominees per post
    // TODO: fix this!
    static int NOMINEES = 4;

    // information about groups, posts, nominees, etc.
    static List<String> groups;
    static List<String> genericPosts;
    static List<List<String>> genericNominees;
    static List<String> nonGenericPosts;
    static List<List<List<String>>> nonGenericNominees;

    // stores number of votes as votes[post][nominee]
    static int votes[][];
    // stores number of voters as voters[total and separate groups]
    static int voters[];
    static String path;

    /**
     * The main executing method.
     *
     * Check arguments and print appropriate usage message. Then, if arguments
     * are all right, try to establish connection and send data. Lastly, go into
     * a never-ending loop to listen for and accept client connections and spawn
     * threads to handle them.
     *
     * @param args the command-line arguments: <input.xml> and <output.txt>
     */
    public static void main(String args[]) {
        System.out.println("VoteCounter");
        System.out.println("Copyright (C) 2012 - 2014 Shardul C. under GNU GPLv3");

        if (args.length != 2) {
            System.err.println("Usage is java votecounter.VoteServer <input.xml> <output.txt>");
            System.exit(-1);
        }

        path = args[1];
        try (java.net.ServerSocket sock = new java.net.ServerSocket(Integer.parseInt(messages.Messages.PORT.msg))) {
            voteserver.InputParser parser = new voteserver.InputParser();
            parser.parse(new java.io.FileInputStream(args[0]));
            groups = Collections.synchronizedList(parser.getGroups());
            genericPosts = Collections.synchronizedList(parser.getGenericPosts());
            genericNominees = Collections.synchronizedList(parser.getGenericNominees());
            nonGenericPosts = Collections.synchronizedList(parser.getNonGenericPosts());
            nonGenericNominees = Collections.synchronizedList(parser.getNonGenericNominees());
            votes = new int[genericPosts.size() + nonGenericPosts.size()*groups.size()][NOMINEES];
            voters = new int[groups.size() + 1];
            while (true) {
                new voteserver.VoteServerThread(sock.accept()).start();
                System.out.println("client started");
            }
        } catch (java.io.IOException ex) {
            System.err.println("Caught IOException: " + ex.getLocalizedMessage());
            System.exit(-2);
        } catch (org.jdom2.JDOMException ex) {
            System.err.println("Caught JDOMException: " + ex.getLocalizedMessage());
            System.exit(-3);
        }
    }

    /**
     * Write votes to output file.
     *
     * This method is synchronized so it can be called in a thread-safe manner.
     */
    synchronized static void writeVotes() {
        try (java.io.BufferedWriter bw = java.nio.file.Files.newBufferedWriter(Paths.get(path), java.nio.charset.StandardCharsets.UTF_8, StandardOpenOption.WRITE, StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING)) {
            bw.write("Number of total voters: " + voters[0]);
            bw.newLine();
            for (int i = 0; i < groups.size(); i++) {
                bw.write(groups.get(i) + " voters: " + voters[i+1]);
                bw.newLine();
            }
            bw.newLine();
            bw.write("Generic posts:");
            bw.newLine();
            for (int i = 0; i < genericPosts.size(); i++) {
                bw.write(genericPosts.get(i) + " --");
                bw.newLine();
                for (int j = 0; j < NOMINEES; j++) {
                    bw.write(genericNominees.get(i).get(j));
                    for(int k = 0; k < (20 - genericNominees.get(i).get(j).length()); k++) {
                        bw.write(" ");
                    }
                    bw.write(votes[i][j]);
                    bw.newLine();
                }
                bw.newLine();
            }
            bw.newLine();
            bw.newLine();
            bw.write("Non-generic posts:");
            bw.newLine();
            for (int i = genericPosts.size(); i < genericPosts.size() + nonGenericPosts.size(); i++) {
                for (int j = 0; j < groups.size(); j++) {
                    bw.write(groups.get(j) + " " + nonGenericPosts.get(i - genericPosts.size()) + ":");
                    bw.newLine();
                    for (int k = 0; k < NOMINEES; k++) {
                        bw.write(nonGenericNominees.get(i - genericPosts.size()).get(j).get(k));
                        for(int l = 0; l < (20 - nonGenericNominees.get(i - genericPosts.size()).get(j).get(k).length()); l++) {
                            bw.write(" ");
                        }
                        bw.write(votes[i + j * VoteServer.nonGenericPosts.size()][k]);
                        bw.newLine();
                    }
                    bw.newLine();
                }
            }
            bw.newLine();
        } catch (java.io.IOException ex) {
            System.err.println("Caught IOExcpetion (important!): " + ex.getLocalizedMessage());
        }
    }

    /**
     * Increment specified vote category.
     *
     * This method is synchronized so it can be called in a thread-safe manner.
     *
     * @param i post
     * @param j nominee
     */
    synchronized static void incVotes(int i, int j) {
        votes[i][j]++;
    }
}

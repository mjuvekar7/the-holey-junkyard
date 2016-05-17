/**
 * VoteServer.java: vote-counting server
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

import java.util.Collections;
import java.util.List;
import javax.swing.*;

/**
 * Server for vote-counting application.
 *
 * {@code VoteServer} is a forking server which can handle multiple clients and
 * record votes in a thread-safe manner. The actual data (some of which is
 * passed to the client) is read and parsed from an input XML file by
 * {@link InputParser}.
 *
 * @author Shardul C.
 */
public class VoteServer {

    private static int votes[][]; // stores number of votes as votes[post][nominee]
    private static String inPath; // input XML file
    private static String outPath = ""; // output results file

    static int voters[]; // stores number of voters as {total, group 1, group 2, ...}
    static final int ROW_WIDTH = 25; // spacing width in results file

    // information about groups, posts, and nominees
    static List<String> groups;
    static List<String> genericPosts;
    static List<List<String>> genericNominees;
    static List<String> nonGenericPosts;
    static List<List<List<String>>> nonGenericNominees;

    /**
     * The main method.
     *
     * This method gets the input and output paths from {@link
     * #getInOutPaths(java.lang.String[])} and reads the input file with {@link
     * voteserver.InputParser}.
     *
     * Following that, this method enters a never-ending loop to listen for
     * client connections. If no arguments were given, a 'Running...' dialog is
     * also shown.
     *
     * @param args the command-line arguments: <input.xml> and <output.txt>, or
     *             none at all
     */
    public static void main(String[] args) {
        System.out.println("VoteCounter Copyright (C) 2012 - 2016 Shardul C.");
        System.out.println("This program comes with ABSOLUTELY NO WARRANTY. " +
                "This is free software, and you are welcome to redistribute " +
                "it under certain conditions; see the COPYING file for more " +
                "details.");

        getInOutPaths(args);

        try (java.net.ServerSocket sock = new java.net.ServerSocket(Integer.parseInt(messages.Messages.PORT.msg))) {
            voteserver.InputParser parser = new voteserver.InputParser();
            parser.parse(new java.io.FileInputStream(inPath));
            groups = Collections.synchronizedList(parser.getGroups());
            genericPosts = Collections.synchronizedList(parser.getGenericPosts());
            genericNominees = Collections.synchronizedList(parser.getGenericNominees());
            nonGenericPosts = Collections.synchronizedList(parser.getNonGenericPosts());
            nonGenericNominees = Collections.synchronizedList(parser.getNonGenericNominees());
            initVoteArrays();

            if (args.length == 0) {
                //<editor-fold defaultstate="collapsed" desc="Set 'Nimbus L&F (optional)">
                /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
                 * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html
                 */
                try {
                    for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                        if ("Nimbus".equals(info.getName())) {
                            javax.swing.UIManager.setLookAndFeel(info.getClassName());
                            break;
                        }
                    }
                } catch (ClassNotFoundException | InstantiationException | IllegalAccessException | javax.swing.UnsupportedLookAndFeelException ex) {
                    System.err.println("Caught exception in 'look and feel' code: " + ex.getLocalizedMessage());
                }
                //</editor-fold>
                showDialog();
            }
            System.out.println("server started");
            while (true) {
                new voteserver.VoteServerThread(sock.accept()).start(); // blocking accept call
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
     * Gets input and output paths.
     *
     * This method checks whether any arguments are provided and if they are in
     * the correct format. If they are valid, then the thereby given input and
     * output files are used; if they are not valid, a usage message is printed
     * and the server exits. If no arguments are given then a graphical file
     * selector and input box is provided for the input file and output file,
     * respectively.
     *
     * @param args the command-line arguments
     */
    private static void getInOutPaths(String[] args) {
        if (args.length == 0) {
            JFileChooser jfc = new JFileChooser();
            jfc.setFileFilter(new javax.swing.filechooser.FileNameExtensionFilter("XML files", "xml"));
            int opt = jfc.showOpenDialog(null);
            if (opt == JFileChooser.CANCEL_OPTION) {
                JOptionPane.showMessageDialog(null, "No input file chosen, exiting application.",
                        "No Input File Chosen", JOptionPane.WARNING_MESSAGE);
                System.exit(-1);
            } else if (opt == JFileChooser.ERROR_OPTION) {
                System.err.println("Error in JFileChooser!");
                System.exit(-1);
            }
            inPath = jfc.getSelectedFile().getPath();

            outPath = JOptionPane.showInputDialog("Enter the output file name:", "results.txt");
            if (outPath.isEmpty()) {
                JOptionPane.showMessageDialog(null, "No output file chosen, exiting application.",
                        "No Output File Chosen", JOptionPane.WARNING_MESSAGE);
                System.exit(-1);
            }
        } else if (args.length == 2) {
            if (!((new java.io.File(args[0])).exists() && args[0].endsWith("xml"))) {
                System.err.println("Usage is VoteServer <input.xml> <output.txt>, or without any arguments.");
                System.exit(0);
            }
            inPath = args[0];
            outPath = args[1];
        } else {
            System.err.println("Usage is VoteServer <input.xml> <output.txt>, or without any arguments.");
            System.exit(0);
        }
    }

    /**
     * Initializes arrays {@code votes} and {@code voters}.
     */
    private static void initVoteArrays() {
        votes = new int[genericPosts.size() + nonGenericPosts.size() * groups.size()][];
        for (int i = 0; i < genericPosts.size(); i++) {
            votes[i] = new int[genericNominees.get(i).size()];
        }
        for (int i = 0; i < nonGenericPosts.size(); i++) {
            for (int j = 0; j < groups.size(); j++) {
                votes[genericPosts.size() + i * groups.size() + j] = new int[nonGenericNominees.get(i).get(j).size()];
            }
        }
        voters = new int[groups.size() + 1];
    }

    /**
     * Shows a 'Server running...' dialog.
     *
     * The dialog also has a 'Stop server' button which confirms the action and
     * immediately stops the server and the voting process.
     */
    private static void showDialog() {
        final JFrame serverFrame = new JFrame("Server Running");
        serverFrame.setDefaultCloseOperation(JDialog.DO_NOTHING_ON_CLOSE);
        JPanel serverPanel = new JPanel(new java.awt.BorderLayout(5, 5));
        serverPanel.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5));

        serverPanel.add(new JLabel("Server running...", SwingConstants.CENTER), java.awt.BorderLayout.CENTER);
        JButton stop = new JButton("Stop server");
        stop.addActionListener(new java.awt.event.ActionListener() {
            @Override
            public void actionPerformed(java.awt.event.ActionEvent e) {
                if (JOptionPane.showConfirmDialog(serverFrame, "Are you sure you want to stop the server? The voting process will be stopped.",
                        "Stop Server", JOptionPane.YES_NO_OPTION) == JOptionPane.YES_OPTION) {
                    System.out.println("server terminated");
                    writeVotes();
                    System.exit(0);
                }
            }
        });
        serverPanel.add(stop, java.awt.BorderLayout.SOUTH);
        serverPanel.setPreferredSize(new java.awt.Dimension(280, 70));

        serverFrame.add(serverPanel);
        serverFrame.pack();
        serverFrame.setVisible(true);
    }

    /**
     * Writes votes to output file.
     *
     * This method is synchronized so it can be called in a thread-safe manner.
     */
    synchronized static void writeVotes() {
        // TODO: messy code
        try (java.io.BufferedWriter bw = java.nio.file.Files.newBufferedWriter(java.nio.file.Paths.get(outPath),
                java.nio.charset.StandardCharsets.UTF_8, java.nio.file.StandardOpenOption.WRITE,
                java.nio.file.StandardOpenOption.CREATE, java.nio.file.StandardOpenOption.TRUNCATE_EXISTING)) {
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
                for (int j = 0; j < genericNominees.get(i).size(); j++) {
                    bw.write(genericNominees.get(i).get(j));
                    for(int k = 0; k < (ROW_WIDTH - genericNominees.get(i).get(j).length()); k++) {
                        bw.write(" ");
                    }
                    bw.write(Integer.toString(votes[i][j]));
                    bw.newLine();
                }
                bw.newLine();
            }
            if (groups.size() > 0 || nonGenericPosts.size() > 0) {
                bw.newLine();
                bw.newLine();
                bw.write("Non-generic posts:");
                bw.newLine();
                for (int i = genericPosts.size(); i < genericPosts.size() + nonGenericPosts.size(); i++) {
                    for (int j = 0; j < groups.size(); j++) {
                        bw.write(groups.get(j) + " " + nonGenericPosts.get(i - genericPosts.size()) + ":");
                        bw.newLine();
                        for (int k = 0; k < nonGenericNominees.get(i - genericPosts.size()).get(j).size(); k++) {
                            bw.write(nonGenericNominees.get(i - genericPosts.size()).get(j).get(k));
                            for (int l = 0; l < (ROW_WIDTH - nonGenericNominees.get(i - genericPosts.size()).get(j).get(k).length()); l++) {
                                bw.write(" ");
                            }
                            bw.write(Integer.toString(votes[i + j*nonGenericPosts.size()][k]));
                            bw.newLine();
                        }
                        bw.newLine();
                    }
                }
                bw.newLine();
            }
        } catch (java.io.IOException ex) {
            System.err.println("Caught IOException (important!): " + ex.getLocalizedMessage());
        }
    }

    /**
     * Increments specified vote category.
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

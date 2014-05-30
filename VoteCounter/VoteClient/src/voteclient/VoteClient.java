/*
 * VoteClient.java: voting client
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
package voteclient;

import java.io.IOException;
import java.net.*;
import java.util.ArrayList;
import java.util.List;
import javax.swing.JOptionPane;
import messages.Messages;

/**
 * Client end for vote counting application.
 *
 * {@code VoteClient} is the independent client end of VoteCounter. It has a Swing GUI,
 * but that is almost all it has -- all the vote counting and recording is done
 * at the server.
 * When an instance of the client is started, it tries to
 * connect to a server at the given address/hostname. Once this connection is
 * successfully established, it reads in the data required (information about
 * the groups, posts, nominees, etc.) and starts the voting. All votes are sent
 * to the server where they are recorded. The client itself does not know
 * anything about the results, or about the next set of options.
 *
 * @author Shardul C.
 */
public class VoteClient extends javax.swing.JFrame {
    // only bound is: there have to be *four* nominees per post
    // TODO: fix this!
    // might not be fixable (how would I lay out the buttons?)
    static int NOMINEES = 4;
    // options for each voter
    private List<List<String>> opts = new ArrayList<>();
    // voter number
    private static int voterNum = 0;
    // serial version UID for serialization
    private static final long serialVersionUID = 1L;

    // data from server
    static List<String> groups;
    static List<String> genericPosts;
    static List<String> nonGenericPosts;

    // current chosen group
    static String group;
    // current position in voting sequence
    static int step;

    // input and output to/from server
    private static java.io.ObjectInputStream in;
    private static java.io.ObjectOutputStream out;

    /**
     * Creates new form VoteClient and starts voting process.
     */
    public VoteClient() {
        initComponents();
        chooseGroup();
    }

    /**
     * Allows the voter to choose a group, and gets corresponding options from
     * server.
     *
     * The method increments both the client and server side voter numbers. If
     * the voter does not choose a group, the program terminates. The group
     * chooser dialog is not shown until the server is ready to accept a new
     * voter.
     */
    @SuppressWarnings("unchecked")
    private void chooseGroup() {
        try {
            // wait for message
            Object temp = in.readObject();
            // select group
            group = (String) JOptionPane.showInputDialog(this, "Voter #" + (voterNum + 1) + ": Choose your house:",
                    "Choose House", JOptionPane.PLAIN_MESSAGE, null, groups.toArray(), "");
            // voter hit cancel
            if (group == null) {
                exitActionPerformed(null);
            }
            voterNum++;
            // if-else to test msg cut out because
            // server only sends one message anyway
            out.writeObject(group);
            opts = (List<List<String>>) in.readObject();
            // start individual voting process
            voterStart();
        } catch (IOException ex) {
            System.err.println("Caught IOException: " + ex.getLocalizedMessage());
        } catch (ClassNotFoundException ex) {
            System.err.println("Caught ClassNotFoundException: " + ex.getLocalizedMessage());
        }
    }

    /**
     * Sets the displayed options.
     *
     * This method displays the options according to the current progress in the
     * voting sequence.
     */
    private void voterStart() {
        // set the proper heading
        num.setText("Voter #" + voterNum);
        if (step < genericPosts.size()) {
            category.setText(genericPosts.get(step));
        } else {
            category.setText(group + " " + nonGenericPosts.get(step - genericPosts.size()));
        }
        // set the proper options
        opt0.setText(opts.get(step).get(0));
        opt1.setText(opts.get(step).get(1));
        opt2.setText(opts.get(step).get(2));
        opt3.setText(opts.get(step).get(3));
    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        category = new javax.swing.JLabel();
        opt0 = new javax.swing.JButton();
        opt1 = new javax.swing.JButton();
        opt2 = new javax.swing.JButton();
        opt3 = new javax.swing.JButton();
        num = new javax.swing.JLabel();
        menuBar = new javax.swing.JMenuBar();
        fileMenu = new javax.swing.JMenu();
        exit = new javax.swing.JMenuItem();
        sep = new javax.swing.JPopupMenu.Separator();
        license = new javax.swing.JMenuItem();
        about = new javax.swing.JMenuItem();

        setDefaultCloseOperation(javax.swing.WindowConstants.DO_NOTHING_ON_CLOSE);
        setTitle("VoteCounter");
        setBounds(new java.awt.Rectangle(600, 300, 0, 0));

        category.setFont(new java.awt.Font("SansSerif", 1, 14)); // NOI18N
        category.setText("Category");
        category.setHorizontalTextPosition(javax.swing.SwingConstants.CENTER);

        opt0.setFont(new java.awt.Font("SansSerif", 1, 14)); // NOI18N
        opt0.setText("One");
        opt0.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                vote(evt);
            }
        });

        opt1.setFont(new java.awt.Font("SansSerif", 1, 14)); // NOI18N
        opt1.setText("Two");
        opt1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                vote(evt);
            }
        });

        opt2.setFont(new java.awt.Font("SansSerif", 1, 14)); // NOI18N
        opt2.setText("Three");
        opt2.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                vote(evt);
            }
        });

        opt3.setFont(new java.awt.Font("SansSerif", 1, 14)); // NOI18N
        opt3.setText("Four");
        opt3.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                vote(evt);
            }
        });

        num.setText("Voter #1");

        fileMenu.setText("File");

        exit.setAccelerator(javax.swing.KeyStroke.getKeyStroke(java.awt.event.KeyEvent.VK_F4, java.awt.event.InputEvent.ALT_MASK));
        exit.setText("Exit");
        exit.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                exitActionPerformed(evt);
            }
        });
        fileMenu.add(exit);
        fileMenu.add(sep);

        license.setText("License");
        license.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                licenseActionPerformed(evt);
            }
        });
        fileMenu.add(license);

        about.setText("About");
        about.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                aboutActionPerformed(evt);
            }
        });
        fileMenu.add(about);

        menuBar.add(fileMenu);

        setJMenuBar(menuBar);

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGap(47, 47, 47)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(opt0)
                    .addComponent(opt2))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, 140, Short.MAX_VALUE)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                    .addComponent(opt3)
                    .addComponent(opt1))
                .addGap(57, 57, 57))
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addContainerGap(160, Short.MAX_VALUE)
                .addComponent(category, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, 90, Short.MAX_VALUE)
                .addComponent(num)
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(num)
                        .addGap(0, 0, Short.MAX_VALUE))
                    .addGroup(layout.createSequentialGroup()
                        .addContainerGap()
                        .addComponent(category, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)))
                .addGap(18, 18, 18)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(opt0)
                    .addComponent(opt1))
                .addGap(18, 18, 18)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(opt2)
                    .addComponent(opt3))
                .addContainerGap())
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void vote(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_vote
        // get source of event (which button?)
        int choice = 0;
        if (evt.getSource() == opt0) {
            choice = 0;
        } else if (evt.getSource() == opt1) {
            choice = 1;
        } else if (evt.getSource() == opt2) {
            choice = 2;
        } else if (evt.getSource() == opt3) {
            choice = 3;
        }
        try {
            // send vote to server
            out.writeObject(Messages.VOTE + " " + choice);
        } catch (IOException ex) {
            System.err.println("Caught IOException: " + ex.getLocalizedMessage());
        }

        // increment current position in voting sequence
        step++;
        // if end of voting sequence
        if (step == genericPosts.size() + nonGenericPosts.size()) {
            // reset
            step = 0;
            JOptionPane.showMessageDialog(this, "Thank You! Your votes have been recorded.", "Exit", JOptionPane.INFORMATION_MESSAGE);
            // start again
            chooseGroup();
        } else {
            // new options
            voterStart();
        }
    }//GEN-LAST:event_vote

    private void exitActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_exitActionPerformed
        // confirm, send goodbye, and exit
        if (JOptionPane.showConfirmDialog(this, "Exit application?", "Exit", JOptionPane.YES_NO_OPTION, JOptionPane.WARNING_MESSAGE) == JOptionPane.YES_OPTION) {
            try {
                out.writeObject(Messages.GOODBYE);
                in.close();
                out.close();
            } catch (IOException ex) {
                System.err.println("Caught IOException: " + ex.getLocalizedMessage());
            }
            System.exit(0);
        }
    }//GEN-LAST:event_exitActionPerformed

    private void licenseActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_licenseActionPerformed
        // display the license
        StringBuilder txt = new StringBuilder();
        try {
            java.io.BufferedReader br = new java.io.BufferedReader(new java.io.InputStreamReader(VoteClient.class.getResourceAsStream("/resources/COPYING")));
            String line = br.readLine();
            while (line != null) {
                txt.append(line);
                txt.append("\n");
                line = br.readLine();
            }
        } catch (IOException ex) {
            System.err.println(ex.getLocalizedMessage());
        }
        javax.swing.JTextArea lic = new javax.swing.JTextArea(txt.toString());
        javax.swing.JScrollPane scroller = new javax.swing.JScrollPane(lic, javax.swing.JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED, javax.swing.JScrollPane.HORIZONTAL_SCROLLBAR_NEVER);
        lic.setVisible(true);
        lic.setEditable(false);
        scroller.setVisible(true);
        javax.swing.JDialog licenseDialog = new javax.swing.JDialog(this, "VoteCounter License");
        licenseDialog.add(scroller);
        licenseDialog.setSize(600, 500);
        licenseDialog.setVisible(true);
    }//GEN-LAST:event_licenseActionPerformed

    private void aboutActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_aboutActionPerformed
        // thank you, thank you! <bow to audience>
        javax.swing.JDialog aboutDialog = new javax.swing.JDialog(this, "About VoteCounter");
        String msg = "<html><center>VoteCounter: Java vote counting application<br />Copyright (C) 2012 - 2014 Shardul C.<br /><br />"
        + "Bugs, tips, suggestions, requests to<br />&lt;shardul.chiplunkar@gmail.com&gt.</center></html>";
        javax.swing.JLabel lbl = new javax.swing.JLabel(msg);
        lbl.setIcon(new javax.swing.ImageIcon(VoteClient.class.getResource("/resources/gpl-v3-logo.png")));
        lbl.setVisible(true);
        aboutDialog.add(lbl);
        aboutDialog.setSize(400, 150);
        aboutDialog.setVisible(true);
    }//GEN-LAST:event_aboutActionPerformed

    /**
     * The main executing method.
     *
     * Check arguments and print appropriate usage message. Then, if arguments
     * are all right, try to establish connection and receive data. Lastly,
     * create form.
     *
     * @param args the command-line arguments: the server address/hostname
     */
    @SuppressWarnings("unchecked")
    public static void main(String args[]) {
        System.out.println("VoteCounter");
        System.out.println("Copyright (C) 2012 - 2014 Shardul C. under GNU GPLv3");

        try {
            // connect to server and create i/o streams
            Socket sock = new Socket(JOptionPane.showInputDialog("Enter server IP address:"), Integer.parseInt(messages.Messages.PORT.msg));
            out = new java.io.ObjectOutputStream(sock.getOutputStream());
            out.flush();
            in = new java.io.ObjectInputStream(sock.getInputStream());

            // get required data
            groups = (List<String>) in.readObject();
            genericPosts = (List<String>) in.readObject();
            nonGenericPosts = (List<String>) in.readObject();
        } catch (IOException ex) {
            System.err.println("Caught IOException: " + ex.getLocalizedMessage());
            System.exit(-2);
        } catch (ClassNotFoundException ex) {
            System.err.println("Caught ClassNotFoundException: " + ex.getLocalizedMessage());
            System.exit(-3);
        }

        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
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

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            @Override
            public void run() {
                new VoteClient().setVisible(true);
            }
        });
    }
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JMenuItem about;
    private javax.swing.JLabel category;
    private javax.swing.JMenuItem exit;
    private javax.swing.JMenu fileMenu;
    private javax.swing.JMenuItem license;
    private javax.swing.JMenuBar menuBar;
    private javax.swing.JLabel num;
    private javax.swing.JButton opt0;
    private javax.swing.JButton opt1;
    private javax.swing.JButton opt2;
    private javax.swing.JButton opt3;
    private javax.swing.JPopupMenu.Separator sep;
    // End of variables declaration//GEN-END:variables
}

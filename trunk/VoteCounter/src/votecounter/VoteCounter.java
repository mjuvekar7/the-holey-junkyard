/**
 * VoteCounter.java: main vote-counting application Copyright (C) 2012, 2013
 * Shardul C.
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
package votecounter;

import java.io.IOException;
import java.nio.file.StandardOpenOption;
import javax.swing.ImageIcon;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JOptionPane;

/**
 * Vote counting application.
 *
 * This vote counting GUI application counts votes for typical school elections.
 * There are categories for the Head Boy/Girl, Sports Prefect Boy/Girl, and
 * House Captain and House Vice Captain for four houses. Currently, the
 * categories and the candidates are hard-coded, but reading them in from a file
 * is planned for the future.
 *
 * @author shardul
 */
public class VoteCounter extends javax.swing.JFrame {

    // progress in current voting sequence
    private static int step = 0;
    // constants for number of categories and candidates
    private static final int CATEGORIES = 6;
    private static final int CANDIDATES = 4;
    private static String house;
    private final static String[] categories = {"Head Boy", "Head Girl", "Sports Prefect Boy", "Sports Prefect Girl", "House Captain", "House Vice Captain"};
    private final static String[] houseOptions = {"Jaguar", "Sher", "Puma", "Cheetah"};
    private final static String[] headBoy = {"Anthony", "Bheem", "Cristopher", "Dhruv"};
    private final static String[] headGirl = {"Anjali", "Beena", "Chhaya", "Dorothy"};
    private final static String[] sportsBoy = {"Amar", "Bhairav", "Chintamani", "Dhananjay"};
    private final static String[] sportsGirl = {"Arya", "Bakul", "Cathy", "Droupadi"};
    private final static String[][] houseCaptain = {{"Arjun", "Beena", "Chhaya", "Dhruv"},
        {"Purushottam", "Padma", "Pam", "Pandu"},
        {"Sahadev", "Seema", "Sam", "Sunder"},
        {"Rahul", "Rohini", "Reshma", "Rohan"}};
    private final static String[][] houseViceCaptain = {{"Edmund", "Mary", "Peter", "Daniel"},
        {"Ram", "Hari", "Vishnudas", "Digambar"},
        {"Mohammed", "Ali", "Akbar", "Dawood"},
        {"Antoniette", "Sylvie", "Francois", "Henry"}};
    // number of votes and voters
    private static int[][] votes = new int[12][CANDIDATES];
    private static int[] voters = new int[5];
    // options for current voting sequence
    private static String[][] options = new String[CATEGORIES][CANDIDATES];
    private static final long serialVersionUID = 1L;
    // default results file
    private static final java.nio.file.Path path = java.nio.file.Paths.get("results.txt");

    /**
     * Creates new form VoteCounter
     */
    public VoteCounter() {
        initComponents();
        // initialize unchanging options
        // that is, initialize Head Boy/Girl and Sports Prefect Boy/Girl
        for (int i = 0; i < CATEGORIES - 2; i++) {
            for (int j = 0; j < CANDIDATES; j++) {
                switch (i) {
                    case 0:
                        options[i][j] = headBoy[j];
                        break;
                    case 1:
                        options[i][j] = headGirl[j];
                        break;
                    case 2:
                        options[i][j] = sportsBoy[j];
                        break;
                    case 3:
                        options[i][j] = sportsGirl[j];
                        break;
                }
            }
        }
        chooseHouse();
        initOptions();
        showOptions();
    }

    /**
     * Opens the dialog for choosing the house.
     */
    private void chooseHouse() {
        // house set to user's choice
        house = (String) JOptionPane.showInputDialog(this, "Choose your house:", "Choose House", JOptionPane.PLAIN_MESSAGE, null, houseOptions, "Jaguar");
        // if user selected an option
        if ((house != null) && (house.length() > 0)) {
            // count total and house-wise voters
            voters[0]++;
            switch (house) {
                case "Jaguar":
                    voters[1]++;
                    break;
                case "Sher":
                    voters[2]++;
                    break;
                case "Puma":
                    voters[3]++;
                    break;
                case "Cheetah":
                    voters[4]++;
                    break;
            }
        }
    }

    /**
     * Initializes displayed options according to house.
     *
     * This method initializes the nominee options which will be displayed
     * according to the house chosen by {@link #chooseHouse()}.
     */
    private void initOptions() {
        // initialize changing options from candidates according to house
        // that is, initialize House Captain and House Vice Captain
        for (int i = 4; i < CATEGORIES; i++) {
            for (int j = 0; j < CANDIDATES; j++) {
                switch (i) {
                    case 4:
                        switch (house) {
                            case "Jaguar":
                                options[i][j] = houseCaptain[0][j];
                                break;
                            case "Sher":
                                options[i][j] = houseCaptain[1][j];
                                break;
                            case "Puma":
                                options[i][j] = houseCaptain[2][j];
                                break;
                            case "Cheetah":
                                options[i][j] = houseCaptain[3][j];
                                break;
                        }
                        break;
                    case 5:
                        switch (house) {
                            case "Jaguar":
                                options[i][j] = houseViceCaptain[0][j];
                                break;
                            case "Sher":
                                options[i][j] = houseViceCaptain[1][j];
                                break;
                            case "Puma":
                                options[i][j] = houseViceCaptain[2][j];
                                break;
                            case "Cheetah":
                                options[i][j] = houseViceCaptain[3][j];
                                break;
                        }
                        break;
                }
            }
        }
    }

    /**
     * Displays the options.
     *
     * This method displays the options according to the current progress in the
     * voting sequence. The options are initialized beforehand by
     * {@link #initOptions()}.
     */
    private void showOptions() {
        category.setText(categories[step]);
        opt0.setText(options[step][0]);
        opt1.setText(options[step][1]);
        opt2.setText(options[step][2]);
        opt3.setText(options[step][3]);
    }

    /**
     * Read XML input file.
     *
     * Right now, we are not doing anything with the data other than printing it
     * out to standard output.
     *
     * @param path the XML input file
     */
    public static void readXMLInput(String path) {
        try {
            votecounter.InputParser.parse((new InputParser()).getClass().getResourceAsStream(path));
        } catch (org.jdom2.JDOMException | java.io.IOException ex) {
            System.err.println(ex);
        }
        System.out.println(votecounter.InputParser.getGroups());
        System.out.println(votecounter.InputParser.getGenericPosts());
        System.out.println(votecounter.InputParser.getNonGenericPosts());
        System.out.println();
        String[][] genericNominees = votecounter.InputParser.getGenericNominees();
        for (int i = 0; i < genericNominees.length; i++) {
            System.out.println(votecounter.InputParser.getGenericPosts().get(i) + " -- ");
            for (int j = 0; j < genericNominees[i].length; j++) {
                System.out.println(genericNominees[i][j]);
            }
            System.out.println();
        }
        String[][][] nonGenericNominees = votecounter.InputParser.getNonGenericNominees();
        for (int i = 0; i < nonGenericNominees.length; i++) {
            System.out.println(votecounter.InputParser.getNonGenericPosts().get(i) + " -- ");
            for (int j = 0; j < nonGenericNominees[i].length; j++) {
                if (nonGenericNominees[i][j] != null) {
                    for (int k = 0; k < nonGenericNominees[i][j].length; k++) {
                        System.out.println(nonGenericNominees[i][j][k]);
                    }
                }
            }
            System.out.println();
        }
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
        choose = new javax.swing.JMenuItem();
        show = new javax.swing.JMenuItem();
        exit = new javax.swing.JMenuItem();
        sep = new javax.swing.JPopupMenu.Separator();
        license = new javax.swing.JMenuItem();
        about = new javax.swing.JMenuItem();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        setTitle("VoteCounter");

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

        choose.setAccelerator(javax.swing.KeyStroke.getKeyStroke(java.awt.event.KeyEvent.VK_H, java.awt.event.InputEvent.CTRL_MASK));
        choose.setText("Next Voter");
        choose.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                chooseActionPerformed(evt);
            }
        });
        fileMenu.add(choose);

        show.setAccelerator(javax.swing.KeyStroke.getKeyStroke(java.awt.event.KeyEvent.VK_A, java.awt.event.InputEvent.CTRL_MASK));
        show.setText("Show Results");
        show.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                showActionPerformed(evt);
            }
        });
        fileMenu.add(show);

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
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
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
                        .addComponent(category, javax.swing.GroupLayout.DEFAULT_SIZE, 21, Short.MAX_VALUE)))
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

    /**
     * Exits the application.
     *
     * @param evt the event which generated this handler
     */
    private void exitActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_exitActionPerformed
        // confirm and exit
        showActionPerformed(evt);
        if (JOptionPane.showConfirmDialog(this, "Exit application?", "Exit", JOptionPane.YES_NO_OPTION, JOptionPane.WARNING_MESSAGE) == JOptionPane.YES_OPTION) {
            System.exit(0);
        }
    }//GEN-LAST:event_exitActionPerformed

    /**
     * Writes the results.
     *
     * This method writes the accumulated results into the default results file.
     * If the method is called multiple times, the file is truncated and the new
     * results are written.
     *
     * @param evt the event which generated this handler
     */
    private void showActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_showActionPerformed
        // all categories
        String[][] nominees = {headBoy, headGirl, sportsBoy, sportsGirl,
            houseCaptain[0], houseCaptain[1], houseCaptain[2], houseCaptain[3],
            houseViceCaptain[0], houseViceCaptain[1], houseViceCaptain[2], houseViceCaptain[3]};
        try (java.io.BufferedWriter bw = java.nio.file.Files.newBufferedWriter(path, java.nio.charset.StandardCharsets.UTF_8, StandardOpenOption.WRITE, StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING)) {

            bw.write("Number of voters: " + voters[0]);
            bw.newLine();
            bw.write("Jaguar voters: " + voters[1]);
            bw.newLine();
            bw.write("Sher voters: " + voters[2]);
            bw.newLine();
            bw.write("Puma voters: " + voters[3]);
            bw.newLine();
            bw.write("Cheetah voters: " + voters[4]);
            bw.newLine();
            bw.newLine();

            // write number of votes
            for (int i = 0; i < 12; i++) {
                switch (i) {
                    case 0:
                        bw.write("Head Boy:");
                        bw.newLine();
                        break;
                    case 1:
                        bw.write("Head Girl:");
                        bw.newLine();
                        break;
                    case 2:
                        bw.write("Sports Prefect Boy:");
                        bw.newLine();
                        break;
                    case 3:
                        bw.write("Sports Prefect Girl:");
                        bw.newLine();
                        break;
                    case 4:
                        bw.write("Jaguar House Captain:");
                        bw.newLine();
                        break;
                    case 5:
                        bw.write("Sher House Captain:");
                        bw.newLine();
                        break;
                    case 6:
                        bw.write("Puma House Captain:");
                        bw.newLine();
                        break;
                    case 7:
                        bw.write("Cheetah House Captain:");
                        bw.newLine();
                        break;
                    case 8:
                        bw.write("Jaguar House Vice Captain:");
                        bw.newLine();
                        break;
                    case 9:
                        bw.write("Sher House Vice Captain:");
                        bw.newLine();
                        break;
                    case 10:
                        bw.write("Puma House Vice Captain:");
                        bw.newLine();
                        break;
                    case 11:
                        bw.write("Cheetah House Vice Captain:");
                        bw.newLine();
                        break;
                }
                for (int j = 0; j < CANDIDATES; j++) {
                    bw.write(nominees[i][j] + " -- " + votes[i][j]);
                    bw.newLine();
                }
                bw.newLine();
                bw.newLine();
            }
        } catch (java.io.IOException e) {
            System.err.println("Caught IOException: " + e.getMessage());
        }

    }//GEN-LAST:event_showActionPerformed

    /**
     * Shows the house chooser dialog.
     *
     * @param evt the event which generated this handler
     */
    private void chooseActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_chooseActionPerformed
        chooseHouse();
        initOptions();
        showOptions();
    }//GEN-LAST:event_chooseActionPerformed

    /**
     * Records the vote.
     *
     * This method is a handler for {@code ActionEvent}s generated by the
     * buttons, and it records votes according to the option selected from the
     * options displayed by {@link #showOptions()}. The vote is recorded in the
     * current category, and the total voters are counted as well.
     *
     * @param evt the event which generated this handler
     */
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

        // record vote according to category and house
        switch (category.getText()) {
            case "Head Boy":
                votes[0][choice]++;
                break;
            case "Head Girl":
                votes[1][choice]++;
                break;
            case "Sports Prefect Boy":
                votes[2][choice]++;
                break;
            case "Sports Prefect Girl":
                votes[3][choice]++;
                break;
            case "House Captain":
                switch (house) {
                    case "Jaguar":
                        votes[4][choice]++;
                        break;
                    case "Sher":
                        votes[5][choice]++;
                        break;
                    case "Puma":
                        votes[6][choice]++;
                        break;
                    case "Cheetah":
                        votes[7][choice]++;
                        break;
                }
                break;
            case "House Vice Captain":
                switch (house) {
                    case "Jaguar":
                        votes[8][choice]++;
                        break;
                    case "Sher":
                        votes[9][choice]++;
                        break;
                    case "Puma":
                        votes[10][choice]++;
                        break;
                    case "Cheetah":
                        votes[11][choice]++;
                        break;
                }
                break;
        }

        // has voting sequence finished?
        step++;
        if (step == 6) {
            JOptionPane.showMessageDialog(this, "Thank You! Your votes have been recorded.", "Exit", JOptionPane.INFORMATION_MESSAGE);
            showActionPerformed(evt);
            step = 0;
            chooseHouse();
            num.setText("Voter #" + voters[0]);
        }

        // next voter
        if (house != null) {
            initOptions();
            showOptions();
        }
    }//GEN-LAST:event_vote

    /**
     * Shows an 'About' dialog box.
     * 
     * The dialog shown includes the author and copyright and an email address
     * for bug reporting or suggestions.
     * 
     * @param evt the event which generated this handler
     */
    private void aboutActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_aboutActionPerformed
        JDialog aboutDialog = new JDialog(this, "About VoteCounter");
        String msg = "<html><pre>   VoteCounter: Java vote counting application    <br />        Copyright (C) 2012, 2013 Shardul C.       <br /><br />"
                + "       Bugs, tips, suggestions, requests to       <br />&lt;shardul.chiplunkar@gmail.com&gt; or &lt;mjuvekar7@gmail.com&gt;.</pre></html>";
        JLabel lbl = new JLabel(msg);
        lbl.setIcon(new ImageIcon("resources/gpl-v3-logo-black.jpg", "GPLv3 logo"));
        lbl.setVisible(true);
        aboutDialog.add(lbl);
        aboutDialog.setSize(400, 150);
        aboutDialog.setVisible(true);
    }//GEN-LAST:event_aboutActionPerformed

    /**
     * Shows the license.
     * 
     * @param evt the event which generated this handler
     */
    private void licenseActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_licenseActionPerformed
        JDialog licenseDialog = new JDialog(this, "VoteCounter GPL License");
        java.io.File file = new java.io.File("resources/COPYING");
        String txt = null;
        try (java.io.BufferedInputStream stream = new java.io.BufferedInputStream(new java.io.FileInputStream(file))) {
            byte[] data;
            data = new byte[(int) file.length()];
            stream.read(data);
            txt = new String(data, "UTF-8");
        } catch (IOException ex) {
            System.err.println(ex.getLocalizedMessage());
        }
        JLabel licenseLabel = new JLabel("<html><body style='width: 450px'><pre>" + txt + "</pre></body></html>");
        javax.swing.JScrollPane scroller = new javax.swing.JScrollPane(licenseLabel, javax.swing.JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED, javax.swing.JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);
        licenseLabel.setVisible(true);
        scroller.setVisible(true);
        licenseDialog.add(scroller);
        licenseDialog.setSize(600, 800);
        licenseDialog.setVisible(true);
    }//GEN-LAST:event_licenseActionPerformed

    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) {
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
            System.err.println(ex.getLocalizedMessage());
        }
        //</editor-fold>

        // Create and display the form
        java.awt.EventQueue.invokeLater(new Runnable() {
            @Override
            public void run() {
                new VoteCounter().setVisible(true);
            }
        });
//        readXMLInput("resources/school.xml");
    }
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JMenuItem about;
    private javax.swing.JLabel category;
    private javax.swing.JMenuItem choose;
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
    private javax.swing.JMenuItem show;
    // End of variables declaration//GEN-END:variables
}

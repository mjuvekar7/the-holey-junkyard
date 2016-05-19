/**
 * VoteClient.java: voting client
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
package voteclient;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;
import java.util.List;
import javax.sound.sampled.*;
import javax.swing.*;
import messages.Messages;

/**
 * Client end for vote-counting application.
 *
 * {@code VoteClient} is the independent client end of VoteCounter. @{code
 * VoteClient} has a Swing GUI which dynamically updates to display buttons for
 * each nominee in the given voting categories. It connects to a running @{code
 * VoteServer} where the votes are recorded.
 *
 * @author Shardul C.
 */
public class VoteClient extends JFrame {

    // GUI-related variables that need to be visible to the rest of the class
    private JPanel buttonPanel;
    private JLabel voterNumLabel;
    private JLabel categoryLabel;
    private GridBagConstraints c;

    // information received from the server
    private List<String> groups;
    private List<String> genericPosts;
    private List<List<String>> genericNominees;
    private List<String> nonGenericPosts;
    private List<List<List<String>>> nonGenericNominees;

    // current state information
    private String group;
    private int voterNum;
    private final List<List<String>> opts = new java.util.ArrayList<>();
    private int step;

    // server communication streams
    private java.io.ObjectInputStream in;
    private java.io.ObjectOutputStream out;

    private static final long serialVersionUID = 1L;

    /**
     * Creates new form VoteClient and starts voting process.
     *
     * The GUI elements are initialized, a connection is made with the server to
     * read in the post and nominee information and send votes, and the voting
     * process is started. If a local server is running, the client connects to
     * it by default (see {@link #VoteClient(boolean)}).
     */
    public VoteClient() {
        initComponents();
        getData(true);
        initGroupAndOptions();
    }

    /**
     * Creates new form VoteClient and starts voting process.
     *
     * The GUI elements are initialized, a connection is made with the server to
     * read in the post and nominee information and send votes, and the voting
     * process is started. The parameter {@code checkLocal} specifies whether to
     * check for a locally-running server by default.
     *
     * @param checkLocal whether to check for a local server
     */
    public VoteClient(boolean checkLocal) {
        initComponents();
        getData(checkLocal);
        initGroupAndOptions();
    }

    /**
     * Initializes GUI components.
     *
     * {@code VoteClient} uses a {@link GridBagLayout} as its top-level layout
     * manager to adjust the vertical space allotted to the header and the
     * buttons properly. The panel containing the buttons also uses a {@code
     * GridBagLayout} for the same reason.
     */
    private void initComponents() {
        // the header panel contains the voter number label and the category label
        JPanel headerPanel = new JPanel(new BorderLayout(5, 5));
        voterNumLabel = new JLabel("Voter #", javax.swing.SwingConstants.TRAILING);
        voterNumLabel.setFont(new Font("SansSerif", Font.ITALIC, 15));
        categoryLabel = new JLabel("Category", javax.swing.SwingConstants.CENTER);
        categoryLabel.setFont(new Font("SansSerif", Font.BOLD, 24));
        headerPanel.add(voterNumLabel, BorderLayout.NORTH);
        headerPanel.add(categoryLabel, BorderLayout.CENTER);

        buttonPanel = new JPanel(new GridBagLayout());

        JMenuBar menuBar = new JMenuBar();
        JMenu fileMenu = new JMenu("File");
        JMenuItem exit = new JMenuItem("Exit");
        JMenuItem license = new JMenuItem("License");
        JMenuItem about = new JMenuItem("About");

        exit.setAccelerator(javax.swing.KeyStroke.getKeyStroke(java.awt.event.KeyEvent.VK_F4, java.awt.event.InputEvent.ALT_MASK));
        exit.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent evt) {
                exit();
            }
        });
        license.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent evt) {
                showLicense();
            }
        });
        about.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent evt) {
                showCredits();
            }
        });

        fileMenu.add(exit);
        fileMenu.add(new JPopupMenu.Separator());
        fileMenu.add(license);
        fileMenu.add(about);
        menuBar.add(fileMenu);
        setJMenuBar(menuBar);

        this.setLayout(new GridBagLayout());

        c = new GridBagConstraints();
        c.gridx = 0;
        c.gridy = 0;
        c.gridwidth = 1;
        c.gridheight = 1;
        c.fill = GridBagConstraints.BOTH;
        c.insets = new Insets(10, 10, 10, 10);
        c.weightx = 1;
        c.weighty = 0.2; // header panel gets 20% of available vertical space
        this.add(headerPanel, c);

        c = new GridBagConstraints();
        c.gridx = 0;
        c.gridy = 1;
        c.gridwidth = 1;
        c.gridheight = 1;
        c.fill = GridBagConstraints.BOTH;
        c.insets = new Insets(10, 10, 10, 10);
        c.weightx = 1;
        c.weighty = 0.8; // button panel gets 80% of available vertical space
        this.add(buttonPanel, c);

        this.setDefaultCloseOperation(DO_NOTHING_ON_CLOSE); // close only throuhg file menu or accelerator
        this.setMinimumSize(new Dimension(750, 400));
        this.setLocationByPlatform(true);
        this.setTitle("VoteCounter");

        this.pack();
    }

    /**
     * Gets required data from server.
     *
     * If the {@code checkLocal} parameter is set, the method tries to connect
     * to a locally-running server. If this fails, then the user is prompted for
     * the server's IP address, which is also the behavior of the method if the
     * {@code checkLocal} parameter is not set.
     *
     * The method also initializes the unchanging portion of the options
     * available to each voter.
     *
     * @param checkLocal whether to check for a local server
     */
    @SuppressWarnings("unchecked")
    private void getData(boolean checkLocal) {
        try {
            java.net.Socket sock = null;
            // connect to local server if possible and required
            if (checkLocal) {
                try {
                    sock = new java.net.Socket((String) null,
                            Integer.parseInt(messages.Messages.PORT.msg));
                } catch (IOException ex) {
                    // connection refused, no local server
                }
            }

            // no local server
            if (sock == null) {
                sock = new java.net.Socket(JOptionPane.showInputDialog("Enter server IP address:"),
                        Integer.parseInt(messages.Messages.PORT.msg));
            }

            // create i/o streams
            out = new java.io.ObjectOutputStream(sock.getOutputStream());
            out.flush(); // required, otherwise client and server wait for each other
            in = new java.io.ObjectInputStream(sock.getInputStream());

            // get required data
            groups = (List<String>) in.readObject();
            genericPosts = (List<String>) in.readObject();
            genericNominees = (List<List<String>>) in.readObject();
            nonGenericPosts = (List<String>) in.readObject();
            nonGenericNominees = (List<List<List<String>>>) in.readObject();

            // the generic part of the options never changes
            for (int i = 0; i < genericNominees.size(); i++) {
                opts.add(genericNominees.get(i));
            }
        } catch (IOException ex) {
            System.err.println("Caught IOException: " + ex.getLocalizedMessage());
            System.exit(-2);
        } catch (ClassNotFoundException ex) {
            System.err.println("Caught ClassNotFoundException: " + ex.getLocalizedMessage());
            System.exit(-3);
        }
    }

    /**
     * Initializes current group and options.
     *
     * Called at the start of each voter's voting process, the method also keeps
     * track of the voter number and calls {@link #nextOptions()} to create the
     * initial buttons in the button panel.
     */
    private void initGroupAndOptions() {
        // suggest GC because each voter creates many anonymous buttons, layout
        // contraints, icons, etc.
        System.gc();
        try {
            // wait for message
            in.readObject();
            voterNum++;
            voterNumLabel.setText("Voter #" + voterNum);

            if (groups.size() > 0) {
                group = null;
                while (true) {
                    group = (String) JOptionPane.showInputDialog(this, "Voter #" + voterNum + ": Choose your house:",
                            "Choose House", JOptionPane.PLAIN_MESSAGE, null, groups.toArray(), "");
                    if (group == null) {
                        exit();
                    } else {
                        break;
                    }
                }
                out.writeObject(group);
            } else {
                out.writeObject(Messages.NO_GROUP.toString());
            }

            int groupIndex = groups.indexOf(group);
            for (int i = 0; i < nonGenericNominees.size(); i++) {
                opts.add(nonGenericNominees.get(i).get(groupIndex));
            }

            nextOptions();
        } catch (IOException ex) {
            System.err.println("Caught IOException: " + ex.getLocalizedMessage());
            System.exit(-2);
        } catch (ClassNotFoundException ex) {
            System.err.println("Caught ClassNotFoundException: " + ex.getLocalizedMessage());
            System.exit(-3);
        }
    }

    /**
     * Sets category and buttons according to current step.
     */
    private void nextOptions() {
        if (step < genericPosts.size()) {
            categoryLabel.setText(genericPosts.get(step));
        } else {
            categoryLabel.setText(group + " " + nonGenericPosts.get(step - genericPosts.size()));
        }

        buttonPanel.removeAll();
        List<String> curOpts = opts.get(step);
        int curSize = curOpts.size();

        for (int i = 0; i < curSize; i++) {
            String curNom = curOpts.get(i);
            // nominee symbols must be in the 'symbols' directory
            // if the nominee is John Doe, then the file should be named johndoe.png or johndoe.jpg
            String imgName = "";
            for (String s: curNom.split(" ")) {
                imgName += s.toLowerCase();
            }
            String curImg = "symbols/" + imgName;

            JButton jb = new NomineeButton(curNom, i);
            jb.setFocusPainted(false); // don't highlight last voter's choice!
            if ((new java.io.File(curImg + ".jpg")).exists()) {
                jb.setIcon(getScaledIcon(new ImageIcon(curImg + ".jpg").getImage(), 35, 35));
            } else if ((new java.io.File(curImg + ".png")).exists()) {
                jb.setIcon(getScaledIcon(new ImageIcon(curImg + ".png").getImage(), 35, 35));
            } else if ((new java.io.File(curImg + ".gif")).exists()) {
                jb.setIcon(getScaledIcon(new ImageIcon(curImg + ".gif").getImage(), 35, 35));
            }
            jb.setFont(new Font("SansSerif", Font.PLAIN, 20));

            jb.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {
                    vote(e);
                }
            });

            c = new GridBagConstraints();
            c.gridx = i % 2 + 1; // left side or right side? (+1 for glue space)
            c.gridy = i / 2; // row number
            // last button occupies entire row if odd number of nominees
            c.gridwidth = ((i == curSize - 1) && (curSize % 2 == 1))? 2: 1;
            c.gridheight = 1;
            c.fill = GridBagConstraints.NONE;
            if ((i == curSize - 1) && (curSize % 2 == 1)) {
                c.anchor = GridBagConstraints.CENTER; // last button if odd number
            } else if (i % 2 == 0) {
                c.anchor = GridBagConstraints.LINE_START;
            } else {
                c.anchor = GridBagConstraints.LINE_END;
            }
            c.insets = new Insets(2, 2, 2, 2);
            c.weightx = 0.15; // each button gets 15% of available horizontal space (see initFillers)
            c.weighty = 1.0;
            buttonPanel.add(jb, c);
        }

        initFillers(curSize);
        this.repaint();
        this.pack();
    }

    /**
     * Initializes fillers for the button panel.
     *
     * There is horizontal glue in the first and last columns (on both sides of
     * the buttons) and vertical glue in the last row (below the buttons).
     *
     * @param curSize number of nominees for the current step
     */
    private void initFillers(int curSize) {
        c = new GridBagConstraints();
        c.gridx = 0;
        c.gridy = 0;
        c.gridwidth = 1;
        c.gridheight = (curSize + 1)/2;
        c.weightx = 0.35; // glue gets 35% of available horizontal space
        c.weighty = 1.0;
        buttonPanel.add(Box.createHorizontalGlue(), c);

        c = new GridBagConstraints();
        c.gridx = 3;
        c.gridy = 0;
        c.gridwidth = 1;
        c.gridheight = (curSize + 1)/2;
        c.weightx = 0.35; // glue gets 35% of available horizontal space
        c.weighty = 1.0;
        buttonPanel.add(Box.createHorizontalGlue(), c);

        c = new GridBagConstraints();
        c.gridx = 0;
        c.gridy = (curSize + 1)/2;
        c.gridwidth = 4;
        c.gridheight = 1;
        c.weightx = 1.0;
        c.weighty = 1.6; // glue gets a vertical weight of 1.6 (compare to each button's 1.0)
        buttonPanel.add(Box.createVerticalGlue(), c);
    }

    /**
     * Confirms and exits the client.
     */
    private void exit() {
        if (JOptionPane.showConfirmDialog(this, "Exit application?", "Exit",
                JOptionPane.YES_NO_OPTION, JOptionPane.WARNING_MESSAGE) == JOptionPane.YES_OPTION) {
            try {
                out.writeObject(Messages.GOODBYE.toString()); // send goodbye to server
                in.close();
                out.close();
            } catch (IOException ex) {
                System.err.println("Caught IOException: " + ex.getLocalizedMessage());
            }
            System.exit(0);
        }
    }

    /**
     * Registers votes on button clicks.
     *
     * This method handles button clicks and conveys the corresponding vote to
     * the server. It also keeps track of the current step in each voter's
     * voting process and calls {@link #nextOptions()} and {@link
     * #initGroupAndOptions()} as needed.
     *
     * @param evt the {@link ActionEvent} that triggered the method call; is
     *            known to be a {@link NomineeButton}
     */
    private void vote(ActionEvent evt) {
        int choice = ((NomineeButton) evt.getSource()).getNum(); // which button?

        try {
            out.writeObject(Messages.VOTE + " " + choice); // send vote to server
        } catch (IOException ex) {
            System.err.println("Caught IOException: " + ex.getLocalizedMessage());
        }

        step++;
        // if end of voting sequence, reset; else next set of options
        if (step == genericPosts.size() + nonGenericPosts.size()) {
            step = 0;
            for (int i = genericPosts.size() + nonGenericPosts.size() - 1; i > genericPosts.size() - 1; i--) {
                opts.remove(i);
            }

            // buzzer
            EventQueue.invokeLater(new Runnable() {
                @Override
                public void run() {
                    bufferedPlay("/resources/buzzer.wav");
                }
            });
            while (true) {
                int opt = JOptionPane.showConfirmDialog(this, "Thank You! Your votes have been recorded. Next voter!",
                        "Next Voter", JOptionPane.OK_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE);
                if (opt == JOptionPane.OK_OPTION) {
                    initGroupAndOptions();
                    break;
                } else {
                    exit();
                }
            }
        } else {
            nextOptions();
        }
    }

    /**
     * Shows the license.
     */
    private void showLicense() {
        StringBuilder txt = new StringBuilder();
        try (java.io.BufferedReader br = new java.io.BufferedReader(new java.io.InputStreamReader(VoteClient.class.getResourceAsStream("/resources/COPYING")))) {
            String line = br.readLine();
            while (line != null) {
                txt.append(line);
                txt.append("\n");
                line = br.readLine();
            }
        } catch (IOException ex) {
            System.err.println(ex.getLocalizedMessage());
        }

        JTextArea lic = new JTextArea(txt.toString());
        JScrollPane scroller = new JScrollPane(lic, JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED,
                JScrollPane.HORIZONTAL_SCROLLBAR_NEVER);
        lic.setVisible(true);
        lic.setEditable(false);
        scroller.setVisible(true);
        JDialog licenseDialog = new JDialog(this, "VoteCounter License");
        licenseDialog.add(scroller);
        licenseDialog.setSize(600, 500);
        licenseDialog.setVisible(true);
    }

    /**
     * Shows credits.
     */
    private void showCredits() {
        // thank you, thank you! <bow to audience>
        JDialog aboutDialog = new JDialog(this, "About VoteCounter");
        String msg = "<html><center>VoteCounter: Java vote counting application<br />Copyright (C) 2012 - 2016 Shardul C.<br /><br />"
        + "Bugs, tips, suggestions, requests to<br />&lt;shardul.chiplunkar@gmail.com&gt.</center></html>";
        JLabel lbl = new JLabel(msg);
        lbl.setIcon(new ImageIcon(VoteClient.class.getResource("/resources/gpl-v3-logo.png")));
        lbl.setVisible(true);
        aboutDialog.add(lbl);
        aboutDialog.setSize(400, 150);
        aboutDialog.setVisible(true);
    }

    /**
     * The main method.
     *
     * This method sets the 'Nimbus' look and feel if possible, and creates a
     * new {@code VoteClient} form and makes it visible.
     *
     * @param args the command-line arguments (none needed)
     */
    public static void main(final String[] args) {
        //<editor-fold defaultstate="collapsed" desc="Set 'Nimbus' L&F (optional)">
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

        EventQueue.invokeLater(new Runnable() {
            @Override
            public void run() {
                new VoteClient(!(args.length > 0 && args[0].equalsIgnoreCase("--no-local"))).setVisible(true);
            }
        });
    }

    /**
     * Plays a sound file.
     * @param filePath the sound file to be played
     */
    private static void bufferedPlay(final String filePath) {
        try {
            AudioInputStream ais = AudioSystem.getAudioInputStream(VoteClient.class.getResource(filePath)); // get audio data stream
            DataLine.Info dataLineInfo = new DataLine.Info(SourceDataLine.class, ais.getFormat()); // get output line

            try (SourceDataLine srcLine = (SourceDataLine) AudioSystem.getLine(dataLineInfo)) {
                final int EXTERNAL_BUFFER_SIZE = 32768;
                final byte[] ABDATA = new byte[EXTERNAL_BUFFER_SIZE];
                int nBytesRead = 0;

                // initialize output line
                srcLine.open(ais.getFormat());
                srcLine.start();

                //continuously write a EXTERNAL_BUFFER_SIZE number of bytes to
                //the output until the file is over
                while (nBytesRead != -1) {
                    nBytesRead = ais.read(ABDATA, 0, ABDATA.length);
                    if (nBytesRead >= 0) {
                        srcLine.write(ABDATA, 0, nBytesRead);
                    }
                    if (Thread.interrupted()) {
                        break;
                    }
                }

                srcLine.drain();
                srcLine.stop();
            }

            //catch exceptions
        } catch (LineUnavailableException | IOException | UnsupportedAudioFileException ex) {
            System.err.printf("An exception occurred! " + ex.toString());
        } //end try-with-resources-catch
    }

    /**
     * Scales given image to given width and height.
     *
     * The code for this method is taken from {@link
     * http://stackoverflow.com/a/6714381/1846915}, written by Suken Shah.
     *
     * @param srcImg the {@link Image} to be scaled
     * @param w the new width
     * @param h the new height
     * @return the scaled {@link ImageIcon}
     */
    private static ImageIcon getScaledIcon(Image srcImg, int w, int h) {
        java.awt.image.BufferedImage resizedImg = new java.awt.image.BufferedImage(w, h, java.awt.image.BufferedImage.TYPE_INT_ARGB);
        Graphics2D g2 = resizedImg.createGraphics();

        g2.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BILINEAR);
        g2.drawImage(srcImg, 0, 0, w, h, null);
        g2.dispose();

        return (new ImageIcon(resizedImg));
    }

    /**
     * A custom subclass of {@link JButton} to represent nominees.
     *
     * The only special functionality implemented is the assignment of a
     * 'nominee number' to each button.
     */
    private static class NomineeButton extends JButton {
        private final int num;
        private static final long serialVersionUID = 1L;

        /**
         * Constructs a {@code NomineeButton}.
         * @param name the name/label of the button
         * @param i the number assigned to the button
         */
        public NomineeButton(String name, int i) {
            super(name);
            num = i;
        }

        /**
         * Gets the number.
         * @return the number associated with this button
         */
        public int getNum() {
            return num;
        }
    }
}
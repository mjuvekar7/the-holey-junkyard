package shapedesigner;

import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.KeyEvent;
import java.io.*;
import java.util.Scanner;
import javax.swing.*;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import javax.swing.filechooser.FileNameExtensionFilter;
import static shapedesigner.GridPanel.COLS;
import static shapedesigner.GridPanel.ROWS;

public class ShapeDesigner extends JFrame {

    private boolean isNamed = false;
    private GridPanel curGrid;
    private String curShape = "";
    private JTextArea codeArea;

    private int firstRow = -1;
    private int lastRow = -1;
    private int firstCol = -1;
    private int lastCol = -1;

    public static boolean isSaved = false;
    private static final long serialVersionUID = 1L;

    public ShapeDesigner() {
        setTitle("Untitled — GoD Shape Designer");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new BoxLayout(getContentPane(), BoxLayout.PAGE_AXIS));
        setResizable(false);
        initMenus();

        curGrid = new GridPanel();
        add(curGrid);

        codeArea = new JTextArea("Enter rules for shape here.", 10, 20);
        codeArea.setLineWrap(true);
        codeArea.setWrapStyleWord(true);
        JScrollPane codePane = new JScrollPane();
        codePane.setViewportView(codeArea);
        codeArea.getDocument().addDocumentListener(new DocumentListener() {
            @Override
            public void insertUpdate(DocumentEvent e) {

            }

            @Override
            public void removeUpdate(DocumentEvent e) {

            }

            @Override
            public void changedUpdate(DocumentEvent e) {
                
            }
        });
        codePane.setBorder(BorderFactory.createCompoundBorder(BorderFactory.createMatteBorder(
                0, 10, 10, 10, Color.WHITE), codePane.getBorder()));
        add(codePane);

        pack();
        setVisible(true);
    }

    private void initMenus() {
        JMenuBar mb = new JMenuBar();

        JMenu file = new JMenu("File");
        JMenuItem newShape = new JMenuItem("New");
        JMenuItem open = new JMenuItem("Open");
        JMenuItem save = new JMenuItem("Save");
        JMenuItem quit = new JMenuItem("Quit");

        newShape.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_N, ActionEvent.CTRL_MASK));
        open.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_O, ActionEvent.CTRL_MASK));
        save.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_S, ActionEvent.CTRL_MASK));
        quit.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_Q, ActionEvent.CTRL_MASK));

        newShape.addActionListener((ActionEvent e) -> {
            newShape();
        });

        open.addActionListener((ActionEvent e) -> {
            openShape();
        });

        save.addActionListener((ActionEvent e) -> {
            try {
                saveShape();
            } catch (IllegalArgumentException ex) {
                System.err.println("IllegalArgumentException in save!");
            }
        });

        quit.addActionListener((ActionEvent e) -> {
            try {
                if (!isSaved && (JOptionPane.showConfirmDialog(this, "Save current changes?", "Save Shape",
                        JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE) == JOptionPane.YES_OPTION)) {
                    saveShape();
                }
                System.exit(0);
            } catch (IllegalArgumentException ex) {
                System.err.println("IllegalArgumentException in save!");
            }

        });

        JMenu edit = new JMenu("Edit");
        JMenuItem change = new JMenuItem("Change initial bounds...");
        JMenuItem prefs = new JMenuItem("Preferences");

//        change.addActionListener((ActionEvent e) -> {
//            changeStart();
//        });
//
//        prefs.addActionListener((ActionEvent e) -> {
//
//        });

        file.add(newShape);
        file.add(open);
        file.add(save);
        file.add(quit);

        edit.add(change);
        edit.add(prefs);

        mb.add(file);
        mb.add(edit);

        setJMenuBar(mb);
    }

    private void checkSaved() {
        if (!isSaved && (JOptionPane.showConfirmDialog(this, "Save current changes?", "Save Shape",
                JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE) == JOptionPane.YES_OPTION)) {
            try {
                saveShape();
                isSaved = true;
            } catch (IllegalArgumentException ex) {
                System.err.println("IllegalArgumentException in save!");
            }
        }
    }

    private void newShape() {
        checkSaved();

        isSaved = false;
        isNamed = false;
        setTitle("Untitled — GoD Shape Designer");
        remove(curGrid);
        curGrid = new GridPanel();
        add(curGrid);
        pack();
    }

    private void openShape() {
        checkSaved();

        JFileChooser fc = new JFileChooser();
        fc.setCurrentDirectory(new File(System.getProperty("user.home")));
        fc.setFileFilter(new FileNameExtensionFilter("GoD shape files (*.god)", "god"));
        int result = fc.showOpenDialog(this);
        if (result == JFileChooser.APPROVE_OPTION) {
            File selectedFile = fc.getSelectedFile();
            setTitle(selectedFile.getName().substring(0, selectedFile.getName().length() - 4) + " — GoD Shape Designer");
            isNamed = true;
            isSaved = true;
            remove(curGrid);

            int i;
            int j;
            boolean[][] lits = new boolean[ROWS][COLS];
            try (Scanner sc = new Scanner(selectedFile)) {
                int startRow = sc.nextInt();
                i = startRow;
                j = sc.nextInt();
                while (sc.hasNextInt()) {
                    int next = sc.nextInt();
                    if (next == 2) {
                        i = startRow;
                        j++;
                        continue;
                    }
                    lits[i++][j] = (next == 1);
                }
            } catch (FileNotFoundException ex) {
                System.err.println("File to be opened not found in open!");
            }

            curGrid = new GridPanel(lits, ROWS, COLS);
            add(curGrid);
            pack();
        }
    }

    private void saveShape() throws IllegalArgumentException {
        getFirstLastRowsCols();
        if (!isNamed) {
            curShape = JOptionPane.showInputDialog(this, "Enter name for shape:",
                    "Shape Name", JOptionPane.QUESTION_MESSAGE);
            isNamed = true;
        }
        File f = new File(curShape + ".god");

        StringBuilder backup = new StringBuilder();
        try (Scanner sc = new Scanner(f)) {
            while (sc.hasNextLine()) {
                backup.append(sc.nextLine());
                backup.append("\n");
            }
        } catch (FileNotFoundException ex) {
            System.err.println("File not found for backup!");
        }

        try (FileWriter fw = new FileWriter(f)) {
            fw.write(Integer.toString(firstRow) + " " + Integer.toString(firstCol) + "\n");
            if ((firstRow == lastRow) && (firstCol == lastCol)) {
                fw.write("1 ");
            } else {
                for (int i = firstRow; i <= lastRow; i++) {
                    for (int j = firstCol; j <= lastCol; j++) {
                        if (curGrid.lits[i][j]) {
                            if ((i > 0) && (curGrid.lits[i - 1][j] || curGrid.lits[i + 1][j])) {
                                fw.write("1 ");
                                continue;
                            } else if (curGrid.lits[i + 1][j]) {
                                fw.write("1 ");
                                continue;
                            }

                            if ((j > 0) && (curGrid.lits[i][j - 1] || curGrid.lits[i][j + 1])) {
                                fw.write("1 ");
                                continue;
                            } else if (curGrid.lits[i][j + 1]) {
                                fw.write("1 ");
                                continue;
                            }

                            JOptionPane.showMessageDialog(this, "Invalid Shape (discontinuous)!",
                                    "Invalid Shape", JOptionPane.ERROR_MESSAGE);
                            fw.write(backup.toString());
                            throw new IllegalArgumentException("Dicontinuous shape");
                        } else {
                            fw.write("0 ");
                        }
                    }
                    fw.write("2\n");
                }
            }
            JOptionPane.showMessageDialog(this, "Shape saved successfully", "Save Successful",
                    JOptionPane.INFORMATION_MESSAGE);
            isSaved = true;
            setTitle(curShape + " — GoD Shape Designer");
        } catch (IOException ex) {
            System.err.println("IOException in save!");
        }
    }

    private void getFirstLastRowsCols() {
        for (int i = 0; i < ROWS; i++) {
            for (int j = 0; j < COLS; j++) {
                if (curGrid.lits[i][j]) {
                    firstRow = i;
                    break;
                }
            }
            if (firstRow >= 0) {
                break;
            }
        }

        for (int i = 0; i < COLS; i++) {
            for (int j = 0; j < ROWS; j++) {
                if (curGrid.lits[j][i]) {
                    firstCol = i;
                    break;
                }
            }
            if (firstCol >= 0) {
                break;
            }
        }

        for (int i = ROWS - 1; i >= 0; i--) {
            for (int j = 0; j < COLS; j++) {
                if (curGrid.lits[i][j]) {
                    lastRow = i;
                    break;
                }
            }
            if (lastRow >= 0) {
                break;
            }
        }

        for (int i = COLS - 1; i >= 0; i--) {
            for (int j = 0; j < ROWS; j++) {
                if (curGrid.lits[j][i]) {
                    lastCol = i;
                    break;
                }
            }
            if (lastCol >= 0) {
                break;
            }
        }
    }

//<editor-fold defaultstate="collapsed" desc="not implemented yet">
/*    private void changeStart() {
        checkSaved();

        int newRow = firstRow;
        boolean valid = false;
        while (!valid) {
            try {
                String row = JOptionPane.showInputDialog(this, "Enter new starting row:");
                if (row == null || row.length() == 0) {
                    return;
                }
                newRow = Integer.parseInt(row);
                if (newRow < 0 || newRow >= ROWS) {
                    throw new NumberFormatException();
                }
                valid = true;
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Please enter a number between 0 and " + ROWS + "!", "Invalid Input", JOptionPane.WARNING_MESSAGE);
            }
        }

        try (RandomAccessFile raf = new RandomAccessFile(curShape + ".god", "rw")) {
            raf.seek(0);
            raf.writeChars(Integer.toString(newRow));
        } catch (IOException ex) {
            System.err.println("IOException in changeStart!");
        }

        remove(curGrid);

        int i;
        int j;
        boolean[][] lits = new boolean[ROWS][COLS];
        Scanner sc = new Scanner(curShape + ".god");
        int startRow = sc.nextInt();
        i = startRow;
        j = sc.nextInt();
        while (sc.hasNextInt()) {
            int next = sc.nextInt();
            if (next == 2) {
                i = startRow;
                j++;
                continue;
            }
            lits[i++][j] = (next == 1);
        }

        curGrid = new GridPanel(lits, ROWS, COLS);
        add(curGrid);
        pack();
    }*/
//</editor-fold>

    public static void main(String[] args) {
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
            System.err.println("Exception in L&F code!");
        }
        //</editor-fold>

        java.awt.EventQueue.invokeLater(() -> {
            new ShapeDesigner();
        });
    }
}

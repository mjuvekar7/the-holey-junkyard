package shapedesigner;

import java.awt.event.ActionEvent;
import java.awt.event.KeyEvent;
import java.io.*;
import java.util.Scanner;
import javax.swing.*;
import javax.swing.filechooser.FileNameExtensionFilter;
import static shapedesigner.GridPanel.COLS;
import static shapedesigner.GridPanel.ROWS;

/**
 *
 * @author Mandar J.
 */
public class ShapeDesigner extends JFrame {

    private GridPanel curGrid;
    public static boolean isSaved = false;

    private static int firstRow = -1;
    private static int lastRow = -1;
    private static int firstCol = -1;
    private static int lastCol = -1;

    private static boolean isNamed = false;
    private static String curShape = "";

    private static final long serialVersionUID = 1L;

    public ShapeDesigner() {
        setTitle("Untitled — GoD Shape Designer");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setResizable(false);
        initMenus();

        curGrid = new GridPanel();
        add(curGrid);
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
        JMenuItem setBounds = new JMenuItem("Change bounds...");
        JMenuItem prefs = new JMenuItem("Preferences");

        setBounds.addActionListener((ActionEvent e) -> {
            changeBounds();
        });

        prefs.addActionListener((ActionEvent e) -> {

        });

        file.add(newShape);
        file.add(open);
        file.add(save);
        file.add(quit);

        edit.add(setBounds);
        edit.add(prefs);

        mb.add(file);
        mb.add(edit);

        setJMenuBar(mb);
    }

    private void newShape() {
        if (!isSaved && (JOptionPane.showConfirmDialog(this, "Save current changes?", "Save Shape",
                JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE) == JOptionPane.YES_OPTION)) {
            try {
                saveShape();
            } catch (IllegalArgumentException ex) {
                System.err.println("IllegalArgumentException in save!");
            }
        }

        isSaved = false;
        isNamed = false;
        setTitle("Untitled — GoD Shape Designer");
        remove(curGrid);
        curGrid = new GridPanel();
        add(curGrid);
        pack();
    }

    private void openShape() {
        if (!isSaved && (JOptionPane.showConfirmDialog(this, "Save current changes?", "Save Shape",
                JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE) == JOptionPane.YES_OPTION)) {
            try {
                saveShape();
            } catch (IllegalArgumentException ex) {
                System.err.println("IllegalArgumentException in save!");
            }
            isSaved = true;
        }

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

    private void changeBounds() {
        int newRow;
        boolean valid = false;
        while (!valid) {
            try {
                newRow = Integer.parseInt(JOptionPane.showInputDialog(this, "Enter new starting row:"));
                valid = true;
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Please enter a number!", "Invalid Input", JOptionPane.WARNING_MESSAGE);
            }
        }
        
    }

    public static void main(String[] args) {
        java.awt.EventQueue.invokeLater(() -> {
            new ShapeDesigner();
        });
    }
}

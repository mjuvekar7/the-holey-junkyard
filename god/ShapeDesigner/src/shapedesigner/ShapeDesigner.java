package shapedesigner;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.KeyStroke;
import javax.swing.filechooser.FileNameExtensionFilter;
import static shapedesigner.GridPanel.*;

/**
 *
 * @author Mandar J.
 */
public class ShapeDesigner extends JFrame {

    private static int firstRow = -1;
    private static int lastRow = -1;
    private static int firstCol = -1;
    private static int lastCol = -1;

    public static boolean isSaved = false;
    private static boolean isNamed = false;
    private static String curShape = "";

    private GridPanel curGrid;

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        java.awt.EventQueue.invokeLater(() -> {
            new ShapeDesigner();
        });
    }

    public ShapeDesigner() {
        setTitle("Untitled — GoD Shape Designer");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setResizable(false);

        JMenuBar mb = new JMenuBar();
        JMenu file = new JMenu("File");
        JMenuItem new_shape = new JMenuItem("New");
        JMenuItem open = new JMenuItem("Open");
        JMenuItem save = new JMenuItem("Save");

        new_shape.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_N, ActionEvent.CTRL_MASK));
        open.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_O, ActionEvent.CTRL_MASK));
        save.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_S, ActionEvent.CTRL_MASK));

        new_shape.addActionListener((ActionEvent e) -> {
            newShape();
        });

        open.addActionListener((ActionEvent e) -> {
            openShape();
        });

        save.addActionListener((ActionEvent e) -> {
            try {
                saveShape();
            } catch (IllegalArgumentException ex) {
                System.err.println("IllegalArgumentException in save!!");
            }
        });

        file.add(new_shape);
        file.add(open);
        file.add(save);
        mb.add(file);

        setJMenuBar(mb);
        curGrid = new GridPanel();
        add(curGrid);
        pack();

        setVisible(true);
    }

    public void saveShape() throws IllegalArgumentException {
        getFirstLastRowsCols();
        if (!isNamed) {
            curShape = JOptionPane.showInputDialog(this, "Enter name for shape:", "Shape Name", JOptionPane.QUESTION_MESSAGE);
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
            System.err.println("File not found for backup!!");
        }

        try (FileWriter fw = new FileWriter(f)) {
            if ((firstRow == lastRow) && (firstCol == lastCol)) {
                fw.write("1 ");
            } else {
                for (int i = firstRow; i <= lastRow; i++) {
                    for (int j = firstCol; j <= lastCol; j++) {
                        if (curGrid.lits[i][j]) {
                            if (i > 0) {
                                if (curGrid.lits[i - 1][j] || curGrid.lits[i + 1][j]) {
                                    fw.write("1 ");
                                    continue;
                                }
                            } else {
                                if (curGrid.lits[i + 1][j]) {
                                    fw.write("1 ");
                                    continue;
                                }
                            }
                            if (j > 0) {
                                if (curGrid.lits[i][j - 1] || curGrid.lits[i][j + 1]) {
                                    fw.write("1 ");
                                    continue;
                                }
                            } else {
                                if (curGrid.lits[i][j + 1]) {
                                    fw.write("1 ");
                                    continue;
                                }
                            }
                            JOptionPane.showMessageDialog(this, "Invalid Shape (discontinuous)!", "Invalid Shape", JOptionPane.ERROR_MESSAGE);
                            fw.write(backup.toString());
                            throw new IllegalArgumentException("Dicontinuous shape");
                        } else {
                            fw.write("0 ");
                        }
                    }
                    fw.write("\n");
                }
            }
            JOptionPane.showMessageDialog(this, "Shape saved successfully", "Save Successful", JOptionPane.INFORMATION_MESSAGE);
            isSaved = true;
            setTitle(curShape + " — GoD Shape Designer");
        } catch (IOException ex) {
            System.err.println("IOException in save!!");
        }
    }

    private void newShape() {
        if (!isSaved && (JOptionPane.showConfirmDialog(this, "Save current changes?", "Save Shape", JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE) == JOptionPane.YES_OPTION)) {
            try {
                saveShape();
            } catch (IllegalArgumentException ex) {
                System.err.println("IllegalArgumentException in save!!");
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
        if (!isSaved && (JOptionPane.showConfirmDialog(this, "Save current changes?", "Save Shape", JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE) == JOptionPane.YES_OPTION)) {
            try {
                saveShape();
            } catch (IllegalArgumentException ex) {
                System.err.println("IllegalArgumentException in save!!");
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
            curGrid = new GridPanel();

            // read file, set curGrid's lits
            add(curGrid);
            pack();
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
}

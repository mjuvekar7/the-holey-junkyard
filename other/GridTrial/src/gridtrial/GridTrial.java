/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package gridtrial;

/**
 *
 * @author shardul
 */
public class GridTrial extends javax.swing.JFrame {

    private static final long serialVersionUID = 1L;

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            @Override
            public void run() {
                new GridTrial();
            }
        });
    }

    public GridTrial() {
        setTitle("GridTrial");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setResizable(false);

        add(new GridPanel());
        pack();

        setVisible(true);
    }
}

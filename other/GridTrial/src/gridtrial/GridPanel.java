package gridtrial;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.GridLayout;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import javax.swing.BorderFactory;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.border.Border;

class GridPanel extends JPanel {

    private static final long serialVersionUID = 1L;
    private static int ROWS = 20;
    private static int COLS = 20;

    private static Color offColor = new Color(240, 240, 240);
    private static Color onColor = new Color(255, 250, 30);

    public GridPanel() {
        setBorder(BorderFactory.createLineBorder(Color.WHITE, 10));
        GridLayout gl = new GridLayout(ROWS, COLS);
        setLayout(gl);
        addGridCells();

        setVisible(true);
    }

    private void addGridCells() {
        for (int i = 0; i < ROWS; i++) {
            for (int j = 0; j < COLS; j++) {
                JLabel jl = new JLabel("");
                jl.setOpaque(true);
                jl.setBackground(offColor);
                jl.setVisible(true);

                Border border;
                if (i < ROWS - 1) {
                    if (j < COLS - 1) {
                        border = BorderFactory.createMatteBorder(1, 1, 0, 0, Color.LIGHT_GRAY);
                    } else {
                        border = BorderFactory.createMatteBorder(1, 1, 0, 1, Color.LIGHT_GRAY);
                    }
                } else {
                    if (j < COLS - 1) {
                        border = BorderFactory.createMatteBorder(1, 1, 1, 0, Color.LIGHT_GRAY);
                    } else {
                        border = BorderFactory.createMatteBorder(1, 1, 1, 1, Color.LIGHT_GRAY);
                    }
                }
                jl.setBorder(border);
                jl.addMouseListener(new MouseAdapter() {
                    @Override
                    public void mouseClicked(MouseEvent evt) {
                        cellClicked(evt);
                    }
                });
                add(jl);
            }
        }
    }

    @Override
    public Dimension getPreferredSize() {
        return new Dimension(600, 600);
    }

    private void cellClicked(MouseEvent evt) {
        JLabel cur = (JLabel) evt.getSource();
        if (cur.getBackground() == offColor) {
            cur.setBackground(onColor);
        } else {
            cur.setBackground(offColor);
        }
    }
}
package shapedesigner;

import javax.swing.JLabel;

/**
 *
 * @author Mandar J.
 */
public class GridCell extends JLabel {
    public int x;
    public int y;
    
    public GridCell(int x, int y) {
        super("");
        this.x = x;
        this.y = y;
    }
}

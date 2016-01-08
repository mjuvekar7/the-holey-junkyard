/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package checkpoint;

import java.util.ArrayList;
import javax.swing.JOptionPane;

/**
 *
 * @author Administrator
 */
public class Checkpoint extends javax.swing.JFrame {

    private static ArrayList<Integer> checkpoints = new ArrayList<>();
    private static int DEBUG_CONST = 1000;
    
    /**
     * Creates new form Checkpoint
     */
    public Checkpoint() {
        initComponents();
    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        enterChecksLabel = new javax.swing.JLabel();
        addField = new javax.swing.JTextField();
        addButton = new javax.swing.JButton();
        checkpointsScrollPane = new javax.swing.JScrollPane();
        checkpointsArea = new javax.swing.JTextArea();
        startButton = new javax.swing.JButton();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);

        enterChecksLabel.setFont(new java.awt.Font("Times New Roman", 0, 14)); // NOI18N
        enterChecksLabel.setText("Enter checkpoint times: (in minutes)");

        addField.setFont(new java.awt.Font("Times New Roman", 0, 14)); // NOI18N
        addField.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                addFieldActionPerformed(evt);
            }
        });

        addButton.setFont(new java.awt.Font("Times New Roman", 0, 14)); // NOI18N
        addButton.setText("Add");
        addButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                addButtonActionPerformed(evt);
            }
        });

        checkpointsArea.setColumns(20);
        checkpointsArea.setFont(new java.awt.Font("Times New Roman", 0, 14)); // NOI18N
        checkpointsArea.setLineWrap(true);
        checkpointsArea.setRows(5);
        checkpointsArea.setEnabled(false);
        checkpointsScrollPane.setViewportView(checkpointsArea);

        startButton.setFont(new java.awt.Font("Times New Roman", 0, 14)); // NOI18N
        startButton.setText("Start");
        startButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                startButtonActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(checkpointsScrollPane)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(addField)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(addButton, javax.swing.GroupLayout.PREFERRED_SIZE, 75, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(enterChecksLabel)
                        .addGap(0, 0, Short.MAX_VALUE))
                    .addGroup(layout.createSequentialGroup()
                        .addGap(148, 148, 148)
                        .addComponent(startButton, javax.swing.GroupLayout.DEFAULT_SIZE, 84, Short.MAX_VALUE)
                        .addGap(148, 148, 148)))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(enterChecksLabel)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(addButton)
                    .addComponent(addField, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(checkpointsScrollPane, javax.swing.GroupLayout.DEFAULT_SIZE, 102, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(startButton)
                .addContainerGap())
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private static void commenceEmergencySequence49131 (int check) {
        // TODO: play l.o.l sound here
    }
    
    private void addButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_addButtonActionPerformed
        try {
            int mints = Integer.parseInt(addField.getText());
            if (mints <= 0) {
                JOptionPane.showMessageDialog(this, "Positive numbers only!", "Invalid Input", JOptionPane.WARNING_MESSAGE);
                return;
            }
            checkpoints.add(mints);
            checkpointsArea.append("Checkpoint #" + checkpoints.size() + ": " + addField.getText() + " minutes \n");
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "Please enter numbers only!", "Invalid Input", JOptionPane.WARNING_MESSAGE);
        } finally {
            addField.setText("");
        }
    }//GEN-LAST:event_addButtonActionPerformed

    private void startButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_startButtonActionPerformed
        this.setVisible(false);
        for (int i = 0; i < checkpoints.size(); i++) {
            try {
                Thread.sleep(checkpoints.get(i)*DEBUG_CONST);
                int opt = JOptionPane.showConfirmDialog(this, "Have you reached Checkpoint #" + (i + 1), "Confirm Checkpoint", JOptionPane.YES_NO_OPTION);
                if (opt == 1) {
                    commenceEmergencySequence49131(i);
                    System.exit(1); 
                }
            } catch (InterruptedException ex) {
                System.err.println("Interrupted!");
            }
        }
        System.exit(0);
    }//GEN-LAST:event_startButtonActionPerformed

    private void addFieldActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_addFieldActionPerformed
        addButtonActionPerformed(evt);
    }//GEN-LAST:event_addFieldActionPerformed

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
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(Checkpoint.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(Checkpoint.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(Checkpoint.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(Checkpoint.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new Checkpoint().setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton addButton;
    private javax.swing.JTextField addField;
    private javax.swing.JTextArea checkpointsArea;
    private javax.swing.JScrollPane checkpointsScrollPane;
    private javax.swing.JLabel enterChecksLabel;
    private javax.swing.JButton startButton;
    // End of variables declaration//GEN-END:variables
}

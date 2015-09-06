import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.io.IOException;

public class GameLauncher {
	private static JFrame frame;
	private static JPanel panel;

	private static void createGUI() {
		// create window
		frame = new JFrame("GameLauncher");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setSize(100,100);

		// add launch button
		JButton button = new JButton("LAUNCH!");
		button.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				launchGame();
			}
		});

		panel = new JPanel();
      	panel.setLayout(new FlowLayout());
      	panel.add(button);
      	frame.add(panel);
      	frame.setVisible(true);
	}

	private static void launchGame() {
		try {
		String command = "python game_gui.pyw";
		Process p = Runtime.getRuntime().exec(command);
		} catch(IOException e) {}
		frame.setVisible(false);
		frame.dispose();
		System.exit(0);
	}

	public static void main(String[] args) {
		createGUI();
	}
}
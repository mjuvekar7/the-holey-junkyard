package sources;

import java.io.IOException;

/**
 * @author fazerlicourice7, shardulc, mandarj
 */
public class Trash {
   
    private static java.io.BufferedReader br;
    
    private static void check() throws IOException {
        System.out.println("Enter the name of the item you want to throw away:");
        String item = br.readLine().toLowerCase();
        
        if (item.contains("plastic")){
            System.out.println("You can either recycle plastic, or reuse it at home!");
            System.out.println("Examples include reusing bottles, jars, carry-bags, " +
                    "and packaging for many purposes.");
            System.out.println("For more information, refer to - http://en.wikipedia.org/wiki/Plastic_recycling");
        } else if (item.contains("leftovers") || item.contains("peel")) {
            System.out.println("You can create a compost pit to recycle all wet garbage.");
            System.out.println("Do you want to create a compost pit? [y/n]");
            String input = br.readLine().toLowerCase();
            while (!(input.equals("y") || input.equals("n"))) {
                System.out.println("Please enter y or n");
                input = br.readLine().toLowerCase();
            }
            if (input.equals("y")){
                compost_pit();
            }
        } else if (item.contains("tin") || item.contains("aluminium") || item.contains("metal")) {
            System.out.println("All metals can be recycled by sending them to the junkyard.");
            System.out.println("For more information, visit - http://www.wikihow.com/Recycle-Metals");
        } else if (item.contains("paper")){
            System.out.println("All used paper can be recycled by taking it to " +
                    "the local 'raddiwala' or paper collector.");
            System.out.println("You can also reuse the used paper to make origami, paper maché and much more!");
            System.out.println("You can also make recycled paper at home. For more information, visit -");
            System.out.println("http://www.arvindguptatoys.com/arvindgupta/origamiforeveryone.pdf");
            System.out.println("http://www.earth911.com/living-well-being/events-entertainement/recycle-your-own-paper/");
        } else if (item.contains("electronic") || item.contains("phone") || item.contains("computer")) {
            System.out.println("Electronic waste can be collected right from your doorstep!");
            System.out.println("Just submit an application with EWasteClient.");
        } else {
            System.out.println("Sorry, I don't know about this item!");
        }
    }

    private static void compost_pit() throws IOException {
        System.out.println("What size would you like your compost pit to be? [h/s]:");
        System.out.println("Enter h for a household, s for a society.");
        String input = br.readLine();

        while (!(input.toLowerCase().equals("h") || input.toLowerCase().equals("s"))) {
            System.out.println("Please enter h or s:");
            input = br.readLine();
        }
        if (input.equals("h")) {
            System.out.println("You will need the following components:");
            System.out.println("1. A suitable container with a lid, "
                    + "at least 3 feet deep and 2 feet in diameter "
                    + "with at least 2 sides made of wire mesh to ensure aeration. "
                    + "The bottom of the container should have holes "
                    + "so that the water can drain out.");
            System.out.println("Price: 500 to 800/-");
            System.out.println("2. Vermiculture (earthworms) are optional "
                    + "but they improve the quality of compost.");
            System.out.println("Price: about 100/-");
            System.out.println("3. Soil which is a mixture of clayey and sandy soil "
                    + "in approximately a 50/50 division.");
            System.out.println("Price: around 300/- for a moderately big container.");
            System.out.println("After a minimum of 2 months, you can start removing "
                    + "compost from a depth of at least 10 inches.");
        } else if (input.equals("s")) {
            System.out.println("You will need the following components:");
            System.out.println("1. A suitable container with a lid, "
                    + "around 5 feet deep and 7 feet in diameter "
                    + "with at least 2 sides made of wire mesh to ensure aeration. "
                    + "The bottom of the container should have holes "
                    + "so that the water can drain out.");
            System.out.println("Price: 1500 to 2000/-");
            System.out.println("2. Vermiculture (earthworms) and bacteria culture.");
            System.out.println("Price: about 400/-");
            System.out.println("3. Soil which is a mixture of clayey and sandy soil "
                    + "in approximately a 50/50 division.");
            System.out.println("Price: around 4000/- for a moderately big container.");
            System.out.println("After a minimum of 2 months, you can start removing "
                    + "compost from a depth of at least 10 inches.");
            System.out.println("To get to know more about compost, refer to - http://en.wikipedia.org/wiki/Compost");
            System.out.println("For an illustrated guide to making compost pits, refer to - http://www.wikihow.com/Make-a-Compost-Pit");
        }
    }
    
    public static void main (String args[]) {
        try {
            br = new java.io.BufferedReader(new java.io.InputStreamReader(System.in));
            check();
        } catch (IOException ex) {
            System.err.println("An IOException occurred: " + ex.getMessage());
        }
    }
}

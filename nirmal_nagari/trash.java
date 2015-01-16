package Smarty_Clear;
import java.io.*;
import java.util.*;
/**
 * @author fazer
 */
public class trash {
   BufferedReader hi = new BufferedReader (new InputStreamReader(System.in)); 
   String Item, input;
   ArrayList part = new ArrayList(Arrays.asList(Item));
   private void check()throws IOException {
       trash obj = new trash();
       System.out.println("Enter the name of the item you want to throw away.");
       Item = hi.readLine();
       List<String> part = Arrays.asList(Item.split(" "));
       if(part.contains("plastic")){
           System.out.println("You can recycle all forms of plastic, by sending it to your community's recyclables collectors.");
       }
       else if (part.contains("peel")){
           System.out.println("You can create a compost pit to recycle all biological waste.");
           System.out.println("Do you want to create a compost pit? [y/n]");
           input = hi.readLine();
           if(input.equals("y")){
               obj.compost_pit();    
           }
       }
       else if (part.contains("leftovers")){
           System.out.println("You can create a compost pit to recycle all biological waste.");
           System.out.println("Do you want to create a compost pit? [y/n]");
           input = hi.readLine();
           if(input.equals("y")){
               obj.compost_pit();    
           }
       }
       else if(part.contains("metal")){
           System.out.println("All metals can be recycled by sending them to the junkyard.");
       }
       else if(part.contains("tin")){
           System.out.println("All metals can be recycled by sending them to the junkyard.");
       }
       else if(part.contains("aluminium")){
           System.out.println("All metals can be recycled by sending them to the junkyard.");
       }
       else if(part.contains("paper")){
           System.out.println("All used paper can be recycled by taking it to the local 'raddiwala' or paper collector.");
       }
       else if(part.contains("computer")) {
           System.out.println("All electronic waste can be recycled by donating them to E-Parisara. Contact them here :  recycle@ewasteindia.com ");
       }
       else if(part.contains("phone")) {
           System.out.println("All electronic waste can be recycled by donating them to E-Parisara. Contact them here :  recycle@ewasteindia.com ");
       }
       else if(part.contains("electronics")) {
           System.out.println("All electronic waste can be recycled by donating them to E-Parisara. Contact them here :  recycle@ewasteindia.com ");
       }
       else if(part.contains("pcb")||part.contains("PCB")) {
           System.out.println("All electronic waste can be recycled by donating them to E-Parisara. Contact them here :  recycle@ewasteindia.com ");
       }
   }
   private void compost_pit()throws IOException{
       trash obj = new trash();
       System.out.println("What size would you like your compost pit to be? [h/s]" +"\n" +"For a household" +"\n" +"For a society");
       input = hi.readLine();
       if(input.equals("h")){
           System.out.println("You will need the following components:");
           System.out.println("1. A suitable container with a lid, at least 3 feet deep and 2 feet in diameter with at least 2 sides made of wire mesh to ensure aeration. The bottom of the container should have holes so that the water can drain out.");
           System.out.println("Price: 500 to 800/-");
           System.out.println("2. Earthworms or regular worms to ensure decomposition of garbage.[Optional]");
           System.out.println("Price: 200/- per 100g of worms");
           System.out.println("3. Soil, half of which should be clayey soil & half of which should be sandey soil");
           System.out.println("Price: 400/- per 100 cubic centimetres & 330/- per 100 cubic centimeters");
           System.out.println("\n" +"After a minimum of 2 months, you can remove the compost from a depth of at least 10 inches.");
       }
       else if(input.equals("s")){
           System.out.println("You will need the following components:");
           System.out.println("1. A suitable container with a lid, around 5 feet deep and 7 feet in diameter with at least 2 sides made of wire mesh to ensure aeration. The bottom of the container should have holes so that the water can drain out.");
           System.out.println("Price: 1500 to 2000/-");
           System.out.println("2. Earthworms or regular worms along with specific bacteria to ensure decomposition of garbage.");
           System.out.println("Price: 2000/- per 1Kg of worms &  ");
           System.out.println("3. Soil, half of which should be clayey soil & half of which should be sandey soil");
           System.out.println("Price: 4000/- per cubic metre & 3300/- per cubic metre");
           System.out.println("\n" +"After a minimum of 3 months, you can remove the compost from a depth of at least 1.5 feet.");
       }
       else {
           System.out.println("Invalid input!");
           obj.compost_pit();
       }
   }
   public static void main(String args[])throws IOException{
       trash obj = new trash();
       obj.check();
   }
}

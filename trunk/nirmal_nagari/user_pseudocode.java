/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Smarty_Clear;
import java.io.*;
import java.util.ArrayList;
import java.nio.file.*;
/**
 *
 * @author fazer
 */
public class user_pseudocode {
    BufferedReader hi = new BufferedReader(new InputStreamReader (System.in));
    ArrayList name = new ArrayList(), balance = new ArrayList();
    String line;
    private void check()throws IOException { 
       System.out.println("Enter your name.");
       String input = hi.readLine();
       Path path = Paths.get("/home/fazer/Documents/database_smarty_clearist");
       try(InputStream in = Files.newInputStream(path);
           BufferedReader reader = new BufferedReader(new InputStreamReader(in))) {
           while((line = reader.readLine()) != null){
               String[] parts = line.split(" ");
               name.add(parts[0]);
               balance.add(parts[1]);
           }
       } 
       catch(IOException x) {
           System.err.println(x);        
       }
       if(name.contains(input)){
           int position = name.indexOf(input);
           System.out.println("Balance in your account is " +balance.get(position));
       }     
       else{
           System.out.println("You do not have an account, please contact the mayor of your town to create one.");
       }
    }
    public static void main(String args[])throws IOException {
        user_pseudocode obj = new user_pseudocode();
        obj.check();
    }
    
}

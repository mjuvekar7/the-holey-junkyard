package Smarty_Clear;

import java.io.*;
import java.nio.file.*;
import static java.nio.file.StandardOpenOption.*;
import java.util.ArrayList;
/**
 * @author fazer
 */
public class manager_pseudocode {
    BufferedReader hi = new BufferedReader(new InputStreamReader(System.in));
    ArrayList name = new ArrayList(), balance = new ArrayList();
    String input, Input, line, FINAL, CURRENT;
    int toBeAdded, current, Final;
    private void add()throws IOException {
        System.out.println("Enter name and amount of clean currency to be added to the corresponding name.");
        Input = hi.readLine();
        input = hi.readLine();
        toBeAdded = Integer.parseInt(input);
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
        if(name.contains(Input)){
            int position = name.indexOf(Input);
            CURRENT = (String) balance.get(position);
            current = Integer.parseInt(CURRENT);
            Final = current + toBeAdded;
            FINAL = Integer.toString(Final);
            balance.remove(position);
            balance.add(position, FINAL);
        }
        else{
            name.add(Input);
            balance.add(toBeAdded);
        }
        for(int i = 0; i < name.size(); i++){
            line = name.get(i) + " " + balance.get(i);
            byte[] liness = line.getBytes();
            System.out.println(line);
            try (OutputStream out = new BufferedOutputStream(Files.newOutputStream(path, WRITE, APPEND))){ // parameter 'WRITE' doesn't work. Find out why!
                out.write(liness); //while creating new entry: replaces all previous information with new entry. If appending already existing entry, then works fine.
            }
            catch (IOException x){
                System.err.println(x);
            }
        }
    }
    public static void main(String[] args)throws IOException{
        manager_pseudocode obj = new manager_pseudocode();
        obj.add();
    }
}

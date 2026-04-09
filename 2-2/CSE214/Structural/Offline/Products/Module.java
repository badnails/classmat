package Products;
import java.util.ArrayList;

import Core.Core;

public class Module implements Core {
    String name;
    ArrayList<Course> courses = new ArrayList<>();

    public Module(String name) {
        this.name = name;
    }

    public void addCourse(Course course) {
        courses.add(course);
    }

    @Override
    public float getDuration() {
        float duration = 0;
        for(Course c: courses){
            duration+=c.getDuration();
        }
        return duration;
    }

    @Override
    public float calculatePrice() {
        float price = 0;
        for(Course c: courses){
            price+=c.calculatePrice();
        }
        return price;
    }

    @Override
    public void print() {
        System.out.println("Module: " + name + ", Duration: " + getDuration() + " hours, Price: $" + calculatePrice());
        for(Course c: courses){
            System.out.print(" |_ ");
            c.print();
            System.out.println();
        }
    }
    
}

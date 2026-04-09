package Products;
import java.util.ArrayList;

import Core.Core;

public class Course implements Core {
    String name;
    ArrayList<Lesson> lessons = new ArrayList<>();

    public Course(String name) {
        this.name = name;
    }

    public void addLesson(Lesson lesson) {
        lessons.add(lesson);
    }

    @Override
    public float getDuration() {
        float duration = 0;
        for(Lesson l: lessons){
            duration+=l.getDuration();
        }
        return duration;
    }

    @Override
    public float calculatePrice() {
        float price = 0;
        for(Lesson l: lessons){
            price+=l.calculatePrice();
        }
        return price;
    }

    @Override
    public void print() {
        System.out.println("Course: " + name + ", Duration: " + getDuration() + " hours, Price: $" + calculatePrice());
        for(Lesson l: lessons){
            System.out.print("   |___ ");
            l.print();
        }
    }
    
}

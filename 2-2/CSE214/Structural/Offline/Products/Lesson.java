package Products;
import Core.Core;

public class Lesson implements Core {
    String name;
    float duration;
    float price;

    public Lesson(String name, float duration, float price) {
        this.name = name;
        this.duration = duration;
        this.price = price;
    }

    public float getDuration() {
        return duration;
    }

    public float calculatePrice() {
        return price;
    }

    public void print() {
        System.out.println("Lesson: " + name + ", Duration: " + duration + " hours, Price: $" + price);
    }   
    
}

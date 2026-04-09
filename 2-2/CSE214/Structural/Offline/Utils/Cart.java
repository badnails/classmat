package Utils;
import java.util.ArrayList;

import Core.Core;

public class Cart implements Core {
    private ArrayList<Core> cart_items = new ArrayList<>();
    
    public void addToCart(Core item) {
        cart_items.add(item);
    }

    public void removeFromCart(Core item) {
        cart_items.remove(item);
    }

    public ArrayList<Core> getItems() {
        return cart_items;
    }

    @Override
    public float getDuration() {
        float duration = 0;
        for(Core item: cart_items){
            duration+=item.getDuration();
        }
        return duration;
    }

    @Override
    public float calculatePrice() {
        float price = 0;
        for(Core item: cart_items){
            price+=item.calculatePrice();
        }
        return price;
    }

    @Override
    public void print() {
        System.out.println("Cart Details:");
        for(Core item: cart_items){
            item.print();
            System.out.println();
        }
        System.out.println("Total Duration: " + getDuration() + " hours");
        System.out.println("Total Price: $" + calculatePrice());
    }

}

package Decorators.Discounts;
import java.util.ArrayList;


import Core.Core;
import Products.Module;
import Utils.Cart;

public class MultiModuleDiscountDecorator extends BaseDiscountDecorator {
    boolean applicable = false;
    float disc_amt = 15;
    public MultiModuleDiscountDecorator(Core wrapee) {
        super(wrapee);
        checkApplicability();
    }

    @Override
    public void checkApplicability() {
        Core cart = getWrapee();
        int module_count = 0;

        while(cart instanceof BaseDiscountDecorator){
            cart = ((BaseDiscountDecorator) cart).getWrapee();
        }
        
        if(cart instanceof Cart){
            Cart c = (Cart) cart;
            ArrayList<Core> cart_items = c.getItems();
            for(Core item: cart_items){
                if(item instanceof Module){
                    module_count++;
                }
            }
            applicable = (module_count >= 2);
        }
    }

    @Override
    public float calculatePrice() {
        if(applicable){
            return super.calculatePrice() - disc_amt;
        }
        return super.calculatePrice();
    }

    @Override
    public void print() {
        super.print();
        if(applicable){
            System.out.println("   - Multi-Module Discount Applied: $" + disc_amt);
        }
    }
}

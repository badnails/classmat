package Decorators.Discounts;
import Core.Core;
import Decorators.BaseDecorator;
import Utils.Cart;

public abstract class BaseDiscountDecorator extends BaseDecorator {

    public BaseDiscountDecorator(Core wrapee) {
        Core leaf = wrapee;
        while(leaf instanceof BaseDecorator){
            leaf = ((BaseDecorator) leaf).getWrapee();
        }
        if(!(leaf instanceof Cart)){
            throw new IllegalArgumentException("Discount can only be added to a Cart");
        }
        super(wrapee);
    }

    abstract public void checkApplicability();

    @Override
    public void print()
    {
        super.print();
        System.out.println("\n"+"Price after Discount: "+calculatePrice());
    }
}
package Decorators.Discounts;

import Core.Core;

public class DevelopingDiscountDecorator extends BaseDiscountDecorator{
    float disc_amt = 10;
    public DevelopingDiscountDecorator(Core wrapee){
        super(wrapee);
        checkApplicability();
    }

    @Override
    public void checkApplicability()
    {
        //Always Applicable
        //Control with runtime logic
    }

    @Override
    public float calculatePrice()
    {
        return super.calculatePrice() - disc_amt;
    }

    @Override
    public void print()
    {
        super.print();
        System.out.println("   - Developing Country discount: $"+disc_amt);
    }
}

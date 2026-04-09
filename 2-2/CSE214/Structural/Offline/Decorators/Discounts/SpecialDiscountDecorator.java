package Decorators.Discounts;

import Core.Core;

public class SpecialDiscountDecorator extends BaseDiscountDecorator{
    
    boolean applicable = false;
    float app_time = 5;
    float disc_amt = 12;

    public SpecialDiscountDecorator(Core wrapee)
    {
        super(wrapee);
        checkApplicability();
    }

    @Override
    public void checkApplicability()
    {
        if(getDuration()>=app_time) applicable = true;
    }

    @Override
    public float calculatePrice()
    {
        if(applicable)
        {
            return super.calculatePrice() - disc_amt;
        }
        return super.calculatePrice();
    }

    @Override
    public void print()
    {
        super.print();
        if(applicable)
        {
            System.out.println("   - Special Discount Applied (>5 hour): $"+disc_amt);
        }
    }
}
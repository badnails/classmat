package Decorators.ModuleAddons;
import Core.Core;

public class PracticeAddonDecorator extends BaseModuleAddonDecorator {
    private float add_price = 10.0f;

    public PracticeAddonDecorator(Core wrapee) {
        super(wrapee);
    }

    @Override
    public float calculatePrice() {
        return super.calculatePrice() + add_price;
    }

    @Override
    public void print() {
        super.print();
        System.out.println("   + Practice Addon: $" + add_price);
    }

}
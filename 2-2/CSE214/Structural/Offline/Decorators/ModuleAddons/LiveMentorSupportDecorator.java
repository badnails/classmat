package Decorators.ModuleAddons;
import Core.Core;

public class LiveMentorSupportDecorator extends BaseModuleAddonDecorator {
    private float add_price = 20.0f;

    public LiveMentorSupportDecorator(Core wrapee) {
        super(wrapee);
    }

    @Override
    public float calculatePrice() {
        return super.calculatePrice() + add_price;
    }

    @Override
    public void print() {
        super.print();
        System.out.println("   + Live Mentor Support: $" + add_price);
    }
}
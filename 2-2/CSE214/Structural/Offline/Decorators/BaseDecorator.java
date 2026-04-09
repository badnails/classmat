package Decorators;
import Core.Core;

public abstract class BaseDecorator implements Core {
    Core wrapee;
    public BaseDecorator(Core wrapee) {
        this.wrapee = wrapee;
    }

    public Core getWrapee() {
        return wrapee;
    }

    @Override
    public float getDuration() {
        return wrapee.getDuration();
    }

    @Override
    public float calculatePrice() {
        return wrapee.calculatePrice();
    }

    @Override
    public void print() {
        wrapee.print();
    }
}
package Decorators.ModuleAddons;
import Core.Core;
import Decorators.BaseDecorator;
import Products.Module;

public abstract class BaseModuleAddonDecorator extends BaseDecorator {
    public BaseModuleAddonDecorator(Core wrapee) {
        Core leaf = wrapee;
        while(leaf instanceof BaseDecorator){
            leaf = ((BaseDecorator) leaf).getWrapee();
        }
        if(!(leaf instanceof Module)){
            throw new IllegalArgumentException("Addon can only be added to a Module");
        }
        super(wrapee);
    }
}
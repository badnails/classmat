import Core.Core;
import Decorators.Discounts.DevelopingDiscountDecorator;
import Decorators.Discounts.MultiModuleDiscountDecorator;
import Decorators.Discounts.SpecialDiscountDecorator;
import Decorators.ModuleAddons.LiveMentorSupportDecorator;
import Decorators.ModuleAddons.PracticeAddonDecorator;
import Products.Course;
import Products.Lesson;
import Products.Module;
import Utils.Cart;

public class Main {
    public static void main(String[] args) {
        Lesson UML = new Lesson("UML Design", 2, 50);
        Lesson CreationalDesignPattern = new Lesson("Creational Design Patterns", 3, 75);
        Lesson BehavioralDesignPattern = new Lesson("Behavioral Design Patterns", 5, 95);
        Lesson StructuralDesignPattern = new Lesson("Structural Design Patterns", 2, 60);

        Course SWE = new Course("Software Engineering");
        SWE.addLesson(UML);
        SWE.addLesson(CreationalDesignPattern);
        SWE.addLesson(BehavioralDesignPattern);
        SWE.addLesson(StructuralDesignPattern);

        Lesson CodeOfEthics = new Lesson("Code of Ethics", 2, 30);
        Lesson PERT = new Lesson("PERT Diagram", 6, 100);
        Lesson DevCycle = new Lesson("Development Cycles", 3, 45);
        Lesson Agile = new Lesson("Agile", 10, 120);

        Course DesignPrinciples = new Course("Design Principles");
        DesignPrinciples.addLesson(Agile);
        DesignPrinciples.addLesson(PERT);
        DesignPrinciples.addLesson(CodeOfEthics);
        DesignPrinciples.addLesson(DevCycle);

        Module module = new Module("CSE 213");
        module.addCourse(SWE);
        module.addCourse(DesignPrinciples);
        
        Core draft;
        draft = new PracticeAddonDecorator(module);
        draft = new LiveMentorSupportDecorator(draft);

        Cart cart = new Cart();
        cart.addToCart(draft);

        Core checkout = (Core) cart;
        checkout = new MultiModuleDiscountDecorator(checkout);
        checkout = new SpecialDiscountDecorator(checkout);
        checkout = new DevelopingDiscountDecorator(checkout);

        checkout.print();
    }
}
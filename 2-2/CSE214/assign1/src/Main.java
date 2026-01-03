import cli.Cli;
import cli.CommandHandler;
import service.ExpenseRepository;

/**
 * Main entry point for BudgetBuddy application.
 * Creates and wires dependencies manually.
 */
public class Main {
    public static void main(String[] args) {
        System.out.println("Starting BudgetBuddy...\n");

        // Manually create the main repository //2205026: Replaced with instance
        ExpenseRepository mainRepository = ExpenseRepository.getInstance();

        // Create command handler with the main repository
        CommandHandler commandHandler = new CommandHandler(mainRepository);

        // Create and start CLI
        Cli cli = new Cli(commandHandler);
        
        // If a file path is provided as argument, auto-load it
        if (args.length > 0) {
            System.out.println("Auto-loading file: " + args[0]);
            commandHandler.handleLoad(args[0]);
        }
        
        cli.start();
    }
}

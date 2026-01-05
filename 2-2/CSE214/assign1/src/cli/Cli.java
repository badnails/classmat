package cli;

import java.util.Scanner;

/**
 * Command-line interface for BudgetBuddy.
 * Reads user input and dispatches commands to the CommandHandler.
 */
public class Cli {
    private final CommandHandler commandHandler;
    private final Scanner scanner;
    private boolean running;

    /**
     * Creates a new CLI with the given command handler.
     *
     * @param commandHandler the handler for processing commands
     */
    public Cli(CommandHandler commandHandler) {
        this.commandHandler = commandHandler;
        this.scanner = new Scanner(System.in);
        this.running = false;
    }

    /**
     * Starts the CLI loop.
     */
    public void start() {
        running = true;
        
        System.out.println("BudgetBuddy v0.1");
        System.out.println("Type 'help' for commands.\n");

        while (running) {
            System.out.print("> ");
            String line = scanner.nextLine().trim();

            if (line.isEmpty()) {
                continue;
            }

            processCommand(line);
        }

        scanner.close();
    }

    /**
     * Processes a single command line.
     *
     * @param line the command line to process
     */
    private void processCommand(String line) {
        String[] parts = line.split("\\s+");
        String command = parts[0].toLowerCase();

        try {
            switch (command) {
                case "load":
                    if (parts.length < 2) {
                        System.err.println("Usage: load <file>");
                        break;
                    }
                    commandHandler.handleLoad(parts[1]);
                    break;

                case "list":
                    commandHandler.handleList();
                    break;

                case "summary":
                    if (parts.length < 3) {
                        System.err.println("Usage: summary month <YYYY-MM> or summary category <YYYY-MM|all>");
                        break;
                    }
                    String summaryType = parts[1].toLowerCase();
                    String param = parts[2];
                    
                    if (summaryType.equals("month")) {
                        commandHandler.handleMonthlySummary(param);
                    } else if (summaryType.equals("category")) {
                        commandHandler.handleCategorySummary(param);
                    } else {
                        System.err.println("Unknown summary type: " + summaryType);
                    }
                    break;

                case "export":
                    if (parts.length < 3) {
                        System.err.println("Usage: export txt <outpath> or export html <outpath>");
                        break;
                    }
                    String exportType = parts[1].toLowerCase();
                    String outputPath = parts[2];
                    
                    if (exportType.equals("txt")) {
                        commandHandler.handleExportTxt(outputPath);
                    } else if (exportType.equals("html")) {
                        commandHandler.handleExportHtml(outputPath);
                    } else {
                        System.err.println("Unknown export type: " + exportType);
                    }
                    break;

                case "help":
                    commandHandler.handleHelp();
                    break;

                case "exit":
                    System.out.println("Bye.");
                    running = false;
                    break;

                default:
                    System.err.println("Unknown command: " + command + ". Type 'help' for available commands.");
                    break;
            }
        } catch (Exception e) {
            System.err.println("Error executing command: " + e.getMessage());
        }
    }
}

package cli;

import io.CsvLoader;
import io.HtmlReportGeneratorFactory;
import io.ReportGeneratorFactory;
import io.ReportWriter;
import io.TxtReportGeneratorFactory;
import model.Expense;
import service.ExpenseRepository;
import service.Summarizer;
import util.DateUtils;
import util.TextUtils;

import java.io.IOException;
import java.time.YearMonth;
import java.util.List;
import java.util.Map;

/**
 * Handles CLI commands and dispatches to appropriate services.
 */
public class CommandHandler {
    private final ExpenseRepository mainRepository;

    /**
     * Creates a CommandHandler with a primary repository.
     *
     * @param mainRepository the main repository to use
     */
    public CommandHandler(ExpenseRepository mainRepository) {
        this.mainRepository = mainRepository;
    }

    /**
     * Loads expenses from a CSV file.
     *
     * @param filePath the file to load
     */
    public void handleLoad(String filePath) {
        try {
            CsvLoader loader = CsvLoader.getInstance();
            List<Expense> expenses = loader.loadFromFile(filePath);

            mainRepository.clear();
            mainRepository.addAll(expenses);

            System.out.println("Loaded " + expenses.size() + " entries.");
        } catch (IOException e) {
            System.err.println("Error loading file: " + e.getMessage());
        } catch (IllegalArgumentException e) {
            System.err.println("Error parsing CSV: " + e.getMessage());
        }
    }

    /**
     * Lists all expenses.
     */
    public void handleList() {
        List<Expense> expenses = mainRepository.findAll();

        if (expenses.isEmpty()) {
            System.out.println("No expenses loaded.");
            return;
        }

        System.out.println("\nAll Expenses:");
        System.out.println(TextUtils.separator(80));

        for (Expense expense : expenses) {
            System.out.println(expense);
        }

        System.out.println(TextUtils.separator(80));
        System.out.println("Total entries: " + expenses.size());
    }

    /**
     * Shows monthly summary for a specific month.
     *
     * @param monthStr the month in YYYY-MM format
     */
    public void handleMonthlySummary(String monthStr) {
        try {
            YearMonth yearMonth = DateUtils.parseYearMonth(monthStr);

            // ExpenseRepository localRepo = new ExpenseRepository();
            // localRepo.addAll(mainRepository.findAll());

            List<Expense> monthExpenses = mainRepository.findByMonth(yearMonth);
            Summarizer summarizer = new Summarizer(monthExpenses);

            System.out.println("\nMonth: " + monthStr);
            System.out.println(TextUtils.separator(60));

            if (monthExpenses.isEmpty()) {
                System.out.println("No expenses found for this month.");
                return;
            }

            double total = summarizer.grandTotal();
            System.out.println("Total: " + TextUtils.formatAmount(total));

            System.out.println("\nCategory totals:");
            Map<String, Double> categoryTotals = summarizer.categoryTotals(null);
            for (Map.Entry<String, Double> entry : categoryTotals.entrySet()) {
                System.out.println("  " + entry.getKey() + ": " + TextUtils.formatAmount(entry.getValue()));
            }

        } catch (IllegalArgumentException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }

    /**
     * Shows category summary for a month or all time.
     *
     * @param monthStr the month in YYYY-MM format, or "all" for all time
     */
    public void handleCategorySummary(String monthStr) {
        try {
            YearMonth yearMonth = monthStr.equalsIgnoreCase("all") ? null : DateUtils.parseYearMonth(monthStr);

            Summarizer summarizer = new Summarizer(mainRepository.findAll());

            Map<String, Double> categoryTotals = summarizer.categoryTotals(yearMonth);

            String period = yearMonth != null ? "Month: " + monthStr : "All Time";
            System.out.println("\nCategory Summary - " + period);
            System.out.println(TextUtils.separator(60));

            if (categoryTotals.isEmpty()) {
                System.out.println("No expenses found.");
                return;
            }

            // Find max for bar visualization
            double maxAmount = categoryTotals.values().stream()
                    .max(Double::compareTo)
                    .orElse(1.0);

            for (Map.Entry<String, Double> entry : categoryTotals.entrySet()) {
                String category = entry.getKey();
                double amount = entry.getValue();
                String bar = TextUtils.createBar(amount, maxAmount, 30);

                System.out.printf("%-15s %12s  %s\n",
                        category,
                        TextUtils.formatAmount(amount),
                        bar);
            }

        } catch (IllegalArgumentException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }

    /**
     * Exports a text report.
     *
     * @param outputPath the output file path
     */
    public void handleExportTxt(String outputPath) {
        try {
            ReportGeneratorFactory repgenfac = new TxtReportGeneratorFactory();
            ReportWriter writer = new ReportWriter(repgenfac);

            // ExpenseRepository exportRepo = new ExpenseRepository();
            // exportRepo.addAll(mainRepository.findAll());

            writer.writeReport(outputPath, mainRepository);
        } catch (IOException e) {
            System.err.println("Error writing report: " + e.getMessage());
        }
    }

    /**
     * Exports an HTML report.
     *
     * @param outputPath the output file path
     */
    public void handleExportHtml(String outputPath) {
        try {
            ReportGeneratorFactory repgenfac = new HtmlReportGeneratorFactory();
            ReportWriter writer = new ReportWriter(repgenfac);

            // ExpenseRepository exportRepo = new ExpenseRepository();
            // exportRepo.addAll(mainRepository.findAll());

            writer.writeReport(outputPath, mainRepository);
        } catch (IOException e) {
            System.err.println("Error writing report: " + e.getMessage());
        }
    }

    /**
     * Shows help information.
     */
    public void handleHelp() {
        System.out.println("\nBudgetBuddy Commands:");
        System.out.println("  load <file>                  - Load expenses from CSV file");
        System.out.println("  list                         - List all expenses");
        System.out.println("  summary month <YYYY-MM>      - Show monthly summary");
        System.out.println("  summary category <YYYY-MM|all> - Show category summary");
        System.out.println("  export txt <outpath>         - Export text report");
        System.out.println("  export html <outpath>        - Export HTML report");
        System.out.println("  help                         - Show this help");
        System.out.println("  exit                         - Exit program");
    }
}

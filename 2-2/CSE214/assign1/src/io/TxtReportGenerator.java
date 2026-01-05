package io;

import model.Expense;
//import service.ExpenseRepository;
import service.Summarizer;
import util.TextUtils;

// import java.io.BufferedWriter;
// import java.io.FileWriter;
import java.io.IOException;
import java.time.YearMonth;
import java.util.List;
import java.util.Map;

/**
 * Writes plain-text expense reports with ASCII formatting.
 */
public class TxtReportGenerator extends ReportGenerator {

    // public void writeReport(String filePath, ExpenseRepository repository) throws IOException {
    //     List<Expense> allExpenses = repository.findAll();
    //     Summarizer summarizer = new Summarizer(allExpenses);

    //     try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath))) {
    //         writer.write(header());
    //         writer.write(monthlySummary(summarizer));
    //         writer.write(categoryBreakdown(summarizer));
    //         writer.write(grandTotal(summarizer));
    //         writer.write(recentEntries(allExpenses));
    //         writer.write(footer());
    //     }

    //     System.out.println("Text report written to: " + filePath);
    // }

    @Override
    public String header() throws IOException {
        StringBuilder sb = new StringBuilder();
        sb.append("=====================================\n");
        sb.append("       BUDGETBUDDY EXPENSE REPORT    \n");
        sb.append("=====================================\n\n");
        return sb.toString();
    }

    @Override
    public String monthlySummary(Summarizer summarizer) throws IOException {
        StringBuilder sb = new StringBuilder();
        sb.append("MONTHLY SUMMARY\n");
        sb.append(TextUtils.separator(60) + "\n");

        Map<YearMonth, Double> monthlyTotals = summarizer.monthlyTotals();
        for (Map.Entry<YearMonth, Double> entry : monthlyTotals.entrySet()) {
            String monthStr = formatMonth(entry.getKey());
            String amountStr = formatAmount(entry.getValue());
            sb.append(String.format("%-10s : %12s\n", monthStr, amountStr));
        }
        sb.append("\n");
        return sb.toString();
    }

    @Override
    public String categoryBreakdown(Summarizer summarizer) throws IOException {
        StringBuilder sb = new StringBuilder();
        sb.append("CATEGORY BREAKDOWN (All Time)\n");
        sb.append(TextUtils.separator(60) + "\n");

        Map<String, Double> categoryTotals = summarizer.categoryTotals(null);
        double maxAmount = categoryTotals.values().stream()
                .max(Double::compareTo)
                .orElse(1.0);

        for (Map.Entry<String, Double> entry : categoryTotals.entrySet()) {
            String category = entry.getKey();
            double amount = entry.getValue();
            String amountStr = formatAmount(amount);
            String bar = createBar(amount, maxAmount);
            sb.append(String.format("%-15s %12s  %s\n", category, amountStr, bar));
        }
        sb.append("\n");
        return sb.toString();
    }

    @Override
    public String grandTotal(Summarizer summarizer) throws IOException {
        StringBuilder sb = new StringBuilder();
        sb.append(TextUtils.separator(60) + "\n");
        sb.append(String.format("GRAND TOTAL: %s\n", formatAmount(summarizer.grandTotal())));
        sb.append(TextUtils.separator(60) + "\n");
        return sb.toString();
    }

    @Override
    public String recentEntries(List<Expense> expenses) throws IOException {
        StringBuilder sb = new StringBuilder();
        sb.append("\nRECENT ENTRIES (Last 10)\n");
        sb.append(TextUtils.separator(60) + "\n");

        int count = 0;
        for (int i = expenses.size() - 1; i >= 0 && count < 10; i--, count++) {
            Expense exp = expenses.get(i);
            String dateStr = formatDate(exp.getDate());
            sb.append(String.format("%s  %-12s %10s  %s\n",
                    dateStr,
                    exp.getCategory(),
                    formatAmount(exp.getAmount()),
                    exp.getNotes()));
        }
        return sb.toString();
    }

    @Override
    public String footer() throws IOException {
        return "";
    }

    @Override
    public String createBar(double value, double maxValue) throws IOException {
        return TextUtils.createBar(value, maxValue, 30);
    }
}

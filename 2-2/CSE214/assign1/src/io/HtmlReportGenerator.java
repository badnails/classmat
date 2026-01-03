package io;

import model.Expense;
//import service.ExpenseRepository;
import service.Summarizer;

// import java.io.BufferedWriter;
// import java.io.FileWriter;
import java.io.IOException;
//import java.time.LocalDate;
import java.time.YearMonth;
// import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Map;

/**
 * Writes HTML expense reports with basic inline styling.
 */
public class HtmlReportGenerator extends ReportGenerator {
    // private final DateTimeFormatter dateFormatter;
    // private final DateTimeFormatter monthFormatter;

    // public HtmlReportGenerator() {
    //     this.dateFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
    //     this.monthFormatter = DateTimeFormatter.ofPattern("yyyy-MM");
    // }

    // public void writeReport(String filePath, ExpenseRepository repository) throws IOException {
    //     List<Expense> allExpenses = repository.findAll();
    //     Summarizer summarizer = new Summarizer(allExpenses);

    //     try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath))) {
    //         writeHtmlHeader(writer);
    //         writeMonthlySummary(writer, summarizer);
    //         writeCategoryBreakdown(writer, summarizer);
    //         writeGrandTotal(writer, summarizer);
    //         writeRecentEntries(writer, allExpenses);
    //         writeHtmlFooter(writer);
    //     }

    //     System.out.println("HTML report written to: " + filePath);
    // }

    @Override
    public String header() throws IOException{
        StringBuilder sb = new StringBuilder();
        sb.append("<!DOCTYPE html>\n");
        sb.append("<html>\n<head>\n");
        sb.append("<title>BudgetBuddy Expense Report</title>\n");
        sb.append("<style>\n");
        sb.append("body { font-family: Arial, sans-serif; margin: 20px; }\n");
        sb.append("h1 { color: #333; }\n");
        sb.append("table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }\n");
        sb.append("th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }\n");
        sb.append("th { background-color: #4CAF50; color: white; }\n");
        sb.append(".bar { background-color: #4CAF50; height: 20px; display: inline-block; }\n");
        sb.append(".total { font-weight: bold; font-size: 1.2em; color: #4CAF50; }\n");
        sb.append("</style>\n");
        sb.append("</head>\n<body>\n");
        sb.append("<h1>BudgetBuddy Expense Report</h1>\n");
        return sb.toString();
    }

    @Override
    public String monthlySummary(Summarizer summarizer) throws IOException {
        StringBuilder sb = new StringBuilder();
        sb.append("<h2>Monthly Summary</h2>\n");
        sb.append("<table>\n");
        sb.append("<tr><th>Month</th><th>Total Amount</th></tr>\n");

        Map<YearMonth, Double> monthlyTotals = summarizer.monthlyTotals();
        for (Map.Entry<YearMonth, Double> entry : monthlyTotals.entrySet()) {
            String monthStr = formatMonth(entry.getKey());
            String amountStr = formatAmount(entry.getValue());
            sb.append(String.format("<tr><td>%s</td><td>%s</td></tr>\n", monthStr, amountStr));
        }
        sb.append("</table>\n");
        return sb.toString();
    }

    @Override
    public String categoryBreakdown(Summarizer summarizer) throws IOException {
        StringBuilder sb = new StringBuilder();
        sb.append("<h2>Category Breakdown (All Time)</h2>\n");
        sb.append("<table>\n");
        sb.append("<tr><th>Category</th><th>Total Amount</th><th>Visual</th></tr>\n");

        Map<String, Double> categoryTotals = summarizer.categoryTotals(null);
        double maxAmount = categoryTotals.values().stream()
                .max(Double::compareTo)
                .orElse(1.0);

        for (Map.Entry<String, Double> entry : categoryTotals.entrySet()) {
            String category = entry.getKey();
            double amount = entry.getValue();
            String amountStr = formatAmount(amount);
            String barHtml = createBar(amount, maxAmount);
            sb.append(String.format("<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n",
                    category, amountStr, barHtml));
        }
        sb.append("</table>\n");
        return sb.toString();
    }

    @Override
    public String grandTotal(Summarizer summarizer) throws IOException {
        StringBuilder sb = new StringBuilder();
        sb.append(String.format("<p class=\"total\">Grand Total: %s</p>\n",
                formatAmount(summarizer.grandTotal())));
        return sb.toString();
    }

    @Override
    public String recentEntries(List<Expense> expenses) throws IOException {
        StringBuilder sb = new StringBuilder();
        sb.append("<h2>Recent Entries (Last 10)</h2>\n");
        sb.append("<table>\n");
        sb.append("<tr><th>Date</th><th>Category</th><th>Amount</th><th>Notes</th></tr>\n");

        int count = 0;
        for (int i = expenses.size() - 1; i >= 0 && count < 10; i--, count++) {
            Expense exp = expenses.get(i);
            String dateStr = formatDate(exp.getDate());
            sb.append(String.format("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n",
                    dateStr,
                    exp.getCategory(),
                    formatAmount(exp.getAmount()),
                    exp.getNotes()));
        }
        sb.append("</table>\n");
        return sb.toString();
    }

    @Override
    public String footer() throws IOException {
        StringBuilder sb = new StringBuilder();
        sb.append("</body>\n</html>\n");
        return sb.toString();
    }

    // @Override
    // public String formatDate(LocalDate date) {
    //     return date.format(dateFormatter);
    // }

    // @Override
    // public String formatMonth(YearMonth month) {
    //     return month.format(monthFormatter);
    // }

    // @Override
    // public String formatAmount(double amount) {
    //     return String.format("%.2f", amount);
    // }

    @Override
    public String createBar(double value, double maxValue) {
        int barWidth = (int) Math.round((value * 200) / maxValue);
        return String.format("<div class=\"bar\" style=\"width: %dpx;\"></div>", barWidth);
    }
}

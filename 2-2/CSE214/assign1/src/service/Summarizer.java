package service;

import model.Expense;

import java.time.YearMonth;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Computes summaries and aggregations over expense data.
 */
public class Summarizer {
    private final List<Expense> expenses;

    /**
     * Creates a Summarizer for a given list of expenses.
     *
     * @param expenses the expenses to summarize
     */
    public Summarizer(List<Expense> expenses) {
        this.expenses = expenses;
    }

    /**
     * Computes total expenses per month.
     *
     * @return map of YearMonth to total amount
     */
    public Map<YearMonth, Double> monthlyTotals() {
        Map<YearMonth, Double> totals = new HashMap<>();

        for (Expense expense : expenses) {
            YearMonth month = YearMonth.from(expense.getDate());
            totals.merge(month, expense.getAmount(), Double::sum);
        }

        return totals;
    }

    /**
     * Computes total expenses per category for a specific month.
     *
     * @param yearMonth the month to filter by, or null for all months
     * @return map of category to total amount
     */
    public Map<String, Double> categoryTotals(YearMonth yearMonth) {
        Map<String, Double> totals = new HashMap<>();

        for (Expense expense : expenses) {
            if (yearMonth == null || YearMonth.from(expense.getDate()).equals(yearMonth)) {
                totals.merge(expense.getCategory(), expense.getAmount(), Double::sum);
            }
        }

        return totals;
    }

    /**
     * Computes the total of all expenses.
     *
     * @return total amount
     */
    public double grandTotal() {
        return expenses.stream()
                .mapToDouble(Expense::getAmount)
                .sum();
    }

    /**
     * Computes the total for a specific month.
     *
     * @param yearMonth the month to compute total for
     * @return total amount for the month
     */
    public double totalForMonth(YearMonth yearMonth) {
        return expenses.stream()
                .filter(e -> YearMonth.from(e.getDate()).equals(yearMonth))
                .mapToDouble(Expense::getAmount)
                .sum();
    }
}

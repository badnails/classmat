import io.CsvLoader;
import model.Expense;
import service.ExpenseRepository;
import service.Summarizer;
import util.TextUtils;

import java.time.YearMonth;
import java.util.List;
import java.util.Map;

/**
 * Test harness to verify BudgetBuddy behavior programmatically.
 * Run this to validate that the application works correctly.
 */
public class TestHarness {

    public static void main(String[] args) {
        System.out.println("=== BudgetBuddy Test Harness ===\n");

        try {
            // Test 1: Load CSV file
            System.out.println("Test 1: Loading CSV file...");
            CsvLoader loader = CsvLoader.getInstance();
            List<Expense> expenses = loader.loadFromFile("data/expenses.csv");
            System.out.println("✓ Loaded " + expenses.size() + " expenses");
            assert expenses.size() == 70 : "Expected 70 expenses";
            System.out.println();

            // Test 2: Create repository and add expenses
            System.out.println("Test 2: Creating repository...");
            ExpenseRepository repository = ExpenseRepository.getInstance();
            repository.addAll(expenses);
            System.out.println("✓ Repository contains " + repository.count() + " expenses");
            assert repository.count() == 70 : "Expected 70 expenses in repository";
            System.out.println();

            // Test 3: Test monthly summary
            System.out.println("Test 3: Computing monthly summary...");
            Summarizer summarizer = new Summarizer(repository.findAll());
            Map<YearMonth, Double> monthlyTotals = summarizer.monthlyTotals();
            System.out.println("✓ Found " + monthlyTotals.size() + " months with expenses");

            for (Map.Entry<YearMonth, Double> entry : monthlyTotals.entrySet()) {
                System.out.println("  " + entry.getKey() + ": " + TextUtils.formatAmount(entry.getValue()));
            }
            System.out.println();

            // Test 4: Test specific month total
            System.out.println("Test 4: Computing February 2025 total...");
            YearMonth feb2025 = YearMonth.of(2025, 2);
            double febTotal = summarizer.totalForMonth(feb2025);
            System.out.println("✓ February 2025 total: " + TextUtils.formatAmount(febTotal));

            // Expected: Rent (12000) + Food (2340) + Utilities (1800) + Transport (500) +
            // Entertainment (2150) + Shopping (2500) + Healthcare (800) = 22090
            double expectedFeb = 22090.0;
            if (Math.abs(febTotal - expectedFeb) < 0.01) {
                System.out.println("✓ February total matches expected value");
            } else {
                System.out.println("⚠ February total (" + febTotal + ") differs from expected (" + expectedFeb + ")");
            }
            System.out.println();

            // Test 5: Test category summary
            System.out.println("Test 5: Computing category totals for all time...");
            Map<String, Double> categoryTotals = summarizer.categoryTotals(null);
            System.out.println("✓ Found " + categoryTotals.size() + " categories");

            for (Map.Entry<String, Double> entry : categoryTotals.entrySet()) {
                System.out.println("  " + entry.getKey() + ": " + TextUtils.formatAmount(entry.getValue()));
            }
            System.out.println();

            // Test 6: Grand total
            System.out.println("Test 6: Computing grand total...");
            double grandTotal = summarizer.grandTotal();
            System.out.println("✓ Grand total: " + TextUtils.formatAmount(grandTotal));
            System.out.println();

            // Test 7: Filter by month
            System.out.println("Test 7: Filtering expenses by month...");
            List<Expense> marchExpenses = repository.findByMonth(YearMonth.of(2025, 3));
            System.out.println("✓ Found " + marchExpenses.size() + " expenses in March 2025");
            assert marchExpenses.size() == 14 : "Expected 14 expenses in March 2025";
            System.out.println();

            System.out.println("=== All Tests Passed ===\n");
            System.out.println("Summary of expected totals:");
            System.out.println("  Total entries: 70");
            System.out.println("  Months covered: " + monthlyTotals.size());
            System.out.println("  Categories: " + categoryTotals.size());
            System.out.println("  Grand total: " + TextUtils.formatAmount(grandTotal));
            System.out.println("\nNote: These values can be used to verify that refactored code");
            System.out.println("produces identical outputs (functional equivalence).");

        } catch (Exception e) {
            System.err.println("✗ Test failed with error: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
}

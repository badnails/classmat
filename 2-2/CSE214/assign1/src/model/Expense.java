package model;

import java.time.LocalDate;
import java.util.Objects;

/**
 * Represents a single expense entry with date, category, amount, and notes.
 * Immutable data class for expense records.
 */
public class Expense {
    private final LocalDate date;
    private final String category;
    private final double amount;
    private final String notes;

    /**
     * Creates a new Expense instance.
     *
     * @param date     the date of the expense
     * @param category the category (e.g., Food, Rent, Transport)
     * @param amount   the amount spent
     * @param notes    additional notes or description
     */
    public Expense(LocalDate date, String category, double amount, String notes) {
        this.date = Objects.requireNonNull(date, "Date cannot be null");
        this.category = Objects.requireNonNull(category, "Category cannot be null");
        if (amount < 0) {
            throw new IllegalArgumentException("Amount cannot be negative");
        }
        this.amount = amount;
        this.notes = notes != null ? notes : "";
    }

    public LocalDate getDate() {
        return date;
    }

    public String getCategory() {
        return category;
    }

    public double getAmount() {
        return amount;
    }

    public String getNotes() {
        return notes;
    }

    @Override
    public String toString() {
        return String.format("%s  %-12s %10.2f   %s",
                date, category, amount, notes);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (o == null || getClass() != o.getClass())
            return false;
        Expense expense = (Expense) o;
        return Double.compare(expense.amount, amount) == 0 &&
                date.equals(expense.date) &&
                category.equals(expense.category) &&
                notes.equals(expense.notes);
    }

    @Override
    public int hashCode() {
        return Objects.hash(date, category, amount, notes);
    }
}

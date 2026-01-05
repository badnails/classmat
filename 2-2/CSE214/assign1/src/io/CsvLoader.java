package io;

import model.Expense;
import util.DateUtils;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

/**
 * Loads expense data from CSV files.
 * Supports both semicolon and comma separators.
 */
public class CsvLoader {
    private static CsvLoader instance;
    private CsvLoader(){}
    public static CsvLoader getInstance(){
        if(instance == null) instance = new CsvLoader();
        return instance;
    }

    /**
     * Loads expenses from a CSV file.
     * Expected format: date;category;amount;notes
     * or: date,category,amount,notes
     *
     * @param filePath path to the CSV file
     * @return list of parsed expenses
     * @throws IOException              if file cannot be read
     * @throws IllegalArgumentException if CSV format is invalid
     */
    public List<Expense> loadFromFile(String filePath) throws IOException {
        List<Expense> expenses = new ArrayList<>();

        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            int lineNumber = 0;
            boolean firstLine = true;

            while ((line = reader.readLine()) != null) {
                lineNumber++;
                line = line.trim();

                if (line.isEmpty()) {
                    continue;
                }

                // Skip header line if it starts with "date"
                if (firstLine && line.toLowerCase().startsWith("date")) {
                    firstLine = false;
                    continue;
                }
                firstLine = false;

                try {
                    Expense expense = parseLine(line, lineNumber);
                    expenses.add(expense);
                } catch (IllegalArgumentException e) {
                    throw new IllegalArgumentException("Error at line " + lineNumber + ": " + e.getMessage(), e);
                }
            }
        }

        System.out.println("Loaded " + expenses.size() + " entries from " + filePath);
        return expenses;
    }

    /**
     * Parses a single CSV line into an Expense object.
     * Tries semicolon separator first, then comma.
     *
     * @param line       the CSV line
     * @param lineNumber the line number (for error messages)
     * @return parsed Expense
     * @throws IllegalArgumentException if line format is invalid
     */
    private Expense parseLine(String line, int lineNumber) {
        String[] parts;

        // Try semicolon separator first
        if (line.contains(";")) {
            parts = line.split(";", -1);
        } else {
            parts = line.split(",", -1);
        }

        if (parts.length < 3) {
            throw new IllegalArgumentException(
                    "Expected at least 3 fields (date, category, amount), found " + parts.length);
        }

        try {
            LocalDate date = DateUtils.parseDate(parts[0].trim());
            String category = parts[1].trim();
            double amount = Double.parseDouble(parts[2].trim());
            String notes = parts.length > 3 ? parts[3].trim() : "";

            if (category.isEmpty()) {
                throw new IllegalArgumentException("Category cannot be empty");
            }

            if (amount < 0) {
                throw new IllegalArgumentException("Amount cannot be negative");
            }

            return new Expense(date, category, amount, notes);
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("Invalid amount format: " + parts[2], e);
        }
    }
}

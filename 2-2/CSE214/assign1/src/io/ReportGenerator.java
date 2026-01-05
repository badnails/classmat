package io;

import java.io.IOException;
import java.time.LocalDate;
import java.time.YearMonth;
import java.time.format.DateTimeFormatter;
import java.util.List;

import model.Expense;
import service.Summarizer;

public abstract class ReportGenerator {
    protected final DateTimeFormatter dateFormatter;
    protected final DateTimeFormatter monthFormatter;

    public ReportGenerator() {
        this.dateFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        this.monthFormatter = DateTimeFormatter.ofPattern("yyyy-MM");
    }

    protected String formatDate(LocalDate date) {
        return date.format(dateFormatter);
    }

    protected String formatMonth(YearMonth month) {
        return month.format(monthFormatter);
    }

    protected String formatAmount(double amount) {
        return String.format("%.2f", amount);
    }

    public abstract String header() throws IOException;
    public abstract String monthlySummary(Summarizer summarizer) throws IOException;
    public abstract String categoryBreakdown(Summarizer summarizer) throws IOException;
    public abstract String grandTotal(Summarizer summarizer) throws IOException;
    public abstract String recentEntries(List<Expense> expenses) throws IOException;
    public abstract String footer() throws IOException;
    public abstract String createBar(double value, double maxValue) throws IOException;
}

package io;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

import service.ExpenseRepository;
import service.Summarizer;
import model.Expense;

public class ReportWriter {
    private ReportGenerator repgen;
    public ReportWriter(ReportGeneratorFactory repgenfac)
    {
        this.repgen = repgenfac.createReportGenerator();
    }
    
    public void writeReport(String filePath, ExpenseRepository repository) throws IOException {
        List<Expense> allExpenses = repository.findAll();
        Summarizer summarizer = new Summarizer(allExpenses);

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath))) {
            // writeHtmlHeader(writer);
            // writeMonthlySummary(writer, summarizer);
            // writeCategoryBreakdown(writer, summarizer);
            // writeGrandTotal(writer, summarizer);
            // writeRecentEntries(writer, allExpenses);
            // writeHtmlFooter(writer);
            writer.write(repgen.header());
            writer.write(repgen.monthlySummary(summarizer));
            writer.write(repgen.categoryBreakdown(summarizer));
            writer.write(repgen.grandTotal(summarizer));
            writer.write(repgen.recentEntries(allExpenses));
            writer.write(repgen.footer());
        }
    }
}

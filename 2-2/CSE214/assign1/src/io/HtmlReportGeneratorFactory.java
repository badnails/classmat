package io;

public class HtmlReportGeneratorFactory implements ReportGeneratorFactory {
    public ReportGenerator createReportGenerator()
    {
        return new HtmlReportGenerator();
    }
}
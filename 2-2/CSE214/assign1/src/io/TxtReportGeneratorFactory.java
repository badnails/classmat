package io;

public class TxtReportGeneratorFactory implements ReportGeneratorFactory {
    public ReportGenerator createReportGenerator()
    {
        return new TxtReportGenerator();
    }
}

package util;

import java.time.LocalDate;
import java.time.YearMonth;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;

/**
 * Utility methods for date parsing and formatting.
 */
public class DateUtils {

    /**
     * Parses a date string in ISO format (YYYY-MM-DD).
     *
     * @param dateStr the date string
     * @return parsed LocalDate
     * @throws IllegalArgumentException if format is invalid
     */
    public static LocalDate parseDate(String dateStr) {
        try {
            return LocalDate.parse(dateStr, DateTimeFormatter.ISO_LOCAL_DATE);
        } catch (DateTimeParseException e) {
            throw new IllegalArgumentException("Invalid date format: " + dateStr + ". Expected YYYY-MM-DD.", e);
        }
    }

    /**
     * Parses a year-month string (YYYY-MM).
     *
     * @param yearMonthStr the year-month string
     * @return parsed YearMonth
     * @throws IllegalArgumentException if format is invalid
     */
    public static YearMonth parseYearMonth(String yearMonthStr) {
        try {
            return YearMonth.parse(yearMonthStr, DateTimeFormatter.ofPattern("yyyy-MM"));
        } catch (DateTimeParseException e) {
            throw new IllegalArgumentException("Invalid year-month format: " + yearMonthStr + ". Expected YYYY-MM.", e);
        }
    }

    /**
     * Formats a LocalDate to ISO format (YYYY-MM-DD).
     *
     * @param date the date to format
     * @return formatted date string
     */
    public static String formatDate(LocalDate date) {
        return date.format(DateTimeFormatter.ISO_LOCAL_DATE);
    }

    /**
     * Formats a YearMonth to YYYY-MM format.
     *
     * @param yearMonth the year-month to format
     * @return formatted year-month string
     */
    public static String formatYearMonth(YearMonth yearMonth) {
        return yearMonth.format(DateTimeFormatter.ofPattern("yyyy-MM"));
    }
}

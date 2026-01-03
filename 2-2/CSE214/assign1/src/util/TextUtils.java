package util;

/**
 * Utility methods for text formatting, ASCII bars, and table padding.
 */
public class TextUtils {

    /**
     * Creates an ASCII horizontal bar visualization for a value.
     * Each block represents a portion of the max value.
     *
     * @param value    the value to visualize
     * @param maxValue the maximum value for scaling
     * @param maxWidth the maximum width of the bar in characters
     * @return ASCII bar string
     */
    public static String createBar(double value, double maxValue, int maxWidth) {
        if (maxValue == 0) {
            return "";
        }
        int blocks = (int) Math.round((value * maxWidth) / maxValue);
        StringBuilder bar = new StringBuilder();
        for (int i = 0; i < blocks; i++) {
            bar.append("█");
        }
        return bar.toString();
    }

    /**
     * Pads a string to a specified width with spaces (left-aligned).
     *
     * @param str   the string to pad
     * @param width the target width
     * @return padded string
     */
    public static String padRight(String str, int width) {
        if (str.length() >= width) {
            return str;
        }
        return str + " ".repeat(width - str.length());
    }

    /**
     * Pads a string to a specified width with spaces (right-aligned).
     *
     * @param str   the string to pad
     * @param width the target width
     * @return padded string
     */
    public static String padLeft(String str, int width) {
        if (str.length() >= width) {
            return str;
        }
        return " ".repeat(width - str.length()) + str;
    }

    /**
     * Creates a horizontal line separator for tables.
     *
     * @param width the width of the separator
     * @return separator string
     */
    public static String separator(int width) {
        return "-".repeat(width);
    }

    /**
     * Formats an amount as a string with 2 decimal places.
     *
     * @param amount the amount to format
     * @return formatted amount string
     */
    public static String formatAmount(double amount) {
        return String.format("%.2f", amount);
    }
}

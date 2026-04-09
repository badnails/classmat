public interface Tier {
    public void setPatient(Patient p);
    public void travelCheck(int distance);
    public void promote();
    public void demote();
    public void setMood(MoodEnum mood);
}
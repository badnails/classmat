public class Patient {
    Tier currentTier;
    PatientStateEnum state;
    int currentDistance;
    MoodEnum mood;

    Patient(Tier init, int currentDistance)
    {
        changeTier(init);
        currentTier.travelCheck(currentDistance);
    }

    void changeTier(Tier t)
    {
        this.currentTier = t;
        currentTier.setPatient(this);
    }

    void activateLux(int hours)
    {
        Tier oldTier = currentTier;
        changeTier(new LuxTier());
        //sleep(hours*3600);
        changeTier(oldTier);
    }

    void promote()
    {
        currentTier.promote();
    }

    void demote()
    {
        currentTier.demote();
    }

}

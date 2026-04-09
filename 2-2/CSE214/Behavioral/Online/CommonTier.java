

public class CommonTier implements Tier{
    Patient patientContext;

    public void setPatient(Patient p){
        this.patientContext = p;
    }
    @Override
    public void travelCheck(int distance){
        if(distance>10){
            patientContext.state = PatientStateEnum.UNSTABLE;
            System.out.println("Bring patient back within 10kms of server");
        }else{
            System.out.println("Patient in coverage");
        }
    }
    @Override
    public void promote(){
        patientContext.changeTier(new PlusTier());
        System.out.println("Promoted to Plus Tier");
    }
    @Override
    public void demote(){
        System.out.println("No change in Tier");
    }
    @Override
    public void setMood(MoodEnum mood){
        System.out.println("Mood Control Unavailable");
    }
}

public class LuxTier implements Tier{
    Patient patientContext;

    public void setPatient(Patient p){
        this.patientContext = p;
    }
    @Override
    public void travelCheck(int distance){
        if(distance>50){
            patientContext.state = PatientStateEnum.UNSTABLE;
            System.out.println("Bring patient back within 50kms of server");
        }else{
            System.out.println("Patient in coverage");
        }
    }
    @Override
    public void promote(){
        System.out.println("No change in Tier");
    }
    @Override
    public void demote(){
        patientContext.changeTier(new PlusTier());
        System.out.println("Demoted to Plus Tier");
    }
    @Override
    public void setMood(MoodEnum mood){
        patientContext.mood = mood
    }
}

public class PlusTier implements Tier {
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
        patientContext.changeTier(new LuxTier());
        System.out.println("Promoted to Lux Tier");
    }
    @Override
    public void demote(){
        patientContext.changeTier(new CommonTier());
        System.out.println("Demoted to Common Tier");
    }
    @Override
    public void setMood(MoodEnum mood){
        System.out.println("Mood Control Unavailable");
    }
}

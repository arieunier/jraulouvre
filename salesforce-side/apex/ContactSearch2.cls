public class ContactSearch2 {

    @AuraEnabled
    public static List<public_voluntary__x > getContacts(String theCode) {
        if (theCode == null || theCode == '') {
       return [Select id__c , firstname__c , lastname__c , email__c , telephone__c , confirmationcode__c , shiftid__c , registrationstatus__c  From public_voluntary__x order by lastname__c  asc limit 10];     
        } else {
       return [Select id__c , firstname__c , lastname__c , email__c , telephone__c , confirmationcode__c , shiftid__c , registrationstatus__c  From public_voluntary__x  Where confirmationcode__c  LIKE : (theCode + '%') OR lastname__c  LIKE : (theCode + '%') OR firstname__c  LIKE : (theCode + '%') order by lastname__c  asc limit 10];
        }
    }
    
	@future(callout=True)
    public static void asyncCallout(String uid, String value)
    {
        public_externalobjectdemo__x obj = new public_externalobjectdemo__x(id__c = uid, val__c=value);
        System.debug(obj.id__c);
        System.debug(obj.val__c);
        Database.SaveResult srList2 = Database.insertAsync(obj);
    }
    
    @AuraEnabled
    public static void checkinContacts(string contactId){
        try{
            public_voluntary__x objCon=[Select id__c , firstname__c , lastname__c , email__c , telephone__c , confirmationcode__c , shiftid__c , registrationstatus__c  From public_voluntary__x where id__c=:contactId limit 1];
            if(objCon !=null){
                if(objCon.registrationstatus__c == 'CONFIRMED') {
                	objCon.registrationstatus__c = 'COMPLETED';
                } else {
                    objCon.registrationstatus__c = 'CONFIRMED';
                }
				Database.SaveResult srList2 = Database.updateAsync(objCon);
            }
            
        }
        catch(Exception ex){}
    } 
}
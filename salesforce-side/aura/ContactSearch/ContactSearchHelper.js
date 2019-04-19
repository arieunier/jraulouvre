({
    loadList: function(component) {
    const action = component.get("c.getContacts");
    const theCode = component.find("nameFilter").get("v.value");
    action.setParams({
    theCode: theCode
    });
    action.setCallback(this, function(a) {
    component.set("v.contacts", a.getReturnValue());
    });
    $A.enqueueAction(action); 
    },
       
       updateContact: function(component,event) {
           let button = event.getSource();
           var buttonType = button.get("v.label");
           //alert(buttonType);
           var contactId = event.getSource().get("v.value");
           var toastEvent = $A.get("e.force:showToast");
           //alert(contactId);
           var action = component.get('c.checkinContacts');
           action.setParams({
               "contactId": contactId,
           });
           
           var self = this;
           action.setCallback(this, function(actionResult) {
               var state= actionResult.getState();
               if(state=='SUCCESS'){
   
       toastEvent.setParams({
           "type": "success",
           "duration": "1000",
           "title": "Succès!",
           "message": "La personne a bien été enregistrée / désenregistrée."
           
       });
                   toastEvent.fire();
                   //button.set('v.disabled',true);
                   //button.set('v.label','Désenregistrement');
                   if (buttonType === 'Enregistrement') {
                       button.set('v.label','Désenregistrement');
                   } else {
                       button.set('v.label','Enregistrement');
                   }
                   $A.get('e.force:refreshView').fire();
               }
           });
           $A.enqueueAction(action);
         }
   })
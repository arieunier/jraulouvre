({
    init: function(component, event, helper) {
       helper.loadList(component);
    },
    handleNameFilterChange: function (component, event, helper) {
       helper.loadList(component);
    },        
   selectChange: function(component, event, helper) {
       helper.updateContact(component,event);
   }
})

Ecomarket.Utils = Ecomarket.Utils || (function(){
    var module = {};

    module.extractMixpanelPropertiesFromForm = function(form, eventMap){
        var properties = {};
        var $form = $(form);
        $.each(eventMap, function(formFieldId, propertyName){
            var field = $form.find(formFieldId);
            var value;
            if( field.is('select') ) {
                value = $('option:selected', field).text();
            }
            else {
                value = field.attr("value");
            }
            properties[propertyName] = value;
        });
        return properties;
    };

    module.getPropertiesFromProductForm = function(form){
        var $form = $(form);
        var properties = module.extractMixpanelPropertiesFromForm($form,
            {
                "#id_title": "Title",
            "#id_description": "Description",
            "#id_primary_category": "Main Category",
            "#id_secondary_category": "Secondary Category",
            "#id_causes": "Product Causes",
            "#id_colors": "Main Colours",
            "#id_keywords": "Keywords",
            "#id_ingredients": "Ingredients",
            "#id_materials": "Eco Materials",
            "#id_occasions": "Occasions",
            "#id_recipients": "Recipients",
            "#id_price-amount_0": "Price"
            });
        var unlimitedStock = $('#stock-level').attr('value') == "unlimited";
        if(unlimitedStock){
            properties["Unlmited Stock"] = true;
        }else{
            properties["Unlimited Stock"] = false;
            var stock = $('#stock').attr('value');
            if(stock == ''){
                stock = 0;
            }
            properties["Number in Stock"] = stock;
        }
        var shippingProfileId = $('#select-id_shipping_profile').attr('value');
        if(shippingProfileId == ''){
            properties["Uses Old Profile"] = false;
        }else{
            properties["Uses Old Profile"] = true
        }
        var shipsWorldwide = $('#shipping-profile-worldwide').attr('value');
        if(shipsWorldwide == 0){
            properties["Ships Worldwide"] = true;
        }else{
            properties["Ships Worldwide"] = false;
        }
        return properties;
    }


    return module;
})();



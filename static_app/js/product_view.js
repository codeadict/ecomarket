/*jslint browser: true*/
/*global $, _, ZeroClipboard, jQuery, Ecomarket */
"use strict";

Ecomarket.ProductView = Ecomarket.ProductView || (function(){
    var module = {};

    module.ShippingRule = function(attributes){
        this.initialize(attributes);
    };
    _.extend(module.ShippingRule.prototype, {
        initialize: function(attributes){
            this.countries = attributes.countries;
            this.rulePrice = attributes.rule_price;
            this.rulePriceExtra = attributes.rule_price_extra;
        },

        appliesToCountry: function(candidateCountry){
            return _.find(this.countries, function(country){
                return country.code === candidateCountry.code;
            });
        }
    });


    module.ShippingProfile = function(attributes){
        this.initialize(attributes);
    };
    _.extend(module.ShippingProfile.prototype, {
        initialize: function(attributes){
            this.rules = _.map(attributes.rules, function(ruleObj){
                return new module.ShippingRule(ruleObj);
            });
            this.defaultCountryCode = attributes.default_country_code;
            this.activeCountry = this.getDefaultCountry();
            this.shipsWorldwide = attributes.ships_worldwide;
            this.shipping_country = attributes.shipping_country;
            if(this.shipsWorldwide){
                this.worldWideRule = {
                    rulePrice: attributes.others_price,
                    rulePriceExtra: attributes.others_price_extra
                };
            }
        },

        getCountries: function(){
            var countryLists = _.map(this.rules, function(rule){
                return rule.countries;
            });
            return _.flatten(countryLists);
        },

        getCountryByCode: function(countryCode){
            var country = _.find(this.getCountries(), function(country){
                return country.code === countryCode;
            });
            if(typeof country === "undefined"
                || countryCode === "rest-of-world"){
                return  {
                    code: "rest-of-world",
                    title: "The rest of the world"
                };
            }
            return country;
        },

        getDefaultCountry: function(){
            if( !this.rules.length && this.shipsWorldwide ) {
                return this.getCountryByCode('rest-of-world');
            }
            return _.find(this.getCountries(), function(country){
                return country.code === this.defaultCountryCode;
            }, this);
        },

        getRuleForCountry: function(country) {
            // XXX: Is rule ever not undefined here?
            if( (typeof rule === 'undefined') && this.shipsWorldWide){
                return this.worldWideRule;
            }
            if( typeof country === 'undefined' || country.code === "rest-of-world" ){
                return this.worldWideRule;
            }
            var rule = _.find(this.rules, function(rule){
                return rule.appliesToCountry(country);
            });
            return rule;
        }

    });

    /*
     Free shipping
     */

    module.FreeShipping = function(shippingData, shippingSelector, profile, price) {
        this.initialize(shippingData, shippingSelector, profile, price);
    };

    _.extend(module.FreeShipping.prototype, {
        initialize: function(shippingData, shippingSelector, profile, price) {
            this.$freeShippingLabel = $(shippingSelector);
            this.data = shippingData;
            this.profile = profile;
            this.price = price;

            this.hasFreeShipping = false;
        },

        checkForFreeShipping: function (rule, destination) {
            var shipping_country = this.profile.shipping_country;
            var entry;
            //var foundOrigin = [];
            var foundDestination = [];
            var match = false;
            var amount = 0;

            for (var x=0;x<this.data.length;x++) {
                entry = this.data[x];

                // check for correct origin
                // DISABLED: http://bit.ly/18JuGZi
                //  foundOrigin = $(entry.origin).filter(function() {
                //  return this.code == shipping_country.code;
                //});

                // check for correct destination
                foundDestination = $(entry.destination).filter(function() {
                    return this.code == destination.code;
                });

                if(foundDestination.length > 0) {
                    match = true;
                    break;
                }
            }

            if (match) {
                amount = this.price * entry.discount;

                if (rule.rulePrice < amount) {
                    this.hasFreeShipping = true;
                } else {
                    this.hasFreeShipping = false;
                }
            } else {
                this.hasFreeShipping = false;
            }
        }
    });

    /*
     ShippingDropDown
     */

    module.ShippingDropDown = function(dropdownSelector, itemPriceSelector, extraItemPriceSelector, shippingProfile, freeShippings){
        this.initialize(dropdownSelector, itemPriceSelector, extraItemPriceSelector, shippingProfile, freeShippings);
    };

    _.extend(module.ShippingDropDown.prototype, {
        initialize: function(dropDownSelector, itemPriceSelector, extraItemPriceSelector, shippingProfile, freeShippings){
            this.$dropDown = $(dropDownSelector);
            this.$dropDown.on("change", _.bind(this.onShippingCountryChanged, this));
            this.$itemPrice = $(itemPriceSelector);
            this.$extraItemPrice = $(extraItemPriceSelector);
            this.profile = shippingProfile;
            this.freeShipping = freeShippings;
            this.activeCountry = this.profile.getDefaultCountry();
            this.render();
        },

        onShippingCountryChanged: function(event){
            var countryCode = this.$dropDown.attr("value");
            this.activeCountry = this.profile.getCountryByCode(countryCode);
            this.render();
        },

        render: function(){
            if (!this.activeCountry) {
                return null;
            }
            var rule = this.profile.getRuleForCountry(this.activeCountry);
            this.freeShipping.checkForFreeShipping(rule, this.activeCountry);

            if(this.freeShipping.hasFreeShipping) {
                this.freeShipping.$freeShippingLabel[0].innerHTML = "this has FREE delivery to the UK!";
                window.currency.render(this.$itemPrice, 0.0);
                window.currency.render(this.$extraItemPrice, 0.0);
            }
            else {
                this.freeShipping.$freeShippingLabel[0].innerHTML = "&nbsp;";
                window.currency.render(this.$itemPrice, rule.rulePrice.toFixed(2));
                window.currency.render(this.$extraItemPrice, rule.rulePriceExtra.toFixed(2));
            }

//            window.currency.render(this.$itemPrice, rule.rulePrice.toFixed(2));
//            window.currency.render(this.$extraItemPrice, rule.rulePriceExtra.toFixed(2));
//            this.$dropDown.val(this.activeCountry.code);
        }
    });

    return module;
}());

jQuery(document).ready(function ($) {
    if( $('#eco-descriptions').length ) {
        $.get('credentials', {}, function(data, status){
            $('#eco-descriptions').html(data);
        });
    }

    // shipping_profile populated by view
    window.profile = new Ecomarket.ProductView.ShippingProfile(window.shipping_profile);
    window.freeShipping = new Ecomarket.ProductView.FreeShipping(
        window.free_shippings,
        "#free-shipping",
        profile,
        window.product_price
    );
    window.shippingDropdown = new Ecomarket.ProductView.ShippingDropDown(
        "#shipping_country",
        "#item-shipping-cost",
        "#extra-item-shipping-cost",
        window.profile,
        window.freeShipping
    );
});

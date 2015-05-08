/*jslint browser: true*/
/*global $, ZeroClipboard, jQuery, mixpanel */
"use strict";

var price_currency = function(price) {
    return currency.symbol()+ " " + price.text;
}

Ecomarket.Widgets.SelectsPrice = function (selector, select_params) {
    selector = selector || $('#id_price');
    selector.each(function (index, item) {
        var num;
        item = $(item);
        num = 8;
        if (item.data('search') === 'hide') {
            num = 99;
        }
        select_params = (typeof (select_params) === 'function') ? select_params(this) : {
			minimumResultsForSearch: num,
			formatResult: price_currency,
			formatSelection: price_currency,
			escapeMarkup: function(m) { return m; }
        };
        $(item).select2(select_params);
    });
};

jQuery(document).ready(function ($) {
	if (Ecomarket.Widgets.SelectsPrice)
		Ecomarket.selects_price = new Ecomarket.Widgets.SelectsPrice();
});

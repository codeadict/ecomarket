var currency = function() {
    var _user_currency = 'GBP';
    var _user_country = 'UK';
    var _all_currency_rates = all_currency_rates;
    var _all_currency_symbols = all_currency_symbols;
    
    var price = function(amount) {
        if (amount != null) {
            var number = amount;
            if( _user_currency != 'GBP' ) {
                number = (Math.round(amount * _all_currency_rates[_user_currency] * 100)/100);
            }

            if( -1 != $.inArray(_user_currency, ['JPY', 'INR']) ) {                                
                return number.toString().split('.')[0];
            }

            var s = number.toString();
            if (s.indexOf('.') == -1) s += '.';
            while (s.length < s.indexOf('.') + 3) s += '0';
            return s;
        }
    }
    
    var symbol = function() {
        return _all_currency_symbols[_user_currency];
    }
    
    var code = function() {
        return _user_currency;
    }
    
    var findCurrency = function(region) {
        if (region == null)
            region = _user_currency;
        europe = ['AD', 'AT', 'BE', 'CY', 'EE', 'FI', 'FR', 'DE', 'GR', 'IE', 'IT', 'XK', 'LU', 'MT', 'MC', 'ME', 'NL', 'PT', 'SM', 'SK', 'SI', 'ES', 'VA']
        if (region == 'US') {
            return 'USD';
        } else if (europe.indexOf(region) != -1) {
            return 'EUR';
        } else if (region == 'JP') {
            return 'JPY';
        } else if (region == 'IN') {
            return 'INR';
        } else if (region == 'SE') {
            return 'SEK';
        } else if (region == 'CA') {
            return 'CAD';
        } else if (region == 'AU') {
            return 'AUD';
        } else {
            return 'GBP';
        }
    }
    
    var setCurrency = function(code, saveToDb) {
        _user_currency = code;
        if (saveToDb)
        	saveCurrency();
    }
    
    var saveCurrency = function() {
    	$.ajax({
    		url: '/accounts/currency/save/',
    		data: {
    			'currency': _user_currency
    		},
    	});
    }
    
    var country = function() {
        return _user_country;
    }
    
    var countryId = function() {
        if (countries) {
            country = _.find(countries, function(country) {
                return country.code == _user_country;
            });
            if (country)
				return country.id;
        }
    }
    
    var setCountry = function(country) {
        if (!parseInt(country)) {
            _user_country = country;
            _user_currency = findCurrency(_user_country);
        } else if (countries) {
            countryId = parseInt(country);
            country = _.find(countries, function(country) {
                return country.id == countryId;
            });
            _user_country = country.code;
            _user_currency = findCurrency(_user_country);
        }
    }
    
    var render = function($el, amount) {
        $el.find('.amount_currency_symbol').text(symbol());
        $el.find('.amount_amount').text(price(amount));
        $el.find('.amount_currency_code').text(_user_currency);
        
		// Update the 'amount' data attribute to reflect the current amount
		$el.data('amount', amount);
    }
    
    var changeAll = function(parent) {
		if (parent == null)
			parent = $('body');
		parent.find('.amount_currency_convert').each(function() {
			if ($(this).data('approx') == true && code() == "GBP")
				$(this).hide();
			else if ($(this).data('amount')) {
				$(this).show();
				render($(this), $(this).data('amount'));
			}
		});
		if (Ecomarket.Widgets.SelectsPrice)
			Ecomarket.selects_price = new Ecomarket.Widgets.SelectsPrice();
	}
    
    return {
        price: price,
        symbol: symbol,
        code: code,
        country: country,
        countryId: countryId,
        render: render,
        
        setCountry: setCountry,
        setCurrency: setCurrency,
        
        changeAll: changeAll,
    }
}();

var currency_dropdown_click = function(e) {
	preferred_currency = $(this).data('value');
	// true is passed to force saving the data to non-logged in user session, OR logged-in user profile + session
	currency.setCurrency(preferred_currency, true);
	// This click is triggered to close the dropdown
	$(this).parent('.dropdown').removeClass('open');
	$('.currency .dropdown a.current').html(
		'<i class="icon icon-' + preferred_currency.toLowerCase() + '"></i> ' + preferred_currency + ' <b class="caret"></b>&nbsp;');
	currency.changeAll();
	e.preventDefault();
	
	render_top_menu_currency_list();
}

var render_top_menu_currency_list = function() {
	// Setup the top menu currency dropdown with all the currencies supported, except the one selected
    $('.currency .dropdown .dropdown-menu').find('li').remove();
    $('.currency .dropdown .dropdown-menu').html('');
    $.each(all_currency_symbols, function(code, sym) {
		if (code != currency.code())
			$('.currency .dropdown .dropdown-menu').append('<li data-value="' + code + '"><a href="#"><i class="icon icon-' + code.toLowerCase() + '"></i> ' + code + '</a></li>');
    });
    $('.currency .dropdown li').click(currency_dropdown_click);
}

$(function() {
	// user's current country comes from CloudFlare, and is set in the variable user_country
	currency.setCountry(user_country);
	
	// preferred_currency comes from web server if the user has set a preference from the top dropdown.
	if (preferred_currency) {
		currency.setCurrency(preferred_currency);
		$('.currency .dropdown a.current').html(
			'<i class="icon icon-' + preferred_currency.toLowerCase() + '"></i> ' + preferred_currency + ' <b class="caret"></b>&nbsp;');
	} else {
		// if user has not set any preferred_currency then we get the currency from the current country.
		$('.currency .dropdown a.current').html(
			'<i class="icon icon-' + currency.code().toLowerCase() + '"></i> ' + currency.code() + ' <b class="caret"></b>&nbsp;');
	}
	
	render_top_menu_currency_list();
    
    /* Handle the click event for the top menu currency dropdown.
     * Set the preference in the backend.
     * Change all prices on the page accordingly.
     */
    $('.currency .dropdown li').click(currency_dropdown_click);
    
    currency.changeAll();
});

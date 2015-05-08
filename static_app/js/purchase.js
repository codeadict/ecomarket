// Purchase related JS
/*global _, Ecomarket, Backbone, mixpanel */

// The arguments to this are global variables created by the template.
Ecomarket.Purchase = (function(cart_id, countries){
    var module = {};

    module.CartStall = Backbone.RelationalModel.extend({
        urlRoot: '/checkout/cart_stalls',
        relations: [{
            type: Backbone.HasMany,
            key: 'cart_products',
            relatedModel: 'Ecomarket.Purchase.CartProduct',
            reverseRelation: {
                key: 'cartStall',
                includeInJSON: 'id'
            }
        }],

        initialize: function(){
            this.get("cart_products").bind("destroy", _.bind(this.cartProdRemoved, this));
        },

        setCountry: function(countryId){
            countryId = parseInt(countryId, 10);
            var newCountry = _.find(countries, function(country){
                return country.id === countryId;
            });
            this.set("country", newCountry);
            if(this.shippingPossible()){
                this.save({}, {
                    success: function(model, response) {
                        window.location.reload();
                    }
                });
            }
        },

        cartProdRemoved: function(){
            if(this.get("cart_products").length === 0){
                this.destroy();
            }
        },

        shippingPossible: function(){
            var countryId = this.get("country").id,
                countryAllowed = _.any(this.get("countries"), function(country){
                return country.id === countryId;
            });
            return countryAllowed;
        },

        getNumItems: function(){
            var total = 0;
            _.each(this.get("cart_products").models, function(cart_prod){
                total += cart_prod.get("quantity");
            });
            return total;
        }

    });

    module.Cart = Backbone.Collection.extend({
        model: module.CartStall,
        url: '/checkout/cart_stalls'

    });

    module.CartProduct = Backbone.RelationalModel.extend({
        url: function(){
            return '/checkout/cart/' + cart_id + '/products/' + this.get("product").id;
        },

        save: function(attributes, options){
            if(options === undefined){
                options = {};
            }

            // The backend methods for cart products return a bunch of info
            // on the updated totals for the cart stall. We need to update the
            // client side model.
            options.success = function(model, response){
                //back reference set by backbone-relational
                var cs = model.get("cartStall");
                if( response.quantity > 0 ) {
                    cs.set("delivery", response.delivery);
                    cs.set("subtotal", response.subtotal);
                    cs.set("discount", response.discount);
                    cs.set("total", response.total);
                }
                else {
                    cs.set("delivery", 0.00);
                    cs.set("subtotal", 0.00);
                    cs.set("discount", 0.00);
                    cs.set("total", 0.00);   
                }
            };
            // call super
            Backbone.RelationalModel.prototype.save.call(this, attributes, options);
        }

    });


    module.CartView = Backbone.View.extend({

        initialize: function(){
            this.collection.bind("destroy", _.bind(this.onDestroy, this));
            _.bindAll(this, "renderCartFull");
        },

        render: function(){
            if(this.collection.length > 0){
                this.renderCartFull();
            }else{
                this.renderCartEmpty();
            }
        },

        renderCartEmpty: function(){
            var emptyCartMessage = this.$el.find('#empty-cart-message');
            emptyCartMessage.show();
        },

        renderCartFull: function(){
            var that = this;
            this.collection.each(function(model){
                var cartStallViewElement = new module.CartStallView(
                    {
                    model: model,
                    cartIndicatorView: that.options.indicator
                }).render().el;
                that.$el.find('h2').after(cartStallViewElement);
            });
        },

        onDestroy: function(){
            // irritatingly this duplicates the logic in the render
            // method, this is because we don't want to render if
            // the collection is not empty as this will re-render
            // all the subviews.
            if(this.collection.length === 0){
                this.render();
            }
            this.options.indicator.update();
        }

    });

    module.CartIndicatorView = Backbone.View.extend({

        update: function(){
            if(this.calculateNumProducts() !== 0){
                this.$el.text(this.calculateNumProducts());
                this.$el.show();
            }else {
                this.$el.hide();
            }
        },

        calculateNumProducts: function(){
            var total = 0;
            this.collection.each(function(cartStall){
                total += cartStall.get("cart_products").length;
            });
            return total;
        }

    });

    module.CartProductView = Backbone.View.extend({
        tagName: 'li',
        className: 'order-item',

        initialize: function(){
            this.template = _.template($('#cart_product_template').html());
            this.model.on("change", this.render, this);
        },

        bindEvents: function(){
            var increase = _.bind(this.increaseQuantity, this),
                decrease = _.bind(this.decreaseQuantity, this);
            this.$el.find(".btn-plus").on("click", function() {
                if (typeof window.ClickTaleExec === 'function') {
                    window.ClickTaleExec('$("' + $(this).getPath() + '").click()');
                }
                increase();
            });
            this.$el.find(".btn-minus").on("click", function() {
                if (typeof window.ClickTaleExec === 'function') {
                    window.ClickTaleExec('$("' + $(this).getPath() + '").click()');
                }
                decrease();
            });
        },

        render: function(){
            var data = this.model.toJSON(),
                remove = _.bind(this.removeSelf, this);
            this.$el.html(this.template({
                cart_product:data,
                product:data.product
            }));
            this.$el.find('.remove-product').on("click", function() {
                if (typeof window.ClickTaleExec === 'function') {
                    window.ClickTaleExec('$("' + $(this).getPath() + '").click()');
                }
                remove();
            });
            this.bindEvents();
            return this;
        },

        increaseQuantity: function(){
            var attrs = {quantity: this.model.get("quantity") + 1};
            this.model.save(attrs, {wait: true, error: _.bind(this.onSaveError, this)});
        },

        decreaseQuantity: function(){
            var attrs = {quantity: this.model.get("quantity") - 1};
            this.model.save(attrs, {wait: true});
        },

        onSaveError: function(model, xhr, options){
            var error = JSON.parse(xhr.responseText),
                alert = new Ecomarket.Notifications.ErrorAlert({heading: error.error_title, message: error.error_message});
            alert.show();
        },

        /**
         * NOTE: The backend does not deliver an updated cart stall.
         * As a quick solution the whole page gets reloaded after a product is properly removed
         * from the cart stall
         */
        removeSelf: function(){
            this.remove();
            this.model.destroy({
                success: function(model, response) {
                    window.location.reload();
                }
           });
        }
    });

    module.CartStallView = Backbone.View.extend({
        tagName: 'div',
        className: 'order-box',

        initialize: function(){
            this.template = _.template($('#cart_stall_template').html());
            // _.bindAll(this);
            this.model.bind("change", _.bind(this.modelChanged, this));
            this.model.get("cart_products").bind("destroy", _.bind(this.cartProductRemoved, this));
        },

        render: function(){
            this.$el.html(this.template({cart_stall: this.model}));
            $('input, textarea').placeholder();
            this.bindEventsToHtmlElements();
            this.$el.find('#shipping-country').select2();
            var that = this;
            this.model.get('cart_products').each(function(cart_product){
                var cart_prod_view = new module.CartProductView({model:cart_product});
                that.$el.find('.orders').append(cart_prod_view.render().el);
            });
            return this;
        },

        bindEventsToHtmlElements: function(){
            this.bindShippingEvent();
            this.bindRemoveEvent();
            this.bindNextStepEvent();
            this.bindCouponUpdatedEvent();
            this.bindCouponUpdateButtonEvent();
            this.bindNoteUpdatedEvent();
            this.updateShippingButton();
        },

        bindShippingEvent: function(){
            var model = this.model;
            this.$el.find('select#shipping-country').on("change", function(){
                model.setCountry($(this).attr("value"));
            });
        },

        bindRemoveEvent: function(){
            var model = this.model,
                that = this;
            this.$el.find('.remove-group').on("click", function(){
                model.destroy();
                that.options.cartIndicatorView.update();
                that.remove();
            });
        },

        bindNextStepEvent: function(){
            var that = this;
            this.$el.find('.btn-paypal').on('click', _.bind(this.onNextButtonClicked, this));
        },

        bindCouponUpdatedEvent: function() {
            this.getCouponInput().on('change', _.bind(this.onCouponInputChanged, this));
        },

        bindCouponUpdateButtonEvent: function() {
            this.getCouponUpdateButton().on('click', _.bind(this.onCouponUpdateButtonClicked, this));
        },

        bindNoteUpdatedEvent: function(){
            this.getNoteTextarea().on('change', _.bind(this.onNoteTextareaChanged, this));
        },

        cartProductRemoved: function(){
            this.options.cartIndicatorView.update();
            if(this.model.get("cart_products").length === 0){
                this.remove();
            }
        },

        modelChanged: function(){
            this.updateTotals();
            this.updateShippingButton();
        },

        updateTotals: function(){
            // This is a bit of a hack and should probably be implemented as a
            // change listener on the Cart. Unfortunately the cart is currently
            // a collection rather than a relational model,
            // TODO: Refactor once cart is moved to a model.
            //window.location.reload();
            this.options.cartIndicatorView.update();
            
            window.currency.render(this.$el.find('.subtotal-value'), this.model.get("subtotal"));
            window.currency.render(this.$el.find('.total-value'), this.model.get("total"));
            window.currency.render(this.$el.find('.discount-value'), this.model.get("discount"));
            window.currency.render(this.$el.find('.delivery-value'), this.model.get("delivery"));
        },

        updateShippingButton: function(){
            var btn = this.$el.find('.btn-paypal'),
                alert_ = this.$el.find('.shipping-alert');
            if(this.model.shippingPossible() && this.model.getNumItems() > 0 ){
                btn.removeClass('btn-disabled');
                btn.addClass('btn-primary');
                btn.attr("disabled", false);
                alert_.hide();
            }
            else{
                btn.addClass('btn-disabled');
                btn.removeClass('btn-primary');
                btn.attr("disabled", true);

                if( ! this.model.shippingPossible() ) {
                    alert_.show();
                }
            }
        },

        onNextButtonClicked: function(event){
            var that = this,
                link, register_modal, noteText;
            event.preventDefault();
            if(!this.model.shippingPossible() || this.model.getNumItems() < 1 ){
                event.preventDefault();
                return;
            }
            if( this.$el.find('.btn-paypal').data('user-id') === '' ) {
                link = $(event.target);
                register_modal = $('#register-modal');
                register_modal.data('tempAction', '/register/?next=' + link.attr('href'));
                register_modal.modal('show');
                return event.preventDefault();
            }
            noteText = this.getNoteTextarea().val();
            this.model.set("note", noteText);
            this.model.save({}, {success: function(model, response){
                that.mixpanelTrackNextButton(function(){
                    document.location.href = model.get("shipping_url");
                });
            }});
        },

        mixpanelTrackNextButton: function(callback){
            mixpanel.track("Clicked Next Step in Cart", {
                "Number of Products in Cart": this.model.get("cart_products").length,
                "Number of Items in Cart": this.model.getNumItems(),
                "Has Special Message": this.model.get("note") !== "",
                "Delivery Country": this.model.get("country").title
            }, callback);
        },

        onCouponInputChanged: function(e, callback) {
            if (!callback) { callback = function() {}; }
            var input = this.getCouponInput();
            this.model.set("coupon", input.val());
            this.model.save({}, {success: callback});
        },

        onCouponUpdateButtonClicked: function(e) {
            this.onCouponInputChanged(e, function() {
                // TODO: Re-fetch model data and re-render the template part,
                // without reloading the whole window.
                window.location.reload();
            });
        },

        onNoteTextareaChanged: function(){
            var noteText = this.getNoteTextarea().val();
            this.model.set("note", noteText);
            this.model.save();
        },

        getCouponInput: function() {
            return this.$el.find(".coupon>input:text");
        },

        getCouponUpdateButton: function() {
            return this.$el.find(".coupon>input:button");
        },

        getNoteTextarea: function(){
            return this.$el.find('.notes textarea');
        }
    });

    return module;
}(window.cart_id, window.countries));

$(function() {
    var cart_stalls, cartIndicator, cartView;
    window.ClickTaleSettings = { XHRWrapper: { Enable: true} };
    // XXX: Is this duplication?
    $.ajaxSetup({
        headers: { "X-CSRFToken": window.csrfmiddlewaretoken },
        cache: false
    });

    if( typeof window.cart_stall_data === "undefined" ) {
        window.cart_stall_data = [];
    }

    cart_stalls = new Ecomarket.Purchase.Cart(window.cart_stall_data);
    if ( window.cart_stall_data.length === 0 ) {    // Fetch if necessary
        cart_stalls.fetch({async: false});
    }
    cartIndicator = new Ecomarket.Purchase.CartIndicatorView({collection: cart_stalls});
    cartIndicator.setElement($('em.cart-badge'));
    cartView = new Ecomarket.Purchase.CartView({
        collection: cart_stalls, indicator: cartIndicator
    });
    cartView.setElement($('div.primary-content-wrap').find('#cart-container'));
    //cartView.collection = cart_stalls;
    cartView.render();
});

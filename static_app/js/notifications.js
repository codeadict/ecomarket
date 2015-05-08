Ecomarket.Notifications = (function(){
    module = {};

    var Alert = module.Alert = function(options){
        this.initialize.call(this, options);
    };

    _.extend(Alert.prototype, {
        initialize: function(options){
            var defaults = {
                alertContainerSelector: 'div#alert-container'
            };
            _.extend(this, defaults, options);
            this.template = _.template($('#alert-template').html());
            this.$alertContainer = $(this.alertContainerSelector);
        },

        show: function(message){
            data = {message: this.message, heading: this.heading, type: this.getType()};
            this.$el = $(this.template(data));
            this.el = this.$el[0];
            this.bindEvents();
            this.$alertContainer.append(this.el);
        },

        bindEvents: function(){
            this.$el.find('.close').on('click', _.bind(this.remove, this));
        },

        remove: function(){
            this.$el.remove();
        },

    });

    //Simplified copy of Backbones' extend.
    Alert.extend = function(protoProps){
        var parent = this;
        var child = function(){ parent.apply(this, arguments);};

        var Surrogate = function(){ this.constructor = child; };
        Surrogate.prototype = parent.prototype;
        child.prototype = new Surrogate;

        _.extend(child.prototype, protoProps);
        return child;
    }

    var ErrorAlert = module.ErrorAlert = Alert.extend({
        getType: function(){
            return "error";
        },
    });

    var WarningAlert = module.WarningAlert = Alert.extend({
        getType: function(){
            return "warning";
        }
    });

    var SuccessAlert = module.SuccessAlert = Alert.extend({
        getType: function(){
            return "success";
        },
    });

    var InformationAlert = module.InformationAlert = Alert.extend({
        getType: function(){
            return "information";
        }
    });

    var AnswerAlert = module.AnswerAlert = Alert.extend({
        getType: function(){
            return "answer";
        },
    });


    return module;
})();

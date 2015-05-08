/**
 * Handling of 'loaded' event for modal with remote is not available by default.
 * Read this - https://github.com/twitter/bootstrap/pull/6846
 **/

(function(){
    $.fn.jqueryLoad = $.fn.load;

    $.fn.load = function(url, params, callback) {
        var $this = $(this);
        var cb = $.isFunction(params) ? params: callback || $.noop;
        var wrapped = function(){
            cb(arguments);
            $this.trigger('loaded');
        };

        if ($.isFunction(params)) {
            params = wrapped;
        } else {
            callback = wrapped;
        }

        $this.jqueryLoad(url, params, callback);

        return this;
    };
})();

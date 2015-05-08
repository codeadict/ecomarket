(function( $ ) {
    // jQuery plugin which tracks changes in a form, initialize it by calling
    // $(selector).fieldtracker() and thereafter retrieve changes by calling
    // $(selector).fieldtracker('changedFields') to retrieve a list of changed
    // field names.

    var hashDiff = function(h1, h2) {
        var d = [];
        for (k in h2) {
            if (h1[k] !== h2[k]){
                d.push(k);
            }
        }
        return d;
    }

    var convertSerializedArrayToHash = function(a) {
        var r = {};
        for (var i = 0;i<a.length;i++) {
            r[a[i].name] = a[i].value;
        }
        return r;
    }

    var methods = {
        init: function(){
            return this.each(function(){
                var $this = $(this);
                var data = $this.data('fieldTracker');
                if(!data){
                    $this.data({fieldTracker: {originalFields: $this.serializeArray()}})
                }
            });
        },

        changedFields: function(){
            result = [];
            this.each(function(){
                var $this = $(this);
                var hash1 = convertSerializedArrayToHash($this.serializeArray());
                var hash2 = convertSerializedArrayToHash($this.data('fieldTracker').originalFields);
                var changedFields = hashDiff(hash1, hash2);
                result = result.concat(changedFields);
            });
            return result;
        }
    }

    $.fn.fieldtracker = function( method ) {
        if ( methods[method] ) {
            return methods[method].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.fieldtracker' );
        }
    }

})( jQuery );

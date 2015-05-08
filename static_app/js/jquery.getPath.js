/**
 * jQuery.fn.getPath
 * 
 * Retrieves the specific path to a DOM object in relation to its topmost parent.
 * 
 * @date 2009-07-31
 */
(function(e){function t(){var t=e(this).attr("id");if(t){t="#"+t}return t||""}function n(){return this.tagName.toLowerCase()}function r(){if(!this.parentNode){return""}var t=e(this.parentNode).children(this.tagName);if(t.length===1){return""}return":eq("+t.index(this)+")"}e.fn.getPath=function(i){var i=e.extend({full:false,limit:false},i);if(typeof this.get(0).tagName==="undefined"){return false}var s=e(this).get(0),o=[],u=u?u:0,a=0,f=0,l=e(s).closest("body").length?true:false,c=false;do{if(typeof s.tagName==="undefined"){break}a++;if(i.limit&&f==i.limit){continue}f++;var h=t.apply(s);if(h){o[o.length]=h;if(!i.full){break}}else{h=n.apply(s)+r.apply(s)}o[o.length]=h}while(s=e(s).parent().get(0));if(!l&&a===f&&o[o.length-1]==="div"){o.splice(o.length-1,1)}return o.reverse().join(" > ")}})(jQuery)

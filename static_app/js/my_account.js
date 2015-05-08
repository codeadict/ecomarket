// MyAccount related JS

Ecomarket.MyAccount.SelectAll = function(){
    var selector = "input:checkbox[name='messages']";
    if($(selector).length == 0) return;

    $(document).on("click", selector, function(event) {
        var $all_rows = $("input:checkbox[name='ids']");
        if ($(this).attr("checked") == "checked"){
            $all_rows.attr("checked", "checked");
        }
        else{
            $all_rows.removeAttr("checked");
        }
    });
};

Ecomarket.MyAccount.BulkAction = function(){
  var selector = "div.actions a";
  if($(selector).length == 0) return;

  $(document).on("click", selector, function(event) {
    var action = $(this).attr('data-action');
    if (action == undefined)
      return;

    var show_prompt = $(this).attr('data-prompt');
    if(show_prompt=="yes"){
        var value = prompt("Enter new value", 1);
        $("input[name='"+ action + "']").val(value);
    }

    var queryset = get_query_set_as_object();

    $("input[name='action']").val(action);
    if ("page" in queryset) {
      $("input[name='page']").val(queryset["page"])
    }
    var overlay = $('.overlay');
    console.log(overlay);

    if (overlay != undefined) {
      overlay.show();
    }

    window.has_changes = false;
    $("#bulk_form").submit();
  });
};

jQuery(document).ready(function($){
    Ecomarket.MyAccount.select_all = new Ecomarket.MyAccount.SelectAll();
    Ecomarket.MyAccount.bulk_action = new Ecomarket.MyAccount.BulkAction();

  window.has_changes = false;

  /**
   * Handles the checkboxes to mark a products stock "unlimited"
   */
  $('.stock_checkbox').change(function(event) {
    var target = event.target;
    // select text input.
    // This works as long as the text input is right before the checkbox!
    var input = $("#"+target.name);

    if (target.id.search("zero") > -1) {
      input.val('0').attr('readonly', 'readonly');
    }
    else {
      input.val('-1').attr('readonly', 'readonly');
    }
  });

  $('.stock_input').keydown(function(e) {
     if (e.shiftKey)
       e.preventDefault();
     else {
       var nKeyCode = e.keyCode;
       //Ignore Backspace and Tab keys
       if (nKeyCode == 8 || nKeyCode == 9)
        return;
        if (nKeyCode < 95) {
          if (nKeyCode < 48 || nKeyCode > 57)
            e.preventDefault();
        }
        else {
          if (nKeyCode < 96 || nKeyCode > 105)
            e.preventDefault();
        }
     }
   }).click(function(event) {
    var target = $(this);
    var id = target.attr('id');

    if (target.is('[readonly]')) {
      window.has_changes = true;
      target.removeAttr('readonly');
      target.val('1');
      target.select();
      $('input[name="' + id + '"]').prop('checked', false);
    }
   }).focusout(function(event) {
      var target = $(this);
      if (!target.val()) {
        $('#' + target.attr('id') + '-zero').prop('checked', true);
        target.val('0').attr('readonly', 'readonly');
      }
    });

  $('.stock_input, .stock_checkbox').bind('change paste keyup', function() {
    window.has_changes = true;
  });

    $(window).bind('beforeunload', function() {
      if (window.has_changes)
        return 'WARNING! You have not yet saved & confirmed your stock check and your changes are about to be lost. To save changed you must click the confirm button at the bottom of the page. Are sure you want to leave the page and lose your current changes?';
    });

  /*
    VIDEOS
   */

  $('.videosplash').on('click', function(){
    var embed_url = $(this).attr('data-source');
    var videoModal = $('#videoModal');
    var body = videoModal.children('.modal-body');
    body.html('<iframe src="' + embed_url + '" width="400" height="300" ' +
      'frameborder="0" allowfullscreen> Your browser does not support iframes </iframe>');
  });
});

function get_query_set_as_object() {
  var vars = [], hash;
  var q = document.URL.split('?')[1];
  if(q != undefined) {
    q = q.split('&');
      for(var i = 0; i < q.length; i++){
        hash = q[i].split('=');
        vars.push(hash[1]);
        vars[hash[0]] = hash[1];
    }
  }
  return vars;
}
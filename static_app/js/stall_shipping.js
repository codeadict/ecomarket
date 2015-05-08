/*jslint browser: true*/
/*global $, Ecomarket, jQuery */
"use strict";

Ecomarket.shipping_rule_adders = [];

function update_worldwide_visibility (shipping_profiles) {
    var sp_el = $(shipping_profiles);
    if( $('#shipping-profile-worldwide').val() == '1' ) {
        $('.shipping-profile-worldwide-prices', sp_el).show();
    }
    else {
        $('.shipping-profile-worldwide-prices', sp_el).hide();   
    }    
}

Ecomarket.Stall.ShippingProfile = function (shipping_profiles) {
    var shipping_profile_changed, signal_change;
    shipping_profile_changed = false;
    signal_change = function () {
        if (!shipping_profile_changed) {
            shipping_profile_changed = true;
            // TODO: create hidden field to record change
        }
    };

    update_worldwide_visibility(shipping_profiles);

    /* $('select#select-id_shipping_profile')
        .select2({allowClear: true}); */

    $('#id_shipping-title')
        .live('blur keyup', signal_change);

    $('.shipping-profile-worldwide-prices input.price')
        .live('blur', signal_change);

    $('input#id_shipping-shipping_postcode')
        .live('blur keyup', signal_change);

    $('select#select-id_shipping-shipping_country')
        .live('change', signal_change);

    /* switch shipping profile */
    $('select#select-id_shipping_profile')
        .live('change', function (evt) {
            var profile_id, shipping_field, shipping_profile;
            profile_id = $(this).val();
            shipping_field = $(this).parents('fieldset.shipping');
            shipping_profile = shipping_field.find('#shipping-profiles');
            shipping_profile.load('/stalls/shipping/profile/?profile=' + profile_id,
                function (data) {
                    new Ecomarket.Widgets.Selects(shipping_profile.find('.select'));
                    if (!profile_id) {
                        add_shipping_rule($(this).find('.shipping-profile-rules'), 'ship_rules');
                    }
                    else {
                        new Ecomarket.Widgets.Selects($('.shipping-rules fieldset.shipping-profile-rule:not(:last) .country-select'));
                        new Ecomarket.Widgets.SelectM2M(shipping_profile);
                    }
                    update_worldwide_visibility(shipping_profiles);
                }
            );
        });

    /* open/close the worldwide box */
    $('select#shipping-profile-worldwide')
        .live('change', function (evt) {
            var product_form = $(this).parents('form');
            if ($(this).val() === '1') {
                product_form
                    .find('.shipping-profile-worldwide-prices')
                    .show();
            } else {
                product_form
                    .find('.shipping-profile-worldwide-prices')
                    .hide();
            }
        });

    $(document).on(
        'click',
        '#stall-shipping a.shipping-profiles-delete',
        function (evt) {
            evt.preventDefault();
            $.post(
                '/stalls/shipping/profile/delete/',
                $(this).parents('form').serialize(),
                function (data) {
                    //
                }
            );
        }
    );

    /* may not be necessary */
    $('input[name=shipping-profile-save]')
        .live('click', function (evt) {
            evt.preventDefault();
        });

    $('input[name=shipping-profile-delete]')
        .live('click', function (evt) {
            evt.preventDefault();
        });

    var shipping_rules_changed, signal_change, update_formset_node, increment_formset_total, update_selected_tags, add_shipping_rule;

    shipping_rules_changed = false;
    signal_change = function () {
        if (!shipping_rules_changed) {
            shipping_rules_changed = true;
            // TODO: create hidden field to record change
        }
    };

    $('.shipping-profile-rule input.price')
        .live('blur',
              signal_change);

    add_shipping_rule = function (profile_rules, prefix) {
        var rules, hidden_add, last_rule, added_rule, added_rule_extra, hidden_add_extra;

        rules = profile_rules.find('.shipping-profile-rule');

        hidden_add = rules.last();
        hidden_add_extra = hidden_add.prevUntil('fieldset');
        last_rule = hidden_add.prevAll('fieldset').first();


        added_rule = hidden_add.clone();
        added_rule_extra = hidden_add_extra.clone();

        if (last_rule.length == 0) {
            rules.parent().prepend(added_rule);
        } else {
            last_rule.after(added_rule);
            added_rule.before(added_rule_extra);
        }

        update_formset_node($('*', hidden_add), prefix, rules.length);
        update_formset_node($(hidden_add_extra[1]), prefix, rules.length);
        update_formset_node($('input', hidden_add_extra[0]), prefix, rules.length);

        update_selected_tags(profile_rules.parents('#shipping-profile'));

        new Ecomarket.Widgets
            .Selects(added_rule.find('.country-select'));

        new Ecomarket.Widgets
            .SelectM2M(added_rule);

        increment_formset_total(profile_rules, prefix);
    }

    update_selected_tags = function (profile) {
        var selected;
        /* get the selected values from the tags */
        selected = [];
        profile
            .find('.tags-list .tag em')
            .each(function () {
                selected.push($(this).attr('data-value'));
            });
        profile
            .find('.shipping-profile-rule')
            .each(function (i, el) {
                var hidden_select, val, item;
                for (item in selected) {
                    if (selected.hasOwnProperty(item)) {
                        val = selected[item];
                        $("option:not(:selected)[value=" + val  + "]", $(this))
                            .remove();
                    }
                }
            });
    }

    /* select shipping rule country */
    $('.shipping-profile-rule .tagger-select')
        .live('change', function (evt) {
            var shipping_form, rule, selected;
            signal_change();
            update_selected_tags($(this).parents('#shipping-profile'));
            /* remove the country from any other shipping rules dropdowns */

        });


    /* unselect shipping rule country */
    $('tags-list .tag .tag-remove')
        .live('click', function (evt) {
            var shipping_form, rule, value, tag, text, new_option, inserted;
            signal_change();

            tag = $(this).parents('.tag');
            value = tag.find('em').attr('data-value');
            text = tag.find('em').text();
            new_option = "<option value="
                + value + ">"
                + text
                + "</option>";
            rule = $(this).parents('.shipping-profile-rule');
            shipping_form = $(this).parents('form');
            shipping_form.find('.shipping-profile-rule').each(function (i, el) {
                if (!$(this).is(rule)) {
                    $(this).find('select.tagger-select option')
                        .each(function () {
                            var node_value;
                            node_value = $(this).val();
                            if (node_value) {
                                if (parseInt(value, 10) < parseInt(node_value, 10)) {
                                    $(this).before(new_option);
                                    inserted = true;
                                }
                            }
                        });
                    if (!inserted) {
                        $(this).find('select.tagger-select').append(new_option);
                    }
                }
            });
        });

    increment_formset_total = function (selector, prefix) {
        var form_total, form_totals_node;

        form_totals_node = $('input[name="'
                     + prefix
                     + '-TOTAL_FORMS' + '"]', selector);

        form_total = parseInt(form_totals_node.val(), 10);

        // increment the number of forms
        form_totals_node
            .val(form_total + 1)
    };

    update_formset_node = function (els, prefix, id) {
        var id_regex, name_regex, replacement, s2_regex, el;

        id_regex = new RegExp('(id_' + prefix + '-\\d+)');
        name_regex = new RegExp('(' + prefix + '-\\d+)');
        s2_regex = new RegExp('(s2id_select-id_' + prefix + '-\\d+)');

        els.each(function () {
            el = $(this);
            if (el.attr('id')) {
            if (el.attr('id').substring(0, 15) == "s2id_select-id_") {
                replacement = 's2id_select-id_' + prefix + '-' + id;
                el.attr('id', el.attr('id')
                    .replace(s2_regex, replacement));
            } else {
                replacement = 'id_' + prefix + '-' + id;
                el.attr('id', el.attr('id')
                    .replace(id_regex, replacement));
            }
            }
            if (el.attr('name')) {
            replacement = prefix + '-' + id;
            el.attr('name', el.attr('name')
                .replace(name_regex, replacement));
            }
            if (el.attr('for')) {
            replacement = 'id_' + prefix + '-' + id;
            el.attr('for', el.attr('for')
                .replace(id_regex, replacement));
            }
        });
    };

    /* add a shipping rule */
    $('a[name=shipping-profile-rule-add]')
        .live('click', function (evt) {
            evt.preventDefault();
            signal_change();
        add_shipping_rule($(this).parents('.shipping-profile-rules'), 'ship_rules');
        });

    /* delete the shipping rule */
    $('.shipping-profile-rule .close')
        .live(
            'click',
            function (evt) {
                evt.preventDefault();
                signal_change();
                // TODO: test that this is not the only rule...
                $(this)
                    .parents('.shipping-profile-rule')
                    .prev().find('input').attr('checked', 'checked');

                $(this)
                    .parents('.shipping-profile-rule')
                    .remove();
            }
        );
};

jQuery(document).ready(function ($) {
    var shipping_profiles = '#shipping-profiles';

    Ecomarket.m2m_countries = new Ecomarket.Widgets.Selects(
    $('.shipping-rules fieldset.shipping-profile-rule:not(:last) .country-select'));

    Ecomarket.product_shipping_profile = new Ecomarket.Stall
        .ShippingProfile(shipping_profiles);

    // make an add shipping rule visible
    if ($('.shipping-profile-rule', shipping_profiles).length == 1) {
       $('a[name=shipping-profile-rule-add]', shipping_profiles).click()
    }

});

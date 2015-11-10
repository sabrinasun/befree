(function ($) {

    function split(val) {
        return val.split(/,\s*/);
    }

    function extractLast(term) {
        return split(term).pop();
    }

    // here we will init all the things that we need for this module

    function initKeywordsAutocomplete() {
        var availableKeywords = [];
        $(".keywords-list").find('a').each(function (index, link) {
            availableKeywords.push(link.innerText);
        });

        $("#keywords").bind("keydown", function (event) {
            if (event.keyCode === $.ui.keyCode.TAB && $(this).autocomplete("instance").menu.active) {
                event.preventDefault();
            }
        }).autocomplete({
            minLength: 0,
            source: function (request, response) {
                // delegate back to autocomplete, but extract the last term
                response($.ui.autocomplete.filter(availableKeywords, extractLast(request.term)));
            },
            focus: function () {
                // prevent value inserted on focus
                return false;
            },
            select: function (event, ui) {
                var terms = split(this.value);
                // remove the current input
                terms.pop();
                // add the selected item
                terms.push(ui.item.value);
                // add placeholder to get the comma-and-space at the end
                terms.push("");
                this.value = terms.join(", ");
                return false;
            }
        });
    }

    $(document).ready(function () {

        $("#login-button").click(function () {
            $("#login-form").trigger("submit");
            return false;
        });

        $(".new-post-form").click(function () {
            $("#post-additional-panel").show();
        });

        $("#btn-add-post").click(function () {
            $("#new-post-form").trigger('submit');
        });

        initKeywordsAutocomplete();
        countryStateInit();
    });

})(jQuery);

function countryStateInit() {

    $("#id_us_state").val($("#id_state").val());

    hideShowState();

    function hideShowState() {
        var country = $("#id_country").find("option:selected").val();
        var state = $("#id_state");
        var usState = $("#id_us_state");
        if (country == "US") {
            state.hide();
            usState.show();
        }
        else {
            state.show();
            usState.hide();
        }
    }

    $("#id_country").change(function () {
        hideShowState();
    });

    $("#id_us_state").change(function () {
        var state = $("#id_us_state").find("option:selected").val();
        $("#id_state").val(state);
    });
}

(function ($) {

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

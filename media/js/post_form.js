var PostForm = (function () {

    var DEFAULT_BORDER = "1px solid rgb(169, 169, 169)";

    var init, split, extractLast, isPostFormValid, initKeywordsAutocomplete, isValidBody, showNotificationFor,
        isValidTitle, setElementBorder;

    split = function (val) {
        return val.split(/,\s*/);
    };
    extractLast = function (term) {
        return split(term).pop();
    };
    showNotificationFor = function ($element, message) {
        $element.notify(
            message,
            {position: 'top right', autoHideDelay: 3000}
        );
    };
    setElementBorder = function($element, border) {
        $element.css('border', border);
    };
    isValidBody = function() {
        var $postBody = $("#post-body"),
            postBody = $postBody.val();
        if (!postBody) {
            setElementBorder($postBody, '1px solid red');
            showNotificationFor($postBody, 'This field should contains at least 1 character');
            $postBody.one('keypress', function() {
                setElementBorder($postBody, DEFAULT_BORDER);
            });
            return false;
        }
        return true;
    };
    isValidTitle = function() {
        var $title = $("#title"),
            title = $title.val();
        if (!title) {
            setElementBorder($title, '1px solid red');
            showNotificationFor($title, 'This field is required.');
            $title.one('keypress', function () {
                setElementBorder($title, DEFAULT_BORDER);
            });
            return false;
        }
        return true;
    };
    isPostFormValid = function () {
        var isValid = isValidBody();
        isValid &= isValidTitle();
        return isValid;
    };
    initKeywordsAutocomplete = function () {
        var availableKeywords = [];
        $(".keywords-list").find('a').each(function (index, link) {
            availableKeywords.push(link.innerText);
        });

        $("#keywords").on("keydown", function (event) {
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
    };

    init = function () {
        initKeywordsAutocomplete();

        $("#new-post-form").on("submit", function(event){
            if (!isPostFormValid()) {
                event.preventDefault();
                return false;
            }
            var postBody = $("#post-body").val();
            $("#post-body").val(postBody.replace(/(?:\r\n|\r|\n)/g, '<br />'));
        });
    };

    return {
        init: init
    }

})();

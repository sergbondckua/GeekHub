$(function () {
    // popovers
    $('[data-toggle="popover"]').popover()

    //Adding a product to the cart
    $("#add").submit(function (e) {
        // preventing from page reload and default actions
        e.preventDefault();
        // serialize the data for sending the form data.
        const serializedData = $(this).serialize();
        // make POST ajax call
        $.ajax({
            type: "POST",
            url: $("#add").attr("action"),
            data: serializedData,
            success: function (response) {
                console.log(response);
                $("#nav").load(location.href + " #nav");
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        });
    })

    // Update qty of the product in cart
    $(document).on("click", "#upd", function (evt) {
        evt.preventDefault();
        let pid = $(this).attr("data-pid");
        const selector = $(this).closest("#body-cart");
        $.ajax({
            type: "POST",
            url: selector.find("form").attr("action"),
            data: $("#change-qty-cart" + pid).serialize(),
            success: function (response) {
                console.log(response);
                // $("#count_item").text(response.qty);
                $(".cart-view").load(location.href + " .cart-view");
                $("#nav").load(location.href + " #nav");
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        });
    })

    //Removing the product from the cart
    $(document).on("click", "#remove-item", function (event) {
        // preventing from page reload and default actions
        event.preventDefault();

        // make GET ajax call
        $.ajax({
            url: $("#remove-item").attr("href"),
            success: function (response) {
                console.log(response);
                $("#nav").load(location.href + " #nav");
                $(".cart-view").load(location.href + " .cart-view");
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        })
    })

    //Clearing cart
    $(document).on("click", "#clear-cart", function (event) {
        // preventing from page reload and default actions
        event.preventDefault();
        // make GET ajax call
        $.ajax({
            // type: "GET",
            url: $("#clear-cart").attr("href"),
            success: function (response) {
                console.log(response);
                 $("#nav").load(location.href + " #nav");
                $(".cart-view").load(location.href + " .cart-view");

            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        })
    })
})